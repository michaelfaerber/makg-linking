import csv
import sys
import Main

# cd /slow/users/mfa/makg/mag-2019-12-26/makg-linking/Wikidata
# python3 opencit_to_makg.py /slow/users/mfa/makg/ mag-2019-12-26
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

    makg_fos_data = Main.read_json_to_dic_list(memorydir + 'FieldsOfStudy/fos_data.json')

    with open(resultsdir + 'wikidata_discipline_ids.csv', 'r', encoding='utf8') as csvfile, open(resultsdir + 'wikidata_discipline.csv', 'w', newline='\n') as discfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        fieldnames = ['MAGPaperID', 'discipline']
        writer = csv.DictWriter(discfile, fieldnames=fieldnames, delimiter=',')
        # skip the header while reading the file
        next(csv_reader, None)
        # Write header to output file
        writer.writeheader()
        for row in csv_reader:
            try:
                paper_id, discipline_id = row
            except ValueError:
                continue

            for dic in makg_fos_data:
                if discipline_id == dic['id']:
                    writer.writerow({'MAGPaperID': paper_id, 'discipline': dic['uname']})
