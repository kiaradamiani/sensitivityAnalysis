import matplotlib as mpl
#if mpl.get_backend<>'agg':
 #  mpl.use('agg')
from sensitivity_analysis import *
import stemCell_custom_methods as SC
import gc
import os
import matplotlib.pyplot as plt
from plot_distribution import *

print 'sys.argv[1]',sys.argv[1]

if sys.argv[1]=='stemTA':
    print 'yessa'
    from stemTAparameters import *
if sys.argv[1]=='stemTAsensor':
    from stemTAsensorParameters import *
if sys.argv[1]=='singleType':
    from singleTypeParameters import *

varName=sys.argv[2]

time2plot=sys.argv[3]

time2plot=int(time2plot)

print 'time2plot',time2plot

timeDelta=1
nSims=500
time=10
cluster = False
timePoints=range(0,time+1,1) #simulation time points to save
saveTimes=timePoints


#fig=plt.figure(figsize=(15, 9))

referenceDistribution=[] 
nBins=0
normalized=True

for param in ParanNamesValues.keys():
    paramName = param
    paramValues = ParanNamesValues[param]

    plotDistribution(sensitivityFolderName,modelFileName,paramName,paramValues,time2plot,nSims,varName,nBins,referenceDistribution,normalized,True,False)

