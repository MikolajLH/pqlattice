import functools
import json
from pathlib import Path

import numpy as np
import pytest


@functools.cache
def _load_json_file(filename: str) -> list[np.ndarray]:
    data_file_path = Path(__file__).parent / "sage_data" / "lattice" / filename

    if not data_file_path.is_file():
        raise FileNotFoundError(f"Test data file not found. Expected at: {data_file_path.resolve()}")

    with data_file_path.open("r") as f:
        data = json.load(f)

    if "-" in filename:
        result = []
        for k, v in data.items():
            result.append((int(k), np.array(v, dtype=int)))
        return result
    elif "x" in filename:
        result = []
        for arr in data:
            result.append(np.array(arr, dtype=int))
        return result
    else:
        raise ValueError(f"unsupported file name: <{filename}>")


def load_lattice_basis(filenames: list[str]):
    all_cases = []

    for filename in filenames:
        data = _load_json_file(filename)

        for i, case_data in enumerate(data):
            test_id = f"{filename.split('.')[0]}-case[{i}]"
            all_cases.append(pytest.param(case_data, id=test_id))

    return all_cases


def load_lattice_sizes(filename: str):
    data = _load_json_file(filename)

    return data
