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
     open('opencit_lang.tsv', 'w') as langfile:
    csv_reader = csv.reader(csvfile, delimiter='\t')
    fieldnames = ['MAGPaperID', 'languagecode']
    writer = csv.DictWriter(langfile, fieldnames=fieldnames, delimiter='\t')
    # skip the header while reading the file
    next(csv_reader, None)
    # Write header to output file
    writer.writeheader()
    for row in csv_reader:
        try:
            doi, paperid = row
        except ValueError:
            continue
        cur.execute("SELECT languagecode FROM paperlanguages WHERE paperid='{}'".format(paperid.strip()))
        mag_lang = cur.fetchone()
        if mag_lang is None:
            continue
        else:
            mag_lang = mag_lang['languagecode']
        writer.writerow({'MAGPaperID': paperid, 'languagecode': mag_lang})
