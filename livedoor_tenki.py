import json
import city_list
from urllib.request import urlopen, Request
#urllibl.request.Request class lets you do a lot of things like import url Input
#in the instructor, the host, the Data
#urlopen opens the url that is passed

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

    #Try clause evaluates the code below, and if any exceptions occur it will run
    #the Except clauses below
    try:
        #入力文字列がから出ないことを確認
        if len(div_text) < 2:
            raise EmptyError(text, "InputCheckError")
        #In the original text argument passed to the function, text[1] will be the place name
        place = div_text[1]
        len_place = len(place)

        #入力の型をチェック
        #If place is not a string raise the TypeError
        if isinstance(place, str) == False:
            raise TypeError(place, "InputCheckError")

        #入力文字数のチェック
        elif len_place > max_len_place:
            raise OverLengthError(place, "InputCheckError")

        #primary_area.xmlから地名と対応するcity_idを格納
        #This calls from an XML file designated in city_list.py
        city_dict = city_list.get_weather_list()

        #地名でリストを検索し、ヒットした地名のcity_idを格納
        #地名がcity_dictから発見できない場合、KeyErrorが発生して、expect文へ
        city_id = city_dict[div_text[1]]

        #livedoor天気情報のWeather HacksのURLを作成
        url = weather_api_url + "?city=" + city_id

        #URLから天気情報をJSON形式で取得し、response_dictへ格納
        #Request class instance has to have at least a url and headers
        #Most web browsers require a User-Agent header to specify what browser is
        #connecting

        response = Request(url, headers = {'User-Agent':'Mozilla/5.0'})
        #Urlopen below opens the URL in the Request
        response = urlopen(response)
        #.loads is a JSON function that takes strings and puts them in dictionary form
        #Regular .load READS (doesnt convert) files in a dictionary format
        response_dict = json.loads(response.read())

        #都道府県名を取得
        title = response_dict["title"]

        #天気概況文を取得
        description = response_dict["description"]["text"]

        #地名をレスポンスに追加
        response_string += title + "です。"

        #JSONから、今日・明日・明後日の天気を取得し、配列に格納
        forecasts_array = response_dict[forecasts]

        forecast_array = [] #This will be used in the response_string

        for forecast in forecasts_array:
            telop = forecast["telop"]
            telop_icon = ''
            #Find looks for the index of where that value is in the string and returns that number
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
            #気温の記述を作成
            temperature = forecast["temperature"]
            min_temp = temperature["min"]
            max_temp = temperature["max"]
            temp_text = ''
            #Makes sure that you are getting at least the min temp to verify them
            #Response worked correctly
            if min_temp is not None:
                #Adds the min and max temps to a string to add to the response string.
                #\n is a newline escape sequence.
                if len(min_temp) > 0:
                    temp_text += '\n最低気温は' + min_temp["celsius"] + "度です。"
                if len(max_temp) > 0:
                    temp_text += '\n最高気温は' + max_temp["celsius"] + "度です。"
                #Append the date, telop (weather kanji), telop icon, and the text regarding
                #the temperature we created above to the forecast_array
                forecast_array.append(forecast["dateLabel"] + ' ' + telop + telop_icon + temp_text)
            if len(forecast_array) > 0:
                #If the length of the forecast_array is more than 1, add it to the
                #response string
                response_string += '\n\n'.join(forecast_array)
            #Response string at this point has the title, the temp text with the
            #emojis.
            #Adding the below description draws from the response_dict above for a
            #complete weather description
            response_string += '\n\n' + description

        #例外処理
    except TypeError as e:
        response_string "すみません…地名をうまく読み取れませんでした…"
        print(e)
        print("Input Data Type is not a string. Please try again.")

    except EmptyError as e:
        response_string = "地名の指定がされていません…すみませんが、「天気　地名」再度入力してください。"
        print(e)
        print("Input Data is Empty. Please try again.")

     except OverLengthError as e:
        response_string = "すみません… 地名は5文字以内の全角日本語で入力してください。"
        print(e)
        print("Over 5 characters. Please try again.")

    except KeyError as e:
        response_string = "すみません… 地名が検索にヒットしませんでした…"
        print(e)
        print("Your Input couldn't discover. Please try another word again.")

    except Exception as e:
        response_string = "すみません… 何らかのエラーが発生しました"
        print(e)
        print("Unknown error.")

    return response_string
