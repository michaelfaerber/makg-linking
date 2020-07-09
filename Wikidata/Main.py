#! /usr/bin/python
# -*- coding: utf-8 -*-
import bisect
import csv
import html
import json
import sys
import operator
from datetime import datetime



class dict_list_index_get_member(object):
    def __init__(self, dict_list, member):
        self.dict_list = dict_list
        self.member = member
    def __getitem__(self, index):
        return self.dict_list[index][self.member]
    def __len__(self):
        return self.dict_list.__len__()


# Returns indices of x in array a if present
def find_index(a, memberclass, x, i=0, arr=None, column='udoi'):
    'Locate the leftmost value exactly equal to x'
    if arr is None:
        arr = []    #important: setting arr=[] in parameters would preserve the list over multiple iterations
    if i == 0:
        i = bisect.bisect_left(memberclass, x)
    if i != len(a) and a[i][column] == x:
        arr.append(i)
        return find_index(a, memberclass, x, i+1, arr, column)
    if len(arr) != 0:
        return True, arr
    return False, arr


# Get the 100 most frequent paper topics from MAKG
def get_top100_fos(filepath):

    fos_top100 = []

    with open(filepath, 'r') as fosFile:
        line = fosFile.readline()

        id = ''
        name = ''
        testcount = 0
        while line:
            if "<http://xmlns.com/foaf/0.1/name>" in line:
                s = line
                id = s[s.find('<http://ma-graph.org/entity/') + len('<http://ma-graph.org/entity/'):s.rfind(
                    '> <http://xmlns.com/foaf/0.1/name>')]
                name = s[s.find('<http://xmlns.com/foaf/0.1/name> "') + len(
                    '<http://xmlns.com/foaf/0.1/name> "'):s.rfind('"^^<http://www.w3.org/2001/XMLSchema#string>')]
            if "<http://ma-graph.org/property/paperCount>" in line:
                s = line
                id_pc = s[s.find('<http://ma-graph.org/entity/') + len('<http://ma-graph.org/entity/'):s.rfind(
                    '> <http://ma-graph.org/property/paperCount>')]
                papercount = s[s.find('<http://ma-graph.org/property/paperCount> "') + len(
                    '<http://ma-graph.org/property/paperCount> "'):s.rfind('"^^<http://www.w3.org/2001/XMLSchema#integer>')]
                if id_pc == id:
                    name_utf8 = (html.unescape(name))
                    temp_dic = {'id': id, 'uname': name_utf8, 'pc': int(papercount)}
                    if name_utf8 != name:
                        temp_dic['name'] = name
                    fos_top100.append(temp_dic)
                    fos_top100.sort(key=operator.itemgetter('pc'), reverse=True)
                    if len(fos_top100) == 101:
                        del fos_top100[-1]

                    testcount += 1
                    if testcount % 1000000 == 0:
                        print('Testcount: ' + str(testcount))
            line = fosFile.readline()

    return fos_top100


# Get MAKG-IDs and corresponding FOS-IDs
def get_makg_id_fos_id(filepath, top100fos_ids):

    #makg_ids = []
    #fos_ids = []
    makg_fos_ids = {}

    with open(filepath, 'r') as fosidFile:
        line = fosidFile.readline()

        # while line:
        testcount = 0
        keycount = 0
        while line:
            if "<http://purl.org/spar/fabio/hasDiscipline>" in line:
                s = line
                makg_id = s[s.find('<http://ma-graph.org/entity/') + len('<http://ma-graph.org/entity/'):s.rfind(
                    '> <http://purl.org/spar/fabio/hasDiscipline>')]
                fos_id = s[s.find('/hasDiscipline> <http://ma-graph.org/entity/') + len(
                    '/hasDiscipline> <http://ma-graph.org/entity/'):s.rfind('> .')]
                temp_dic = {'mid': makg_id, 'fid': fos_id}
                if fos_id in top100fos_ids:

                    if len(makg_id) == 1:
                        fileid = makg_id + 'x'
                    else:
                        fileid = makg_id[:2]
                    if fileid not in makg_fos_ids.keys():
                        makg_fos_ids[fileid] = []
                        makg_fos_ids[fileid].append(temp_dic)
                        keycount += 1
                    else:
                        makg_fos_ids[fileid].append(temp_dic)
                    testcount += 1
                    if testcount % 1000000 == 0:
                        print('Testcount: ' + str(testcount))

                #if fos_id in top100fos_ids:
                #    index = bisect.bisect_left(makg_ids, makg_id)
                #    makg_ids.insert(index, makg_id)
                #    fos_ids.insert(index, fos_id)

            line = fosidFile.readline()

    testcount2 = 1
    for key in makg_fos_ids.keys():
        print('Sorting key ' + str(testcount2) + ' of ' + str(keycount))
        makg_fos_ids[key].sort(key=operator.itemgetter('mid'))
        testcount2 += 1

    return makg_fos_ids, testcount


def get_makg_id_languagecode(filepath):

    #makg_ids = []
    #lang_codes = []

    makg_lang_codes = {}

    with open(filepath, 'r') as langFile:
        line = langFile.readline()

        # while line:
        testcount = 0
        keycount = 0
        while line:
            if "<http://purl.org/dc/terms/language>" in line:
                s = line
                makg_id = s[s.find('<http://ma-graph.org/entity/') + len('<http://ma-graph.org/entity/'):s.rfind(
                    '> <http://purl.org/dc/terms/language>')]
                lang_code = s[s.find('<http://purl.org/dc/terms/language> "') + len(
                    '<http://purl.org/dc/terms/language> "'):s.rfind('"^^<http://www.w3.org/2001/XMLSchema#language>')]
                temp_dic = {'mid': makg_id, 'lang': lang_code}
                if len(makg_id) == 1:
                    fileid = makg_id + 'x'
                else:
                    fileid = makg_id[:2]

                if fileid not in makg_lang_codes.keys():
                    makg_lang_codes[fileid] = []
                    makg_lang_codes[fileid].append(temp_dic)
                    keycount += 1
                else:
                    makg_lang_codes[fileid].append(temp_dic)
                testcount += 1
                if testcount % 1000000 == 0:
                    print('Testcount: ' + str(testcount))
                #index = bisect.bisect_left(makg_ids, makg_id)
                #makg_ids.insert(index, makg_id)
                #lang_codes.insert(index, lang_code)

            line = langFile.readline()

    testcount2 = 1
    for key in makg_lang_codes.keys():
        print('Sorting key ' + str(testcount2) + ' of ' + str(keycount))
        makg_lang_codes[key].sort(key=operator.itemgetter('mid'))
        testcount2 += 1

    return makg_lang_codes, testcount


# Returns i) sorted list of MAKG-DOI's, ii) list of corresponding MAKG-ID's
def get_makg_data(filepath):

    #MAKG_dois_utf8 = []
    #MAKG_dois = []
    #MAKG_ids = []
    #MAKG_occurences = []

    MAKG_data = {}

    with open(filepath, 'r') as paperFile:
        line = paperFile.readline()
        cnt = 1
        # while line:
        testcount = 0
        keycount = 0
        while line:

            if "<http://purl.org/spar/datacite/doi>" in line:
                s = line
                id = s[s.find('<http://ma-graph.org/entity/') + len('<http://ma-graph.org/entity/'):s.rfind(
                    '> <http://purl.org/spar/datacite/doi>')]
                doi = s[s.find('<http://purl.org/spar/datacite/doi>"') + len(
                    '<http://purl.org/spar/datacite/doi>"'):s.rfind('"^^<http://www.w3.org/2001/XMLSchema#string>')]
                doi_utf8 = (html.unescape(doi)).lower().strip()
                temp_dic = {'udoi': doi_utf8, 'id': id, 'occ': [0, 0]}
                if doi_utf8 != doi:
                    temp_dic['doi'] = doi
                lth = len(doi_utf8)
                if lth not in MAKG_data.keys():
                    MAKG_data[lth] = []
                    MAKG_data[lth].append(temp_dic)
                    keycount += 1
                else:
                    MAKG_data[lth].append(temp_dic)
                testcount += 1
                if testcount % 1000000 == 0:
                    print('Testcount: ' + str(testcount))
                #index = bisect.bisect_left(MAKG_dois_utf8, doi_utf8)
                #MAKG_dois_utf8.insert(index, doi_utf8)
                #MAKG_dois.insert(index, doi)
                #MAKG_ids.insert(index, id)
                #MAKG_occurences.append({'OC': 0, 'WD': 0})
                cnt += 1
            line = paperFile.readline()
    testcount2 = 1
    for key in MAKG_data.keys():
        print('Sorting key ' + str(testcount2) + ' of ' + str(keycount))
        MAKG_data[key].sort(key=operator.itemgetter('udoi'))
        testcount2 += 1

    #return MAKG_dois_utf8, MAKG_dois, MAKG_ids,MAKG_occurences, cnt

    return MAKG_data, cnt


# Get Wikidata-MAKG linkings
def get_linkings_wd_makg(csvfile_p, outfile_p, notfoundfile_p, operation, makg_doi_data, lengths):

    rows_in_wd = 0
    mappings_wd_makg = 0
    linkings_wd_makg = 0

    with open(csvfile_p, 'r', encoding='utf8') as csvfile, open(notfoundfile_p, operation) as notfoundfile, open(outfile_p, operation, newline='\n') as outfile:

        csv_reader = csv.reader(csvfile, delimiter=' ')

        fieldnames = ['WikidataID', 'MAGPaperID', 'DOI']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=',')
        # skip the header while reading the file
        next(csv_reader, None)
        # Write header to output file
        if operation == "w":
            writer.writeheader()

        for row in csv_reader:
            if len(row) != 2:
                print('Error regarding row: ' + row)
                continue

            try:
                wd_id, doi = row
            except ValueError:
                continue

            rows_in_wd += 1

            l_doi = doi.lower()

            if len(l_doi) in lengths:

                makg_indices = find_index(makg_doi_data[len(l_doi)], dict_list_index_get_member(makg_doi_data[len(l_doi)], 'udoi'), l_doi)

                if makg_indices[0]:
                    mappings_wd_makg += 1
                    for i in makg_indices[1]:
                        if makg_doi_data[len(l_doi)][i]['occ'][1] == 0:
                            writer.writerow({'DOI': doi, 'MAGPaperID': makg_doi_data[len(l_doi)][i]['id'], 'WikidataID': wd_id})
                        makg_doi_data[len(l_doi)][i]['occ'][1] += 1
                        linkings_wd_makg += 1
                else:
                    notfoundfile.write('{}\n'.format(doi))

    return rows_in_wd, linkings_wd_makg, mappings_wd_makg


def write_list_to_file(filepath, list):
    with open(filepath, "w") as f:
        for s in list:
            f.write(str(s) + "\n")


def write_dic_list_to_file(filepath, dic_list):
    with open(filepath, 'w', encoding='utf-8') as f:
        for dic in dic_list:
            json.dump(dic, f)
            f.write("\n")


def read_file_to_list(filepath):
    dt = datetime.now()
    print(dt + '   Fetching: ' + filepath)
    lines = []
    with open(filepath) as file:
        lines = [line.strip() for line in file]
    return lines


def read_json_to_dic_list(filepath):
    dt = datetime.now().strftime("%H:%M:%S")
    print(dt + '   Fetching: ' + filepath)
    lines = []
    with open(filepath) as file:
        lines = [json.loads(line.strip()) for line in file]
    return lines


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

    ocdir = homedir + 'opencitations/'
    wddir = homedir + 'wikidata/'

    ### DOI-MAKG-DATA ###

    print( 'Start mag/Papers.txt.nt')
    makg_data, doi_count = get_makg_data(makgdir + 'mag/Papers.txt.nt')
    write_list_to_file(memorydir + 'DOI/makg_doi_count.txt', [doi_count])
    i = 1
    for key in makg_data:
        print("Writing Key #" + str(i) + ': ' + str(key))
        print('\tLength: ' + str(len(makg_data[key])))
        write_dic_list_to_file(memorydir + 'DOI/makg_doi_' + str(key) + '.json', makg_data[key])
        i += 1
    print('Finished mag/Papers.txt.nt')


    ### FieldsOfStudy ###

    print('Start advanced/FieldsOfStudy.txt.nt')
    fos_data = get_top100_fos(makgdir + 'advanced/FieldsOfStudy.txt.nt')
    write_dic_list_to_file(memorydir + 'FieldsOfStudy/fos_data.json', fos_data)
    print('Finished advanced/FieldsOfStudy.txt.nt')

    ### PaperFieldsOfStudy ###

    print('Start advanced/PaperFieldsOfStudy.txt.nt')
    ls = []
    for dic in fos_data:
        ls.append(dic['id'])
    makg_fos_data, makg_fos_count = get_makg_id_fos_id(makgdir + 'advanced/PaperFieldsOfStudy.txt.nt', ls)
    write_list_to_file(memorydir + 'PaperFieldsOfStudy/makg_fos_count.txt', [makg_fos_count])
    i = 1
    for key in makg_fos_data:
        print("Writing Key #" + str(i) + ': ' + str(key))
        print('\tLength: ' + str(len(makg_fos_data[key])))
        write_dic_list_to_file(memorydir + 'PaperFieldsOfStudy/makg_fos_data_' + key + '.json', makg_fos_data[key])
        i += 1
    print('Finished advanced/PaperFieldsOfStudy.txt.nt')


    ### PaperLanguages ###
    print('Start mag/PaperLanguages.txt.nt')
    makg_lang_data, makg_lang_codes_count = get_makg_id_languagecode(makgdir + 'mag/PaperLanguages.txt.nt')
    write_list_to_file(memorydir + 'PaperLanguages/makg_lang_count.txt', [makg_lang_codes_count])
    i = 1
    for key in makg_lang_data:
        print("Writing Key #" + str(i) + ': ' + str(key))
        print('\tLength: ' + str(len(makg_lang_data[key])))
        write_dic_list_to_file(memorydir + 'PaperLanguages/makg_lang_data_' + key + '.json', makg_lang_data[key])
        i += 1
    print('Finished mag/PaperLanguages.txt.nt')
