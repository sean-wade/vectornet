'''
Author: zhanghao
LastEditTime: 2023-03-08 14:30:38
FilePath: /TNT_Vectornet_SG/core/dataloader/sg_dataloader.py
LastEditors: zhanghao
Description: 
'''
import os
import copy
import glob
import pickle
import numpy as np
from tqdm import tqdm

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


def collate_padding(samples):
    traj_nums = np.array([d["traj_num"] for d in samples])
    lane_nums = np.array([d["lane_num"] for d in samples])
    valid_nums = traj_nums + lane_nums
    num_valid_len_max = np.max(valid_nums)
    candidate_nums = np.array([d["candidate"].shape[0] for d in samples])
    num_candi_len_max = np.max(candidate_nums)


def collate_list(samples):
    # for sample in samples:
    #     sample["x"] = torch.unsqueeze(sample["x"], 0)
    #     sample["y"] = torch.unsqueeze(sample["y"], 0)
    #     sample["cluster"] = torch.unsqueeze(sample["cluster"], 0).long()
    return samples


class SGTrajDataset(Dataset):
    def __init__(self,
                data_root,
                in_mem = True):
        self.data_root = data_root
        self.in_mem = in_mem
        self.data_paths = sorted(glob.glob(data_root + "/*.pkl"))

        if self.in_mem:
            self.data = [self.extract_data(idx) for idx in tqdm(range(len(self)), desc="Loading data in memory")]


    def __len__(self):
        return len(self.data_paths)


    def __getitem__(self, idx):
        if self.in_mem:
            return self.data[idx]
        else:
            return self.extract_data(idx)


    def extract_data(self, idx):
        raw_data = pickle.load(open(self.data_paths[idx], "rb"))
        return raw_data


if __name__ == '__main__':
    dataset = SGTrajDataset(data_root = '/mnt/data/SGTrain/rosbag/train_feature', in_mem=True)
    
    loader = DataLoader(dataset=dataset, batch_size=2, shuffle=False, collate_fn=collate_list)

    for data in loader:
        print(data[0]["seq_id"], data[1]["seq_id"])
