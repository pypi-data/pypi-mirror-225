import flowpytertask as ft
import flowpytertask
from flowpytertask import build_flowpyter_task
import pytest
import datetime
from tempfile import TemporaryDirectory
from pathlib import Path
from contextlib import contextmanager
from airflow import DAG
from airflow.utils.state import TaskInstanceState
from airflow.models import Variable

TEST_DAG_ID = "flowpytertask_test_dag"
TEST_TASK_ID = "flowpytertask_test_task"


START_DATE = datetime.datetime(2021, 9, 13)
END_DATE = datetime.timedelta(days=1)


def mock_nb_folder(key):
    if key == "host_notebook_dir":
        return str(Path(__file__).parent)
    else:
        return "unset"

@pytest.fixture
def tmp_out_dir():
    outdir = Path(__file__).parent / "out"
    outdir.mkdir(exist_ok=True)
    try:
        yield outdir
    finally:
        for child in outdir.iterdir():
            child.unlink()
        outdir.rmdir()


def test_task_builder_inner(monkeypatch, tmp_out_dir):
    monkeypatch.setattr(Variable, "get", mock_nb_folder)
    monkeypatch.setattr(
        flowpytertask, "CONTAINER_NOTEBOOK_DIR", str(Path(__file__).parent)
    )
    task = build_flowpyter_task("test_task")
    task.function(
        notebook_name="test_nb",
        nb_params = {"input":"DEADBEEF"}
    )
    assert (tmp_out_dir / "test_nb-None.ipynb").exists()
    assert "DEADBEEF" in (tmp_out_dir / "test_nb-None.ipynb").read_text()
