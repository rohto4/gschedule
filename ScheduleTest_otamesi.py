# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime, pickle, os.path, sys, json
from requests_oauthlib import OAuth1Session
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date

# user define class
#@UnresolvedImport
from util.JsonUtil import readJsonData, writeBreakStatus, writeJsonData, addJsonData



# 初期設定
search_url = 'https://api.twitter.com/1.1/search/tweets.json'# 検索用URL設定
SCOPE = ['https://www.googleapis.com/auth/calendar'] # GoogleCalendar
CHECK_SCOPE = ['https://www.googleapis.com/auth/calendar.events.readonly'] # 重複Check用GoogleCalendar
EVENTS_SCOPE = ['https://www.googleapis.com/calendar/v3/calendars/calendarId/events']
TCK = TCS = TAK = TAS = None

class ScheduleTest:

    # 読み取り
    def readTextSchedule():
        f = open('schedule.txt', encoding='utf-8')
        data1 = f.read()
        return lines1

    # twitterセッション取得
    def createSession():
        f = open('../auth/twitter', encoding='utf-8')
        data = f.read()
        keys = data.split('\n')
        TCK = keys[0].split(' ')[0]
        TCS = keys[1].split(' ')[0]
        TAK = keys[2].split(' ')[0]
        TAS = keys[3].split(' ')[0]
        f.close()
        session = OAuth1Session(TCK, TCS, TAK, TAS)
        # session = OAuth1Session(os.environ['CONSUMER_KEY'],os.environ['CONSUMER_SECRET'],\
        #                         os.environ['ACCESS_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
        return session

    # tweetから読み込み
    def readTweetSchedule(session):
        # search param setting
        q = 'arai_rehabili "2020.04g"'
        params = {
            'q':q,
            'lang':'ja',
            'result_type':'recent',
            'count':100
            }
        # check
        # print(params)

        # 検索実施
        res = session.get(search_url, params = params)
        # check
        # print(res_text)
        res_text = json.loads(res.text)

        if res.headers['X-Rate-Limit-Remaining'] is not None:
            print ('アクセス可能回数 %s' % res.headers['X-Rate-Limit-Remaining'])
            print ('リセット時間 %s' % res.headers['X-Rate-Limit-Reset'])
        else:
            print('ヘッダが正常に取得できませんでした')

        # output check
        now = datetime.datetime.now()
        str_now = now.strftime('%Y%m%d_%H%M%S')

        # check json
        # writeJsonData('log/tweet_' + str_now + '.json', res_text['statuses'])

        # check
        for tweet_data in res_text['statuses']:
            print(tweet_data['user']['name'])
            print(tweet_data['created_at'])
            print(tweet_data['text'])
            print("-----")

        # 対象のツイート群を返す
        result_text = []
        for tweet_data in res_text['statuses']:
            result_text.append(tweet_data['text'])

        # check
        print(result_text)
        return result_text

    # credentials.json または token.pickle を使用し、
    # GoogleCalendar を取得する
    def readWriteCalendar():
        '''
        /弄らない
        '''
        creds = None
        # token.pickle ファイルは認証フローの初回完了時に作成される
        # access token & refresh tokemnを保持する
        if os.path.exists('../auth/token.pickle'):
            with open('../auth/token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # 有効な資格情報の読込、確認、取得、ログイン
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../auth/credentials.json', SCOPE)
                creds = flow.run_local_server(port=0)

            # 次回実行のため、資格情報保存
            with open('../auth/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # 対象のカレンダーを取得
        return build('calendar', 'v3', credentials=creds)


    def readCalendarEvents():
        '''
        ----------
        '''
        creds = None
        # token.pickle ファイルは認証フローの初回完了時に作成される
        # access token & refresh tokemnを保持する
        if os.path.exists('../auth/token.pickle'):
            with open('../auth/token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # 有効な資格情報の読込、確認、取得、ログイン
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../auth/credentials.json', SCOPE)
                creds = flow.run_local_server(port=0)

            # 次回実行のため、資格情報保存
            with open('../auth/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        calendar = build('calendar', 'v3', credentials=creds)
        '''
        ----------
        '''

        events_result = calendar.events().list(calendarId='arai.rehabilitation@gmail.com',
                                  maxResults=10).execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        # 4/22 これのテストまで完了
        # 本ファイルに移し、token取得部を共通関数にする

    # 対象日付のタイトルが挿入済みであれば
    # is_insert = False を返却
    def checkOverlapSchedule(calendar, event):
        if True :
            return False
        # else :
        #     return True

    def main():
        ScheduleTest.readCalendarEvents()
        exit()
        # credentials.json または token.pickle を使用し、
        # GoogleCalendar を取得する
        calendar = ScheduleTest.readWriteCalendar()

        # 引数に応じて読み込み先を変える
        read_data = None
        if len(sys.argv) == 2 and sys.argv[1] == "t" :
            # tweet
            session = ScheduleTest.createSession()
            read_data = ScheduleTest.readTweetSchedule(session)
        else:
            # txtfile
            read_data = ScheduleTest.readTextSchedule()

        ### 挿入用テキスト処理 ###

        # データ分繰り返す
        for data in read_data:
            # 日付取り出し
            # check
            # print(data)

            data_lines = data.split('\n')
            yearmon = data_lines[0]
            tmp_ym = yearmon.split(".")
            # check
            # print(tmp_ym)

            year = int(tmp_ym[0])
            mon = int(tmp_ym[1][:2])
            # check
            print(str(year))
            print(str(mon))

            # チェック用比較用カレンダー設定
            if mon == 1 or mon == 3 or mon == 5 or mon == 7 or mon == 8 or mon == 10 or mon == 12:
                num_days = 31
            elif mon == 2:
                num_days = 28
            else :
                num_days = 30
            print("data")
            print(data)

            # 内容部
            for txt in data_lines:
                # check
                print("txt")
                print(txt)
                # 一行を日付_時間_内容に分割
                line_txt = txt.split(' ')
                # 改行のみの行をスキップ（一行目）
                if(len(line_txt) == 1): continue
                # コメント行をスキップ
                if("#" is line_txt[0]): continue

                # start date, end date設定
                year_s = year_e = year
                mon_s = mon_e = mon
                print(line_txt)
                day_s = day_e = int(line_txt[0])

                # 変動する挿入テキストの設定
                # Hour Minutu
                # [day text]
                if(len(line_txt) == 2):
                    ins = {'hour_s': 0, 'min_s': 0, 'hour_e': 0, 'min_e': 0}
                    txt_i = 1
                # [day time text]
                elif(len(line_txt[1]) == 4):
                    ins = {'hour_s': int(line_txt[1][0:2]), 'min_s': int(line_txt[1][2:4]),
                           'hour_e': int(line_txt[1][0:2]), 'min_e': int(line_txt[1][2:4])}
                    txt_i = 2
                # [day time-time text]
                elif(len(line_txt[1]) == 9):
                    ins = {'hour_s': int(line_txt[1][0:2]), 'min_s': int(line_txt[1][2:4]),
                           'hour_e': int(line_txt[1][5:7]), 'min_e': int(line_txt[1][7:9])}
                    txt_i = 2
                ins['txt'] = line_txt[txt_i]
                # check
                # print(ins)

                # 12月の処理
                if(mon == 12 and day_e == 31):
                    year_e = year + 1

                if(num_days == day_e):
                    day_e = 1
                    if mon == 12: mon_e = 1
                    else: mon_e = mon_e + 1

                ins_dateTime_s = '{0}-{1:02}-{2}T{3:02}:{4:02}:{5:02}'.format(year_s, mon_s, day_s, ins.get('hour_s'), ins.get('min_s'), 0)
                ins_datetime_e = '{0}-{1:02}-{2}T{3:02}:{4:02}:{5:02}'.format(year_e, mon_e, day_e, ins.get('hour_e'), ins.get('min_e'), 0)

                # 挿入データ設定
                event = {
                    'summary': '{}'.format(ins.get('txt')),
                    'location': 'aliesan\'s nest',
                    'description': '',
                    'start': {
                        'dateTime': ins_datetime_s,
                        'timeZone': 'Japan',
                    },
                    'end': {
                        'dateTime': ins_datetime_e,
                        'timeZone': 'Japan',
                    },
                }
                # check
                # print(event)

                # 挿入データの重複チェック
                is_insert = ScheduleTest.checkOverlap(calendar, event)
                # 重複が無ければ挿入
                if is_insert :
                    # 挿入
                    event = calendar.events().insert(calendarId='arai.rehabilitation@gmail.com', body=event).execute()

                # 挿入値をクリア
                ins.clear()
            # /内容部



if __name__ == '__main__':
  ScheduleTest.main()
