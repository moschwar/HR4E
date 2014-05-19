import csv
import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
import xml.dom.minidom as MD
#SubElement

if __name__ == '__main__':

	f = csv.reader(open(sys.argv[1], "rU"), dialect=csv.excel_tab)

	#every row in f is a list of each category
	for row in f: 
		#we are examining every category in one person's list
		print "new person:"
		
		root = Element("FamilyHistory", {'classCode':"OBS", 'moodCode':"EVN"})
		#SubElement(root, "id", {'root':"test", 'extension':"test2", 'assigningAthorityName':"test3"})
		#SubElement(root, "code", {'code':"test", 'codeSystemName':"test2", 'displayName':"test3"})
		SubElement(root, "code", {'code':"10157-6", 'codeSystemName':"LOINC"})
		#child = SubElement(root, "text")
		#child.text = "This file was created by the Umass HL7-Mgh Translator"
		#SubElement(root, "effectiveTime", {'value':"test"})
		subject = SubElement(root, "subject", {'typeCode':"SBJ"})
		patient = SubElement(subject, "patient", {'classCode':"PAT"})
		patientPerson = SubElement(patient, "patientPerson", {'classCode':"PSN", 'determinerCode':"INSTANCE"})
		SubElement(patientPerson, "id", {'extention':"1"})
		SubElement(patientPerson, "adminsitrativeGenderCode", {'code':"F"})
		
		rough_string = ET.tostring(root, 'utf-8')
		reparsed = MD.parseString(rough_string)
		print reparsed.toprettyxml(indent="\t")
		
		for information in row:
			category = information.split(',')
			for elem in category:
				print elem