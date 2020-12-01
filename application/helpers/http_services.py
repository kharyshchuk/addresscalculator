import http.client
import json

import pandas as pd
from arcgis import geocoding
from arcgis.features import Feature, FeatureSet
from arcgis.gis import GIS
from arcgis.network.analysis import generate_origin_destination_cost_matrix

conn = http.client.HTTPSConnection("geocode.arcgis.com")
payload = ''
headers = {
  'authority': 'geocode.arcgis.com',
  'cache-control': 'max-age=0',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'none',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
  'cookie': 'at_check=true; AMCVS_ED8D65E655FAC7797F000101%40AdobeOrg=1; s_dfa=esriglobalext; AMCV_ED8D65E655FAC7797F000101%40AdobeOrg=-637568504%7CMCIDTS%7C18597%7CMCMID%7C84486529739923289354000551208256687416%7CMCAAMLH-1607365060%7C6%7CMCAAMB-1607365060%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1606767460s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.1.1; adcloud={%22_les_v%22:%22y%2Carcgis.com%2C1606762060%22}; s_cc=true; mbox=session#5e73d5226a01493b8588eb75bcd98730#1606762143|PC#5e73d5226a01493b8588eb75bcd98730.37_0#1670005061; OptanonConsent=isIABGlobal=false&datestamp=Mon+Nov+30+2020+20%3A18%3A02+GMT%2B0200+(Eastern+European+Standard+Time)&version=5.15.0&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1&hosts=&legInt=&AwaitingReconsent=false; gpv_pn=developers.arcgis.com%3A%20features%3A%20geocoding; s_tp=3958; gpv_v9=developers.arcgis.com%3A%20features%3A%20geocoding; dmdbase_cdc=DBSET; sat_track=true; pi_opt_in8202=true; esri_gdpr=true; OptanonAlertBoxClosed=2020-11-30T18:18:04.756Z; _biz_uid=f99caca21c39485bca6c94729d4ea2ec; _biz_sid=329d2a; _biz_nA=2; s_ptc=0.45%5E%5E0.00%5E%5E0.00%5E%5E0.00%5E%5E0.09%5E%5E0.00%5E%5E3.37%5E%5E0.01%5E%5E3.93; _uetsid=643b7350333811ebb45b1f379a5f2933; _uetvid=643bbfd0333811ebaaa45b0739881203; _biz_pendingA=%5B%5D; _gcl_au=1.1.1957418785.1606760286; _fbp=fb.1.1606760285919.630193670; _biz_flagsA=%7B%22Version%22%3A1%2C%22Ecid%22%3A%22-1308799129%22%2C%22ViewThrough%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D; s_ppv=developers.arcgis.com%253A%2520features%253A%2520geocoding%2C45%2C23%2C1796; s_sq=esriglobalext%3D%2526c.%2526a.%2526activitymap.%2526page%253Ddevelopers.arcgis.com%25253A%252520features%25253A%252520geocoding%2526link%253DZoom%252520to%2526region%253DlocateAddressMapView%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Ddevelopers.arcgis.com%25253A%252520features%25253A%252520geocoding%2526pidt%253D1%2526oid%253Dfunction%252528a%252529%25257Bc%252528%252522domEvent%252522%25252Ca%252529%25253Bvare%25253Dd%252528%252529%25252Cg%25253Bg%25253Da.currentTarget%25253Bfor%252528varh%25253De.domNode%25252Ck%25253D%25255B%25255D%25253Bg%252521%25253D%25253Dh%25253B%252529k.push%252528g%252529%25252Cg%25253D%2526oidt%253D2%2526ot%253DDIV; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1',
}

request_str = "/arcgis/rest/services/World/GeocodeServer/reverseGeocode?location={{Longitude}}%2C{{Latitude}}&langCode=en&outSR=&forStorage=false&f=pjson"

my_gis = GIS()


# `X` is longitude
# `Y` is latitude
def get_address_by_gis(lon, lat):
    reverse_geocode = None
    try:
        reverse_geocode = geocoding.reverse_geocode({"x": lon, "y": lat}, lang_code='en')
    except Exception as exp:
        print(exp)

    return reverse_geocode['address']['LongLabel']


def get_address_by_http_request(lon, lat):
    conn.request("GET", request_str.replace('{{Longitude}}', str(lon)).replace('{{Latitude}}', str(lat)), payload, headers)
    res = conn.getresponse()
    data = res.read()
    address_obj = json.loads(data.decode("utf-8"))

    return address_obj['address']['LongLabel']


# not used
def get_geo_location_info_by_OD_matrix(lon, lat):
    origin_coords = ['50.448069, 30.5194453', '50.448616, 30.5116673', '50.913788, 34.7828343']
    # origin_coords = ['-117.187807, 33.939479', '-117.117401, 34.029346']

    origin_features = []

    for origin in origin_coords:
        reverse_geocode = geocoding.reverse_geocode({"x": origin.split(',')[0],
                                                     "y": origin.split(',')[1]})

        origin_feature = Feature(geometry=reverse_geocode['location'],
                                 attributes=reverse_geocode['address'])
        origin_features.append(origin_feature)

    origin_fset = FeatureSet(origin_features, geometry_type='esriGeometryPoint',
                             spatial_reference={'latestWkid': 4326})

    destinations_address = r"data/destinations_address.csv"
    destinations_df = pd.read_csv(destinations_address)
    destinations_sdf = pd.DataFrame.spatial.from_df(destinations_df, "Address")

    destinations_fset = destinations_sdf.spatial.to_featureset()

    try:
        results = generate_origin_destination_cost_matrix(origins=origin_fset,  # origins_fc_latlong,
                                                          destinations=destinations_fset,  # destinations_fs_address,
                                                          cutoff=200,
                                                          origin_destination_line_shape='Straight Line')
        od_df = results.output_origin_destination_lines.sdf

        # filter only the required columns
        od_df2 = od_df[['DestinationOID', 'OriginOID', 'Total_Distance', 'Total_Time']]

        # user pivot_table
        od_pivot = od_df2.pivot_table(index='OriginOID', columns='DestinationOID')
        return od_pivot
    except Exception as exp:
        print(exp)

    return None