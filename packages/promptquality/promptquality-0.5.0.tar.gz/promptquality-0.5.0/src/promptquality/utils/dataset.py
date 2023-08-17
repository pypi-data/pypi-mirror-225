from collections import ChainMap
from csv import DictWriter
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, List, Optional, Union

DatasetType = Union[Path, str, Dict[str, List[str]], List[Dict[str, str]]]


def transpose_dict_to_rows(dataset: Dict[str, List[str]]) -> List[Dict[str, str]]:
    key_rows = [[{key: value} for value in values] for key, values in dataset.items()]
    return [dict(ChainMap(*key_row)) for key_row in zip(*key_rows)]


def dataset_to_path(dataset: DatasetType) -> Path:
    dataset_path: Optional[Path] = None
    if isinstance(dataset, Path):
        dataset_path = dataset
    elif isinstance(dataset, str):
        dataset_path = Path(dataset)
    elif isinstance(dataset, (dict, list)):
        if isinstance(dataset, dict):
            dataset_rows = transpose_dict_to_rows(dataset)
        else:
            dataset_rows = dataset
        with NamedTemporaryFile(mode="wt", suffix=".csv", delete=False) as dataset_file:
            field_names = dataset_rows[0].keys()
            writer = DictWriter(dataset_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(dataset_rows)
        dataset_path = Path(dataset_file.name)
    else:
        raise ValueError(f"Invalid dataset type: {type(dataset)}.")
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file {dataset_path} does not exist.")
    return dataset_path
