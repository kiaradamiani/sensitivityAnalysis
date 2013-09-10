    # -*- coding: cp1252 -*-

from sensitivity_analysis import *
import stemCell_custom_methods as SC
import gc
import os
from distance_methods import *
import numpy as np 

 
varName=sys.argv[1]

timeDelta=1
nSims=500
time=10
cluster = False
timePoints=range(0,time+1,1) #simulation time points to save
saveTimes=timePoints

days=[2,3,4,5,6,7]


nBins=0 #per ora scrpt prevede solo BIN UNITARIO



from stemTAparameters import *
StemTAParamNamesValues=ParanNamesValues
StemTAParanNamesMarkers=ParanNamesMarkers
StemTAsensitivityFolderName=sensitivityFolderName

#from stemTAsensorParameters import *
#StemTAsensorParamNamesValues=ParanNamesValues
#StemTAsensorParanNamesMarkers=ParanNamesMarkers
#StemTASensorsensitivityFolderName=sensitivityFolderName
#
#from singleTypeParameters import *
#singleTypeParamNamesValues=ParanNamesValues
#singleTypeParanNamesMarkers=ParanNamesMarkers
#SingleTypesensitivityFolderName=sensitivityFolderName


IntegralStemTAParamNamesValuesDistances={}
#IntegralStemTAsensorParamNamesValuesDistances={}
#IntegralSingleTypeParamNamesValuesDistances={}
#

StemTAParamNamesValuesDistances={}

timeCurves={}

Integrals={}


#creo per ogni giorno un dizionario delle distanze di ogni parametro
nday=0
for day in days:
    fileName='PARK_MCF10A'+os.sep+'Dati_'+str(day)+'days_PARK'
    #    print 'fileName',fileName
    ReferenceHistogram=getReferenceHistogram(fileName)
    #distancess day 0
    StemTAParamNamesValuesDistances[day]=computeOverallDistances(StemTAsensitivityFolderName,day,nBins,StemTAParamNamesValues,varName,"stemTA.L",timePoints,timeDelta,nSims,time,saveTimes,cluster,ReferenceHistogram)


#creo per ogni parametro un dizionario delle distanze dei giorni
for param in StemTAParamNamesValues.keys():
        x=np.asarray(days)+1
        x=[math.log(p) for p in x]

        Integrals[param]=[]
    
        paramValues=StemTAParamNamesValues[param]

        nValue=0
        for v in paramValues:
            timeCurves[v]=[]
            for day in days:
               timeCurves[v].append(StemTAParamNamesValuesDistances[day][param][nValue])

            #calcolo integrale di ogni param value e la appendo all'integrale di quel parametro


            y=timeCurves[v]
            integral_sum=0
            for a in range(0,len(y)-1):
                for b in range (1,len(y)):
                    integral_ab=(x[b]-x[a])*(y[a]+y[b])/2
                    integral_sum=integral_sum+integral_ab
    
            Integrals[param].append(integral_sum)


            nValue=nValue+1





plt.figure()
plt.suptitle('Integral days '+str(days)+' NumDivisons'+varName)
plt.hold(True)
nParam=0
for param in StemTAParamNamesValues.keys():
    
   plt.subplot(1,5,nParam)

    
   plt.ylim([MinExt(Integrals.values()),MaxExt(Integrals.values())])


   paramValues = StemTAParamNamesValues[param]

   titolo='stemTA'
   plt.title(titolo)

   #annotation='TOTdist:'+str(overallDistance)

   plt.plot(paramValues,Integrals[param],'+-',label=param,marker=StemTAParanNamesMarkers[param][0],color=StemTAParanNamesMarkers[param][1])

   plt.xlabel(param)

   nParam=nParam+1




#save plot
file_name=varName+'CompareDistances.png'
plt.savefig(file_name,dpi=700)
#
#
plt.show()


    #plt.ylim([min( MinExt(IntegralStemTAParamNamesValuesDistances.values()),MinExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MinExt(IntegralSingleTypeParamNamesValuesDistances.values())), max( MaxExt(IntegralStemTAParamNamesValuesDistances.values()),MaxExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MaxExt(IntegralSingleTypeParamNamesValuesDistances.values()) ) ])
#
##plt.legend(loc='best')
#   nParam=nParam+1
#


#############################################
##            M A I N                       #
############################################
#
##print 'min IntegralStemTAParamNamesValuesDistances:', MinExt(IntegralStemTAParamNamesValuesDistances.values())
##print "min IntegralStemTAsensorParamNamesValuesDistances:" , MinExt(IntegralStemTAsensorParamNamesValuesDistances.values())
##print "min IntegralSingleTypeParamNamesValuesDistances:" , MinExt(IntegralSingleTypeParamNamesValuesDistances.values())
#
#
#
#
#plt.figure()
##plt.ylim([min( MinExt(IntegralStemTAParamNamesValuesDistances.values()),MinExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MinExt(IntegralSingleTypeParamNamesValuesDistances.values()) ), max( MaxExt(IntegralStemTAParamNamesValuesDistances.values()),MaxExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MaxExt(IntegralSingleTypeParamNamesValuesDistances.values()) ) ])
#
#
#
#plt.suptitle('Integral days '+str(days)+' NumDivisons'+varName)
#
#plt.hold(True)
#nParam=0
#for param in StemTAParamNamesValues.keys():
#   plt.subplot(1,5,nParam)
#   plt.ylim([MinExt(IntegralStemTAParamNamesValuesDistances.values()),MaxExt(IntegralStemTAParamNamesValuesDistances.values())])
#
#
#
#   paramValues = StemTAParamNamesValues[param]   
#   #overallDistance=sum(ParanNamesValuesDistances[param])
#               
#   titolo='stemTA'
#   plt.title(titolo)
#
#   #annotation='TOTdist:'+str(overallDistance)
#   
#   plt.plot(paramValues,IntegralStemTAParamNamesValuesDistances[param],'+-',label=param,marker=StemTAParanNamesMarkers[param][0],color=StemTAParanNamesMarkers[param][1])
#
#   plt.xlabel(param)
#   
#    #plt.ylim([min( MinExt(IntegralStemTAParamNamesValuesDistances.values()),MinExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MinExt(IntegralSingleTypeParamNamesValuesDistances.values())), max( MaxExt(IntegralStemTAParamNamesValuesDistances.values()),MaxExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MaxExt(IntegralSingleTypeParamNamesValuesDistances.values()) ) ])
#
##plt.legend(loc='best')
#   nParam=nParam+1
#   
##plt.hold(True)
##plt.subplot(1,3,2)
##plt.figure()
##plt.ylim([min( MinExt(IntegralStemTAParamNamesValuesDistances.values()),MinExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MinExt(IntegralSingleTypeParamNamesValuesDistances.values())), max( MaxExt(IntegralStemTAParamNamesValuesDistances.values()),MaxExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MaxExt(IntegralSingleTypeParamNamesValuesDistances.values()) ) ])
#
#
##nParam=0
##for param in StemTAsensorParamNamesValues.keys():
##
##   paramValues = StemTAsensorParamNamesValues[param]   
##   #overallDistance=sum(ParanNamesValuesDistances[param])
##               
##   titolo='stemTAsensor'
##   plt.title(titolo)
##
##   #annotation='TOTdist:'+str(overallDistance)
##   
##   plt.plot(IntegralStemTAsensorParamNamesValuesDistances[param],'+-',label=param,marker=StemTAsensorParanNamesMarkers[param][0],color=StemTAsensorParanNamesMarkers[param][1])
##   
##   plt.ylim([min( MinExt(IntegralStemTAParamNamesValuesDistances.values()),MinExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MinExt(IntegralSingleTypeParamNamesValuesDistances.values())), max( MaxExt(IntegralStemTAParamNamesValuesDistances.values()),MaxExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MaxExt(IntegralSingleTypeParamNamesValuesDistances.values()) ) ])
##
##   #plt.legend(loc='best')      
##   nParam=nParam+1
##   
##plt.hold(True)
##plt.subplot(1,3,3)
###plt.figure()
##
##
##nParam=0
##for param in singleTypeParamNamesValues.keys():
##
##   paramValues =singleTypeParamNamesValues[param]   
##   #overallDistance=sum(ParanNamesValuesDistances[param])
##               
##   titolo='singleType'
##   plt.title(titolo)
##
##   #annotation='TOTdist:'+str(overallDistance)
##   
##   plt.plot(IntegralSingleTypeParamNamesValuesDistances[param],'+-',label=param,marker=singleTypeParanNamesMarkers[param][0],color=singleTypeParanNamesMarkers[param][1])
##   
##   plt.ylim([min( MinExt(IntegralStemTAParamNamesValuesDistances.values()),MinExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MinExt(IntegralSingleTypeParamNamesValuesDistances.values())), max( MaxExt(IntegralStemTAParamNamesValuesDistances.values()),MaxExt(IntegralStemTAsensorParamNamesValuesDistances.values()),MaxExt(IntegralSingleTypeParamNamesValuesDistances.values()) ) ])
##
##   #plt.legend(loc='best')      
##   nParam=nParam+1    
#
#             

#
#







        
     

