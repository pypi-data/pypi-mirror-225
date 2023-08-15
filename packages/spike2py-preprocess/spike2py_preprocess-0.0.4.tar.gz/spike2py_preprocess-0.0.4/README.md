[![spike2py](https://raw.githubusercontent.com/MartinHeroux/spike2py_preprocess/master/spike2py_preprocess_icon_600x300.png)](https://github.com/MartinHeroux/spike2py)


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
    [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)

**spike2py_preprocess** provides a simple way to batch (pre)process data with [spike2py](https://github.com/MartinHeroux/spike2py).

**spike2py_preprocess** can be used to batch read a series of `.mat` files and save them to `.pkl` files. However, the power of **spike2py_preprocess** is its ability to also preprocess the data, and this for a single trial, all trials from a subject, or all trials from a study.

### Trial

In python:
```python
>>> from spike2py.trial import TrialInfo
>>> from spike2py_preprocess import preprocess
>>> trial_info = TrialInfo(file="0004.mat",
                           name='h_reflex_curve',
                           subject_id='sub01',
                           path_save_trial='./proc')
>>> preprocess.trial(trial_info)
```

On the command line:
```bash
$ python spike2py_preprocess.py trial --help
$ python spike2py_preprocess.py trial <path_to_trial_info_json>
```

Here, we need to point `spike2py_preprocess.py` to a valid json file.
The json file requires the following fields:

```json
{
  "file": "/home/maple/study/sub01/data/raw/sub01_DATA000_H_B.mat",
  "channels": ["FDI", "W_EXT", "stim"],
  "name": "biphasic_high_fq",
  "subject_id": "sub01",
  "path_save_trial": "/home/maple/study/sub01/data/proc"
}
```

### Subject:

In Python:
```python
>>> from spike2py_preprocess import preprocess
>>> from pathlib import Path
>>> subject_folder = Path('sub01')
>>> preprocess.subject(subject_folder)
```
On the command line:
```bash
$ python spike2py_preprocess.py subject --help
$ python spike2py_preprocess.py subject /home/maple/study/sub01
```

### Study:

In Python: 

```python
>>> from spike2py_preprocess import preprocess
>>> from pathlib import Path
>>> study_folder = Path('great_study')
>>> preprocess.study(study_folder)
```

On the command line:
```bash
$ python spike2py_preprocess.py study --help
$ python spike2py_preprocess.py study /home/maple/study/
```

## Preprocess

You can specify the preprocessing settings to apply to one or more channels by including one or more `<level>_preprocess.json` files.

For a single trial, **spike2py_preprocess** looks for `<trialname.mat>_preprocess.json` in the same folder as the `.mat` file.

For all trials for a subject, **spike2py_preprocess** looks for `subject_preprocess.json` in the provided subject folder.

Finally, for all trials in a study, **spike2py_preprocess** looks for `study_preprocess.json` in the provided study folder.

### Controlling the preprocessing

By including `study_preprocess.json`, `subject_preprocess.json` and `<trialname.mat>_preprocess.json` files in a given file structure, it is possible to provide a general preprocess scheme, but that can be overridden for a given subject or a given trial.

## File structure

Below is an example of the required file/folder structure for **spike2py_preprocess**.

In the example, `sub02_DATA000_H_B.mat` has its own preprocess details located in **preprocess_sub02_DATA000_H_B.json**.

Similarly, at the subject level, `sub02` has a `subject_preprocess.json` file. This means all their files (excluding `sub02_DATA000_H_B.mat`) will be preprocessed in the same way.

Finally, because `sub01` does not include a dedicated `.json` file, their data would simply be read and saved as `.pkl` files if their data was analysed on their own. 
However, if **spike2py_preprocess** was used to preprocess all trials in the study, trials from `sub01` would be preprocessed with the details provided in `study_preprocess.json`.

```bash

study1/
├── study_info.json
├── study_preprocess.json
├── sub01
│   ├── raw
│   │   ├── sub01_DATA000_H_B_trial_info.json
│   │   ├── sub01_DATA000_H_B.mat
│   │   ├── sub01_DATA001_C_B.mat
│   │   ├── sub01_DATA002_C_M.mat
│   │   └── sub01_DATA003_H_M.mat
│   └── subject_info.json
└── sub02
    ├── raw
    │   ├── preprocess_sub02_DATA000_H_B.json
    │   ├── sub02_DATA000_H_B.mat
    │   ├── sub02_DATA001_C_B.mat
    │   ├── sub02_DATA002_C_M.mat
    │   └── sub02_DATA003_H_M.mat
    ├── subject_info.json
    └── subject_preprocess.json
```

## subject_info.json
This file contains details about the subject. Additional information can appear in this file, but at a minimum it requires
that "subject_id" be provided, as well as "trials", which contains the various trials to be processed for this subject.
For each trial, the minimum data required is "name" and "file". If "channels" is provided, only these channels will be 
included and preprocessed; if not provided, all channels will be included.

```json
{
  "subject_id": "sub01",
  "age": 50,
  "gender": "F",
  "trials": {
    "trial1": {
      "name": "conv_biphasic",
      "file": "sub01_001.mat"
    },
    "trial2": {
      "name": "khz_biphasic",
      "file": "sub01_002.mat",
      "channels": ["FDI", "W_EXT", "stim"]
    }
  }
}

```
## study_info.json
This file contains details about the study. Additional information can appear in this file, but at a minimum it requires
that "name" and "subjects" be provided. If "channels" is provided, only these channels will be included and preprocessed,
noting that this can be trumped 
```json
{
    "name": "TSS_H-reflex",
    "subjects": [
      "sub01",
      "sub02"
    ],
  "channels": ["FDI", "W_EXT", "stim"]
}

```
## Installing

**spike2py_preprocess** is available on PyPI:

```console
$ python -m pip install spike2py_preprocess
```

**spike2py** officially supports Python 3.8+.

## Contributing

Like this project? Want to help? We would love to have your contribution! Please see [CONTRIBUTING](CONTRIBUTING.md) to get started.

## Code of conduct

This project adheres to the Contributor Covenant code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [heroux.martin@gmail.com](heroux.martin@gmail.com).

## License

[GPLv3](./LICENSE)
