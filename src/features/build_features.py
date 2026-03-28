import pathlib
import pandas as pd
import numpy as np
from feature_definitions import feature_build

from sklearn.model_selection import train_test_split

def load_data(data_path):
    df = pd.read_csv(data_path)
    return df


def split_data(df,test_split=0.2,seed=42):
    train,test = train_test_split(df,test_size = test_split,random_state=seed)
    return train,test


def save_data(train,test,output_path):
    pathlib.Path(output_path).mkdir(parents=True,exist_ok=True)
    train.to_csv(output_path+'/train.csv',index=False)
    test.to_csv(output_path+'/test.csv',index=False)


# if __name__ == '__main__':
#     curr_dir = pathlib.Path(__file__)
#     home_dir = curr_dir.parent.parent.parent
#     train_path = home_dir.as_posix()+'/data/raw/train.csv'
#     test_path = home_dir.as_posix()+'/data/raw/test.csv'

#     do_not_use_for_training = ['id','pickup_datetime','check_trip_duration','pickup_date','avg_speed_h','pickup_lat_bin','pickup_long_bin','center_lat_bin','center_long_bin','pickup_dt_bin','pickup_datetime_group']

#     feature_name = [f for f in feature_build(load_data(train_path)).columns if f not in do_not_use_for_training]
#     print(f"We have {len(feature_name)} features to train the model on")

#     train_data = pd.read_csv(train_path,nrows = 10)
#     test_data = pd.read_csv(test_path,nrows = 10)

#     output_path = home_dir.as_posix() + '/data/processed'



if __name__ == '__main__':
    curr_dir = pathlib.Path(__file__)
    home_dir = curr_dir.parent.parent.parent
    train_path = home_dir.as_posix()+'/data/raw/train.csv'
    test_path = home_dir.as_posix()+'/data/raw/test.csv'

    do_not_use_for_training = ['id','pickup_datetime','dropoff_datetime','check_trip_duration','pickup_date','avg_speed_h','avg_speed_m','pickup_datetime_group']

    feature_name = [f for f in feature_build(load_data(train_path)).columns if f not in do_not_use_for_training]
    print(f"We have {len(feature_name)} features to train the model on")

    # Loading the data (Note: I removed nrows=10 so it processes the full dataset, 
    # but you can add it back if you are just testing!)
    train_data = pd.read_csv(train_path)
    test_data = pd.read_csv(test_path)

    # 1. Define the output path and create the directory if it doesn't exist
    output_path = home_dir.as_posix() + '/data/processed'
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    # 2. Build the features for both datasets
    train_processed = feature_build(train_data)
    test_processed = feature_build(test_data)

    # 3. Save the processed files into the data/processed directory
    train_processed.to_csv(output_path + '/train.csv', index=False)
    test_processed.to_csv(output_path + '/test.csv', index=False)
    
    print(f"Successfully saved processed data to {output_path}")

