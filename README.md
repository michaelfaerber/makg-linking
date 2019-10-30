### Mappings between the MAKG and OpenCitations/Wikidata
This repository provides code for generating owl:sameAs links between instances in the [Microsoft Academic Knowledge Graph (MAKG)](http://ma-graph.org) and [OpenCitations](http://opencitations.net)/[Wikidata](http://wikidata.org). For more background information, see my repository [MAKG] and the ISWC 2019 paper [The Microsoft Academic Knowledge Graph: A Linked Data Source with 8 Billion Triples of Scholarly Data].

## Wikidata <-> MAKG
Mapping instances of Wikidata to the MAKG is done using __map_wikidata_to_mag.py__. This produces 2 files:
1. __wikidata_mag_mapping.tsv__ which contains the mapping from Wikidata to the MAKG. This tsv file contains the DOI, the Wikidata ID and the MAG paper id.
2. __wikidata_not_in_mag.txt__ which contains a list of DOIs which could not be mapped from Wikidata to MAKG.
The following command is run on this file to get a unique list of DOIs which couldn't be mapped: `sort wikidata_not_in_mag.txt | uniq -u > wikidata_not_in_mag_uniq.txt`

Frequencies for Wikidata:
* wikidata_not_in_mag.txt: Wikidata DOIs that are not in the MAKG: 10,812,141
* wikidata_mag_mapping.tsv: Wikidata DOIs that are in the MAKG: 5,472,038
* total Wikidata records: 16,324,110

## OpenCitations <-> MAKG
Mapping instances of OpenCitations to the MAKG is done using `map_opencit_to_mag_latest.py`. This produces 2 files as well:
1. opencit_mag_mapping.tsv
2. opencit_not_in_mag.txt
Run `sudo cut -f1,3 opencit_mag_mapping.tsv | tail -n +2 | sort -S52G --parallel=42 -u > opencit_mag_mapping_real.txt` to get the final file opencit_mag_mapping_real.txt
This is a tab-separated file with 2 columns: DOI and MAG paper id.

Frequencies for OpenCitations:
* opencit_not_in_mag.txt: OpenCitations DOIs that are not in the MAKG
* opencit_mag_mapping_real.txt: OpenCitations DOIs which are in the MAKG: 15,666,233
* total opencit records: 449,842,375

Frequency of MAG:
209,792,741 papers in the MAKG (Nov 2018)



The rest of the programs are used to get the percentage of these papers (that have been mapped from Wikidata/Opencit to the MAG/MAKG!) which are written in different languages/belong to different fields of study.

PROGRAMS for discipline statistics:
```
map_opencit_discipline.py
map_opencit_discipline_ids.py
map_wikidata_discipline.py
map_wikidata_discipline_ids.py
get_discipline_stats.py
```
PROGRAMS for language statistics:
```
map_opencit_lang.py
map_wikidata_lang.py
get_lang_stats.py
```

Final discipline stats are present in the following files (csv file with columns: discipline,frequency,percentage):

```
opencit_discipline_stats.txt
wikidata_discipline_stats.txt
```

In the above files, the disciplines are the top-level fields of study in the MAG/MAKG.

Final language stats are present in the following files (csv file with columns: languagecode,frequency,percentage):
```
opencit_lang_stats.txt
wikidata_lang_stats.txt
```
In the above files, the language codes are as given in the paperlanguages file in the MAG/MAKG (2-letter codes).


__Overall findings:__
* The MAKG is considerably larger than Wikidata's representation of bibliographic information (209,792,741 papers in the MAKG as of Nov 2018; 16,324,110 papers in Wikidata).
* We could create 15,666,233 mappings between papers modeled in OpenCitations and papers modeled in the MAKG. This corresponds to 7.47% of the MAG's papers (v2018-11) and 3.48% of OpenCitations' papers.
* We could create 5,472,038 mappings between papers modeled in Wikidata and papers modeled in the MAKG. This corresponds to 2.61% of the MAG's papers and 33.52% of the Wikidata's papers.

## Contact & More Information
More information can be found in my ISWC'19 paper [The Microsoft Academic Knowledge Graph: A Linked Data Source with 8 Billion Triples of Scholarly Data](http://dbis.informatik.uni-freiburg.de/content/team/faerber/papers/MAKG_ISWC2019.pdf).

Feel free to reach out to me in case of questions or comments:

[Michael Färber](https://sites.google.com/view/michaelfaerber), michael.faerber@kit.edu

## How to Cite
Please cite my work (described in [this paper](http://dbis.informatik.uni-freiburg.de/content/team/faerber/papers/MAKG_ISWC2019.pdf)) as follows:
```
@inproceedings{DBLP:conf/semweb/Farber19,
  author    = {Michael F{\"{a}}rber},
  title     = "{The Microsoft Academic Knowledge Graph: {A} Linked Data Source with
               8 Billion Triples of Scholarly Data}",
  booktitle = "{Proceedings of the 18th International Semantic Web Conference}",
  series    = "{ISWC'19}",
  location  = "{Auckland, New Zealand}",
  pages     = {113--129},
  year      = {2019},
  url       = {https://doi.org/10.1007/978-3-030-30796-7\_8},
  doi       = {10.1007/978-3-030-30796-7\_8}
}

```
