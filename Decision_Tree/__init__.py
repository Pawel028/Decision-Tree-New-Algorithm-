from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def find_string(string, array):
    for i in array:
        if i == string:
            return True
        
    return False

def exec_func_mat(mat,command):
    exec(command, globals())

class Data_Tree_BinaryDepvar:
    def __init__(self,data,depvar,usable_vars, min_size_to_split,metric_string,method = 'exclusion'):
        self.data = data
        self.depvar = depvar
        self.tracker = [""]*len(data[depvar])
        self.usable_vars = usable_vars
        self.min_size_to_split = min_size_to_split
        self.metric_string = metric_string
        self.method = method

    def Best_Split(self):
        diff = 0
        split_var=''
        neg_split_var_cat=np.array([])
        pos_split_var_cat=np.array([])

        for var in self.usable_vars:
            length = len(self.data[var].unique())
            neg_split = np.array([])
            pos_split = np.array([])
            
            str_new = "threshold = "+self.metric_string.replace("mat","self.data")
            lcls=locals()                    
            exec(str_new,globals(),lcls)
            threshold = lcls["threshold"]
            

            if (length >1 and var != self.depvar and var != "Claims"):
                for cat in self.data[var].unique():
                    if self.method == 'exclusion':
                        mat = self.data[self.data[var]!=cat]
                    elif self.method == 'inclusion':
                        mat = self.data[self.data[var]==cat]

                    str_new = "mtr = "+self.metric_string
                    lcls=locals()                    
                    exec(str_new,globals(),lcls)
                    mtr = lcls["mtr"]
                    print(var,cat,mtr,threshold)

                    if mtr>=threshold:
                        neg_split = np.append(neg_split,cat)
                    else:
                        pos_split = np.append(pos_split,cat)
                mat_neg = self.data[self.data[var].isin(neg_split)]
                mat_pos = self.data[self.data[var].isin(pos_split)]
                str_new = "neg_metric = "+self.metric_string.replace("mat","mat_neg")
                lcls=locals()
                exec(str_new,globals(),lcls)
                neg_metric = lcls["neg_metric"]
                str_new = "pos_metric = "+self.metric_string.replace("mat","mat_pos")
                lcls=locals()
                exec(str_new)
                pos_metric = lcls["pos_metric"]
                # print(neg_metric,pos_metric)
                diff1=abs(neg_metric-pos_metric)
                if diff1>diff:
                    split_var=var
                    neg_split_var_cat = neg_split
                    pos_split_var_cat = pos_split
        # print(len(self.data),split_var)
        return split_var, neg_split_var_cat, pos_split_var_cat


    def split_data1(self):
        split_var, neg_split_var_cat, pos_split_var_cat = self.Best_Split()

        if split_var != '' and len(self.data)>self.min_size_to_split:
            neg_data = Data_Tree_BinaryDepvar(self.data[self.data[split_var].isin(neg_split_var_cat)], self.depvar, self.usable_vars, self.min_size_to_split,self.metric_string,self.method)
            neg_data.split_data1()

            pos_data = Data_Tree_BinaryDepvar(self.data[self.data[split_var].isin(pos_split_var_cat)], self.depvar, self.usable_vars, self.min_size_to_split,self.metric_string,self.method)
            pos_data.split_data1()

            str_neg=""
            for k in neg_split_var_cat:
                if type(k)==str:
                    str_neg = str_neg+str(k)+","
                else:
                    str_neg = str_neg+str(int(k))+","


            str_pos=""
            for k in pos_split_var_cat:
                if type(k)==str:
                    str_pos = str_pos+str(k)+","
                else:
                    str_pos = str_pos+str(int(k))+","

            print(str_neg,str_pos)

            neg_data.tracker = list(map(lambda x: str(split_var)+"-> Negative ["+str_neg+"]: "+x, neg_data.tracker)) # type: ignore
            pos_data.tracker = list(map(lambda x: str(split_var)+"-> Positive ["+str_pos+"]: "+x, pos_data.tracker)) # type: ignore
            self.tracker = neg_data.tracker+pos_data.tracker
            self.data = pd.concat([neg_data.data, pos_data.data], ignore_index=True)
        else:
            self.tracker = [""]*len(self.data)
            self.data = self.data
        return self



