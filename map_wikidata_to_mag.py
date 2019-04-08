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

with open('/home/ashwath/Files/wikidata-20190121-dois.csv','r') as csvfile,\
    open('wikidata_not_in_mag.txt', 'a') as notfoundfile,\
    open('wikidata_mag_mapping.tsv', 'w') as outfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    fieldnames = ['DOI', 'wikidata_id', 'MAGPaperID']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    # skip the header while reading the file
    next(csv_reader, None)
    # Write header to output file
    writer.writeheader()
    for row in csv_reader:
        try:
            wikidata_id, doi = row
        except ValueError:
            continue
        cur.execute("SELECT paperid FROM papers WHERE doi='{}'".format(doi.strip()))
        mag_paperid = cur.fetchone()
        if mag_paperid is None:
            notfoundfile.write('{}\n'.format(doi))
            continue
        else:
            mag_paperid = mag_paperid['paperid']
        writer.writerow({'DOI': doi, 'wikidata_id': wikidata_id, 'MAGPaperID': mag_paperid})
