import pandas as pd
df = pd.read_csv('wikidata_lang.tsv', sep='\t')

language_stats_wiki = pd.DataFrame(df['languagecode'].value_counts())
language_stats_wiki.columns = ['frequency']
language_stats_wiki.index.name = 'languagecode'

language_stats_wiki['percentage'] = language_stats_wiki['frequency']*100/language_stats_wiki['frequency'].sum()

language_stats_wiki.to_csv('wikidata_lang_stats.txt')

df2 = pd.read_csv('opencit_lang.tsv', sep='\t')
language_stats_open = pd.DataFrame(df2['languagecode'].value_counts())
language_stats_open.columns = ['frequency']
language_stats_open.index.name = 'languagecode'

language_stats_open['percentage'] = language_stats_open['frequency']*100/language_stats_open['frequency'].sum()
language_stats_open.to_csv('opencit_lang_stats.txt')
