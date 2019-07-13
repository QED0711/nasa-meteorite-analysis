def get_countries(df, start_idx):
    """
    given lat and long coordinates in a df (and id), finds the country name at that 
    location via the google maps api.
    
    Saves resulting data in multiple csv files. This is to protect previous data in the case that there is an 
    error later on that wipes a given file. 
    
    NOTE: Do not run on large sets unless you are absolutely sure confident that the data you pass in 
    will have no errors in the API calls.
    """
    import csv
    
    for i in range(start_idx, df.shape[0]):
        country, country_short_name = (None, None)
        file = f"countries/countries-{(i // 1000)}.csv"
        
        
        row_id, lat, lng = (df.id[i], df.reclat[i], df.reclong[i])
        
        req_str = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={keys['mapsAPI']}"

        resp = requests.get(req_str).json()

        for r in resp['results']:
            if "country" in r['types']:
                country = r['address_components'][0]['long_name']
                country_short_name = r['address_components'][0]['short_name']
        
        if country and country_short_name:
            try:    
                with open(file, 'a') as countries:
                    country_writer = csv.writer(countries, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                    country_writer.writerow([row_id, lat, lng, country, country_short_name])
            except:
                print(i)
                return
        


# UNCOMMENT TO RUN API CALLS
# get_countries(geo_df[17062:].reset_index())
# get_countries(geo_df.reset_index(), start_idx=0)