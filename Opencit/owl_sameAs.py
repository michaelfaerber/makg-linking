import sys
import csv
import Main

if __name__ == "__main__":

    homedir = ''
    makgdir = ''

    if len(sys.argv) > 2:
        homedir = sys.argv[1]
        makgdir = homedir + sys.argv[2] + '/'
        memorydir = homedir + 'makg-linking/Memory/MAKG/' + sys.argv[2] + '/'
        resultsdir = homedir + 'makg-linking/Opencit/results/' + sys.argv[2] + '/'
    else:
        raise Exception('Missing run parameters')

    ocdir = homedir + 'opencitations/'

    with open(resultsdir + 'opencit_mag_mapping.csv', 'r', encoding='utf8') as csvfile:

        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader, None)

        rows = []

        for row in csv_reader:
            try:
                doi, paperid = row
            except ValueError:
                continue
            doi = '<http://dx.doi.org/' + doi + '> '
            sameas = '<http://www.w3.org/2002/07/owl#sameAs> '
            makg_id = '<http://ma-graph.org/entity/' + paperid + '> .'
            rows.append(doi+sameas+makg_id)

        Main.write_list_to_file(resultsdir + 'opencit_makg_sameas.nt', rows)

