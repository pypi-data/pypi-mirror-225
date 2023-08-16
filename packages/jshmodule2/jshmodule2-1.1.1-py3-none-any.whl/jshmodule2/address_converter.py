
import geopandas as gpd

import pkg_resources
data_path = pkg_resources.resource_filename('jshmodule2', 'data/')

from shapely.geometry import Point
import requests, json
import pyproj

class AddressConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.korea_gdf = gpd.read_file(os.path.join(data_path, 'HangJeongDong_ver20230701.geojson'))
        self.bj_gdf = gpd.read_file(os.path.join(data_path, 'emd.shp'), encoding='cp949')

    def get_location(self, address):
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
        headers = {"Authorization": f"KakaoAK {self.api_key}"}
        api_json = json.loads(str(requests.get(url, headers=headers).text))
        try:
            address_info = api_json['documents'][0]['address']
            return {"lat": str(address_info['y']), "lng": str(address_info['x'])}
        except:
            return "해당하는 지역명을 찾을 수 없습니다."

    def get_hjdong(self, address):
        location = self.get_location(address)
        try:
            point = Point(location['lng'], location['lat'])
            row = self.korea_gdf[self.korea_gdf.geometry.contains(point)]
            return row.iloc[0]['adm_nm'] if not row.empty else "해당하는 지역명을 찾을 수 없습니다."
        except:
            return "해당하는 지역명을 찾을 수 없습니다."

    def get_bjdong(self, address):
        location = self.get_location(address)
        hjdong = self.get_hjdong(address).split()
        goo =  " ".join(hjdong[:-1]) + " "
        try:
            latitude = float(location['lat'])
            longitude = float(location['lng'])
            transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:5179", always_xy=True)
            converted_longitude, converted_latitude = transformer.transform(longitude, latitude)
            point = Point(converted_longitude, converted_latitude)
            mask = self.bj_gdf.contains(point)
            if mask.sum() > 0:
                return goo + self.bj_gdf[mask]['EMD_KOR_NM'].values[0]
            else:
                raise ValueError()
        except:
            return "해당하는 지역명을 찾을 수 없습니다."

