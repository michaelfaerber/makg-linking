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

    makg_fos_data = Main.read_json_to_dic_list(memorydir + 'FieldsOfStudy/fos_data.json')

    mapping = {}

    for dic in makg_fos_data:
        mapping[dic['id']]= dic['uname']


    df = pd.read_csv(resultsdir + 'wikidata_discipline_ids.csv', sep=',')
    df['discipline'] = df['discipline'].astype(str).map(mapping)
    discipline_stats_open = pd.DataFrame(df['discipline'].value_counts())
    discipline_stats_open.columns = ['frequency']
    discipline_stats_open.index.name = 'discipline'
    discipline_stats_open['percentage'] = discipline_stats_open['frequency'] * 100 / discipline_stats_open[
        'frequency'].sum()
    discipline_stats_open.to_csv(resultsdir + 'wikidata_discipline_stats.txt', sep='\t')
