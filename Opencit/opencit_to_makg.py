import csv
import Main
import sys
import os
from datetime import datetime

# cd /slow/users/mfa/makg/mag-2019-12-26/makg-linking/Opencit
# python3 opencit_to_makg.py /slow/users/mfa/makg/ mag-2019-12-26
if __name__ == "__main__":

    #oc_datasets = ['2019-10-21T22_41_20_', '2020-01-13T19:31:19_', '2020-04-25T04:48:36_']
    oc_datasets = ['2019-10-21T22:41:20_', '2020-01-13T19:31:19_', '2020-04-25T04:48:36_']

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

    makg_doi_data = {}
    lengths = []

    for filename in os.listdir(memorydir + 'DOI/'):
        if filename.endswith(".json"):
            lth = int(os.path.splitext(filename)[0].replace('makg_doi_', ''))
            if lth not in lengths:
                lengths.append(lth)
            makg_doi_data[lth] = Main.read_json_to_dic_list(memorydir + 'DOI/' + filename)

    rows_oc = 0
    linkings_makg_oc = 0
    mappings_makg_oc = 0

    for key in oc_datasets:
        print('Start ' + key)
        oc_files = []

        for filename in os.listdir(ocdir):
            if key in filename:
                oc_files.append(filename)

        oc_files.sort()

        i = 0
        for file in oc_files:
            i += 1
            dt = datetime.now().strftime("%H:%M:%S")
            print('\t' +dt + '   Mapping file ' + str(i) + ' of ' + str(len(oc_files)))
            if i == 1:
                rows_in_oc, connections_oc_makg_single, connections_oc_makg_total = Main.get_linkings_oc_makg(ocdir + file, resultsdir + 'opencit_mag_mapping.csv', resultsdir + 'opencit_not_in_mag.txt', 'w', makg_doi_data, lengths)
                rows_oc += rows_in_oc
                linkings_makg_oc += connections_oc_makg_single
                mappings_makg_oc += connections_oc_makg_total
            else:
                rows_in_oc, connections_oc_makg_single, connections_oc_makg_total = Main.get_linkings_oc_makg(ocdir + file, resultsdir + 'opencit_mag_mapping.csv', resultsdir + 'opencit_not_in_mag.txt', 'a', makg_doi_data, lengths)
                rows_oc += rows_in_oc
                linkings_makg_oc += connections_oc_makg_single
                mappings_makg_oc += connections_oc_makg_total

    Main.write_list_to_file(resultsdir + 'rows_oc.txt', [rows_oc])
    Main.write_list_to_file(resultsdir + 'linkings_makg_oc.txt', [linkings_makg_oc])
    Main.write_list_to_file(resultsdir + 'mappings_makg_oc.txt', [mappings_makg_oc])

    i=1
    for key in makg_doi_data:
        dt = datetime.now().strftime("%H:%M:%S")
        print(dt + '   Writing Key #' + str(i) + ': ' + str(key))
        print('\tLength: ' + str(len(makg_doi_data[key])))
        Main.write_dic_list_to_file(resultsdir + 'DOI/makg_doi_' + str(key) + '.json', makg_doi_data[key])
        i += 1

