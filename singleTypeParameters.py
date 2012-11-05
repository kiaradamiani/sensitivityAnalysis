# -*- coding: cp1252 -*-
import numpy as np

modelFileName="singleTypeProgenitor.L"
sensitivityFolderName="singleTypeSensitivity10"



rateDifferiantedApoptosis=np.linspace(0, 1, num=11)
StaminalDivisionRate=np.linspace(0.4, 2.4, num=11)
PrecursorDivisionRate=np.linspace(0.4, 2.4, num=11)
PrecursorSymmetricDivisionProbability=np.linspace(0,0.5, num=11)
StaminalAsymmetricDivisionProbability=np.linspace(0, 1, num=11) #num è quanti intervalli voglio


ParanNamesValues={}

ParanNamesValues['$rateDifferiantedApoptosis$']=rateDifferiantedApoptosis
ParanNamesValues['$StaminalDivisionRate$']=StaminalDivisionRate
ParanNamesValues['$PrecursorDivisionRate$']=PrecursorDivisionRate
ParanNamesValues['$PrecursorSymmetricDivisionProbability$']=PrecursorSymmetricDivisionProbability
ParanNamesValues['$StaminalAsymmetricDivisionProbability$']=StaminalAsymmetricDivisionProbability
