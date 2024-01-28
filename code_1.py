from Decision_Tree import Data_Tree_BinaryDepvar
import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

train = pd.read_csv("./Data/train.csv")
test = pd.read_csv("./Data/test.csv")
X=train
y=train.Exited
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.15, random_state=42)
metric_str = "(mat[self.depvar].sum()/len(mat[self.depvar]))"
data=Data_Tree_BinaryDepvar(X_train,"Exited",['Geography','Gender',	'NumOfProducts',	'HasCrCard',	'IsActiveMember'], 50000,metric_str)
data.split_data1()
x=data.data
x['tracker']=data.tracker
# print(data.tracker)
x.to_csv("Updated_train_data_new.csv")
# X_val.to_csv("Validation_data_new.csv")

# for k in x.tracker.unique():
#     x[x.tracker==k]