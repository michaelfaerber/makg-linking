import sys
import csv

# cd /slow/users/mfa/makg/mag-2019-12-26/makg-linking/Opencit
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

    N = 0
    path = '/slow/users/mfa/makg/wikidata/'
    with open(wddir + 'id_doi.csv', 'w', newline='\n') as discfile:
        with open(wddir + sys.argv[1], "r") as file:
            fieldnames = ['id', 'doi']
            writer = csv.DictWriter(discfile, fieldnames=fieldnames, delimiter=',')
            line = next(file).strip()
            while line:
                if N % 1000000 == 0:
                    print(N)
                if '<http://www.wikidata.org/prop/direct/P356>' in line:
                    s = line
                    id = s[s.find('<http://www.wikidata.org/entity/') + len('<http://www.wikidata.org/entity/'):s.rfind(
                        '> <http://www.wikidata.org/prop/direct/P356>')]
                    doi = s[s.find('prop/direct/P356> "') + len(
                        'prop/direct/P356> "'):s.rfind('" .')]
                    writer.writerow({'id': id, 'doi': doi})

                N += 1

