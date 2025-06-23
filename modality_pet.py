# This is the script for PET modality. See MARLAB for pre processing
import pandas as pd

def calculate_suvr(raw_input_data, output_file_name, output_file_path):
    suvr_dataframe = pd.DataFrame()
    suvr_dataframe['Patient_ID'] = raw_input_data.iloc[:, 0]

    # drop the second empty column, this may change in the future, check the inpit data before
    raw_input_data = raw_input_data.drop(raw_input_data.columns[[1]], axis=1, inplace=True)

    # group the cerebellum cols together 
    cerebellum_cols = [col for col in raw_input_data.columns if 'sum_cerebellum' in col.lower()]

    # check the cerebellum cols
    print('cerevellum_cols:')
    for col in cerebellum_cols:
        print(col)
    
    # sum the cerebellum in to one
    suvr_dataframe['SUV_Cerebellum'] = raw_input_data[cerebellum_cols].sum(axis=1)

    # now collect all the sum_ columns
    sum_columns = [col for col in raw_input_data.columns if 'sum_' in col.lower()]

    # calc the suvr for each region
    for col in sum_columns:
        suvr_dataframe[f'{col.replace("sum_", "SUVR_")}'] = raw_input_data[col] / suvr_dataframe['SUV_Cerebellum']
    
    # save the dataframe as a csv
    suvr_dataframe.to_csv(f'{output_file_path}/{output_file_name}.csv', index=False)

    return None

