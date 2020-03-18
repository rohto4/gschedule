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

GCI = '285905973498-ga8hun0hne3ofqetubo4far44jood1nv.apps.googleusercontent.com'
GCS = 'uqGwJwlkYCkDEMjWTAOK5sgg'

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
            s = i.split(' ')
            if(len(s) == 1): continue

            # 開始日,終了日設定
            d_s = int(s[0])
            d_e = int(s[0])
            m_s = mon
            m_e = mon
            y_s = year
            y_e = year

            # 12月の処理
            if(mon == 12 and d_e == 31):
                y_e = year + 1

            if(num_days == d_e):
                d_e = 1
                if mon == 12: m_e = 1
                else: m_e = m_e + 1

            # 挿入データ設定
            event = {
                'summary': '{}'.format(s[1]),
                'location': 'aliesan\'s nest',
                'description': '{}'.format(s[1]),
                'start': {
                    'date': '{}-{}-{}'.format(y_s,m_s,d_s),
                    'timeZone': 'Japan',
                },
                'end': {
                    'date': '{}-{}-{}'.format(y_e,m_e,d_e),
                    'timeZone': 'Japan',
                },
            }
            print(event)

            # 挿入
            event = service.events().insert(calendarId='arai.rehabilitation@gmail.com', body=event).execute()
            print(event['id'])


if __name__ == '__main__':
  ScheduleTest.main()
