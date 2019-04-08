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

with open('wikidata_mag_mapping.tsv', 'r') as csvfile,\
     open('wikidata_discipline.txt', 'w') as discfile:
    csv_reader = csv.reader(csvfile, delimiter='\t')
    fieldnames = ['MAGPaperID', 'discipline']
    writer = csv.DictWriter(discfile, fieldnames=fieldnames, delimiter='\t')
    # skip the header while reading the file
    next(csv_reader, None)
    # Write header to output file
    writer.writeheader()
    for row in csv_reader:
        try:
            doi, wikidata_id, paperid = row
        except ValueError:
            continue
        cur.execute("""select displayname from fieldsofstudy where fieldofstudyid in (SELECT fieldofstudyid FROM paperfieldsofstudy WHERE paperid={} and fieldofstudyid in (select fieldofstudyid from fieldsofstudy where level=0))
 """.format(paperid.strip()))
        displayname = cur.fetchone()
        if displayname is None:
            continue
        else:
            displayname = displayname['displayname']
        writer.writerow({'MAGPaperID': paperid, 'discipline': displayname})
