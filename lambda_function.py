import json
import os
import livedoor_tenki
from urllib.request import urlopen, Request
from urllib.parse import parse_qs

def lambda_handler(event, context):
    print("event",event)
    token = os.environ['SLACK_TOKEN']
    query = parse_qs(event.get('body') or '')

    # エラー解析用にCloudWatchへログ出力
    print("query",query)

    if query.get('token', [''])[0] != token:
        # 予期しない呼び出し。400 Bad Requestを返す
        return { 'statusCode': 400,
            'body': json.dumps({
            'text': "400 Bad Request"
        })}

    slackbot_name = 'slackbot'

    if query.get('user_name', [slackbot_name])[0] == slackbot_name:
        # Botによる書き込み。無限ループを避けるために、何も書き込まない
        return { 'statusCode': 200 }

    # slackの投稿を slack_input_text へ格納
    slack_input_text = str(query['text'][0])

    m = str(slack_input_text.find('天気'))

    # slackの投稿に「天気」の文字列が入っている場合、livedoor天気情報
    if m != -1:
       msg = livedoor_tenki.getWeatherInformation(slack_input_text)

    response = {
        'statusCode': 200,
        'body': json.dumps({
            'text': msg
        })
    }

    print(response)
    return response
