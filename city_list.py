from xml.etree import ElementTree
from urllib.request import urlopen, Request, urlretrieve

def get_weather_list():
    # parse()関数でフィルを読み込んでElementTreeオブジェクトを得る
    url = "http://weather.livedoor.com/forecast/rss/primary_area.xml"

    #savename = 'primary_area.xml'
    #urlretrieve(url, savename)
    #Parses over all the elementree XML elements
    tree = ElementTree.parse('primary_area.xml')

    #getroot() メソッドでXMLのルート要素（この例ではrss要素）に対応する
    #Elementオブジェクトを得る
    #Getroot grabs the first element in the XML tree
    root = tree.getroot()

    #都市リスト:city_dictの初期化
    city_dict = {}

    #findall()メソッドでXPathにマッチする要素のリストを取得する
    for pref in root.findall('.//pref'):

        pref_name = pref.get('title')

        for city in pref.findall('.//city'):
            city_name = city.get('title')
            city_id = city.get('id')
            city_dict[city_name] = city_id

    return city_dict
