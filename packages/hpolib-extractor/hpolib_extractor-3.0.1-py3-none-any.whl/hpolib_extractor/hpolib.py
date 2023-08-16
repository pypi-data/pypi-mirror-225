from __future__ import annotations

import json
import os
import pickle
from typing import Dict, List, Union

import h5py

from hpolib_extractor.base_extractor import BaseExtractor

import numpy as np

from tqdm import tqdm

import ujson


SEARCH_SPACE: Dict[str, List[Union[int, float, str]]] = {
    "activation_fn_1": ["relu", "tanh"],
    "activation_fn_2": ["relu", "tanh"],
    "batch_size": [8, 16, 32, 64],
    "dropout_1": [0.0, 0.3, 0.6],
    "dropout_2": [0.0, 0.3, 0.6],
    "init_lr": [5e-4, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1],
    "lr_schedule": ["cosine", "const"],
    "n_units_1": [16, 32, 64, 128, 256, 512],
    "n_units_2": [16, 32, 64, 128, 256, 512],
}
VALUE_IDENTIFIERS = {k: {v: i for i, v in enumerate(vals)} for k, vals in SEARCH_SPACE.items()}
KEY_ORDER: List[str] = list(SEARCH_SPACE.keys())
DATASET_NAMES = ["slice_localization", "protein_structure", "naval_propulsion", "parkinsons_telemonitoring"]


class HPOLibExtractor(BaseExtractor):
    _URL = "http://ml4aad.org/wp-content/uploads/2019/01/fcnet_tabular_benchmarks.tar.gz"
    _BUDGETS = list(range(1, 101))
    _SEARCH_SPACE = SEARCH_SPACE.copy()
    _N_SEEDS = 4
    _KEY_ORDER = KEY_ORDER[:]
    _VALUE_IDENTIFIERS = VALUE_IDENTIFIERS.copy()

    def __init__(self, dataset_id: int, data_dir: str, epochs: List[int]):
        self._dataset_name = DATASET_NAMES[dataset_id]
        data_path = os.path.join(data_dir, f"fcnet_{self._dataset_name}_data.hdf5")
        super().__init__(data_path=data_path, epochs=np.sort(epochs))

        self._db = h5py.File(data_path, "r")
        self._epochs -= 1

    def collect(self) -> None:
        # max_epoch: 99, min_epoch: 0
        loss_key = "valid_mse"
        runtime_key = "runtime"
        n_params_key = "n_params"
        for it in tqdm(self._get_iterator(), total=self.n_total):
            config_id = self._get_config_id(config=it)
            config = {k: v for k, v in zip(SEARCH_SPACE.keys(), it)}
            key = json.dumps(config, sort_keys=True)
            target_data = self._db[key]
            self._collected_data[config_id] = {  # type: ignore
                loss_key: [
                    {e + 1: float(target_data[loss_key][s][e]) for e in self._epochs} for s in range(self._N_SEEDS)
                ],
                runtime_key: [float(target_data[runtime_key][s]) for s in range(self._N_SEEDS)],
                n_params_key: float(target_data[n_params_key][0]),
            }


def extract_hpolib(data_dir: str, epochs: List[int] = [11, 33, 100], overwrite: bool = False) -> None:
    for i in range(len(DATASET_NAMES)):
        extractor = HPOLibExtractor(dataset_id=i, epochs=epochs, data_dir=data_dir)
        pkl_path = os.path.join(data_dir, f"{extractor.dataset_name}.pkl")
        if os.path.exists(pkl_path) and not overwrite:
            print(f"Skip extracting {extractor.dataset_name} because {pkl_path} already exists")
            print("Use overwrite=True to force the overwrite.")
            continue

        print(f"Start extracting {extractor.dataset_name}")
        extractor.collect()
        pickle.dump(extractor._collected_data, open(pkl_path, "wb"))


def extract_indiv_hpolib(data_dir: str):
    for i in range(len(DATASET_NAMES)):
        dataset_name = DATASET_NAMES[i]
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
