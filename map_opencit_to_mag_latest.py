import csv
import psycopg2
import psycopg2.extras

# After program,
# faerberm@shetland:/home/ashwath/Programs/OpenCit_MAG_Wikidata$ sudo cut -f1,3 opencit_mag_mapping.tsv | tail -n +2 | sort -S52G --parallel=42 -u > opencit_mag_mapping_real.txt
# faerberm@shetland:/home/ashwath/Programs/OpenCit_MAG_Wikidata$ wc -l opencit_mag_mapping_real.txt 

conn = psycopg2.connect("dbname=MAG user=mag password=1maG$ host=localhost")
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

with open('/home/ashwath/Files/OpenCitations/data.csv','r') as csvfile, open('opencit_mag_mappingold.tsv', 'w') as outfile, open('opencit_not_in_mag.txt', 'w') as notfoundfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    fieldnames = ['DOI', 'OCI', 'MAGPaperID']
    #writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    # skip the header while reading the file
    next(csv_reader, None)
    # Write header to output file
    #writer.writeheader()
    for oci, citing_doi, cited_doi ,_ ,_ ,_ ,_ in csv_reader:
        cur.execute("SELECT paperid FROM papers WHERE doi='{}'".format(citing_doi.strip()))
        mag_paperid = cur.fetchone()
        if mag_paperid is None:
            notfoundfile.write('{}\n'.format(citing_doi))
            continue
        else:
            mag_paperid = mag_paperid['paperid']
        #writer.writerow({'DOI': citing_doi, 'OCI': oci, 'MAGPaperID': mag_paperid})
