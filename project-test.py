#!usr/bin/python
#changing XML to CSV

import csv
import sys


if __name__ == '__main__':

    with open(sys.argv[1],'rU') as input:
        with open('riskservice_questionnaire.csv','w') as output:
            writer = csv.writer(output,lineterminator='\n')
            reader = csv.reader(input)
            
            all = []
            row = next(reader)
            row.append('Risk Assessment Output')
            all.append(row)
            for row in reader:
                row.append('0')
                all.append(row)
                
            writer.writerows(all)
            
        
    input.close()
    output.close()