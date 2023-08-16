from __future__ import annotations

import itertools
import os
from abc import ABCMeta, abstractmethod
from typing import Dict, Iterator, List, Tuple, Union

import numpy as np


class BaseExtractor(metaclass=ABCMeta):
    _dataset_name: str
    _SEARCH_SPACE: Dict[str, List[Union[int, float, str]]]
    _BUDGETS: List[int]
    _VALUE_IDENTIFIERS: Dict[str, Dict[Union[int, float, str], int]]
    _N_SEEDS: int
    _KEY_ORDER: List[str]
    _URL: str

    def __init__(self, data_path: str, epochs: np.ndarray):
        self._epochs = epochs
        self._collected_data: Dict[str, Union[List, float]] = {}

        self._validate_data_path(data_path)
        self._validate_budgets()

    def _validate_data_path(self, data_path: str) -> None:
        if not os.path.exists(data_path):
            raise FileNotFoundError(
                f"{data_path} does not exist. Please make sure that you already download and "
                f"locate the datasets at {data_path}."
                f"Datasets are available at {self._URL}"
            )

    def _validate_budgets(self) -> None:
        if any(e not in self._BUDGETS for e in self._epochs):
            raise ValueError(f"epochs must be in {self._BUDGETS}, but got {self._epochs.tolist()}")

    def _get_config_id(self, config: Tuple[Union[int, float, str], ...]) -> str:
        config_id = "".join([str(self._VALUE_IDENTIFIERS[k][v]) for k, v in zip(self._KEY_ORDER, config)])
        return config_id

    def _get_iterator(self) -> Iterator:
        return itertools.product(*list(self._SEARCH_SPACE.values()))

    @property
    def n_total(self) -> int:
        return int(np.prod([len(vals) for vals in self._SEARCH_SPACE.values()]))

    @property
    def dataset_name(self) -> str:
        return self._dataset_name

    @abstractmethod
    def collect(self) -> None:
        raise NotImplementedError
