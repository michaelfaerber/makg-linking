import csv
import psycopg2
import psycopg2.extras

conn = psycopg2.connect("dbname=MAG user=mag password=1maG$ host=localhost")
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
citing_doi = '10.1002/pol.1985.170230422'
cur.execute("SELECT paperid FROM papers WHERE doi='{}'".format(citing_doi.strip()))
mag_paperid = cur.fetchone()['paperid']
if mag_paperid is None:
    print('None')
else:
    print(mag_paperid)