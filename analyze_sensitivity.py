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


def getAndPlotCoefficietnsRanking(ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,show=True,save=False):

    plt.figure()
    plt.hold(True)

    for param in ParanNamesValues.keys():
        paramName = param
        paramValues = ParanNamesValues[param]

        paramCoefficient=SC.get_sensitivity_coefficient(paramName,paramValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,sensitivityFolderName)

        plt.plot(timePoints[1:-1], paramCoefficient[1:-1],label=param)

    plt.legend(loc='best')

    title="%s%s" % ("Sensitivity ranking NumDivisions", varName)

    plt.title(title)
    ##save plot
    figName="%s%s%s%s" % (modelFileName.strip('.L'),"RankingNumDivisions",varName,".png")
    plt.savefig(figName)


    plt.show()


getAndPlotCoefficietnsRanking(ParanNamesValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster)
