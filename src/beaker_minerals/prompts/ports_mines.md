Additionally, you have data on the location of global ports and the location of mines that produce critical minerals.

This data was obtained from Wikidata with the following SPARQL queries:

Ports query:
```
#title: Critical Mineral Mines Worldwide with Lat/Lon
#defaultView:Map
SELECT DISTINCT ?mine ?mineLabel ?mineral ?mineralLabel 
       ?coordinates 
       (REPLACE(STR(?coordinates), ".*\\(([^ ]*) ([^)]*)\\).*", "$1") AS ?lon)
       (REPLACE(STR(?coordinates), ".*\\(([^ ]*) ([^)]*)\\).*", "$2") AS ?lat)
       ?country ?countryLabel 
WHERE {
  # Find mines
  ?mine wdt:P31/wdt:P279* wd:Q820477.  # Instance of mine or subclass
  
  # Get coordinates
  ?mine wdt:P625 ?coordinates.
  
  # Optional country
  OPTIONAL {
    ?mine wdt:P131* ?location.
    ?location wdt:P17 ?country.
  }
  
  # Find mineral associations
  {
    # Try different properties that might connect mines to minerals
    {?mine wdt:P517 ?mineral.} UNION  # used as
    {?mine wdt:P1056 ?mineral.} UNION # product
    {?mine wdt:P366 ?mineral.}        # use
    
    # Complete 2022 critical minerals list
    VALUES ?mineral {
      wd:Q759    # Aluminum
      wd:Q935    # Antimony
      wd:Q871    # Arsenic
      wd:Q622649 # Barite
      wd:Q1542   # Beryllium
      wd:Q896    # Bismuth
      wd:Q658    # Cerium
      wd:Q754    # Cesium
      wd:Q1322   # Chromium
      wd:Q677    # Cobalt
      wd:Q1296   # Dysprosium
      wd:Q1316   # Erbium
      wd:Q1299   # Europium
      wd:Q458586 # Fluorspar (Fluorite)
      wd:Q1344   # Gadolinium
      wd:Q731    # Gallium
      wd:Q911    # Germanium
      wd:Q1049   # Graphite
      wd:Q838    # Hafnium
      wd:Q1329   # Holmium
      wd:Q1093   # Indium
      wd:Q1098   # Iridium
      wd:Q655    # Lanthanum
      wd:Q622    # Lithium
      wd:Q1358   # Lutetium
      wd:Q661    # Magnesium
      wd:Q842    # Manganese
      wd:Q864    # Neodymium
      wd:Q662    # Nickel
      wd:Q1090   # Niobium
      wd:Q9554   # Palladium
      wd:Q771    # Platinum
      wd:Q659    # Praseodymium
      wd:Q1060   # Rhodium
      wd:Q1097   # Rubidium
      wd:Q1089   # Ruthenium
      wd:Q1156   # Samarium
      wd:Q860    # Scandium
      wd:Q1189   # Tantalum
      wd:Q1100   # Tellurium
      wd:Q1234   # Terbium
      wd:Q1322   # Thulium
      wd:Q769    # Tin
      wd:Q752    # Titanium
      wd:Q706    # Tungsten
      wd:Q917    # Vanadium
      wd:Q1354   # Ytterbium
      wd:Q927    # Yttrium
      wd:Q1118   # Zinc
      wd:Q924    # Zirconium
    }
  }
  
  # Labels
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?countryLabel ?mineralLabel
LIMIT 20000
```

Mines query:
```
#title: Major Ports Around the World
#defaultView:Map
SELECT DISTINCT ?port ?portLabel 
       ?coordinates 
       (REPLACE(STR(?coordinates), ".*\\(([^ ]*) ([^)]*)\\).*", "$1") AS ?lon)
       (REPLACE(STR(?coordinates), ".*\\(([^ ]*) ([^)]*)\\).*", "$2") AS ?lat)
       ?country ?countryLabel 
WHERE {
  # Find ports - focusing on major port categories with direct instance
  ?port wdt:P31 ?portType.
  VALUES ?portType {
    wd:Q44782    # port
    wd:Q11314    # seaport
    wd:Q2257142  # cargo port
  }
  
  # Get coordinates - this is required
  ?port wdt:P625 ?coordinates.
  
  # Country - this is required to improve performance
  ?port wdt:P17 ?country.
  
  # Labels
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?countryLabel ?portLabel
LIMIT 10000
```

This data is stored in `data/port_locations.csv` and `data/critical_mineral_mines.csv`. You can use this data to answer questions about 
the locations where minerals are produced and possibly the ports where they are imported and exported.