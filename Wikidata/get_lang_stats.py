import pandas as pd
import pandas as pd
import sys
import Main

if __name__ == "__main__":

    homedir = ''
    makgdir = ''

    if len(sys.argv) > 2:
        homedir = sys.argv[1]
        makgdir = homedir + sys.argv[2] + '/'
        memorydir = homedir + 'makg-linking/Memory/MAKG/' + sys.argv[2] + '/'
        resultsdir = homedir + 'makg-linking/Wikidata/results/' + sys.argv[2] + '/'
    else:
        raise Exception('Missing run parameters')

    ocdir = homedir + 'wikidata/'

    df = pd.read_csv(resultsdir + 'wikidata_lang.csv', sep=',')
    language_stats_open = pd.DataFrame(df['languagecode'].value_counts())
    language_stats_open.columns = ['frequency']
    language_stats_open.index.name = 'languagecode'

    language_stats_open['percentage'] = language_stats_open['frequency'] * 100 / language_stats_open['frequency'].sum()
    language_stats_open.to_csv(resultsdir + 'wikidata_lang_stats.txt', sep='\t')



