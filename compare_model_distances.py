# -*- coding: cp1252 -*-

from sensitivity_analysis import *
import stemCell_custom_methods as SC
import gc
import os
from distance_methods import *

 
varName=sys.argv[1]

timeDelta=1
nSims=500
time=10
cluster = False
timePoints=range(0,time+1,1) #simulation time points to save
saveTimes=timePoints

day=int(sys.argv[2])
nBins=0 #per ora scrpt prevede solo BIN UNITARIO

fileName='DATI_SPERIMENTALI'+os.sep+'Dati_'+str(day)+'days'

ReferenceHistogram=getReferenceHistogram(fileName)



from stemTAparameters import *

StemTAParamNamesValuesDistances=computeOverallDistances(sensitivityFolderName,day,nBins,ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,ReferenceHistogram)
StemTAParamNamesValues=ParanNamesValues

from stemTAsensorParameters import *

StemTASensorParamNamesValuesDistances=computeOverallDistances(sensitivityFolderName,day,nBins,ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,ReferenceHistogram)
StemTASensorParamNamesValues=ParanNamesValues


from singleTypeParameters import *

singleTypeParamNamesValuesDistances=computeOverallDistances(sensitivityFolderName,day,nBins,ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,ReferenceHistogram)
singleTypeParamNamesValues=ParanNamesValues


############################################
#            M A I N                       #
############################################

print 'min StemTA:', MinExt(StemTAParamNamesValuesDistances.values())
print "min StemTA Sensor:" , MinExt(StemTASensorParamNamesValuesDistances.values())
print "min SingleType Sensor:" , MinExt(singleTypeParamNamesValuesDistances.values())

    


#===============================================================================
# plt.figure()
# plt.ylim([0, max( MaxExt(StemTAParamNamesValuesDistances.values()),MaxExt(StemTASensorParamNamesValuesDistances.values()),MaxExt(singleTypeParamNamesValuesDistances.values()) ) ])
# 
# plt.suptitle('NumDivisons'+varName)
# 
# plt.hold(True)
# plt.subplot(1,3,1)
# 
# 
# nParam=0
# for param in StemTAParamNamesValues.keys():
# 
#    paramValues = StemTAParamNamesValues[param]   
#    #overallDistance=sum(ParanNamesValuesDistances[param])
#                
#    titolo='stemTA'
#    plt.title(titolo)
# 
#    #annotation='TOTdist:'+str(overallDistance)
#    
#    plt.plot(paramValues,StemTAParamNamesValuesDistances[param],'+-',label=param)
#    
#    plt.legend(loc='best')      
#    nParam=nParam+1
#    
#              
# #save plot
# file_name=varName+'CompareDistances.png'
# plt.savefig(file_name,dpi=700)
# 
# 
# plt.show()
#===============================================================================


        






        
     

