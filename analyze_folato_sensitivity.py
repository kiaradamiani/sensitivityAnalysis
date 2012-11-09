# -*- coding: cp1252 -*-

from sensitivity_analysis import *
#from process_Loutput import *
import folato_custom_methods as FC

timeDelta=1
nSims=88
time=40
cluster = False
timePoints=range(0,time+1,1) #simulation time points to save
saveTimes=timePoints



#ParanNamesValues={}
#ParanNamesValues['FTS_Vmax']=[int (x) for x in np.linspace(100, 300, num=3)]

ParanNamesValues={}
ParanNamesValues['FTS_Vmax']=[100, 1000, 2000, 3900, 5000, 10000, 100000, 250000, 400000, 486000]
#ParanNamesValues['FTS_Kthf']=[0.1, 1, 2, 3, 5, 10, 50, 100, 300, 600]
#ParanNamesValues['FTS_Kcoo'] = [8, 15, 25, 40, 43, 50, 100, 250, 500, 1000]
ParanNamesValues['fMTCH_Vmax'] = [880, 20000, 50000, 100000, 300000, 450000, 500000, 550000, 800000, 1380000]
####ParanNamesValues['fMTCH_K1cf'] = [4, 5, 7, 10, 15, 30, 60, 120, 180, 250]
#ParanNamesValues['rMTCH_Vmax'] = [10.5, 100, 1000, 10000, 20000, 50000, 100000, 250000, 750000, 1380000]
####ParanNamesValues['rMTCH_K10f'] = [20, 65, 100, 150, 200, 250, 300, 350, 400, 450]
ParanNamesValues['fMTD_Vmax'] = [520, 20000, 50000, 80000, 140000, 220000, 320000, 420000, 500000, 594000]
####ParanNamesValues['fMTD_K2cf'] = [2, 2.3, 2.6, 2.9, 3.2, 3.5, 3.9, 4.3, 4.7, 5]
#ParanNamesValues['rMTD_Vmax'] = [594000, 594650,595300, 595950, 596600, 597250, 597900, 598550, 599200, 600000]
####ParanNamesValues['rMTD_K1cf'] = [1, 2, 3,4, 5, 6, 7, 8, 9, 10]

ParanNamesMarkers={}
markers=['o','v','^','<','>','1','2','3','4','s','p','*','h','H','+','x']
colors=['b','g','r','c','m','y','k']

ParanNamesMarkers['FTS_Vmax']=[markers[0],colors[0],'FTHFS Vmax']
ParanNamesMarkers['FTS_Kthf']=[markers[1],colors[1],'Km THF']
ParanNamesMarkers['FTS_Kcoo']=[markers[2],colors[2],'Km Formate']
ParanNamesMarkers['fMTCH_Vmax'] = [markers[3],colors[3],'MTHFC Vmax']
ParanNamesMarkers['fMTCH_K1cf'] =[markers[4],colors[5]]
ParanNamesMarkers['rMTCH_Vmax'] = [markers[5],colors[4]]
ParanNamesMarkers['rMTCH_K10f'] = [markers[6],colors[6]]
ParanNamesMarkers['fMTD_Vmax'] = [markers[7],colors[0],'MTHFD Vmax']
ParanNamesMarkers['fMTD_K2cf'] =[markers[8],colors[1]]
ParanNamesMarkers['rMTD_Vmax'] = [markers[9],colors[2],'MTHFD Vmax']
ParanNamesMarkers['rMTD_K1cf'] = [markers[10],colors[3]]


print 'ParanNamesValues',ParanNamesValues

varName='[CH2=THF]'
varCol=4 #colonna relativa alla variabile di interesse

modelFileName='test'

output_file_suffix='Vmax'

#procedura per calcolare sensitivity coefficient di una variabile rispetto ad un parametro

## dalle varie sim creo un dizionario (param,time) con i valori di una data  variabile per i valori di un dato parametro
## passo il dizionario a get_3d_freqse ottengo matrice 3d delel frequenze
## la matrice 3d a compute_sensitivity e ottengo curve di sentisitivà

def get_sensitivity_coefficient(paramName,paramValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,useKernel,plotMean=True):
    #inizializzo dizionari
    aggregateVariable_in_time_dictionary={}

    paramValuePos=0
    for param in paramValues:

        #devo aggreggare tutti i lanci per quel valore di parametro
        aggregateVariable_in_time=FC.aggregate_runs(modelFileName,paramName,param,paramValuePos,varCol,varName,nSims,saveTimes)

        paramValuePos=paramValuePos+1 

        #metto aggregate output in dizionario relativo alal variabile
        aggregateVariable_in_time_dictionary[param]=DataSummary(aggregateVariable_in_time)

    #controllo che ci sia qualche lista non vuota nel dizionario
    len_aggregateVariable_in_time_dictionary=sum([x.total for x in aggregateVariable_in_time_dictionary.values()])

    if len_aggregateVariable_in_time_dictionary>0:
        
        #da dizionario 3d delle simulazioni ottengo array 3d (parametro, tempo e bins) delle frequenze kernel e istogramma
        Variable_paramTime_freqsKernel,Variable_bins=get_3D_freqs(aggregateVariable_in_time_dictionary)

        #scelgo quali frequenze usare
        if useKernel:
            Variable_sensitivity=compute_sensitivity(Variable_paramTime_freqsKernel,aggregateVariable_in_time_dictionary.keys())
        else:
            Variable_sensitivity=compute_sensitivity(Variable_paramTime_freqsRel,aggregateVariable_in_time_dictionary.keys())
            
        fileName="%s%s%s%s%s" % (modelFileName.strip('.L'),varName,"_sensitivity_",paramName,'.txt')
        np.savetxt(fileName,Variable_sensitivity)
        #salvo frequenze assolute
        fileNameFreqKernel="%s%s%s%s%s" % (modelFileName.strip('.L'),varName,"_freqsKernel_",paramName,'.txt')
        save_freqs3D(fileNameFreqKernel,Variable_paramTime_freqsKernel,paramName,paramValues)

        fileNameBins="%s%s%s%s%s" % (modelFileName.strip('.L'),varName,"_bins_",paramName,'.txt')
        np.savetxt(fileNameBins,Variable_bins)


        Variable_coefficient=compute_sensitivity_coefficient(Variable_sensitivity,timePoints,np.asarray(paramValues))


        return Variable_coefficient



############################################
#            M A I N                       #
############################################


plt.figure(1)
#plt.figure(2)

#ranking kernel ON
#####################
plt.hold(True)
for param in ParanNamesValues.keys():
    paramName = param
    paramValues = ParanNamesValues[param]

    paramCoefficient=get_sensitivity_coefficient(paramName,paramValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,useKernel=True,plotMean=True)
    #print 'paramCoefficient',paramCoefficient
    plt.figure(1)
    plt.plot(timePoints[2:-1], paramCoefficient[2:-1],label=ParanNamesMarkers[param][2],marker=ParanNamesMarkers[param][0],color=ParanNamesMarkers[param][1])

    print 'paramCoefficient',paramCoefficient

    file_name="%s%s%s" % ("sens_coefficient_",param,".txt")
    np.savetxt(file_name,paramCoefficient)
    
title="%s%s" % ("Sensitivity ranking ",varName)
plt.title(title)

plt.xticks(timePoints[1:-1],np.linspace(0.1, 4, num=39))

plt.xticks([1,10,20,30,40],['0.1','1','2','3','4'])

rankplothist=plt.legend(loc='best')
plt.xlabel('time (hrs)')
#save plot
figName="%s%s%s%s" % ("Ranking_kernel_",varName,output_file_suffix,".png")
plt.savefig(figName)
plt.show()


plt.close()

##ranking kernel OFF
###################
##plt.hold(True)
##for param in ParanNamesValues.keys():
##    paramName = param
##    paramValues = ParanNamesValues[param]
##
##    paramCoefficient=get_sensitivity_coefficient(paramName,paramValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,useKernel=False,plotMean=False)
##    #print 'paramCoefficient',paramCoefficient
##    plt.figure(2)
##    plt.plot(timePoints[1:-1], paramCoefficient[1:-1],label=param,marker=ParanNamesMarkers[param][0],color=ParanNamesMarkers[param][1])
##
##title="%s%s" % ("Sensitivity ranking (histogram) ",varName)
##plt.title(title)
##
##
##plt.legend(loc=1)
##plt.xlabel('time')
##save plot
##figName="%s%s%s%s" % ("Ranking_histogram_",varName,output_file_suffix,".png")
##plt.savefig(figName)
##plt.close()
##plt.show()
