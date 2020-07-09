### Mappings between the MAKG and OpenCitations/Wikidata
This repository provides code for generating owl:sameAs links between instances in the [Microsoft Academic Knowledge Graph (MAKG)](http://ma-graph.org) and [OpenCitations](http://opencitations.net)/[Wikidata](http://wikidata.org). For more background information, see my repository [MAKG](http://ma-graph.org) and the ISWC 2019 paper [The Microsoft Academic Knowledge Graph: A Linked Data Source with 8 Billion Triples of Scholarly Data](http://dbis.informatik.uni-freiburg.de/content/team/faerber/papers/MAKG_ISWC2019.pdf).

The numbers mentioned below are with respect to the MAKG version 2019-12-26.

## Wikidata <-> MAKG
Start by filtering the Wikidata dataset with __filter_wikidata_papers.py__.
Mapping instances of Wikidata to the MAKG is done using __map_wikidata_to_mag.py__. This produces 2 files:
1. __wikidata_mag_mapping.tsv__ which contains the mapping from Wikidata to the MAKG. This tsv file contains the DOI, the Wikidata ID and the MAG paper id.
2. __wikidata_not_in_mag.txt__ which contains a list of DOIs which could not be mapped from Wikidata to MAKG.

Frequencies for Wikidata:
* wikidata_not_in_mag.txt: Wikidata DOIs that are not in the MAKG: 1,296,686
* wikidata_mag_mapping.tsv: Wikidata DOIs that are in the MAKG: 24,148,216
* total Wikidata records: 25,444,902

## OpenCitations <-> MAKG
Mapping instances of OpenCitations to the MAKG is done using `map_opencit_to_mag_latest.py`. This produces 2 files as well:
1. opencit_mag_mapping.tsv
2. opencit_not_in_mag.txt

Frequencies for OpenCitations:
* opencit_not_in_mag.txt: OpenCitations DOIs that are not in the MAKG: 35,977,347
* opencit_mag_mapping.txt: OpenCitations DOIs which are in the MAKG: 666,795,182
* total opencit records: 702,772,529


Frequency of MAG:
378,988,501 papers in the MAKG (June 2020)
88,342,106 papers in the MAKG with DOIs (June 2020)


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
* The MAKG is considerably larger than Wikidata's representation of bibliographic information (378,988,501 papers in the MAKG as of June 2020; 25,444,902 papers in Wikidata).
* We could create 666,795,182 mappings between citations modeled in OpenCitations and papers modeled in the MAKG. This corresponds to 94.89% of OpenCitations' citations.
* We could create 24,148,216 mappings between papers modeled in Wikidata and papers modeled in the MAKG. This corresponds to 6.37% of the MAG's papers and 94.90% of the Wikidata's papers.

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

## Last Major Update
2020-07-09
