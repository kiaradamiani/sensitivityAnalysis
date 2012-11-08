import matplotlib as mpl
if mpl.get_backend<>'agg':
    mpl.use('agg')
from sensitivity_analysis import *
import stemCell_custom_methods as SC
import gc
import os
import matplotlib.pyplot as plt

if sys.argv[1]=='stemTA':
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


fig=plt.figure(figsize=(15, 9))

def plotDistribution(sensitivityFolderName,modelFileName,paramName,paramValues,time2plot,showPlots=True):


    fig=plt.figure(figsize=(15, 9))

    freq_list=[]

    nParam=0
    for param in paramValues:
        nParam=nParam+1


        simFolderName="%s%s%s%s%s" % (sensitivityFolderName,os.sep,modelFileName.strip('.L'),paramName,param)

        print 'simFolderName',simFolderName


        #importo valori aggregato nel tempo per quel parametro
        aggregateVariable_in_time=SC.read_aggregate_variable_timestep(simFolderName,modelFileName,nSims,varName,'NumDivisions',time2plot)

        #importo bins
        fileNameBins="%s%s%s%s%s" % (modelFileName.strip('.L'),varName,'_binsKernel',paramName,'.txt')
        binsKernel=np.loadtxt(fileNameBins)

        m=binsKernel[0]
        M=binsKernel[-1]

        #bins=range(int(m),int(M)+2,1)

        bins=np.linspace(int(m),int(M)+2,100)
        binsticks=np.linspace(int(m),int(M)+2,4)


        list2hist=aggregateVariable_in_time

        freq,binss=np.histogram(list2hist,bins,normed=False)

        freq_list.append(list(freq))

        #print 'bins',bins

        #sovrascrivo sempre la stessa figura 1
        plt.figure(1)

        #print 'bins',bins
        #print 'freq',freq

        plt.subplot(2,6,nParam)

        #plt.bar(bins[0:-1],freq)
        plt.bar(bins[0:-1],freq)


        titolo="%s%s" % ('=',param)
        plt.title(titolo)

        plt.xticks([m,M],[m,M])

        plt.ylim([0, MaxExt(freq_list)])



    #save plot
    file_name="%s%s%s%s%s%s" % (modelFileName,varName,'Time',time2plot,paramName,'.png')
    plt.suptitle(paramName)
    plt.savefig(file_name,dpi=700)


    if(showPlots):
        plt.show()


    plt.clf()
    gc.collect()


for param in ParanNamesValues.keys():
    paramName = param
    paramValues = ParanNamesValues[param]

    plotDistribution(sensitivityFolderName,modelFileName,paramName,paramValues,time2plot)

