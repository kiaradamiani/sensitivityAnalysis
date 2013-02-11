import matplotlib as mpl
#if mpl.get_backend<>'agg':
 #   mpl.use('agg')
from sensitivity_analysis import *
import stemCell_custom_methods as SC
import gc
import os
import matplotlib.pyplot as plt

#fig=plt.figure(figsize=(15, 9))


def getDistribution(simFolderName,fileNameBins,modelFileName,nSims,varName,time2plot,nBins,normalized):
    
        #importo valori aggregato nel tempo per quel parametro
        aggregateVariable_in_time=SC.read_aggregate_variable_timestep(simFolderName,modelFileName,nSims,varName,'NumDivisions',time2plot)
        

        binsKernel=np.loadtxt(fileNameBins)

        m=binsKernel[0]
        M=binsKernel[-1]

        #bins=range(int(m),int(M)+2,1)
        
        if nBins==0:
            bins=range(int(m),int(M)+2,1)

        else:
            bins=np.linspace(int(m),int(M)+2,nBins)

        list2hist=aggregateVariable_in_time

        freq,binss=np.histogram(list2hist,bins,normed=normalized)
        #print 'bins hist',bins,'freq hist',freq

        return [freq,bins]
    
    
#if nBins is seto to 0 all the possible bins will be plotted
def plotDistribution(sensitivityFolderName,modelFileName,paramName,paramValues,time2plot,nSims,varName,nBins,referenceDistribution,normalized,titlesList,showPlots,savePlots):


    fig=plt.figure(figsize=(15, 9))

    freq_list=[]

    nParam=0
    for param in paramValues:
        nParam=nParam+1


        simFolderName="%s%s%s%s%s" % (sensitivityFolderName,os.sep,modelFileName.strip('.L'),paramName,param)
        fileNameBins="%s%s%s%s%s" % (modelFileName.strip('.L'),varName,'_binsKernel',paramName,'.txt')
  

        print 'simFolderName',simFolderName

        Distribution=getDistribution(simFolderName,fileNameBins,modelFileName,nSims,varName,time2plot,nBins,normalized)
        
        freq=Distribution[0]
        bins=Distribution[1]

        freq_list.append(list(freq))
        

        #sovrascrivo sempre la stessa figura 1
        #plt.figure(1)
        plt.hold(True)

        #print 'bins',len(bins),'freq',len(freq)
    
        plt.subplot(2,6,nParam)

        plt.bar(bins[0:-1],freq)
        
        #plotto distribuzione di riferimento
        if(referenceDistribution!=[]):
            plt.hold(True)
            plt.bar(referenceDistribution[1][0:-1],referenceDistribution[0],color='r')
            plt.hold(False)
            plt.ylim([0, max(MaxExt(freq_list),max(referenceDistribution[0]))+0.1 ])
            
            #se fornita aggiungo etichetta con valore distanza
            if titlesList!=[]:
                print 'titlesList',titlesList
                annotation='dist:'+str(titlesList[nParam-1])
                plt.text(0.5,0.5,annotation)
        
        else:
            plt.ylim([0, MaxExt(freq_list)+0.1 ])




        titolo="%s%s" % ('=',param)
        plt.title(titolo)

        plt.xticks([bins[0],bins[-1]],[bins[0],bins[-1]])
        

        #print 'freq_list',freq_list
        
        #print 'max(MaxExt(freq_list)',MaxExt(freq_list),'max(referenceDistribution[0]))+0.1',max(referenceDistribution[0]),'max(MaxExt(freq_list),max(referenceDistribution[0]))',max(MaxExt(freq_list),max(referenceDistribution[0]))
    
    plt.suptitle(paramName)


    if (savePlots):
        #save plot
        file_name="%s%s%s%s%s%s" % (modelFileName,varName,'Time',time2plot,paramName,'.png')
        plt.savefig(file_name,dpi=700)


    if(showPlots):
        plt.show()
        
    plt.close()
    plt.clf()
    gc.collect()
