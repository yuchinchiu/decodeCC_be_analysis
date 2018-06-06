# -*- coding: utf-8 -*-
"""
Created on 2/19/2018
@author: yc180
- fMRI subjects

"""

import os
import pandas as pd

version = 'fMRI_v1'

currentDir = os.path.dirname(os.path.realpath(__file__))
#'C:\\Users\\yc180\\Documents\\1_decodeCC_fMRI\\be_data'

os.chdir("..")

GpDataDir = os.getcwd() + "\\be_data"
os.chdir(currentDir)
#%% Do a quick first past to exclude sbj whose stroop task accuracy is too low <75%
sbjList = [3, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        
taskName = 'stroop'
gpData = pd.DataFrame()    
for S in sbjList:
    D = pd.DataFrame()        
    for runNr in range(1,5):
        dataDir = GpDataDir + os.sep + 'S' + str(S) + os.sep 
        f = dataDir + taskName + '_S' + str(S) + '_r' + str(runNr) +'.csv'
        df = pd.read_csv(f)
        df.drop(df.columns[[0,1]],axis=1,inplace=True)  # there were two unamed column- drop that one
        D = pd.concat([D, df], axis=0).reset_index(drop=True)
    # concatenate to Group DataFrame
    D['sbjId'] = S        
    gpData = pd.concat([gpData, D], axis=0).reset_index(drop=True)

# output group DataFrame
outputFileName = 'gp_' + taskName + '_' + version
gpData.to_pickle(outputFileName + '.pkl')
gpData.to_csv(outputFileName + '.csv',encoding='utf-8', index=False)
    
#%%
taskName = 'memory'
gpData = pd.DataFrame()    
for S in sbjList:
    D = pd.DataFrame()        
    for runNr in range(5,7):
        dataDir =  GpDataDir + os.sep + 'S' + str(S) + os.sep 
        f = dataDir + taskName + '_S' + str(S) + '_r' + str(runNr) +'.csv'
        df = pd.read_csv(f)
        df.drop(df.columns[[0,1]],axis=1,inplace=True)  # there were two unamed column- drop that one
        D = pd.concat([D, df], axis=0).reset_index(drop=True)            
        D['sbjId'] = S
    # preprocessing - calculate Memory task Accuracy
    D['sbjACC'] = 0         
    if S%2==0:
        D.loc[(D.sbjResp<=2) & (D.corrAns=='new'), 'sbjACC']=1
        D.loc[(D.sbjResp>=3) & (D.corrAns=='old'), 'sbjACC']=1
        D.sbjResp.replace(1,'defNew',inplace=True)
        D.sbjResp.replace(2,'probNew',inplace=True)
        D.sbjResp.replace(3,'probOld',inplace=True)
        D.sbjResp.replace(4,'defOld',inplace=True)
    else:
        D.loc[(D.sbjResp>=3) & (D.corrAns=='new'), 'sbjACC']=1
        D.loc[(D.sbjResp<=2) & (D.corrAns=='old'), 'sbjACC']=1
        D.sbjResp.replace(4,'defNew',inplace=True)
        D.sbjResp.replace(3,'probNew',inplace=True)
        D.sbjResp.replace(2,'probOld',inplace=True)
        D.sbjResp.replace(1,'defOld',inplace=True)
        
        
    
        
    # concatenate to Group DataFrame
    gpData = pd.concat([gpData, D], axis=0).reset_index(drop=True)        
    
        

# output group DataFrame
outputFileName = 'gp_' + taskName + '_' + version
gpData.to_pickle(outputFileName + '.pkl')
gpData.to_csv(outputFileName + '.csv',encoding='utf-8', index=False)

