# -*- coding: cp1252 -*-

from sensitivity_analysis import *
import stemCell_custom_methods as SC
import gc
import os
from plot_distribution import *


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

#importa istogramma dati sperimentali
def getReferenceHistogram(fileName):
    bins=[]
    freqRel=[]
    
    with open(fileName, "r") as f:
        for row in f.readlines():
            thisline=row.split(' ')
            if thisline[0]=='generation':
                bins.append(int(thisline[1])-1)
                freqRel.append(float(thisline[3])/100)
    #BISOGNA AGGIUNGERE UN BIN PER POTER PLOTTARE
    bins.append(max(bins)+1)            
    #print bins, freqRel
    #print 'len bins reference',len(bins),len(freqRel)
    #print 'sum',sum(freqRel)
    return [freqRel,bins]
    

#per un dato valore di parametro ricavo istogramma a dato istante temporale
#def getParamValueHistogram(fileName):
 
#per un dato parametro tira fuori istogramma per ogni valore di quel parametro (a tempo t)
#def computeParamDistances(paramName,paramValues, varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,show=True,save=False):
   # for ParamValue in paramValues:
        
    #    print paramName,': ',ParamValue  

     #   bins,freqs=getParamValueHistogram(paramName,paramValue,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,sensitivityFolderName)


#scorre i parametri analizzati e per ogni parametro tirafuori istogramma per ogni valore di quel parametro a tempo t
def computeOverallDistances(ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,ReferenceHistogram,normalized=True,show=True,save=True):

    for param in ParanNamesValues.keys():
        paramName = param
        paramValues = ParanNamesValues[param]
                
        plotDistribution(sensitivityFolderName,modelFileName,paramName,paramValues,day,nSims,varName,nBins,ReferenceHistogram,normalized,show,save)

        
        #ParamDistances=computeParamDistances(paramName,paramValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,sensitivityFolderName)
        


ReferenceHistogram=getReferenceHistogram(fileName)
computeOverallDistances(ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,ReferenceHistogram)
