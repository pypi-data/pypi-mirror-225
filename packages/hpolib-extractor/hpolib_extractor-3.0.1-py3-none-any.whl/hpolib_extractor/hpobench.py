from __future__ import annotations

import os
import pickle
from dataclasses import dataclass
from typing import Dict, Final, List, Union

from hpolib_extractor.base_extractor import BaseExtractor

import numpy as np

import pyarrow.parquet as pq  # type: ignore

from tqdm import tqdm

import ujson


@dataclass(frozen=True)
class ResultKeys:
    runtime: str = "cost"
    acc: str = "acc"
    bal_acc: str = "bal_acc"
    precision: str = "precision"
    f1: str = "f1"


RESULT_KEYS = ResultKeys()
DATASET_INFO = [
    ("credit_g", 31),
    ("vehicle", 53),
    ("kc1", 3917),
    ("phoneme", 9952),
    ("blood_transfusion", 10101),
    ("australian", 146818),
    ("car", 146821),
    ("segment", 146822),
]
BUDGETS: Final[List[int]] = [3, 9, 27, 81, 243]
SEARCH_SPACE = {
    "alpha": [
        1e-08,
        7.742637e-08,
        5.994842e-07,
        4.641589e-06,
        3.5938137e-05,
        0.00027825593,
        0.0021544348,
        0.016681006,
        0.12915497,
        1,
    ],
    "batch_size": [4, 6, 10, 16, 25, 40, 64, 101, 161, 256],
    "depth": [1, 2, 3],
    "learning_rate_init": [
        1e-05,
        3.5938137e-05,
        0.00012915497,
        0.0004641589,
        0.0016681006,
        0.0059948424,
        0.021544347,
        0.07742637,
        0.27825594,
        1,
    ],
    "width": [16, 25, 40, 64, 101, 161, 256, 406, 645, 1024],
}
VALUE_IDENTIFIERS = {k: {v: i for i, v in enumerate(vals)} for k, vals in SEARCH_SPACE.items()}  # type: ignore
N_SEEDS = 5
N_FOR_CONFIG = N_SEEDS * len(BUDGETS)
KEY_ORDER: List[str] = list(SEARCH_SPACE.keys())  # iter, seed follow
assert KEY_ORDER == ["alpha", "batch_size", "depth", "learning_rate_init", "width"]


class HPOBenchExtractor(BaseExtractor):
    _URL = "https://ndownloader.figshare.com/files/30379005"
    _BUDGETS = BUDGETS[:]
    _SEARCH_SPACE = SEARCH_SPACE.copy()  # type: ignore
    _N_SEEDS = 5
    _KEY_ORDER = KEY_ORDER[:]
    _VALUE_IDENTIFIERS = VALUE_IDENTIFIERS.copy()

    def __init__(self, dataset_id: int, data_dir: str, epochs: List[int], target_keys: List[str]):
        self._dataset_name, idx = DATASET_INFO[dataset_id]
        data_path: Final[str] = os.path.join(data_dir, f"{idx}/nn_{idx}_data.parquet.gzip")
        super().__init__(data_path=data_path, epochs=np.sort(epochs))

        allowed_keys = list(RESULT_KEYS.__dict__.keys())
        if any(k not in allowed_keys for k in target_keys):
            raise ValueError(f"target_keys be in {allowed_keys}, but got {target_keys}")

        # subsample has only one value (subsample=1.0)
        self._db = pq.read_table(data_path)["result"].to_pylist()
        self._target_keys = target_keys[:]

    def collect(self) -> None:
        start = 0
        indices = np.array(
            [np.arange(self._N_SEEDS) + self._N_SEEDS * self._BUDGETS.index(e) for e in self._epochs]
        ).flatten()

        for it in tqdm(self._get_iterator(), total=self.n_total):
            config_id = self._get_config_id(config=it)
            entry: Dict[str, List[Dict[str, Union[List, float]]]] = {
                k: [{} for _ in range(self._N_SEEDS)] for k in self._target_keys
            }

            results = self._db[start : start + N_FOR_CONFIG]  # noqa: E203
            assert len(results) == N_FOR_CONFIG
            start += N_FOR_CONFIG
            for i in indices:
                result = results[i]
                budget, seed = self._BUDGETS[i // 5], i % 5
                for k, v in RESULT_KEYS.__dict__.items():
                    if k not in self._target_keys:
                        continue

                    if k == "runtime":
                        entry[k][seed][budget] = float(result[v])
                    else:
                        entry[k][seed][budget] = float(result["info"]["val_scores"][v])

            self._collected_data[config_id] = entry  # type: ignore


def extract_hpobench(
    data_dir: str,
    epochs: List[int] = [3, 9, 27, 81, 243],
    target_keys: List[str] = ["precision", "f1", "bal_acc", "runtime"],
    overwrite: bool = False,
) -> None:
    for i in range(len(DATASET_INFO)):
        extractor = HPOBenchExtractor(dataset_id=i, epochs=epochs, data_dir=data_dir, target_keys=target_keys)
        pkl_path = os.path.join(data_dir, f"{extractor.dataset_name}.pkl")
        if os.path.exists(pkl_path) and not overwrite:
            print(f"Skip extracting {extractor.dataset_name} because {pkl_path} already exists")
            print("Use overwrite=True to force the overwrite.")
            continue

        print(f"Start extracting {extractor.dataset_name}")
        extractor.collect()
        pickle.dump(extractor._collected_data, open(pkl_path, "wb"))


def extract_indiv_hpobench(data_dir: str) -> None:
    for i in range(len(DATASET_INFO)):
        dataset_name, _ = DATASET_INFO[i]
        pkl_path = os.path.join(data_dir, f"{dataset_name}.pkl")
        if not os.path.exists(pkl_path):
            print(f"Skip extracting {dataset_name} because {pkl_path} does not exist.")
            print("First run `extract_hpobench`.")

        with open(pkl_path, mode="rb") as f:
            data = pickle.load(f)
            dir_name = os.path.join(data_dir, dataset_name)
            os.makedirs(dir_name, exist_ok=True)
            for config_id, v in tqdm(data.items()):
                with open(os.path.join(dir_name, f"{config_id}.json"), mode="w") as f:
                    ujson.dump(v, f)
