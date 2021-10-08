# -*- coding: utf-8 -*-
"""VentilatorLSTM

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B7htLwj8lnamAh3sWwVNr5h8j_ZmZote
"""

!nvidia-smi

from google.colab import drive
drive.mount('/content/drive')

!pip install -q kaggle
!mkdir -p .kaggle
!cp "./drive/MyDrive/Study/config/kaggle.json" .kaggle/
!chmod 600 .kaggle/kaggle.json
!mv .kaggle /root

!kaggle competitions download -c ventilator-pressure-prediction

!unzip sample_submission.csv.zip
!unzip train.csv.zip
!unzip test.csv.zip

!rm *zip

!pip install -U torch wandb transformers

with open("./drive/MyDrive/Study/config/wandb.txt", "r") as f:
    for line in f:
        wandb_key = line.replace("\n", "")

!wandb login {wandb_key}

import gc
import os
import random
import wandb
import math

import numpy as np
import pandas as pd

from sklearn.model_selection import GroupKFold
from tqdm.notebook import tqdm

import torch
import torch.nn as nn
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader

from transformers import AdamW
from transformers import get_cosine_schedule_with_warmup
from sklearn.preprocessing import RobustScaler

device = torch.device("cuda")

class config:
    EXP_NAME = "exp076_transformer"
    
    INPUT = "/content/"
    OUTPUT = "/content/drive/MyDrive/Study/ventilator-pressure-prediction"
    N_FOLD = 5
    SEED = 0
    
    LR = 5e-3
    N_EPOCHS = 50
    EMBED_SIZE = 64
    HIDDEN_SIZE = 256
    BS = 512
    WEIGHT_DECAY = 1e-3

    USE_LAG = 4
    ROLLING = [2, 4, 8]

    CATE_FEATURES = ['R_cate', 'C_cate', 'RC_dot', 'RC_sum']
    CONT_FEATURES = ['u_in', 'u_out', 'time_step'] + ['u_in_cumsum', 'u_in_cummean', 'area', 'cross', 'cross2']
    LAG_FEATURES = ['breath_time']
    LAG_FEATURES += [f'u_in_lag_{i}' for i in range(1, USE_LAG+1)]
    LAG_FEATURES += [f'u_in_time{i}' for i in range(1, USE_LAG+1)]
    LAG_FEATURES += [f'u_out_lag_{i}' for i in range(1, USE_LAG+1)]
    ROLLING_FEATURES = [f"u_in_rolling_mean{w}" for w in ROLLING]
    ROLLING_FEATURES += [f"u_in_rolling_max{w}" for w in ROLLING]
    ROLLING_FEATURES += [f"u_in_rolling_min{w}" for w in ROLLING]
    ROLLING_FEATURES += [f"u_in_rolling_std{w}" for w in ROLLING]
    ALL_FEATURES = CATE_FEATURES + CONT_FEATURES + LAG_FEATURES #+ ROLLING_FEATURES
    NORM_FEATURES = CONT_FEATURES + LAG_FEATURES #+ ROLLING_FEATURES
    
    NOT_WATCH_PARAM = ['INPUT']

def set_seed(seed=config.SEED):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

class VentilatorDataset(Dataset):
    
    def __init__(self, df, label_dic=None):
        self.dfs = [_df for _, _df in df.groupby("breath_id")]
        self.label_dic = label_dic
        
    def __len__(self):
        return len(self.dfs)
    
    def __getitem__(self, item):
        df = self.dfs[item]
        X = df[config.ALL_FEATURES].values
        y = df['pressure'].values
        if self.label_dic is None:
            label = [-1]
        else:
            label = [self.label_dic[i] for i in y]

        d = {
            "X": torch.tensor(X).float(),
            "y" : torch.tensor(label).long(),
        }
        return d

class VentilatorModel(nn.Module):
    
    def __init__(self):
        super(VentilatorModel, self).__init__()
        self.r_emb = nn.Embedding(3, 2, padding_idx=0)
        self.c_emb = nn.Embedding(3, 2, padding_idx=0)
        self.rc_dot_emb = nn.Embedding(8, 4, padding_idx=0)
        self.rc_sum_emb = nn.Embedding(8, 4, padding_idx=0)
        self.seq_emb = nn.Sequential(
            nn.Linear(12+len(config.NORM_FEATURES), config.EMBED_SIZE),
            nn.LayerNorm(config.EMBED_SIZE),
        )
        
        #self.lstm = nn.LSTM(config.EMBED_SIZE, config.HIDDEN_SIZE, batch_first=True, bidirectional=True, num_layers=4)
        encoder_layers = nn.TransformerEncoderLayer(d_model=config.EMBED_SIZE, nhead=1, dim_feedforward=2048, dropout=0.0, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers=2)
        self.head = nn.Sequential(
            nn.Linear(config.EMBED_SIZE, config.EMBED_SIZE),
            nn.LayerNorm(config.EMBED_SIZE),
            nn.Tanh(),
            nn.Linear(config.EMBED_SIZE, 950),
        )
        '''
        self.head = nn.Sequential(
            nn.Linear(config.HIDDEN_SIZE * 2, config.HIDDEN_SIZE * 2),
            nn.LayerNorm(config.HIDDEN_SIZE * 2),
            nn.ReLU(),
            nn.Linear(config.HIDDEN_SIZE * 2, 950),
        )
        '''

        # Encoder
        initrange = 0.1
        self.r_emb.weight.data.uniform_(-initrange, initrange)
        self.c_emb.weight.data.uniform_(-initrange, initrange)
        self.rc_dot_emb.weight.data.uniform_(-initrange, initrange)
        self.rc_sum_emb.weight.data.uniform_(-initrange, initrange)
        
        # LSTM
        for n, m in self.named_modules():
            if isinstance(m, nn.LSTM):
                print(f'init {m}')
                for param in m.parameters():
                    if len(param.shape) >= 2:
                        nn.init.orthogonal_(param.data)
                    else:
                        nn.init.normal_(param.data)

    def forward(self, X, y=None):
        # embed
        bs = X.shape[0]
        r_emb = self.r_emb(X[:,:,0].long()).view(bs, 80, -1)
        c_emb = self.c_emb(X[:,:,1].long()).view(bs, 80, -1)
        rc_dot_emb = self.rc_dot_emb(X[:,:,2].long()).view(bs, 80, -1)
        rc_sum_emb = self.rc_sum_emb(X[:,:,3].long()).view(bs, 80, -1)
        
        seq_x = torch.cat((r_emb, c_emb, rc_dot_emb, rc_sum_emb, X[:, :, 4:]), 2)
        emb_x = self.seq_emb(seq_x)
        
        #out, _ = self.lstm(emb_x, None) 
        out = self.transformer_encoder(emb_x)
        logits = self.head(out)

        if y is None:
            loss = None
        else:
            loss = self.loss_fn(logits, y)
            
        return logits, loss
    
    def loss_fn(self, y_pred, y_true):
        loss = nn.CrossEntropyLoss()(y_pred.reshape(-1, 950), y_true.reshape(-1))
        return loss

def train_loop(model, optimizer, scheduler, loader):
    losses, lrs = [], []
    model.train()
    optimizer.zero_grad()
    for d in loader:
        out, loss = model(d['X'].to(device), d['y'].to(device))
        
        losses.append(loss.item())
        step_lr = np.array([param_group["lr"] for param_group in optimizer.param_groups]).mean()
        lrs.append(step_lr)
        
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        scheduler.step()

    return np.array(losses).mean(), np.array(lrs).mean()

def valid_loop(model, loader, target_dic_inv):
    losses, predicts = [], []
    model.eval()
    for d in loader:
        with torch.no_grad():
            out, loss = model(d['X'].to(device), d['y'].to(device))
        losses.append(loss.item())
        predicts.append(out.argmax(2).cpu())

    return np.array(losses).mean(), target_dic_inv[torch.vstack(predicts).reshape(-1)].numpy()

def test_loop(model, loader, target_dic_inv):
    predicts = []
    model.eval()
    for d in loader:
        with torch.no_grad():
            out, _ = model(d['X'].to(device))
        predicts.append(out.argmax(2).cpu())

    return target_dic_inv[torch.vstack(predicts).reshape(-1)].numpy()

'''def add_feature(df):
    df['time_delta'] = df.groupby('breath_id')['time_step'].diff().fillna(0)
    df['delta'] = df['time_delta'] * df['u_in']
    df['area'] = df.groupby('breath_id')['delta'].cumsum()

    df['cross']= df['u_in']*df['u_out']
    df['cross2']= df['time_step']*df['u_out']
    
    df['u_in_cumsum'] = (df['u_in']).groupby(df['breath_id']).cumsum()
    df['one'] = 1
    df['count'] = (df['one']).groupby(df['breath_id']).cumsum()
    df['u_in_cummean'] =df['u_in_cumsum'] / df['count']
    
    df = df.drop(['count','one'], axis=1)
    return df

def add_lag_feature(df):
    # https://www.kaggle.com/kensit/improvement-base-on-tensor-bidirect-lstm-0-173
    for lag in range(1, config.USE_LAG+1):
        df[f'breath_id_lag{lag}']=df['breath_id'].shift(lag).fillna(0)
        df[f'breath_id_lag{lag}same']=np.select([df[f'breath_id_lag{lag}']==df['breath_id']], [1], 0)

        # u_in 
        df[f'u_in_lag_{lag}'] = df['u_in'].shift(lag).fillna(0) * df[f'breath_id_lag{lag}same']
        df[f'u_in_time{lag}'] = df['u_in'] - df[f'u_in_lag_{lag}']
        df[f'u_out_lag_{lag}'] = df['u_out'].shift(lag).fillna(0) * df[f'breath_id_lag{lag}same']

    # breath_time
    df['time_step_lag'] = df['time_step'].shift(1).fillna(0) * df[f'breath_id_lag{lag}same']
    df['breath_time'] = df['time_step'] - df['time_step_lag']

    drop_columns = ['time_step_lag']
    drop_columns += [f'breath_id_lag{i}' for i in range(1, config.USE_LAG+1)]
    drop_columns += [f'breath_id_lag{i}same' for i in range(1, config.USE_LAG+1)]
    df = df.drop(drop_columns, axis=1)

    # fill na by zero
    df = df.fillna(0)
    return df

c_dic = {10: 0, 20: 1, 50:2}
r_dic = {5: 0, 20: 1, 50:2}
rc_sum_dic = {v: i for i, v in enumerate([15, 25, 30, 40, 55, 60, 70, 100])}
rc_dot_dic = {v: i for i, v in enumerate([50, 100, 200, 250, 400, 500, 2500, 1000])}    

def add_category_features(df):
    df['C_cate'] = df['C'].map(c_dic)
    df['R_cate'] = df['R'].map(r_dic)
    df['RC_sum'] = (df['R'] + df['C']).map(rc_sum_dic)
    df['RC_dot'] = (df['R'] * df['C']).map(rc_dot_dic)
    return df

def add_rolling_features(df):
    for w in config.ROLLING:
        df[f"u_in_rolling_mean{w}"] = df[["breath_id", "u_in"]].groupby("breath_id").rolling(w).mean()["u_in"].reset_index(drop=True)
        df[f"u_in_rolling_max{w}"] = df[["breath_id", "u_in"]].groupby("breath_id").rolling(w).max()["u_in"].reset_index(drop=True)
        df[f"u_in_rolling_min{w}"] = df[["breath_id", "u_in"]].groupby("breath_id").rolling(w).min()["u_in"].reset_index(drop=True)
        df[f"u_in_rolling_std{w}"] = df[["breath_id", "u_in"]].groupby("breath_id").rolling(w).std()["u_in"].reset_index(drop=True)
    return df

def norm_scale(train_df, test_df):
    scaler = RobustScaler()
    all_u_in = np.vstack([train_df[config.NORM_FEATURES].values, test_df[config.NORM_FEATURES].values])
    scaler.fit(all_u_in)
    train_df[config.NORM_FEATURES] = scaler.transform(train_df[config.NORM_FEATURES].values)
    test_df[config.NORM_FEATURES] = scaler.transform(test_df[config.NORM_FEATURES].values)
    return train_df, test_df'''

def main():
    
    #train_df = pd.read_csv(f"{config.INPUT}/train.csv")
    #test_df = pd.read_csv(f"{config.INPUT}/test.csv")
    train_df = pd.read_feather(f"{config.OUTPUT}/features/train_v1_all_norm.ftr")
    _df = pd.read_csv(f"{config.INPUT}/train.csv")[['pressure', 'breath_id', 'id']]
    train_df['id'] = _df['id']
    train_df['pressure'] = _df['pressure']
    train_df['breath_id'] = _df['breath_id']
    del _df
    test_df = pd.read_feather(f"{config.OUTPUT}/features/test_v1_all_norm.ftr")
    test_df['breath_id'] = pd.read_csv(f"{config.INPUT}/test.csv")['breath_id']
    test_df['pressure'] = -1
    sub_df = pd.read_csv(f"{config.INPUT}/sample_submission.csv")

    oof = np.zeros(len(train_df))
    test_preds_lst = []

    target_dic = {v:i for i, v in enumerate(sorted(train_df['pressure'].unique().tolist()))}
    target_dic_inv = torch.tensor(list(target_dic.keys()))

    gkf = GroupKFold(n_splits=config.N_FOLD).split(train_df, train_df.pressure, groups=train_df.breath_id)
    for fold, (_, valid_idx) in enumerate(gkf):
        train_df.loc[valid_idx, 'fold'] = fold

    #train_df = add_feature(train_df)
    #train_df = add_lag_feature(train_df)
    #train_df = add_category_features(train_df)
    #train_df = add_rolling_features(train_df)

    #test_df = add_feature(test_df)
    #test_df = add_lag_feature(test_df)
    #test_df = add_category_features(test_df)
    #test_df = add_rolling_features(test_df)

    #train_df, test_df = norm_scale(train_df, test_df)

    test_dset = VentilatorDataset(test_df)
    test_loader = DataLoader(test_dset, batch_size=config.BS,
                             pin_memory=True, shuffle=False, drop_last=False, num_workers=os.cpu_count())
    
    for fold in range(config.N_FOLD):
        print(f'Fold-{fold}')
        train_dset = VentilatorDataset(train_df.query(f"fold!={fold}"), target_dic)
        valid_dset = VentilatorDataset(train_df.query(f"fold=={fold}"), target_dic)

        set_seed()
        train_loader = DataLoader(train_dset, batch_size=config.BS,
                                  pin_memory=True, shuffle=True, drop_last=True, num_workers=os.cpu_count(),
                                  worker_init_fn=lambda x: set_seed())
        valid_loader = DataLoader(valid_dset, batch_size=config.BS,
                                  pin_memory=True, shuffle=False, drop_last=False, num_workers=os.cpu_count())

        model = VentilatorModel()
        model.to(device)

        optimizer = AdamW(model.parameters(), lr=config.LR, weight_decay=config.WEIGHT_DECAY)
        num_train_steps = int(len(train_loader) * config.N_EPOCHS)
        num_warmup_steps = int(num_train_steps / 10)
        scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=num_warmup_steps, num_training_steps=num_train_steps)

        uniqe_exp_name = f"{config.EXP_NAME}_f{fold}"
        wandb.init(project='Ventilator', entity='trtd56', name=uniqe_exp_name, group=config.EXP_NAME)
        wandb_config = wandb.config
        wandb_config.fold = fold
        for k, v in dict(vars(config)).items():
            if k[:2] == "__" or k in config.NOT_WATCH_PARAM:
                continue
            wandb_config[k] = v
        wandb.watch(model)
        
        os.makedirs(f'{config.OUTPUT}/{config.EXP_NAME}', exist_ok=True)
        model_path = f"{config.OUTPUT}/{config.EXP_NAME}/ventilator_f{fold}_best_model.bin"
        
        valid_best_score = float('inf')
        valid_best_score_mask = float('inf')
        for epoch in tqdm(range(config.N_EPOCHS)):
            train_loss, lrs = train_loop(model, optimizer, scheduler, train_loader)
            valid_loss, valid_predict = valid_loop(model, valid_loader, target_dic_inv)
            valid_score = np.abs(valid_predict - train_df.query(f"fold=={fold}")['pressure'].values).mean()

            mask = (train_df.query(f"fold=={fold}")['u_out'] == 0).values
            _score = valid_predict - train_df.query(f"fold=={fold}")['pressure'].values
            valid_score_mask = np.abs(_score[mask]).mean()

            if valid_score < valid_best_score:
                valid_best_score = valid_score
                torch.save(model.state_dict(), model_path)
                oof[train_df.query(f"fold=={fold}").index.values] = valid_predict

            if valid_score_mask < valid_best_score_mask:
                valid_best_score_mask = valid_score_mask

            wandb.log({
                "train_loss": train_loss,
                "valid_loss": valid_loss,
                "valid_score": valid_score,
                "valid_best_score": valid_best_score,
                "valid_score_mask": valid_score_mask,
                "valid_best_score_mask": valid_best_score_mask,
                "learning_rate": lrs,
            })
            
            torch.cuda.empty_cache()
            gc.collect()
        
        model.load_state_dict(torch.load(model_path))
        test_preds = test_loop(model, test_loader, target_dic_inv)
        test_preds_lst.append(test_preds)
        
        sub_df['pressure'] = test_preds
        sub_df.to_csv(f"{config.OUTPUT}/{config.EXP_NAME}/sub_f{fold}.csv", index=None)

        train_df['oof'] = oof
        train_df[['id', 'pressure', 'oof']].to_csv(f"{config.OUTPUT}/{config.EXP_NAME}/oof.csv", index=None)
        wandb.finish()

        del model, optimizer, scheduler, train_loader, valid_loader, train_dset, valid_dset
        torch.cuda.empty_cache()
        gc.collect()
    
    sub_df['pressure'] = np.stack(test_preds_lst).mean(0)
    sub_df.to_csv(f"{config.OUTPUT}/{config.EXP_NAME}/submission_mean.csv", index=None)

    sub_df['pressure'] = np.median(np.stack(test_preds_lst), axis=0)
    sub_df.to_csv(f"{config.OUTPUT}/{config.EXP_NAME}/submission_median.csv", index=None)

    # Post Processing: https://www.kaggle.com/snnclsr/a-dummy-approach-to-improve-your-score-postprocess
    unique_pressures = train_df["pressure"].unique()
    sorted_pressures = np.sort(unique_pressures)
    total_pressures_len = len(sorted_pressures)

    def find_nearest(prediction):
        insert_idx = np.searchsorted(sorted_pressures, prediction)
        if insert_idx == total_pressures_len:
            return sorted_pressures[-1]
        elif insert_idx == 0:
            return sorted_pressures[0]
        lower_val = sorted_pressures[insert_idx - 1]
        upper_val = sorted_pressures[insert_idx]
        return lower_val if abs(lower_val - prediction) < abs(upper_val - prediction) else upper_val
    
    sub_df = pd.read_csv(f"{config.OUTPUT}/{config.EXP_NAME}/submission_mean.csv")
    sub_df["pressure"] = sub_df["pressure"].apply(find_nearest)
    sub_df.to_csv(f"{config.OUTPUT}/{config.EXP_NAME}/submission_mean_pp.csv", index=None)
    
    sub_df = pd.read_csv(f"{config.OUTPUT}/{config.EXP_NAME}/submission_median.csv")
    sub_df["pressure"] = sub_df["pressure"].apply(find_nearest)
    sub_df.to_csv(f"{config.OUTPUT}/{config.EXP_NAME}/submission_median_pp.csv", index=None)
    
    cv_score = train_df.apply(lambda x: abs(x['oof'] - x['pressure']), axis=1).mean()
    print("CV:", cv_score)

if __name__ == "__main__":
    main()

wandb.finish()



