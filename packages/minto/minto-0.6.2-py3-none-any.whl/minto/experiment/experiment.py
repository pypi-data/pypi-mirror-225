from __future__ import annotations

import inspect
import json
import pathlib
import types
import uuid
from typing import Any, Callable, Literal, Optional, TypedDict

import h5py
import jijmodeling as jm
import numpy as np
import pandas as pd
from google.protobuf.text_encoding import CEscape
from jijzept.response import JijModelingResponse
from pandas import DataFrame

from minto.consts.default import DEFAULT_RESULT_DIR
from minto.records.records import (
    Index,
    ParameterContent,
    ParameterInfo,
    ResultContent,
    ResultInfo,
    SolverContent,
    SolverInfo,
)
from minto.records.sampleset_expansion import expand_sampleset
from minto.table.table import SchemaBasedTable
from minto.utils.rc_sampleset import SampleSet, from_old_sampleset, serialize_sampleset


class DatabaseComponentSchema(TypedDict):
    info: SchemaBasedTable
    content: SchemaBasedTable


class DatabaseSchema(TypedDict):
    index: SchemaBasedTable
    solver: DatabaseComponentSchema
    parameter: DatabaseComponentSchema
    result: DatabaseComponentSchema


class Experiment:
    """Stores data related to an benchmark.

    The Experiment class stores the results obtained from a benchmark as Artifact and Table objects and assists in managing the benchmark process.
    With this class, you can add and save experimental results, as well as view them in various formats.

    Attributes:
        name (str): The name of the experiment.
        savedir (str | pathlib.Path): The directory where the experiment will be saved.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        savedir: str | pathlib.Path = DEFAULT_RESULT_DIR,
    ):
        self.name = name or str(uuid.uuid4())
        self.savedir = pathlib.Path(savedir)

        database: DatabaseSchema = {
            "index": SchemaBasedTable(Index.dtypes),
            "solver": {
                "info": SchemaBasedTable(SolverInfo.dtypes),
                "content": SchemaBasedTable(SolverContent.dtypes),
            },
            "parameter": {
                "info": SchemaBasedTable(ParameterInfo.dtypes),
                "content": SchemaBasedTable(ParameterContent.dtypes),
            },
            "result": {
                "info": SchemaBasedTable(ResultInfo.dtypes),
                "content": SchemaBasedTable(ResultContent.dtypes),
            },
        }
        object.__setattr__(self, "database", database)

    def __enter__(self) -> Experiment:
        """Set up Experiment.
        Automatically makes a directory for saving the experiment, if it doesn't exist.
        """
        savedir = pathlib.Path(self.savedir) / self.name
        (savedir / "tables").mkdir(parents=True, exist_ok=True)
        (savedir / "artifacts").mkdir(parents=True, exist_ok=True)
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        """Saves the experiment if autosave is True."""
        pass

    def run(self) -> Experiment:
        """Run the experiment."""
        database: DatabaseSchema = getattr(self, "database")

        if database["index"].empty():
            run_id = 0
        else:
            run_id = database["index"][-1].series()["run_id"] + 1
        database["index"].insert(Index(experiment_name=self.name, run_id=run_id))

        return self

    def table(
        self,
        key: Literal["solver", "parameter", "result"] | None = None,
        enable_sampleset_expansion: bool = True,
    ) -> pd.DataFrame:
        """Merge the experiment table and return it as a DataFrame.

        Returns:
            pd.DataFrame: The merged table.
        """
        database: DatabaseSchema = getattr(self, "database")

        solver_df = _get_component_dataframe(self, "solver")
        if key == "solver":
            return solver_df
        parameter_df = _get_component_dataframe(self, "parameter")
        if key == "parameter":
            return parameter_df
        result_df = _get_component_dataframe(self, "result")
        if key == "result":
            return result_df

        df = database["index"].dataframe()
        # Merge solver
        if not solver_df.empty:
            df = df.merge(
                _pivot(solver_df, columns="solver_name", values="content"),
                on=["experiment_name", "run_id"],
            )
        # Merge parameter
        if not parameter_df.empty:
            df = df.merge(
                _pivot(parameter_df, columns="parameter_name", values="content"),
                on=["experiment_name", "run_id"],
            )
        # Merge result
        if not result_df.empty:
            df = df.merge(_pivot(result_df, columns="result_name", values="content"))

        # Expand sampleset
        if enable_sampleset_expansion:
            sampleset_df = expand_sampleset(database["result"]["content"].dataframe())
            if not sampleset_df.empty:
                sampleset_df = pd.merge(
                    database["result"]["info"].dataframe()[
                        ["experiment_name", "run_id", "result_id"]
                    ],
                    sampleset_df,
                    on="result_id",
                ).drop(columns="result_id")

                result_names = result_df["result_name"].unique().tolist()
                df = df.merge(sampleset_df, on=["experiment_name", "run_id"]).drop(
                    columns=result_names
                )
        return df

    def log_solver(self, name: str, solver: Callable[..., Any]) -> None:
        database: DatabaseSchema = getattr(self, "database")

        run_id = int(database["index"][-1].series()["run_id"])
        solver_id = len(database["solver"]["info"])

        if isinstance(solver, types.FunctionType):
            source = inspect.getfile(solver)
        else:
            if _is_running_in_notebook():
                source = "Dynamically generated in Jupyter Notebook"
            else:
                if isinstance(solver, types.MethodType):
                    source = inspect.getfile(solver)
                else:
                    source = inspect.getfile(solver.__class__)

        info = SolverInfo(
            experiment_name=self.name,
            run_id=run_id,
            solver_name=name,
            source=source,
            solver_id=solver_id,
        )
        content = SolverContent(solver_id=solver_id, content=solver)

        database["solver"]["info"].insert(info)
        database["solver"]["content"].insert(content)

    def log_parameter(self, name: str, parameter: Any) -> None:
        """Log a parameter to the experiment.

        Args:
            parameter (Parameter): The parameter to be logged.
        """
        database: DatabaseSchema = getattr(self, "database")

        run_id = int(database["index"][-1].series()["run_id"])
        parameter_id = len(database["parameter"]["info"])

        info = ParameterInfo(
            experiment_name=self.name,
            run_id=run_id,
            parameter_name=name,
            parameter_id=parameter_id,
        )
        content = ParameterContent(parameter_id=parameter_id, content=parameter)

        database["parameter"]["info"].insert(info)
        database["parameter"]["content"].insert(content)

    def log_result(self, name: str, result: Any) -> None:
        database: DatabaseSchema = getattr(self, "database")

        run_id = int(database["index"][-1].series()["run_id"])
        result_id = len(database["result"]["info"])

        info = ResultInfo(
            experiment_name=self.name,
            run_id=run_id,
            result_name=name,
            result_id=result_id,
        )
        content = ResultContent(result_id=result_id, content=result)

        database["result"]["info"].insert(info)
        database["result"]["content"].insert(content)

    def save(self) -> None:
        """Save the experiment to a file."""
        database: DatabaseSchema = getattr(self, "database")

        table_dir = self.savedir / self.name / "tables"
        artifact_dir = self.savedir / self.name / "artifacts"

        info_dtypes: dict[str, dict[str, str]] = {}
        content_dtypes: dict[str, dict[str, str]] = {}

        keys: list[Literal["index", "solver", "parameter", "result"]] = [
            "index",
            "solver",
            "parameter",
            "result",
        ]
        for key in keys:
            if key == "index":
                database[key].dataframe().to_csv(table_dir / f"{key}.csv", index=False)
                info_dtypes[key] = database[key].pandas_dtypes
            else:
                database[key]["info"].dataframe().to_csv(
                    table_dir / f"{key}.csv", index=False
                )
                info_dtypes[key] = database[key]["info"].pandas_dtypes

                if key in ["parameter", "result"]:
                    with h5py.File(artifact_dir / f"{key}.h5", "w") as f:
                        for index, record in database[key]["content"].dict().items():
                            group = f.create_group(str(index))
                            for name, value in record.items():
                                if name == "content":
                                    if isinstance(value, jm.Problem):
                                        value = CEscape(
                                            jm.to_protobuf(value), as_utf8=False
                                        )
                                    elif isinstance(value, JijModelingResponse):
                                        value = serialize_sampleset(
                                            from_old_sampleset(value.sample_set)
                                        )
                                    elif isinstance(value, (SampleSet, jm.SampleSet)):
                                        value = serialize_sampleset(
                                            from_old_sampleset(value)
                                        )

                                    value = json.dumps(value, cls=_NumpyEncoder)
                                group.create_dataset(name, data=value)
                    content_dtypes[key] = database[key]["content"].pandas_dtypes

        with open(table_dir / "dtypes.json", "w") as f:
            json.dump(info_dtypes, f)

        with open(artifact_dir / "dtypes.json", "w") as f:
            json.dump(content_dtypes, f)


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)


def _get_component_dataframe(
    experiment: Experiment, key: Literal["solver", "parameter", "result"]
) -> DataFrame:
    database: DatabaseSchema = getattr(experiment, "database")

    return pd.merge(
        database[key]["info"].dataframe(),
        database[key]["content"].dataframe(),
        on=f"{key}_id",
    )


def _pivot(df: DataFrame, columns: str | list[str], values: str) -> DataFrame:
    return df.pivot_table(
        index=["experiment_name", "run_id"],
        columns=columns,
        values=values,
        aggfunc=lambda x: x,
    ).reset_index()


def _is_running_in_notebook():
    try:
        ipython = get_ipython()
        if "IPKernelApp" in ipython.config:  # Jupyter Notebook or JupyterLab
            return True
    except NameError:
        return False
