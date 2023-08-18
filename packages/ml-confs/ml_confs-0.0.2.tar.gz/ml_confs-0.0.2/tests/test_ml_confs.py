import os
import pytest
import dataclasses
import ml_confs as mlc
from ml_confs.lib import InvalidStructureError, check_structure
import shutil
from pathlib import Path

tests_path = Path(__file__).parent

valid_file_confs = [
    tests_path / 'test_configs/valid_conf.json',
    tests_path / 'test_configs/valid_conf.yaml',
]
invalid_file_confs = [
    tests_path / 'test_configs/invalid_conf.json',
    tests_path / 'test_configs/invalid_conf.yaml',
]
# Path: tests/ml_confs_tests.py
valid_dict = {
    'int': 1,
    'float': 1.0,
    'str': '1',
    'bool': True,
    'none': None,
    'list': [1, 2, 3],
}

invalid_dict_unsupported_type = {
    'unsupported_type': dict()
}

invalid_dict_unsupported_iterable = {
    'unsupported_iterable': (1, 2, 3)
}

invalid_dict_unsupported_iterable_heterogenous = {
    'unsupported_iterable': [1, 2, '3']
}

def test_check_structure():
    check_structure(valid_dict)
    with pytest.raises(InvalidStructureError):
        check_structure(invalid_dict_unsupported_type)
    with pytest.raises(InvalidStructureError):
        check_structure(invalid_dict_unsupported_iterable)
    with pytest.raises(InvalidStructureError):
        check_structure(invalid_dict_unsupported_iterable_heterogenous)

@pytest.mark.parametrize('path', valid_file_confs)
def test_from_file(path: os.PathLike):
    mlc.from_file(path)

@pytest.mark.parametrize('path', invalid_file_confs)
def test_from_file_invalid(path: os.PathLike):
    with pytest.raises(InvalidStructureError):
        mlc.from_file(path)

def test_from_dict():
    mlc.from_dict(valid_dict)

@pytest.mark.parametrize('path', valid_file_confs)
def test_load_save_reload(path: os.PathLike):
    configs = mlc.from_file(path)
    f_name = os.path.basename(path).split('.')[0]
    for ext in ['json', 'yaml', 'yml']:
        tmp_path = tests_path / f'tmp/{f_name}.{ext}'
        configs.to_file(tmp_path)
        loaded_configs = mlc.from_file(tmp_path)
        shutil.rmtree(tests_path / 'tmp/')
        assert dataclasses.asdict(configs) == dataclasses.asdict(loaded_configs)

def test_tabulate():
    configs = mlc.from_dict(valid_dict)
    print("\n") #Formatting
    configs.tabulate()

def test_frozen():
    with pytest.raises(dataclasses.FrozenInstanceError):
        configs = mlc.from_dict(valid_dict)
        configs.int = 2

def test_starstar():
    configs = mlc.from_dict(valid_dict)
    def foo(**kwargs):
        assert kwargs == valid_dict
    foo(**configs)