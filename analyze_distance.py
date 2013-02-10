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
    print 'len bins reference',len(bins),len(freqRel)
    #print 'sum',sum(freqRel)
    return [freqRel,bins]
    

 
#per un dato parametro tira fuori istogramma per ogni valore di quel parametro (a tempo t)
def computeParamDistances(ReferenceHistogram,paramName,paramValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,normalized,show=True,save=False):
    ReferenceHistogram_tmp=ReferenceHistogram
    
    ParamValuesDistances=[] #qui salvero per ogni valore di parametro la differenza dell'istograma relativo a quel valore con l'istogramma di riferimento
    print paramName,':',paramValues
    for ParamValue in paramValues:
               
        simFolderName="%s%s%s%s%s" % (sensitivityFolderName,os.sep,modelFileName.strip('.L'),paramName,ParamValue)
        fileNameBins="%s%s%s%s%s" % (modelFileName.strip('.L'),varName,'_binsKernel',paramName,'.txt')
        
        print simFolderName
        
        Distribution=getDistribution(simFolderName,fileNameBins,modelFileName,nSims,varName,day,nBins,normalized)
        #azzero reference istagram
        ReferenceHistogram=ReferenceHistogram_tmp
        
        #print 'before: len(Distribution)',len(Distribution[0]),len(Distribution[1]),'len(reference)',len(ReferenceHistogram[0]),len(ReferenceHistogram[1])
        
        #ALLINEO ISTOGRAMMI PRIMA DI CALCOLARE DISTANZA
        Distribution,ReferenceHistogram=getAllineatedHistograms(Distribution,ReferenceHistogram) 
        #print 'after: len(Distribution)',len(Distribution[0]),len(Distribution[1]),'len(reference)',len(ReferenceHistogram[0]),len(ReferenceHistogram[1])
        
        #CALCOLO DISTANZA TRA ISTOGRAMMI ALLINEATI
        distance=getHistogramsDistance(Distribution,ReferenceHistogram)
                
        ParamValuesDistances.append(distance)
        
        #print 'distance',distance
        #print 'ParamValuesDistances',ParamValuesDistances        
    return ParamValuesDistances



        
#distanza tra due istogrammi con bin ALLINEATI      
def getHistogramsDistance(hist1,hist2):
    
    freqs1=hist1[0]
    freqs2=hist2[0]

    distance=0
    for i in range (0,len(freqs1)):
        diff=abs(freqs1[i]-freqs2[i])
        distance=distance+diff
        return distance


#allinea due istogrammi con bin unitari (non necesariamente lo stesso numero) mettendo 0 alle frequenze che mancano, VA BENE ACHE SE NON UNITARI MA con gli stessi edges (es: 2, 4 ,6) non (3, 5, 79   
def getAllineatedHistograms(hist1,hist2):
        
    bins1=list(hist1[1])
    bins2=list(hist2[1])
    
    freqs1=list(hist1[0])
    freqs2=list(hist2[0])
    
    #print 'bins1 berfore',bins1,'bins2',bins2
    #print 'freq1 before',freqs1,'freq2',freqs2  
    
    #devo allineare le due dizstribuzioni (mettendo la frequenza a 0 per i bin che non coincidono
    #scorro prima distribuzione e aggiungo mancanti nella seconda
    for bin in bins1:
        if bin not in bins2:
            #devo capire in che posizione inserirlo #scorro lista bins fino a che non trovo bin maggiore di quello e lo piazzo li
            i=len(bins2)-1
            while bins2[i]>bin and i>0:
                i=i-1     
            bins2.insert(i+1,bin)
            freqs2.insert(i+1,0)
        
    #e vicenversa
    nbin=0    
    for bin in bins2:
        if bin not in bins1:
            #devo capire in che posizione inserirlo #scorro lista bins fino a che non trovo bin maggiore di quello e lo piazzo li
            i=len(bins1)-1
            while bins1[i]>bin and i>=0:
                i=i-1  
            bins1.insert(i+1,bin)
            freqs1.insert(i+1,0)
    
    #print 'bins1 after',bins1,'bins2',bins2
    #print 'freq1 after',freqs1,'freq2 ',freqs2      
    #print 'len bins1 after',len(bins1),'bins2',len(bins2)
    #print 'len freq1 after',len(freqs1),'freq2 ',len(freqs2)  
    
    return [freqs1,bins1],[freqs2,bins2]
    
    

#scorre i parametri analizzati e per ogni parametro tirafuori (in un dizionario) distanze istogramma da istogramma di riferimento per ogni valore di quel parametro a tempo t
def computeOverallDistances(ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,ReferenceHistogram,normalized=True,show=True,save=True):
    
    ParanNamesValuesDistances={}

    for param in ParanNamesValues.keys():
        paramName = param
        paramValues = ParanNamesValues[param]
        
        #plotta distribuzioni di quel parametro (una per valore di parametro) against la distribuzione di riferimento        
        #plotDistribution(sensitivityFolderName,modelFileName,paramName,paramValues,day,nSims,varName,nBins,ReferenceHistogram,normalized,show,save)

        #per ogni valore di parametro calcola distanza distribuzione da distribuzione di riferimento               
        ParamValuesDistances=computeParamDistances(ReferenceHistogram,paramName,paramValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,normalized)
        
        ParanNamesValuesDistances[param]=ParamValuesDistances
    
    return ParanNamesValuesDistances
        


ReferenceHistogram=getReferenceHistogram(fileName)
ParanNamesValuesDistances=computeOverallDistances(ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,ReferenceHistogram)

#print ParanNamesValuesDistances

#summurizeDistances(ParanNamesValuesDistances)
