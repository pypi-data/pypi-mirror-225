from pathlib import Path

import typer

import preprocess
from spike2py.trial import TrialInfo


app = typer.Typer()


SUBJECT_TEST_ORDER_PATH = Path(".").cwd() / "subject_test_order"
DATA_PATH = Path(".").cwd() / "data"


@app.command()
def trial(trial_info_json: str):
    """Preprocess trial

    trial_info_json: Contains details required by spike2py.trial.TrialInfo
    """
    preprocess.trial_from_command_line(trial_info_json)


@app.command()
def subject(subject_path: str):
    """Preprocess all trials for a subject

    subject_path: path to subject folder
    """
    preprocess.subject_from_command_line(subject_path)


@app.command()
def study(study_path):
    """Preprocess all trials from all subjects for a study

    study_path: path to study folder"""
    preprocess.study_from_command_line(study_path)


if __name__ == "__main__":
    app()
