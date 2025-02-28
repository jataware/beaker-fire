You are able to query the ACLED API for data on conflicts and events around the world. ACLED is the Armed Conflict Location and Event Data Project.

Here is an example of how to query the ACLED API:

```python
import requests
import json
import pandas as pd
import folium
import os
from datetime import datetime, timedelta

# Store dates for reference
end_date = datetime.now()
start_date = end_date - timedelta(days=180)
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

print(f"Querying events from {start_date_str} to {end_date_str}")

# ACLED API parameters
params = {
    'email': os.getenv('ACLED_EMAIL'),
    'key': os.getenv('ACLED_API'),
    'country': 'Ukraine',
    'event_date': f"{start_date_str}|{end_date_str}",
    'limit': 1000
}

# Make request to ACLED API
response = requests.get('https://api.acleddata.com/acled/read', params=params)
data = response.json()

print("\nAPI Response:")
print(json.dumps(data, indent=2)[:1000]) 
```

Note that you can expect to have access to the `ACLED_EMAIL` and `ACLED_API` environment variables and use them as such. You should note. 

The API does have limits. owever, even when using query filters, the returned dataset may be very large. If you do not need every event defined by your query filters, you can limit the size of the returned file. In particular, you can specify the number of events in the returned data by including a limit statement in your URL (e.g., limit=2000 means you will receive data for 2000 events). Without a ‘limit’ in your URL, ACLED’s API will return a maximum of 5000 events. In cases where you are expecting events beyond the default limit, you are advised to use pagination which allows you to split your call into multiple smaller ones and ensure your call executes successfully. These calls do not count toward your API rate limits.

The suggested method for requesting large amounts of data from ACLED’s API is by using pagination. Pagination is simply the process of splitting one very large API call into several smaller calls or “pages”. The advantage of pagination is that it helps avoid timeout errors.

You can add pagination to your URL by including the &page=X parameter at the end of the URL, where X denotes the page number. To receive all of your data you should rerun the API call, incrementing the page number by 1 each time, until you have received all the rows you requested. For instance, if you suspect there are many events that match your query filters, you should execute an API call with a URL including &page=1. You should then repeat the call and increase the page number to 2 (i.e. &page=2), and so on, until the data request returns a number of rows less than the limit (e.g. if you request limit=5000 but you receive 4999 rows or fewer - the limit by default is 5000.).

For example, from January 2018 to December 2022, there are around 12000 events from Argentina in the ACLED event dataset. You can request these data using pagination:

— 1st Call (Returns the first 5000 rows)

`https://api.acleddata.com/acled/read.csv?key=your_key&email=your_email&country=Argentina&year=2018|2022&year_where=BETWEEN&page=1`

— 2nd Call (Returns the second 5000 rows)

`https://api.acleddata.com/acled/read.csv?key=your_key&email=your_email&country=Argentina&year=2018|2022&year_where=BETWEEN&page=2`

Here are the query filters available for ACLED:

| Filter Name | Type | String |
|------------|------|---------|
| key | = | ?key={api_key} |
| email | = | ?email={email address associated with key} |
| event_id_cnty | LIKE | ?event_id_cnty={text} |
| event_date | = | ?event_date={yyyy-mm-dd} |
| year | = | ?year={yyyy} |
| time_precision | = | ?time_precision={number} |
| disorder_type | LIKE | ?disorder_type={text} |
| event_type | LIKE | ?event_type={text} |
| sub_event_type | LIKE | ?sub_event_type={text} |
| actor1 | LIKE | ?actor1={text} |
| assoc_actor_1 | LIKE | ?assoc_actor_1={text} |
| inter1 | = | ?inter1={number} |
| actor2 | LIKE | ?actor2={text} |
| assoc_actor_2 | LIKE | ?assoc_actor_2={text} |
| inter2 | = | ?inter2={number} |
| interaction | = | ?interaction={number} |
| inter_num | = | ?inter_num={0,1} |
| civilian_targeting | LIKE | ?civilian_targeting={text} |
| iso | = | ?iso={number} |
| region | = | ?region={number} |
| country | = | ?country={text} |
| admin1 | LIKE | ?admin1={text} |
| admin2 | LIKE | ?admin2={text} |
| admin3 | LIKE | ?admin3={text} |
| location | LIKE | ?location={text} |
| latitude | = | ?latitude={number} |
| longitude | = | ?longitude={number} |
| geo_precision | = | ?geo_precision={number} |
| source | LIKE | ?source={text} |
| source_scale | LIKE | ?source_scale={text} |
| notes | LIKE | ?notes={text} |
| fatalities | = | ?fatalities={number} |
| tags | LIKE | ?tags={text} |
| timestamp | >= | ?timestamp={number or yyyy-mm-dd} |
| export_type | = | ?export_type={text} |
| population | = | ?population={TRUE&#124;full} |

If you fetch a lot of data (e.g., more than 100 events) and want to plot it, you should use Datashader to plot it since there are just too many points to plot with Folium in active conflict zones (such as Ukraine).