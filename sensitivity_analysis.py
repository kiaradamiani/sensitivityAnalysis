# -*- coding: cp1252 -*-

import numpy as np
import matplotlib
import pylab
from scipy.stats import gaussian_kde
import time
import matplotlib.pyplot as plt
import sys
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D

#plotta l'istogramma di una lista di numeri (possono anche essre in formato stringa) c


class DataSummary:
    def __init__(self, data):
        def get_density(x):
            if len(x) == 0 or min(x) == max(x):
                return None
            return gaussian_kde(x)
        
        self.min = MinExt(data)
        self.max = MaxExt(data)
        self.nTimes = len(data)

        self.n_values_per_time = np.zeros(self.nTimes)
        self.density = [None]*self.nTimes
        self.max_per_time = np.zeros(self.nTimes)
        for i in range(self.nTimes):
            self.n_values_per_time[i] = len(data[i])
            self.max_per_time[i] = max(data[i]) if len(data[i]) > 0 else None
            self.density[i] = get_density(data[i])
            
        self.total = sum(self.n_values_per_time)


def plotHistogram(list2hist,title):

    #trasformo lista di stringhe relativa a quel tempo in lista di interi
    list2hist=list(float(a) for a in  list2hist)

    m=int( min(list2hist)) #bin inferiore
    M=int( max(list2hist)) #bin superiore

    bins=range(m,M+2,1)

    freq,bins=np.histogram(list2hist,bins,density=False)

    pylab.bar(bins[:-1],freq)

    pylab.title(title)
    pylab.gca().get_xaxis().tick_bottom()
    pylab.gca().get_yaxis().tick_left()

    pylab.xticks(bins, bins)
    pylab.show()

#salva l'istogramma di una lista di numeri (possono anche essre in formato stringa) con il titolo scelto e il nome del file fornito
#il numero di bin è dato dalla granularitòà minima
def saveHistogram(list2hist, file_name, title):
    pylab.figure()

    #trasformo lista di stringhe relativa a quel tempo in lista di interi
    list2hist=list(float(a) for a in  list2hist)

    m=int( min(list2hist)) #bin inferiore
    M=int( max(list2hist)) #bin superiore

    bins=range(m,M+2,1)

    freq,bins=np.histogram(list2hist,bins,density=True)
    pylab.bar(bins[:-1],freq)

    pylab.title(title)
    pylab.gca().get_xaxis().tick_bottom()
    pylab.gca().get_yaxis().tick_left()

    pylab.xticks(bins, bins)
    pylab.savefig(file_name)

    pylab.close(fig)

#salva l'istogramma di una lista di numeri (possono anche essre in formato stringa) e la relativa interpolazione kernel con il titolo scelto e il nome del file fornito
#il numero di bin è dato dalla granularitòà minima
#adatta il caso della distribuzione uniforme (evitando di usare la kernel)
def saveHistogramKernel(list2hist, file_name,title):
    plt.figure()

    #trasformo lista di stringhe relativa a quel tempo in lista di interi
    list2hist=list(float(a) for a in  list2hist)

    m=int( min(list2hist)) #bin inferiore
    M=int( max(list2hist)) #bin superiore

    bins=range(m,M+2,1)

    freq,bins=np.histogram(list2hist,bins,normed=True)
    plt.bar(bins[:-1],freq)

    #kernel density estimation
    ##-------------------------
    data=list(float(a) for a in  list2hist)
    binsKernel=range(m,M+1,1)

    #controllo che non ci sia solo un valore
    if (m==M):
        print 'WARNING:',title, ' density whose mass is peaked at one value is not a Gaussian'
        freqKernel=[1]
    else:
        density = gaussian_kde(data)
        freqKernel=density(binsKernel)

    plt.plot(binsKernel,freqKernel,'-r+')
    plt.title(title)
    
    plt.savefig(file_name)

    plt.clf()
    plt.close()
#ritorna le frequenze assolute (istogramma) e le freuqneze stimate con il kernel di una lista, devo dare i bins 
def getKernelFreqs(summary,idx,binsKernel):
    #kernel density estimation
    ##-------------------------
    #controllo che non ci sia solo un valore
    if (summary.density[idx] is None):
        print 'WARNING: density whose mass is peaked at one value is not a Gaussian'
        freqKernel=np.zeros(len(binsKernel))
        if summary.max_per_time[idx] is not None:
            pos=summary.max_per_time[idx]-min(binsKernel)
            freqKernel[pos] = 1.0
    else:
        try:
            freqKernel=summary.density[idx](binsKernel)
        except:
            assert False
            
    #print 'n_values_per_time',summary.n_values_per_time[idx]
    #print 'freqKernel',freqKernel        
            
    return freqKernel

def getKernelFreqs_orig(list2hist,binsKernel,m,M):
    #fig=pylab.figure()

    bins=range(int(m),int(M)+2,1)

    freq,bins=np.histogram(list2hist,bins,normed=True)
    freqAbs,bins=np.histogram(list2hist,bins,normed=False)


    #kernel density estimation
    ##-------------------------
    data=list(float(a) for a in  list2hist)

    #controllo che non ci sia solo un valore
    if (max(list2hist)==min(list2hist)):
        print 'WARNING: density whose mass is peaked at one value is not a Gaussian'
        freqKernel=freq
    else:
        try:
            density = gaussian_kde(data)
            freqKernel=density(binsKernel)
        except:
            assert False
            
    return freqKernel,freqAbs


#prende in input in dizionario in cui ad ogni chiave corrisponde un valore di parametro ed una lista di liste in cui la prima dimensione è il tempo, la seconda i valori che assume quella data variabile negli N lanci (param,time)
#ritorna una matrice tridimensionale con le frequenze assolute, una con le frequenze relative (time, bins, param) e i bins che sono stati usati per calcolarle
def get_3D_freqs(ParamTimeVariableDictionary):
    #trovo il valore massimo osservato in tutto il dizionario (nel tempo e nei diversi parametri)
    #funzione che mi da massimo e minimo del dizionario (se le liste sono tutte vuote da zero, devo fare controllo prima)

    M=max([x.max for x in ParamTimeVariableDictionary.values()])
    m=min([x.min for x in ParamTimeVariableDictionary.values()])

    binsKernel=range(int(m),int(M+1),1)

    nParams=len(ParamTimeVariableDictionary)

    nTimes=ParamTimeVariableDictionary.values()[0].nTimes #prendo il primo elemento del dizionario per capire quanti passi tmporali ci sono

    nBins=len(binsKernel)

    #inizializzo array tridimensionale
    paramTime_freqs=np.zeros((nTimes,nBins,nParams))
    paramTime_freqsAbs=np.zeros((nTimes,nBins,nParams))

    #per ogni parametro e per ogni tempo ottengo frequenze
    p=0
    for param in ParamTimeVariableDictionary.keys():
        summary = ParamTimeVariableDictionary[param]
        for t in range(nTimes):
            if summary.n_values_per_time[t]>0:
                    paramTime_freqs[t,:,p]=getKernelFreqs(summary,t,binsKernel)
        p=p+1

    return paramTime_freqs,binsKernel




def MaxExt(item):
    """
     Restituisce il massimo di una lista.
     La lista puo' contenere numeri o liste a sua volta, anche in modo non omogeneo, ossia [0,[1,2]] e' ammesso.
     Gli elementi alla radice devono essere semplicemente ordinabili, in teoria non devono per forza essere dei numeri.
     """
    if isinstance(item, list): # item e' una lista (di qualcosa: liste, numeri, numeri e liste, etc...)
        max = 0
        for child in item: # ciclo sugli elementi della lista
            childMax = MaxExt(child) # calcolo ricorsivamente il massimo riconducendomi al caso base
            if childMax > max: # comparo gli elementi rispetto al massimo che ho calcolato fino ad ora
                max = childMax # aggiorno se serve
        return max # restituisco il massimo
    else:
        return item # caso base: il massimo di un elemento e' l'elemento stesso

def MinExt(item):
    """
     Restituisce il minimo di una lista.
     La lista puo' contenere numeri o liste a sua volta, anche in modo non omogeneo, ossia [0,[1,2]] e' ammesso.
     Gli elementi alla radice devono essere semplicemente ordinabili, in teoria non devono per forza essere dei numeri.
    """
    if isinstance(item, list):
        min = 1000000000000000000000000000000000000000
        for child in item:
            childMax = MinExt(child)
            if childMax < min:
                min = childMax
        return min
    else:
        return item

def compute_sensitivity(paramTime_freqs,paramVector):
    """
    Prende in input la matrice tridimensionale delle frequenze (time, bins, param) e ritorna la curva di sensitività di ogni parametro nel tempo (time,param)
      """
    #print 'paramVector',paramVector
    #scalo i valoi del parametro di 1 in modo di non avere parametri che valgono a 0 e avere sensitivita 0 quando normalizzi
    paramVector=np.array(paramVector)+1


     
    nParams=paramTime_freqs.shape[2]
    nTimes=paramTime_freqs.shape[0] #la prima dimensione mi dice quanti step temporali ci sono
    nBins=paramTime_freqs.shape[1]

    derivata_frequenze=np.zeros((nTimes,nBins,nParams))
    derivata_frequenze2D=np.zeros((nBins,nParams))
    sensitivity=np.zeros((nTimes,nParams))


    #%%%%%%%%%%%%%%
    #FOR TIME STEPS
    #%%%%%%%%%%%%%%
    for t in range(1,nTimes):


        #estraggo frquenze per quel tempo

        matrix2derive=np.empty((nBins,nParams) )
        matrix2derive[:,:]=paramTime_freqs[t,:,:]

        #print 'matrix2derive',matrix2derive
        derivata_t=compute_derivative(matrix2derive,paramVector)

        derivata_frequenze[t,:,:]=derivata_t

        #print 'derivata_t',derivata_t
        
        #calcolo sensitivity di questo t
        derivata_frequenze2D[:,:]=derivata_frequenze[t,:,:];
        membro_formula=np.absolute(derivata_frequenze2D)*matrix2derive; #moltiplico ogni derivata per il valore della densit? in quel punto

        integrale_derivata=np.sum(membro_formula,0);

        sensitivity[t,:]=integrale_derivata*paramVector #normalizzo sensitivity moltiplicando per il valore baseline del parametro

    #print 'sensitivity',sensitivity
    return sensitivity
 
#prende ogni riga di una matrice 2d e calcola la derivata di quella curva in ogni punto (valore), restituisce una matrice 2d con i valori delle derivate
def compute_derivative(matrix2derive,paramVector):

    y = matrix2derive

    x=np.array(paramVector)

    #print 'x derivata',x

    #inizializzo matrice sensitività
    derivata=np.empty([len(y),len(x)])

    for freq in range(0,len(y)):

        curva=y[freq,:]
        derivata[freq,:]=np.asarray(matplotlib.mlab.slopes(x, curva).copy())

    #print 'curva',curva
    #print 'derivata',derivata
    
    return derivata


def save_freqs3D(filename,freqs3D,paramName,paramValues):
    """
    salva la matrice 3d (time, bins, param) su file
    """
    data = freqs3D

    # Write the array to disk
    with file(filename, 'w') as outfile:
        # I'm writing a header here just for the sake of readability
        # Any line starting with "#" will be ignored by numpy.loadtxt
        outfile.write('# Array shape (nTimes,nBins,nParamValues): {0}\n'.format(data.shape))

        # Iterating through a ndimensional array produces slices along
        # the last axis. This is equivalent to data[i,:,:] in this case
        param=0
        for data_slice in data:

            # The formatting string indicates that I'm writing out
            # the values in left-justified columns 7 characters in width
            # with 2 decimal places.
            np.savetxt(outfile, data_slice, fmt='%-7.2f')

            # Writing out a break to indicate different slices...
            outfile.write('#New Time Step \n')
            param=param+1

   
def compute_sensitivity_coefficient(sensitivityCurve_inTime,timePoints,paramValues):

    sensitivityCoefficient=[]

    #scalo valori parametri di 1 (per evirtar di avere logaritmo di 0) e faccio logaritmo
    x=paramValues+1
    x=[math.log(p) for p in x]

    #per ogni t
    #-----------------
    for t in timePoints:
        y=sensitivityCurve_inTime[t,:]
        integral_sum=0
        for a in range(0,len(y)-1):
            for b in range (1,len(y)):
                integral_ab=(x[b]-x[a])*(y[a]+y[b])/2
                integral_sum=integral_sum+integral_ab
        sensitivityCoefficient.append(integral_sum)
    #print 'sensitivityCoefficient',sensitivityCoefficient
    return sensitivityCoefficient
