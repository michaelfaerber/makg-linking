import pandas as pd
import psycopg2
import psycopg2.extras

conn = psycopg2.connect("dbname=MAG user=mag password=1maG$ host=localhost")
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
cur.execute("select fieldofstudyid, displayname from fieldsofstudy where level=0")
mapping = {}
for row in cur:
    mapping[row['fieldofstudyid']] = row['displayname']

print(mapping)
df = pd.read_csv('wikidata_discipline_ids.txt', sep='\t')
df['discipline'] = df['discipline'].map(mapping)
df.to_csv('wikidata_discipline.txt', sep='\t', index=False)
discipline_stats_wiki = pd.DataFrame(df['discipline'].value_counts())
discipline_stats_wiki.columns = ['frequency']
print(discipline_stats_wiki)
discipline_stats_wiki.index.name = 'discipline'
discipline_stats_wiki['percentage'] = discipline_stats_wiki['frequency']*100/discipline_stats_wiki['frequency'].sum()
discipline_stats_wiki.to_csv('wikidata_discipline_stats.txt')

df2 = pd.read_csv('opencit_discipline_ids.txt', sep='\t')
df2['discipline'] = df2['discipline'].map(mapping)
df2.to_csv('opencit_discipline.txt', sep='\t', index=False)
discipline_stats_open = pd.DataFrame(df2['discipline'].value_counts())
discipline_stats_open.columns = ['frequency']
discipline_stats_open.index.name = 'discipline'
discipline_stats_open['percentage'] = discipline_stats_open['frequency']*100/discipline_stats_open['frequency'].sum()
discipline_stats_open.to_csv('opencit_discipline_stats.txt')
