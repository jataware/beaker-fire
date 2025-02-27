Additionally, you have data on the location of global ports and the location of mines around the world.

This data was obtained from Wikidata with the following SPARQL queries:

Ports query:
```
#title: All Mines Worldwide
#defaultView:Map
SELECT DISTINCT ?mine ?mineLabel 
       ?coordinates 
       (REPLACE(STR(?coordinates), ".*\\(([^ ]*) ([^)]*)\\).*", "$1") AS ?lon)
       (REPLACE(STR(?coordinates), ".*\\(([^ ]*) ([^)]*)\\).*", "$2") AS ?lat)
       ?country ?countryLabel 
       (GROUP_CONCAT(DISTINCT ?mineralLabel; separator=", ") as ?minerals)
WHERE {
  # Find mines - direct instance of mine for better performance
  ?mine wdt:P31 wd:Q820477.  # Instance of mine
  
  # Get coordinates
  ?mine wdt:P625 ?coordinates.
  
  # Get country
  OPTIONAL {
    ?mine wdt:P17 ?country.
  }
  
  # Optional minerals
  OPTIONAL {
    # Try different properties that might connect mines to minerals
    {?mine wdt:P517 ?mineral.} UNION  # used as
    {?mine wdt:P1056 ?mineral.} UNION # product
    {?mine wdt:P366 ?mineral.}        # use
    
    # Get mineral label
    ?mineral rdfs:label ?mineralLabel.
    FILTER(LANG(?mineralLabel) = "en")
  }
  
  # Labels for mine and country
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
GROUP BY ?mine ?mineLabel ?coordinates ?lon ?lat ?country ?countryLabel
ORDER BY ?countryLabel ?mineLabel
LIMIT 100000
```

Ports query:
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

This data is stored in `data/port_locations.csv` and `data/mine_locations.csv`. You can use this data to answer questions about 
the locations where minerals are produced and possibly the ports where they are imported and exported.