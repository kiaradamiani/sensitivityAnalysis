# -*- coding: cp1252 -*-

from sensitivity_analysis import *
import stemCell_custom_methods as SC
import gc
import os
from distance_methods import *


if sys.argv[1]=='stemTA':
 from stemTAparameters import *
if sys.argv[1]=='stemTAsensor':
 from stemTAsensorParameters import *
if sys.argv[1]=='singleType':
 from singleTypeParameters import *
 
varName=sys.argv[2]

timeDelta=1
nSims=500
time=10
cluster = False
timePoints=range(0,time+1,1) #simulation time points to save
saveTimes=timePoints


############################################
#            M A I N                       #
############################################
day=int(sys.argv[3])
nBins=0 #per ora scrpt prevede solo BIN UNITARIO



fileName='DATI_SPERIMENTALI'+os.sep+'Dati_'+str(day)+'days'


ReferenceHistogram=getReferenceHistogram(fileName)
ParanNamesValuesDistances=computeOverallDistances(sensitivityFolderName,day,nBins,ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,ReferenceHistogram)
summurizeDistances(ParanNamesValuesDistances,ParanNamesValues,varName,modelFileName)
        
     

