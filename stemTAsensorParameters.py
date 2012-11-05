# -*- coding: cp1252 -*-
import numpy as np

modelFileName="stemTAsensor.L"
sensitivityFolderName="stemTAsensorSensitivity10"



rateDifferiantedApoptosis=np.linspace(0, 1, num=11)
StaminalDivisionRate=np.linspace(0.4, 2.4, num=11)
PrecursorDivisionRate=np.linspace(0.4, 2.4, num=11)
max_divisions=np.linspace(3, 13, num=11)
StaminalAsymmetricDivisionProbability=np.linspace(0, 1, num=11) #num è quanti intervalli voglio
sizeSensor=np.linspace(5, 15, num=11)
sizeSensorStaminalDivisionRate=np.linspace(0, 0.66, num=11)


ParanNamesValues={}

ParanNamesValues['$max_divisions$']=np.asarray([int(x) for x in  max_divisions])
ParanNamesValues['$rateDifferiantedApoptosis$']=rateDifferiantedApoptosis
ParanNamesValues['$StaminalDivisionRate$']=StaminalDivisionRate
ParanNamesValues['$PrecursorDivisionRate$']=PrecursorDivisionRate
ParanNamesValues['$StaminalAsymmetricDivisionProbability$']=StaminalAsymmetricDivisionProbability
ParanNamesValues['$sizeSensor$']=sizeSensor
ParanNamesValues['$sizeSensorStaminalDivisionRate$']=sizeSensorStaminalDivisionRate
