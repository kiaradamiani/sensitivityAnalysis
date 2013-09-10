# -*- coding: cp1252 -*-

from sensitivity_analysis import *
import stemCell_custom_methods as SC
import gc
import os

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

paramName='$StaminalDivisionRate$'

paramvalues=ParanNamesValues[paramName]


SC.get_sensitivity_coefficient_plottingEverything(paramName,paramvalues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,sensitivityFolderName,loadAggregate=True)

