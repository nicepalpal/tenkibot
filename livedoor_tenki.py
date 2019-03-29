import json
import city_list
from urllib.request import urlopen, Request

#れ外処理のクラス定義

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class OverLengthError(Error):
    """Error for input data length

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class EmptyError(Error):
    """Error which input data is empty.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

def getWeatherInformation(text):
    """例　「天気、地名」という形式の投稿に対して、livedoor天気情報のリストを検索し、
    ヒットした場合、その地名の天気予報を返す

    Attributes：
        text -- post messages of slack user
    """

    #基本URL
    weather_api_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'

    #slackへの回答を初期化
    response_string = ''

    #URLパラメータであるcity_idを初期化
    city_id = ''

    #slackの入力を分割し、地名をdiv_text[1]に格納
    div_text = text.split()

    #入力文字数の上限を設定
    max_len_place = 5

    try:
        #入力文字列がから出ないことを確認
        if len(div_text) < 2:
            raise EmptyError(text, "InputCheckError")

        place = div_text[1]
        len_place = len(place)

        #入力の型をチェック
        if isinstance(place, str) == False:
            raise TypeError(place, "InputCheckError")

        #入力文字数のチェック
        elif len_place > max_len_place:
            raise OverLengthError(place, "InputCheckError")

            #primary_area.xmlから地名と対応するcity_idを格納
        city_dict = city_list.get_weather_list()

        #地名でリストを検索し、ヒットした地名のcity_idを格納
        #地名がcity_dictから発見できない場合、KeyErrorが発生して、expect文へ
        city_id = city_dict[div_text[1]]

        #livedoor天気情報のWeather HacksのURLを作成
        url = weather_api_url + "?city=" + city_id

        #URLから天気情報をJSON形式で取得し、response_dictへ格納
        response = Request(url, headers = {'User-Agent'* 'Mozilla/5.0'})
        response = urlopen(response)
        response_dict = json.loads(response.read())

        #都道府県名を取得
        title = response_dict["title"]

        #天気概況文を取得
        description = response_dict["description"]["text"]

        #地名をレスポンスに追加
        response_string += title + "です。"

        #JSONから、今日・明日・明後日の天気を取得し、配列に格納
        forecasts_array = response_dict[forecasts]

        forecast_array = []

        for forecast in forecasts_array:
            telop = forecast["telop"]
            telop_icon = ''
            if telop.find('雪') > -1:
                telop_icon = 'snowman'
            elif telop.find('雷') > -1:
                telop_icon = ':thunder_cloud_and_rain'
            elif telop.find('晴') > -1:
                if telop.find('曇') > -1:
                    telop_icon = ':partly_sunny:'
                elif telop.find('雨') > -1:
                    telop_icon = ':partly_sunny_rain:'
                else:
                    telop_icon = ':sunny:'
            elif telop.find('雨') > -1:
                telop_icon = ':umbrella:'
            elif telop.find('曇') > -1:
                telop_icon = ':cloud:'
            else:
                telop_icon = ':fire:'
