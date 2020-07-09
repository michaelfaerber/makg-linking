import sys
import Main
import os


# cd /slow/users/mfa/makg/mag-2019-12-26/makg-linking/Wikidata
# python3 wikidata_to_makg.py /slow/users/mfa/makg/ mag-2019-12-26
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

    wddir = homedir + 'wikidata/'

    makg_doi_data = {}
    lengths = []

    for filename in os.listdir(memorydir + 'DOI/'):
        if filename.endswith(".json"):
            lth = int(os.path.splitext(filename)[0].replace('makg_doi_', ''))
            if lth not in lengths:
                lengths.append(lth)
            makg_doi_data[lth] = Main.read_json_to_dic_list(memorydir + 'DOI/' + filename)

    rows_wd = 0
    linkings_makg_wd = 0
    mappings_makg_wd = 0

    rows_in_wd, linkings_wd_makg, mappings_wd_makg = Main.get_linkings_wd_makg(
        wddir + 'id_doi.csv', resultsdir + 'wikidata_mag_mapping.csv', resultsdir + 'wikidata_not_in_mag.txt', 'w',
        makg_doi_data, lengths)

    Main.write_list_to_file(resultsdir + 'rows_wd.txt', [rows_in_wd])
    Main.write_list_to_file(resultsdir + 'linkings_makg_wd.txt', [linkings_wd_makg])
    Main.write_list_to_file(resultsdir + 'mappings_makg_wd.txt', [mappings_wd_makg])


