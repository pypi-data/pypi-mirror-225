from __future__ import annotations

import json
import pathlib
from typing import TYPE_CHECKING, Any, Literal

import h5py
import pandas as pd

from minto.consts.default import DEFAULT_RESULT_DIR
from minto.experiment.experiment import Experiment
from minto.records.records import SolverInfo
from minto.table.table import SchemaBasedTable
from minto.typing import ArtifactDataType
from minto.utils.rc_sampleset import (
    EvaluationResult,
    ExprEvaluation,
    Sample,
    SampleSet,
    VariableSparseValue,
)

if TYPE_CHECKING:
    from minto.experiment.experiment import DatabaseSchema


def load(
    experiment_name: str,
    savedir: str | pathlib.Path = DEFAULT_RESULT_DIR,
) -> Experiment:
    """Load and return an artifact, experiment, or table from the given directory.

    Args:
        name_or_dir (str | pathlib.Path): Name or directory of the benchmark.
        experiment_names (list[str] | None, optional): List of names of experiments to be loaded, if None, all experiments in `savedir` will be loaded. Defaults to None.
        savedir (str | pathlib.Path, optional): Directory of the experiment. Defaults to DEFAULT_RESULT_DIR.
        return_type (tp.Literal[&quot;Artifact&quot;, &quot;Experiment&quot;, &quot;Table&quot;], optional): Type of the returned object. Defaults to "Experiment".
        index_col (int | list[int] | None, optional): The column(s) to set as the index(MultiIndex) of the returned Table.. Defaults to None.

    Raises:
        FileNotFoundError: If `name_or_dir` is not found in the `savedir` directory.
        ValueError: If `return_type` is not one of "Artifact", "Experiment", or "Table".

    Returns:
        Experiment | Artifact | Table: The loaded artifact, experiment, or table.
    """

    savedir = pathlib.Path(savedir)
    if not (savedir / experiment_name).exists():
        raise FileNotFoundError(f"{(savedir / experiment_name)} is not found.")

    exp = Experiment(experiment_name, savedir=savedir)

    database: DatabaseSchema = getattr(exp, "database")
    table_dir = savedir / experiment_name / "tables"
    artifact_dir = savedir / experiment_name / "artifacts"

    with open(table_dir / "dtypes.json", "r") as f:
        info_dtypes = json.load(f)

    # with open(artifact_dir / "dtypes.json", "r") as f:
    #    content_dtypes = json.load(f)

    keys: list[Literal["index", "solver", "parameter", "result"]] = [
        "index",
        "solver",
        "parameter",
        "result",
    ]
    for key in keys:
        df = pd.read_csv(table_dir / f"{key}.csv").astype(info_dtypes[key])
        if key == "index":
            database["index"] = SchemaBasedTable.from_dataframe(df)
        else:
            if key == "solver":
                database[key]["info"] = SchemaBasedTable(SolverInfo.dtypes)
            else:
                database[key]["info"] = SchemaBasedTable.from_dataframe(
                    pd.read_csv(table_dir / f"{key}.csv")
                )

            if key in ("parameter", "result"):
                with h5py.File(artifact_dir / f"{key}.h5", "r") as f:
                    obj: ArtifactDataType = {}
                    for index in f:
                        obj[index] = {}
                        for name in f[index]:
                            if name == "content":
                                value = json.loads(f[index][name][()])
                                if isinstance(value, dict):
                                    if set(value.keys()) == {
                                        "data",
                                        "measuring_time",
                                        "run_info",
                                        "run_times",
                                        "set_id",
                                        "set_info",
                                    }:
                                        value = to_samplset(value)
                            else:
                                value = f[index][name][()]
                            obj[index][name] = value
                    database[key]["content"] = SchemaBasedTable.from_dict(obj)
    return exp


def to_samplset(obj: dict[str, Any]) -> SampleSet:
    for sampleset_field_name, sampleset_field in obj.items():
        if sampleset_field_name == "data":
            for i, sample in enumerate(sampleset_field):
                sample_dict = {}
                for sample_field_name, sample_field in sample.items():
                    if sample_field_name == "vars":
                        for var_name, var_dict in sample_field.items():
                            sample_dict["vars"] = {
                                var_name: VariableSparseValue(
                                    **deserialize_sparse_variable(var_dict)
                                )
                            }
                    elif sample_field_name == "evaluation_result":
                        eval_result_dict = {}
                        for (
                            eval_result_field_name,
                            eval_result_field,
                        ) in sample_field.items():
                            if eval_result_field_name == "constraints":
                                if eval_result_field:
                                    for (
                                        constraint_name,
                                        constraint_dict,
                                    ) in eval_result_field.items():
                                        eval_result_dict["constraints"] = {
                                            constraint_name: ExprEvaluation(
                                                **constraint_dict
                                            )
                                        }
                                else:
                                    eval_result_dict["constraints"] = {}
                            elif eval_result_field_name == "penalties":
                                eval_result_dict["penalties"] = {}
                            else:
                                eval_result_dict[
                                    eval_result_field_name
                                ] = eval_result_field
                        sample_dict["evaluation_result"] = EvaluationResult(
                            **eval_result_dict
                        )
                obj["data"][i] = Sample(**sample_dict)

    return SampleSet(**obj)


def deserialize_sparse_variable(
    obj: dict[str, Any],
) -> dict[str, Any]:
    for field_name, field in obj.items():
        if field_name == "value":
            obj["value"] = {tuple(i): v for i, v in zip(field[0], field[1])}
    return obj
