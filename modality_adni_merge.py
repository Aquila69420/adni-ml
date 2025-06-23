import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

adni_merge_file = pd.read_csv("data\ADNIMERGE_19Jun2025.csv")

def filter_file_by_cols(file, cols):
    new_file = file.filter(cols)
    return new_file

def numeric_cols(df, cols):
    df[cols] = df[cols].replace(r'^[><]*', '', regex = True).astype(float)
    return df

def filter_by_followup(df, month):
    follow_up_df = df[df['Month'] == month]
    return follow_up_df

def map_dx_and_dx_bl(df):
    dx_mapping = {'Dementia': 'AD', 'CN': 'CN', 'MCI': 'MCI'}
    dx_bl_mapping = {'EMCI': 'MCI', 'LMCI': 'MCI', 'CN': 'CN', 'SMC': 'SMC', 'AD': 'AD'}

    df['DX'] = df['DX'].map(dx_mapping, )
    df['DX_bl'] = df['DX_bl'].map(dx_bl_mapping)
    return df


# processes the ADNI merge database to include the relevant cols. Change as you need


cols = ['PTID', 'DX_bl', 'DX', 'AV45','AV45_bl', 'TAU_bl', 'TAU', 'PTAU_bl', 'PTAU', 'ABETA', 'ABETA_bl','AGE','PTGENDER','PTEDUCAT','PTRACCAT','MMSE_bl',
        'EcogPtTotal_bl','FHQMOM','FHQMOMAD','FHQDAD','FHQDADAD','LDELTOTAL_BL','mPACCdigit_bl','mPACCtrailsB_bl','RAVLT_immediate_bl','RAVLT_learning_bl',
        'RAVLT_forgetting_bl','RAVLT_perc_forgetting_bl','Month', 'EXAMDATE']

new_df = filter_file_by_cols(adni_merge_file, cols)

new_df = numeric_cols(new_df,['AV45','AV45_bl', 'Month', 'TAU_bl', 'TAU', 'PTAU_bl', 'PTAU', 'ABETA', 'ABETA_bl'])

follow_up_df = filter_by_followup(new_df, 24)

complete_df = follow_up_df.dropna()

mapped_df = map_dx_and_dx_bl(complete_df)

print(mapped_df)

