import csv
import psycopg2
import psycopg2.extras

conn = psycopg2.connect("dbname=MAG user=mag password=1maG$ host=localhost")
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Removed 3 rows which had extra delimiter:
# find /home/ashwath/Files/ -name "*-dois.csv" |xargs sed -r -i '/[0-9]+,[a-zA-Z0-9.]+,/d'
# Q46030113,10,7334/PSICOTHEMA2013.87
# Q47762238,10,7334/PSICOTHEMA2012.229
# Q50857157,10,7334/PSICOTHEMA2012.180

with open('opencit_mag_mapping_real.txt', 'r') as csvfile,\
     open('opencit_discipline_ids.txt', 'w') as discfile:
    csv_reader = csv.reader(csvfile, delimiter='\t')
    fieldnames = ['MAGPaperID', 'discipline']
    writer = csv.DictWriter(discfile, fieldnames=fieldnames, delimiter='\t')
    # skip the header while reading the file
    next(csv_reader, None)
    # Write header to output file
    writer.writeheader()
    for row in csv_reader:
        try:
            doi, paperid = row
        except ValueError:
            continue
        cur.execute("""SELECT fieldofstudyid FROM paperfieldsofstudy WHERE paperid={} and fieldofstudyid in (95457728, 127313418,162324750,205649164, 138885662, 185592680, 144024400, 33923547, 192562407, 41008148,86803240,71924100, 17744445,127413603,15744967,39432304,144133560,121332964,142362112)
 """.format(paperid.strip()))
        fieldofstudyid = cur.fetchone()
        if fieldofstudyid is None:
            continue
        else:
            fieldofstudyid = fieldofstudyid['fieldofstudyid']
        writer.writerow({'MAGPaperID': paperid, 'discipline': fieldofstudyid})
