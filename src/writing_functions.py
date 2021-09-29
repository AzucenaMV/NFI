import pandas as pd
from src.classes import *

def save_data_to_csv(data_to_save: TrainInput, names: List):
    tracedata = data_to_save.data
    labels = data_to_save.labels
    for trace_index in range(len(tracedata)):
        scans = range(1, 4801)
        df_dict = {'scan': scans}
        for dye in range(6):
            df_dict['dye'+str(dye+1)] = tracedata[trace_index][:,dye].tolist()
        df_dict['dye5'], df_dict['dye6'] = df_dict['dye6'], df_dict['dye5']
        for dye in range(6):
            df_dict['dye'+str(dye+1)+'GT'] = labels[trace_index][:,dye].tolist()
        df_dict['dye5GT'], df_dict['dye6GT'] = df_dict['dye6GT'], df_dict['dye5GT']

        dataframe = pd.DataFrame(df_dict)
        dataframe.to_csv('csvs/sizestd5th/train/'+names[trace_index]+'_train.csv', index=False)
    pass

