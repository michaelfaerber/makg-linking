import Main
import sys
import csv

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

    with open(resultsdir + 'wikidata_mag_mapping.csv', 'r', encoding='utf8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader, None)
        rows = []
        for row in csv_reader:
            try:
                wd_id, paperid, doi = row
            except ValueError:
                continue
            wdid = '<https://www.wikidata.org/wiki/' + wd_id + '>'
            sameas = '<http://www.w3.org/2002/07/owl#sameAs>'
            makg_id = '<http://ma-graph.org/entity/' + paperid + '> .'
            rows.append(wdid + sameas + makg_id)

        Main.write_list_to_file(resultsdir + 'wikidata_makg_sameas.nt', rows)

