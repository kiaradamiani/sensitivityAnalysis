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

#funzione che ritorna il valore della variabile di ogni pattern (all'interno di una stringa nel file dei titoli delle colonne)
def get_variable_value(c,variableString):
    nd_match = re.search(variableString, c)
    return nd_match.group(1) if nd_match is not None else None
	
def get_columns_dictionary(results_folder,experiment,pattern,variableNamesList):
    filename = "%s%s%s.%s.ms.cols.txt" % (results_folder,'\\',experiment, pattern)
    print filename
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
    
##
##def variable2csv(nome_file,time_list):
##    print 'time_list',time_list
##    with open(nome_file, 'wb') as the_file:
##        csv.register_dialect("custom", delimiter=" ", skipinitialspace=True)
##        writer = csv.writer(the_file, dialect="custom")
##        for tup in time_list:
##                print 'tup',tup
##                writer.writerow(tup)


def variable2csv(nome_file,time_list):
    np.savetxt(nome_file,np.asarray(time_list))
                
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
	



def read_variable_in_time(nome_file,skipFirstLine=0):
    with open(nome_file, 'r') as the_file:
        f=the_file.readlines()
        return f[skipFirstLine:] #skip first line (1 if yes 0 if not)


#importa il valore della variabile per ogni lancio e appende in una lista di liste, in cui ogni lista corrisponde ad un passo temporale 
def aggregate_runs(modelFileName,paramName,paramValue,paramValuePos,varCol,varName,nSims,saveTimes):

    #nome cartella relativa a quel parametro

    #FTS_Vmax_0_test_100
    simFolderName="%s%s%s%s%s%s%s" % (paramName,'_',paramValuePos,'_',modelFileName,'_',paramValue)
    print 'simFolderName',simFolderName
 
    aggregate_variable_in_time=[]


    #per ogni sim
    for run in range(0,nSims):
        #print 'run',run
        
        #ANALISI RISULTATI
        #FUNZIONE CUSTOM ???????????????????????????????????????????????????????
        #FTS_Vmax_0_test_100_0.csv
        filename="%s%s%s%s%s%s" % (simFolderName,os.sep,simFolderName,'_',run,'.csv')
        variable_in_time=read_variable_in_time(filename)
        #???????????????????????????????????????????????????????

        
    #METTO TUTTI I LANCI AGGREGATI IN UNA LISTA UNICA
        #al primo run creo la prima lista di liste
        if run==0:
            #variabile num division staminal
            for time_variable in variable_in_time: ####SKIP FIRST LINE
                varcols=time_variable.strip().split(',')
                #print 'varcols',varcols[varCol]
                aggregate_variable_in_time.append([float(varcols[varCol])])
         
        #per i run successivi concateno
        else:
            for t in range(0,len(variable_in_time)):  ####SKIP FIRST LINE
                #print 't',t
                varcols=variable_in_time[t].strip().split(',')
                #print 'aggregate_variable_in_time[t]',aggregate_variable_in_time[t]
                aggregate_variable_in_time[t]=aggregate_variable_in_time[t]+[float(varcols[varCol])]

    #print' aggregate_variable_in_time',aggregate_variable_in_time

    #FUNZIONE CUSTOM ???????????????????????????????????????????????????????
    filename="%s%s%s%s%s%s" % (simFolderName,'\\',simFolderName,'_aggregate',nSims,'.csv')
    variable2csv(filename,aggregate_variable_in_time)
    #???????????????????????????????????????????????????????

 
    return aggregate_variable_in_time
