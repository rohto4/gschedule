# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import pickle
import os.path
from requests_oauthlib import OAuth1Session
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# 初期設定
search_url = 'https://api.twitter.com/1.1/search/tweets.json'# 検索用URL設定

TCK = 'o46La2iGb7bIn41XyXqHyYw8A'                             # Consumer Key
TCS = 'eTeaiw1nJ71KNgH2AwU6cQkgbByk6ZLfi58FEel6ENrsNAm5gR'    # Consumer Secret
TAT = '773885677507321856-bypmqmScqUcCPAuEQRuhRDllEqtXXeT'    # Access Token
TAS = 'pGq6OYipTDRzRtv8QXI0cdCZ2yWkXIYNLvv91fh8Cob61'         # Accesss Token Secert

# googleCalendar
SCOPE = ['https://www.googleapis.com/auth/calendar']

class ScheduleTest:

    # 読み取り
    def readschedule():
        f = open('schedule.txt')
        data1 = f.read()
        lines1 = data1.split('\n')
        f.close()
        return lines1

    def main():
        creds = None

        # token.pickle ファイルは
        # 認証フローの初回完了時に作成される
        # access token & refresh tokemnを保持する
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # 有効な資格情報が無い場合、ログインする
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPE)
                creds = flow.run_local_server(port=0)

            # 次回実行のため、資格情報保存
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # 対象のカレンダーを取得
        service = build('calendar', 'v3', credentials=creds)

        # ??
        ScheduleTest.readschedule()
        print(ScheduleTest.readschedule())

        ### テキスト処理 ###

        # 日付取り出し
        yearmon = ScheduleTest.readschedule()[0]
        tmp = yearmon.split(".")
        year = int(tmp[0])
        mon = int(tmp[1])

        # チェック用比較用カレンダー設定
        if mon == 1 or mon == 3 or mon == 5 or mon == 7 or mon == 8 or mon == 10 or mon == 12:
            num_days = 31
        elif mon == 2:
            num_days = 28
        else :
            num_days = 30

        # 内容部
        for i in ScheduleTest.readschedule():
            txtl = i.split(' ')

            # 内容の無い行をスキップ
            if(len(txtl) == 1): continue

            # 開始日時,終了日時設定
            year_s = year
            year_e = year
            mon_s = mon
            mon_e = mon
            day_s = int(txtl[0])
            day_e = int(txtl[0])

            # [day text]
            if(len(txtl) == 2):
                hour_s = 0
                min_s = 0
                hour_e = 0
                min_e = 0
                txt_i = 1

            # [day time text]
            elif(len(txtl[1]) == 4):
                hour_s = int(txtl[1][0:2])
                hour_e = int(txtl[1][0:2])
                min_s = int(txtl[1][2:4])
                min_e = int(txtl[1][2:4])
                txt_i = 2

            # [day time-time text]
            elif(len(txtl[1]) == 9):
                hour_s = int(txtl[1][0:2])
                min_s = int(txtl[1][2:4])
                hour_e = int(txtl[1][5:7])
                min_e = int(txtl[1][7:9])
                txt_i = 2

            print("hour_s : " + str(hour_s))
            print("min_s : " + str(min_s))
            # 12月の処理
            if(mon == 12 and day_e == 31):
                year_e = year + 1

            if(num_days == day_e):
                day_e = 1
                if mon == 12: mon_e = 1
                else: mon_e = mon_e + 1

            # 挿入データ設定
            event = {
                'summary': '{}'.format(txtl[txt_i]),
                'location': 'aliesan\'s nest',
                'description': '{}'.format(txtl[txt_i]),
                'start': {
                    'dateTime': '{0}-{1:02}-{2}T{3:02}:{4:02}:{5:02}'.format(year_s, mon_s, day_s, hour_s, min_s, 0),
                    'timeZone': 'Japan',
                },
                'end': {
                    'dateTime': '{0}-{1:02}-{2}T{3:02}:{4:02}:{5:02}'.format(year_e, mon_e, day_e, hour_e, min_e, 0),
                    'timeZone': 'Japan',
                },
            }
            print(event)

            # 挿入
            event = service.events().insert(calendarId='arai.rehabilitation@gmail.com', body=event).execute()
            print(event['id'])


if __name__ == '__main__':
  ScheduleTest.main()