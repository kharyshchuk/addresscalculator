import math
import uuid

from constants import GIS, HTTP, R, LATITUDE, LONGITUDE, ADDRESS, NAME, POINTS, LINKS, DISTANCE
from db_layers.result_repository import RESULT_ID
from helpers.http_services import get_address_by_gis, get_address_by_http_request


def get_addresses_info(df, client_type=HTTP):
    df = df.rename(columns={
        'Point': NAME,
    })
    df[ADDRESS] = ''

    result = {RESULT_ID: str(uuid.uuid4()), POINTS: [], LINKS: []}

    def fill_data(df, index):
        current_row = df.loc[index]
        address = get_address_by_gis(current_row[LONGITUDE], current_row[LATITUDE]) \
            if client_type == GIS \
            else get_address_by_http_request(current_row[LONGITUDE], current_row[LATITUDE])

        result[POINTS].append({NAME: current_row[NAME], ADDRESS: address})

        # calculate distances
        i = index + 1
        while i < df_length:
            next_row = df.loc[i]
            distance = get_distanse(current_row[LONGITUDE], current_row[LATITUDE], next_row[LONGITUDE],
                                    next_row[LATITUDE])
            result[LINKS].append({NAME: f'{current_row[NAME]}{next_row[NAME]}', DISTANCE: distance})
            i += 1

    index = 0
    df_length = len(df)
    while index < df_length:
        fill_data(df, index)
        index += 1

    return result


def get_distanse(lon1, lat1, lon2, lat2):
    lat1_r = math.radians(lat1)
    lon1_r = math.radians(lon1)

    lat2_r = math.radians(lat2)
    lon2_r = math.radians(lon2)

    dlon = lon2_r - lon1_r  # change in coordinates

    dlat = lat2_r - lat1_r

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2 # Haversine formula

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance
