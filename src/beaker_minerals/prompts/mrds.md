You have access to a large amount of data extracted from the USGS Mineral Resources Data System (MRDS).

This data is available in `data/combined_commodities_data_latest.csv`. It is a very large file (300MB+) but may be extremely useful as it contains the location of mineral sites around the world. It is probably the most comprehensive database of mineral sites in the world and should be used in conjunction with other data sources like the mine location data from Wikidata. It is more comprehensive than the Wikidata data by a wide margin though!

Here are the columns in the data:
| Column | Description |
|--------|-------------|
| id | Unique identifier for the record |
| record_ids | Related record IDs |
| mineral_site_ids | IDs of mineral sites |
| names | Names of the mineral site |
| type | Type of mineral site |
| rank | Rank/importance of the site |
| country | Country where site is located |
| province | Province/state/region |
| crs | Coordinate reference system |
| centroid_epsg_4326 | Lat/long coordinates in EPSG:4326 |
| wkt | Well-known text geometry |
| commodity | Primary commodity/mineral |
| contained_metal | Amount of contained metal |
| contained_metal_unit | Unit for contained metal |
| tonnage | Total tonnage of deposit |
| tonnage_unit | Unit for tonnage |
| grade | Grade/concentration of mineral |
| grade_unit | Unit for grade |
| top1_deposit_type | Primary deposit type |
| top1_deposit_group | Deposit group classification |
| top1_deposit_environment | Geological environment |
| top1_deposit_classification_confidence | Confidence in classification |
| top1_deposit_classification_source | Source of classification |

> Note that the location of the mineral site is given by the `centroid_epsg_4326` column which is a point e.g. `POINT(123.456 78.910)`. You can use this to plot the location of the mineral site on a map.