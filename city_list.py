from xml.etree import ElementTree
from urllib.request import urlopen, Request, urlretrieve

def get_weather_list():
    # parse()関数でフィルを読み込んでElementTreeオブジェクトを得る
    url = "http://weather.livedoor.com/forecast/rss/primary_area.xml"

    #savename = 'primary_area.xml'
    #urlretrieve(url, savename)
    tree = ElementTree.parse('primary_area.xml')

    #getroot() メソッドでXMLのルート要素（この例ではrss要素）に対応する
    #Elementオブジェクトを得る
    root = tree.getroot()

    #都市リスト:city_dictの初期化
    city_dict = {}

    #findall()メソッドでXPathにマッチする要素のリストを取得する
