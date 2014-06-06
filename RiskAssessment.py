import csv
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import datetime
import time
from xml.etree.ElementTree import Element, SubElement
from datetime import date
from suds.client import Client

#-----------------------------------------------------------------------------------------
# pancreaticCancer() and endometrialCancer() are sample functions we created. These type
# of functions can be used in the future when the csv questionnaire properly translates
# to features that can be fully interpreted by Bayes Mendel Risk Assessment. By calling one
# of these functions in the main function, it will append an xml subtree the tree
# in the main method. It uses the element tree module; the documentation can be found here:
# https://docs.python.org/2/library/xml.etree.elementtree.html
#-----------------------------------------------------------------------------------------

def pancreaticCancer(root):
	clinicObs = SubElement(root, "clinicalObservation", {'classCode':"OBS", 'moodCode': "EVN"})
	SubElement(clinicObs, "code", {'code':"C3850", 'codeSystemName':"NCI", 'displayName':"Pancreatic Cancer"})
	subject = SubElement(clinicObs, "subject", {'typeCode':"SUBJ"})
	est_age = SubElement(subject, "dataEstimatedAge", {'classCode':"OBS", 'moodCode':"EVN"})
	code = SubElement(est_age, "code", {'code':"397659008", 'displayName':"Age", 'codeSystemName':"SNOMED CT"})
	value = SubElement(est_age, "value")
	SubElement(value, "low", {'value':"55"})
	SubElement(value, "high", {'value':"55"})
	
def endometrialCancer(root):
	clinicObs = SubElement(root, "clinicalObservation", {'classCode':"OBS", 'moodCode': "EVN"})
	SubElement(clinicObs, "code", {'code':"371973000", 'codeSystemName':"SNOMED CT", 'displayName':"Uterine Cancer"})
	subject = SubElement(clinicObs, "subject", {'typeCode':"SUBJ"})
	est_age = SubElement(subject, "dataEstimatedAge", {'classCode':"OBS", 'moodCode':"EVN"})
	code = SubElement(est_age, "code", {'code':"397659008", 'displayName':"Age", 'codeSystemName':"SNOMED CT"})
	value = SubElement(est_age, "value")
	SubElement(value, "low", {'value':"62"})
	SubElement(value, "high", {'value':"62"})
	
# function returns age when birthdate is passed in. my not work for corner cases
# such as age 104 and age 4 (2014 or 1914)
# a proper function would involve having the full year -> 2/22/2014 instead of 2/22/14
# provided in the csv.

def get_age(birthdate):
	today = date.today()
	
	bday_split = birthdate.split("/")
	
	month = bday_split[0]
	day = bday_split[1]
	year = bday_split[2]
	
	year_today = today.year - 2000 + 100
	
	if year < year_today:
		year += 100 #if they are over 100, we are forcing them to be under five
		
	age = year_today - int(year)	
	
	if today.month < int(month):
		age -= 1
	elif today.month == int(month) and today.day < int(day):
		age -= 1
		
	return age
	
#main function
	
if __name__ == '__main__':

	f = csv.reader(open(sys.argv[1], "rU"), dialect=csv.excel_tab)
	next(f, None) #skip the header row
	
	#every row in f is a list of each category
	for row in f: 
		#we are examining every category in one person's list by looking at the entire row
		
		#----------------------------------------------------------------
		#we create a base xml structure in which subtrees can be appended
		#utilises element tree module
		#----------------------------------------------------------------
		
		root = Element("FamilyHistory", {'classCode':"OBS", 'moodCode':"EVN"})
		#SubElement(root, "id", {'root':"test", 'extension':"test2", 'assigningAthorityName':"HR4E"})
		#SubElement(root, "code", {'code':"test", 'codeSystemName':"test2", 'displayName':"test3"})
		SubElement(root, "code", {'code':"10157-6", 'codeSystemName':"LOINC"})
		#child = SubElement(root, "text")
		#child.text = "This file was created by the Umass HL7-Mgh Translator"
		#SubElement(root, "effectiveTime", {'value':"test"})
		subject = SubElement(root, "subject", {'typeCode':"SBJ"})
		patient = SubElement(subject, "patient", {'classCode':"PAT"})
		patientPerson = SubElement(patient, "patientPerson", {'classCode':"PSN", 'determinerCode':"INSTANCE"})
		SubElement(patientPerson, "id", {'extension':"1"})
		
        
		for information in row:
			#examine each column
			#each index in category is a different column.
			category = information.split(',')
			
			#print category
			#print category[7]
			
			age = get_age(category[7])
			#print age
			
			#append age information to main tree
			subject_1 = SubElement(patient, "subjectOf1", {'typeCode':"SBJ"})
			living_age = SubElement(subject_1, "livingEstimatedAge", {'classCode':"OBS", 'moodCode':"EVN"})
			code = SubElement(living_age, "code", {'code':"21611-9", 'displayName':"ESTIMATED AGE", 'codeSystemName':"LOINC"})
			value = SubElement(living_age, "value", {'value':str(age)})
			
			#--------------------Diseases--------------------
			#once a proper csv questionnaire file is created,
			#every column can have information that builds up
			#the main xml tree. every index corresponds to 
			#each row. By checking the information, we can know
			#the proper subtree to append and grow our main tree.
			#The main tree will be sent to the risk assessment.
			#Some sample code for pancreatic cancer and endometrial
			#cancer is provided.
			#------------------------------------------------
							
			#if category[18] == "Yes":
				#The person has had ovarian cancer
			#else:
				#The person has not had ovarian cancer
				
			#if category[19] == "Yes":
				#The person's relative has had ovarian cancer
			#else:
				#the person's relative has not had ovarian cancer
				
			#3 : pHxBreastCA : Have you ever had  breast cancer or ductal carcinoma in situ (DCIS)?.
			#if category[20] == "Yes":
				#fill
			#else:
				#fill
				
			#4 : fHxBrCASuscGene : Have any close blood relatives been confirmed to have BRCA gene mutations?
			#5 : fHxBreastCA : Have any close blood relatives had breast cancer?
			#6 : ashkenaziJewishCloseRels : Is any close blood relative  Ashkenazi Jewish?.  Ashkenazi Jewish people have a higher chance of BRCA gene mutations. 
			#7 : fHxSufficient : Have any of your female close blood relatives lived beyond age 45 years?
			#8 : pHxBrCALE50Yrs : What was your age when your breast cancer was first diagnosed?
			#9 : Yes : Age 50 or under
			
			
			#10 : No : Age 51 or older
			#11 : pHxBrCA3Neg : Was your cancer triple negative, without receptors for estrogen, progesterone and HER2?
			#12 : pHxBrCAGT1PrimarySame : Was your cancer found in more than one location in the same breast?
			#13 : pHxBrCAGT1PrimaryBoth : Have you had cancer in both breasts?
			#14 : pHxBrCAGE1RelBrCALE50Years : Do you have any close blood relatives with breast cancer who were diagnosed at age 50 years or younger?
			#15 : pHxBrCAGE2RelBrPancCA : Did two or more close blood relatives from the same side of your family have breast or pancreatic cancer?
			#16 : ashkenaziJewishOneRel : Do you have at least one close blood relative who is   Ashkenazi Jewish?    Ashkenazi Jewish people have a higher chance of BRCA gene mutations.
			#17 : pHxBrCAOther : Please indicate any of the following conditions you have had:
			#18 : pHxBrCAThyroidCA : Thyroid cancer
			#19 : pHxBrCASarcoma : Sarcoma
			#20 : pHxBrCAAdrenalCA : Adrenal cancer
			#21 : pHxBrCAEndometrialCA : Cancer of the uterus
			
			
			#22 : pHxBrCAPancreaticCA : Pancreatic cancer
			#23 : pHxBrCABrainTumors : Brain tumors
			#24 : pHxBrCAGastricCA : Stomach cancer
			#25 : pHxBrCALeukLymphoma : Leukemia or lymphoma
			#26 : fHxBrCAMale : Has any male blood relative had breast cancer?
			#27 : fHxBrCASameSideGE2 : Have two or more close blood relatives from the same side of your family had breast cancer?
			#28 : fHxBrCAOther : For any of your close blood relatives who had breast cancer, please indicate if that same relative also had:
			#29 : fHxBrCADermMan : Breast cancer involving the skin overlying the breast
			#30 : fHxBrCAThyroidCA : Thyroid cancer
			#31 : fHxBrCASarcoma : Sarcoma
			#32 : fHxBrCAAdrenalCA : Adrenal cancer
			#33 : fHxBrCAEndometrialCA : Cancer of the uterus
			#if category[50] == "Cancer of the uterus":
				#endometrialCancer(tree_node)
			#else:
				#print "no endometrial Cancer"
			
			#34 : fHxBrCAPancreaticCA : Pancreatic cancer
			
			
			#35 : fHxBrCABrainTumors : Brain tumors
			#36 : fHxBrCAGastricCA : Stomach cancer
			#37 : fHxBrCALeukLymphoma : Leukemia or lymphoma
				
				
			#------------------------------------------------------	
				
				
			#for elem in category:
				#print elem
				
				
		#we take the element tree and transform it into a string
		rough_string = ET.tostring(root, 'utf-8')
		reparsed = MD.parseString(rough_string)
		
		#we turn the string into "pretty" format
		pretty = reparsed.toprettyxml(indent="\t", encoding="utf-8")
		#print pretty
		
		outfile = open("sample_output.txt", 'w')
		
		#--------------------------------------------------------
		#use suds library to post to the risk assessment service.
		#--------------------------------------------------------
		url = 'http://bayesmendel.dfci.harvard.edu:8080/RiskService/services/Converter?wsdl'
		client = Client(url)
		result = client.service.getRiskHL7(pretty, 'fd319f62-eafe-4728-90f3-b9423e1178e3', False, False)
		print>>outfile, result
		print>>outfile, "\n"
		
		#the string result is the output xml code


		