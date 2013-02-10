# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 08:19:20 2012

@author: schiavinotto
"""

#import pandas
import re
import os
import numpy as np
import numpy.numarray as na
import matplotlib
import csv
import sys
import gc
from sensitivity_analysis import *


def get_sensitivity_coefficient(paramName,paramValues,varName,modelFileName,timePoints,timeDelta,nSims,time,saveTimes,cluster,sensitivityFolderName,loadAggregate=True):
#procedura per calcolare sensitivity coefficient di una variabile rispetto ad un parametro

## dalle varie sim creo un dizionario (param,time) con i valori di una data  variabile per i valori di un dato parametro
## passo il dizionario a get_3d_freqse ottengo matrice 3d delel frequenze
## la matrice 3d a compute_sensitivity e ottengo curve di sentisitivà

    nSims=nSims+1
    
    #inizializzo dizionari
    aggregateVariable_in_time_dictionary={}
    
    for param in paramValues:
        print paramName,'=',param
        #nome cartella relativa a quel parametro
        simFolderName="%s%s%s%s%s" % (sensitivityFolderName,os.sep,modelFileName.strip('.L'),paramName,param)

        if(loadAggregate==False):

            if varName=='sphereSize':
                aggregateVariable_in_time=aggregate_runs_sphereSize(simFolderName,modelFileName,nSims,saveTimes)
            else:
                aggregateVariable_in_time=aggregate_runs_totalReadout(simFolderName,modelFileName,nSims,saveTimes,varName)
        else:
                aggregateVariable_in_time=read_aggregate_variable_in_time(simFolderName,modelFileName,nSims-1,varName,'NumDivisions')
                #print 'aggregateVariable_in_time[t]',aggregateVariable_in_time


    #assert False

        #print 'aggregateVariable_in_time',aggregateVariable_in_time

        #metto aggregate output in dizionario relativo alal variabile
        aggregateVariable_in_time_dictionary[param]=DataSummary(aggregateVariable_in_time)
        aggregateVariable_in_time=None
        gc.collect()
        
    #controllo che ci sia qualche lista non vuota nel dizionario
    len_aggregateVariable_in_time_dictionary=sum([x.total for x in aggregateVariable_in_time_dictionary.values()])

    if len_aggregateVariable_in_time_dictionary>0:
        #da dizionario 3d delle simulazioni ottengo array 3d (parametro, tempo e bins) delle frequenze kernel
        Variable_paramTime_freqs,Variable_bins=get_3D_freqs(aggregateVariable_in_time_dictionary)
        Variable_sensitivity=compute_sensitivity(Variable_paramTime_freqs,paramValues)   
        Variable_coefficient=compute_sensitivity_coefficient(Variable_sensitivity,timePoints,paramValues)


        fileName="%s%s%s%s%s" % (modelFileName.strip('.L'),varName,"_sensitivity_",paramName,'.txt')
        np.savetxt(fileName,Variable_sensitivity)

        fileNameFreqKernel="%s%s%s%s%s" % (modelFileName.strip('.L'),varName,'_freqsKernel',paramName,'.txt')
        save_freqs3D(fileNameFreqKernel,Variable_paramTime_freqs,paramName,paramValues)
        fileNameBins="%s%s%s%s%s" % (modelFileName.strip('.L'),varName,'_binsKernel',paramName,'.txt')
        np.savetxt(fileNameBins,Variable_bins)

        return Variable_coefficient


#funzione che ritorna il valore della variabile di ogni pattern (all'interno di una stringa nel file dei titoli delle colonne)
def get_variable_value(c,variableString):
    nd_match = re.search(variableString, c)
    return nd_match.group(1) if nd_match is not None else None
	
def get_columns_dictionary(results_folder,experiment,pattern,variableNamesList):
    filename = "%s%s%s.%s.ms.cols.txt" % (results_folder,'\\',experiment, pattern)
    #print filename
    dictionary={}
    with open(filename, "r") as f:
    #per ogni titolo di colonna
        nColumn=0
        for column in f.readlines():
            #estrai valore delle variabili che si vogliono estrarre per quel pattern
            flag=0
            for variableName in variableNamesList:
                regularExpression="%s%s" % (variableName,":=(\d+)")
                variableValue = get_variable_value(column,regularExpression)
                if variableValue is not None:
                    flag=1
                    #inizializzo dizionario se non è già stato inizializzato
                    try:
                        dictionary[nColumn]
                    except: 
                         dictionary[nColumn]={}
                    dictionary[nColumn][variableName]=variableValue
            if flag==1: #se ho inizializzato il dizionario incremento il numero della colonna
             nColumn=nColumn+1
    #print 'dictionary',dictionary  
    return dictionary

def read_abnormal_csv(filename):
    def get_values(l):
        return [float(s) for s in l.split(",")]
    def fill_values(l, size):
        return l+[0]*(size-len(l))
    
    with open(filename, "r") as f:
        values = [get_values(l) for l in f.readlines()]
    final_size = len(values[-1])
    full_values = np.array([fill_values(l, final_size) for l in values]).T
    return full_values[0], full_values[1:]

#funzione che ritorna array concentrazioni e dizionario con titoli colonne
def read_values(results_folder,experiment, pattern,variableNamesList,timePoints,delta):
    filename = "%s%s%s.%s.ms.csv" % (results_folder,'\\',experiment, pattern)
    times, values = read_abnormal_csv(filename)
    #print 'len(times)', len(times)
    delta_times, delta_values=get_delta_times(times,values.T,timePoints,delta)
   # print 'len(delta_times)', len(delta_times)

    cols = get_columns_dictionary(results_folder,experiment, pattern,variableNamesList)
    return  delta_times, delta_values, cols

def rename_ColFiles(results_folder,experiment, pattern,nSim):
    oldFilename ="%s%s%s.%s.ms.cols.txt" % (results_folder,'\\',experiment, pattern)
    newFilename = "%s%s%s.%s.tree.sim%d.txt" % (results_folder,'\\',experiment, pattern,nSim)
    os.rename(oldFilename,newFilename)

def get_delta_times(times,values,timePoints,delta):
            #converto matrice tempie matrici valori in liste

            times=list(times)
            values=values.tolist()

            #inizializzo nuove liste dei delta
            delta_times=[times[0]]
            delta_values=[values[0]]
            j=0;
            for y in range(1,len(timePoints)):
                threshold = y*delta+delta/2
                while ( j<=len(times)-1 and threshold>times[j] ):
                    j=j+1;
                j=j-1;
             
                delta_times.append(timePoints[y])
                delta_values.append(values[j])
                
            return np.asarray(delta_times),np.asarray(delta_values)
        
##           
#funzione che legge concentrazioni da ouptut L e crea una lista di liste in cui compare il valore di una variabile a seconda delal sua frequenza (nel tempo)
def get_variable_in_time(variable, times, values, cols):
	time_list=[]
        #per ogni step temporale
	for t in range (0, len(times)):
		value_list=[]
		#print t
		#per ogni specie (colonna) del file
		for col in range (0,len(cols)): 
			freq_var=values[t,col] #frequenza variabile (concentrazione specie)
			val_var=cols[col][variable] #valore variabile
			if freq_var>0:
				value_list=value_list+[val_var]*int(freq_var) #appendo ad una lista in cui i valori della variabile csono compaiiono con la loro frequenza 
                time_list.append(value_list) #lista di liste coni valori delle variabili ripetute per ogni passo temporale
        #print time_list
        return time_list
    

def variable2csv(results_folder,modelFileName, pattern,variable,suffix,nSim,time_list,win):
    if win==True:
        nome_file= "%s%s%s%s%s%s%s%s" % (results_folder,'\\',modelFileName, pattern,variable,suffix,nSim,'.csv')
    else:
        nome_file= "%s%s%s%s%s%s%s%s" % (results_folder,'/',modelFileName, pattern,variable,suffix,nSim,'.csv')

    with open(nome_file, 'wb') as the_file:
        csv.register_dialect("custom", delimiter=" ", skipinitialspace=True)
        writer = csv.writer(the_file, dialect="custom")
        for tup in time_list:

                writer.writerow(tup)


#funzione che legge concentrazioni da ouptut L e aggiunge alla  lista di liste in cui compare il valore di una variabile a seconda delal sua frequenza (nel tempo) relòativa alla simulazine precendeten 
def append_variable_in_time(variable, times, values, cols,variable_in_time):
        #per ogni step temporale
	for t in range (0, len(variable_in_time)):
		value_list=variable_in_time[t]
		#print t
		#per ogni specie (colonna) del file
		for col in range (0,len(cols)): 
			freq_var=values[t,col] #frequenza variabile (concentrazione specie)
			val_var=cols[col][variable] #valore variabile
			if freq_var>0:
				value_list=value_list+[val_var]*int(freq_var) #appendo ad una lista in cui i valori della variabile csono compaiono con la loro frequenza 
                variable_in_time[t]=value_list #lista di liste coni valori delle variabili ripetute per ogni passo temporale
        #print time_list
        return variable_in_time

#funzione che legge concentrazioni da ouptut L e aggiunge alla  lista di liste in cui compare il valore di una variabile a seconda delal sua frequenza (nel tempo) relòativa alla simulazine precendeten 
def aggregatge_variables_in_time(old_variable_in_time,new_variable_in_time):
        #per ogni step temporale
	for t in range (0, len(variable_in_time)):
            aggregate_variable_in_time[t]=new_variable_in_time[t]+new_variable_in_time
        return aggregate_variable_in_time   
	
def processResults_stemTA(results_folder,modelFileName,nSim,timePoints,delta,win):
    staminal_times, staminal_values, staminal_cols = read_values(results_folder,modelFileName, "P_Staminal",['num_divisions'],timePoints,delta)
    rename_ColFiles(results_folder,modelFileName,"P_Staminal",nSim)
    precursor_times,precursor_values,precursor_cols = read_values(results_folder,modelFileName, "P_Precursor",['num_divisions','precursor_divisions','max_divisions'],timePoints,delta)
    rename_ColFiles(results_folder,modelFileName,"P_Precursor",nSim)
    diff_times,diff_values,diff_cols = read_values(results_folder,modelFileName, "P_Differentiated",['num_divisions'],timePoints,delta)
    rename_ColFiles(results_folder,modelFileName,"P_Differentiated",nSim)

    variable_in_time_staminal=get_variable_in_time('num_divisions',staminal_times, staminal_values, staminal_cols)
    variable2csv(results_folder,modelFileName, 'Staminal','NumDivisions','Sim',nSim,variable_in_time_staminal,win)

    variable_in_time_precursor=get_variable_in_time('num_divisions',precursor_times, precursor_values, precursor_cols)
    variable2csv(results_folder,modelFileName, 'Progenitor','NumDivisions','Sim',nSim,variable_in_time_precursor,win)

    variable_in_time_precursor=get_variable_in_time('precursor_divisions',precursor_times, precursor_values, precursor_cols)
    variable2csv(results_folder,modelFileName, 'Progenitor','ProgenitorDivisions','Sim',nSim,variable_in_time_precursor,win)

    variable_in_time_precursor=get_variable_in_time('max_divisions',precursor_times, precursor_values, precursor_cols)
    variable2csv(results_folder,modelFileName, 'Progenitor','MaxDivisions','Sim',nSim,variable_in_time_precursor,win)

    variable_in_time_differentiated=get_variable_in_time('num_divisions',diff_times,diff_values, diff_cols)
    variable2csv(results_folder,modelFileName, 'Differentiated','NumDivisions','Sim',nSim,variable_in_time_differentiated,win)

def processResults_singleType(results_folder,modelFileName,nSim,timePoints,delta,win):
    staminal_times, staminal_values, staminal_cols = read_values(results_folder,modelFileName, "P_Staminal",['num_divisions'],timePoints,delta)
    rename_ColFiles(results_folder,modelFileName,"P_Staminal",nSim)
    precursor_times,precursor_values,precursor_cols = read_values(results_folder,modelFileName, "P_Precursor",['num_divisions','precursor_divisions','max_divisions'],timePoints,delta)
    rename_ColFiles(results_folder,modelFileName,"P_Precursor",nSim)
    diff_times,diff_values,diff_cols = read_values(results_folder,modelFileName, "P_Differentiated",['num_divisions'],timePoints,delta)
    rename_ColFiles(results_folder,modelFileName,"P_Differentiated",nSim)

    variable_in_time_staminal=get_variable_in_time('num_divisions',staminal_times, staminal_values, staminal_cols)
    variable2csv(results_folder,modelFileName, 'Staminal','NumDivisions','Sim',nSim,variable_in_time_staminal,win)

    variable_in_time_precursor=get_variable_in_time('num_divisions',precursor_times, precursor_values, precursor_cols)
    variable2csv(results_folder,modelFileName, 'Progenitor','NumDivisions','Sim',nSim,variable_in_time_precursor,win)

    variable_in_time_differentiated=get_variable_in_time('num_divisions',diff_times,diff_values, diff_cols)
    variable2csv(results_folder,modelFileName, 'Differentiated','NumDivisions','Sim',nSim,variable_in_time_differentiated,win)


def read_variable_in_time2(results_folder,modelFileName,run,pattern,variable):
    nome_file= "%s%s%s%s%s%s%s%s" % (results_folder,'/',modelFileName, pattern,variable,'Sim',run,'.csv')

    with open(nome_file, 'r') as the_file:
        f=the_file.readlines()
        return f

def read_aggregate_variable_in_time(simFolderName,modelFileName,nSims,pattern,variable):
    results_folder="%s%s" % (simFolderName,'/Results')
    nome_file= "%s%s%s%s%s%s%s%s" % (results_folder,'/',modelFileName,pattern,variable,'aggregate',nSims,'.csv')
    lst=[]
    with open(nome_file, 'r') as the_file:
        i=0
        for l in the_file.readlines():
            lst.append([])
            strs = filter(lambda x:len(x)>0, l.strip().split(' '))
            values = [float(val) for val in strs]
            lst[i] = values
            i+=1
    return lst


def read_aggregate_variable_timestep(simFolderName,modelFileName,nSims,pattern,variable,timestep):
    #print timestep
    results_folder="%s%s" % (simFolderName,'/Results')
    nome_file= "%s%s%s%s%s%s%s%s" % (results_folder,'/',modelFileName,pattern,variable,'aggregate',nSims,'.csv')
    lst=[]
    values=[]
    with open(nome_file, 'r') as the_file:
        i=0
        for l in the_file.readlines():
            if i==timestep:
                strs = filter(lambda x:len(x)>0, l.strip().split(' '))
                values = [float(val) for val in strs]
                #print 'len(values)', len(values)
            i+=1
    return values

def read_variable_in_time(lst,results_folder,modelFileName,run,pattern,variable):
    nome_file= "%s%s%s%s%s%s%s%s" % (results_folder,'/',modelFileName, pattern,variable,'Sim',run,'.csv')

    createSlots = len(lst) == 0
    with open(nome_file, 'r') as the_file:
        i=0
        for l in the_file.readlines():
            if createSlots:
                lst.append([])
            strs = filter(lambda x:len(x)>0, l.strip().split(' '))
            values = [float(val) for val in strs]
            #lst[i] = lst[i] + filter(lambda x:len(x)>0, l.strip().split(' '))
            lst[i] = lst[i] + values
            i+=1


def read_variableLenght_in_time(lst,results_folder,modelFileName,run,pattern,variable):
    nome_file= "%s%s%s%s%s%s%s%s" % (results_folder,'/',modelFileName, pattern,variable,'Sim',run,'.csv')

    createSlots = len(lst) == 0
    with open(nome_file, 'r') as the_file:
        i=0
        for l in the_file.readlines():
            if createSlots:
                lst.append([])
            strs = filter(lambda x:len(x)>0, l.strip().split(' '))
            values = [len(val)]
            #lst[i] = lst[i] + filter(lambda x:len(x)>0, l.strip().split(' '))
            lst[i] = lst[i] + values
            i+=1


#importa il valore della variabile per ogni lancio e appende in una lista di liste, in cui ogni lista corrisponde ad un passo temporale 
def aggregate_runs(simFolderName,modelFileName,nSims,saveTimes):
    
    aggregate_variable_in_time=[]

    results_folder="%s%s" % (simFolderName,'/Results')

    #per ogni sim
    for run in range(1,nSims):

        #ANALISI RISULTATI
        #FUNZIONE CUSTOM ???????????????????????????????????????????????????????
     
        variable_in_time=read_variable_in_time(results_folder,modelFileName.strip('.L'),run,'Staminal','NumDivisions')
        #???????????????????????????????????????????????????????
        
    #METTO TUTTI I LANCI AGGREGATI IN UNA LISTA UNICA
        #al primo run creo la prima lista di liste
        if run==1:
            #variabile num division staminal
            for time_variable in variable_in_time:
                aggregate_variable_in_time.append(filter(lambda x:len(x)>0, time_variable.strip().split(' ')))
 
        #per i run successivi concateno
        else:
            for t in range(0,len(variable_in_time)):
                aggregate_variable_in_time[t]=aggregate_variable_in_time[t]+filter(lambda x:len(x)>0, variable_in_time[t].strip().split(' '))

    #FUNZIONE CUSTOM ???????????????????????????????????????????????????????
    variable2csv(results_folder,modelFileName, 'Staminal','NumDivisions','aggregate',nSims-1,aggregate_variable_in_time,False)
    #???????????????????????????????????????????????????????

    #converto aggregati in FLOAT
    for t in range(0,len(aggregate_variable_in_time)):
        aggregate_variable_in_time[t]=list(float(a) for a in  aggregate_variable_in_time[t])
        
    return aggregate_variable_in_time

#importa il valore della variabile per ogni lancio e appende in una lista di liste, in cui ogni lista corrisponde ad un passo temporale 
def aggregate_runs_totalReadout(simFolderName,modelFileName,nSims,saveTimes,varName):
    
    aggregate_variable_in_time=[]


    #per ogni sim
    variable_in_time = []
    for run in range(1,nSims):

        #print 'run ',run

        #ANALISI RISULTATI
        results_folder="%s%s" % (simFolderName,'/Results')

        if (varName=='Staminal' or varName=='Total'): 
            read_variable_in_time(variable_in_time, results_folder,modelFileName.strip('.L'),run,'Staminal','NumDivisions')
        if (varName=='Progenitor' or varName=='Total'): 
            read_variable_in_time(variable_in_time, results_folder,modelFileName.strip('.L'),run,'Progenitor','NumDivisions')
        if (varName=='Differentiated' or varName=='Total'): 
            read_variable_in_time(variable_in_time, results_folder,modelFileName.strip('.L'),run,'Differentiated','NumDivisions')
       

    aggregate_variable_in_time = variable_in_time

    variable2csv(results_folder,modelFileName, 'Total','NumDivisions','aggregate',nSims-1,aggregate_variable_in_time,False)

    return aggregate_variable_in_time


#importa il valore della variabile per ogni lancio e appende in una lista di liste, in cui ogni lista corrisponde ad un passo temporale 
def aggregate_runs_sphereSize(simFolderName,modelFileName,nSims,saveTimes):
    
    aggregate_variable_in_time=[]


    #per ogni sim
    for run in range(1,nSims):

        #ANALISI RISULTATI
        #FUNZIONE CUSTOM ???????????????????????????????????????????????????????
        results_folder="%s%s" % (simFolderName,'/Results')
        variable_in_time_Staminal=read_variable_in_time2(results_folder,modelFileName.strip('.L'),run,'Staminal','NumDivisions')
        #print 'variable_in_time_Staminal',variable_in_time_Staminal

        variable_in_time_Progenitor=read_variable_in_time2(results_folder,modelFileName.strip('.L'),run,'Progenitor','NumDivisions')
        #print 'variable_in_time_Progenitor',variable_in_time_Progenitor

        variable_in_time_Differentiated=read_variable_in_time2(results_folder,modelFileName.strip('.L'),run,'Differentiated','NumDivisions')
        #print 'variable_in_time_Differentiated',variable_in_time_Differentiated

        #devo concatenare le tre variable in time dei tre pattern
        variable_in_time=[]
        for t in range(0,len(variable_in_time_Staminal)):
            variable_in_time.append(variable_in_time_Staminal[t].strip()+" "+variable_in_time_Progenitor[t].strip()+" "+variable_in_time_Differentiated[t].strip())

        #print 'variable_in_time',variable_in_time

        #???????????????????????????????????????????????????????
        
        #METTO TUTTI I LANCI AGGREGATI IN UNA LISTA UNICA
        #al primo run creo la prima lista di liste
        if run==1:
            #variabile num division staminal
            for time_variable in variable_in_time:
                aggregate_variable_in_time.append([ str(len(filter(lambda x:len(x)>0, time_variable.strip().split(' '))))])
                #print 'aggregate_variable_in_time',aggregate_variable_in_time
 
        #per i run successivi concateno
        else:
            for t in range(0,len(variable_in_time)):
                aggregate_variable_in_time[t]=aggregate_variable_in_time[t]+[ str(len(filter(lambda x:len(x)>0, variable_in_time[t].strip().split(' ') )))]

    #FUNZIONE CUSTOM ???????????????????????????????????????????????????????
    variable2csv(results_folder,modelFileName, 'SphereSize','NumDivisions','aggregate',nSims-1,aggregate_variable_in_time,False)
    #???????????????????????????????????????????????????????
    
    #converto aggregati in FLOAT
    for t in range(0,len(aggregate_variable_in_time)):
        aggregate_variable_in_time[t]=list(float(a) for a in  aggregate_variable_in_time[t])
    return aggregate_variable_in_time

