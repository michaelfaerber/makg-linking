import csv
import sys
import Main
import os

# cd /slow/users/mfa/makg/mag-2019-12-26/makg-linking/Opencit
# python3 opencit_to_makg.py /slow/users/mfa/makg/ mag-2019-12-26
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

    makg_lang_data = {}
    starts = []

    for filename in os.listdir(memorydir + 'PaperLanguages/'):
        if filename.endswith(".json"):
            start = int(os.path.splitext(filename)[0].replace('makg_lang_data_', '').replace('x', ''))
            if start not in starts:
                starts.append(start)
                makg_lang_data[start] = Main.read_json_to_dic_list(memorydir + 'PaperLanguages/' + filename)

    with open(resultsdir + 'opencit_mag_mapping.csv', 'r', encoding='utf8') as csvfile, open(resultsdir + 'opencit_lang.csv', 'w', newline='\n') as discfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        fieldnames = ['MAGPaperID', 'languagecode']
        writer = csv.DictWriter(discfile, fieldnames=fieldnames, delimiter=',')
        next(csv_reader, None)
        writer.writeheader()
        for row in csv_reader:
            try:
                doi, paperid = row
            except ValueError:
                continue
            makg_id = 0
            if len(paperid) == 1:
                makg_id = int(paperid)
            else:
                makg_id = int(paperid[:2])

            if makg_id in starts:
                makg_indices = Main.find_index(makg_lang_data[makg_id], Main.dict_list_index_get_member(makg_lang_data[makg_id], 'mid'), paperid, column='mid')

                if makg_indices[0]:
                    for i in makg_indices[1]:
                        writer.writerow({'MAGPaperID': paperid, 'languagecode': makg_lang_data[makg_id][i]['lang']})
