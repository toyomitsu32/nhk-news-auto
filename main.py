import os
import json
import gspread
import feedparser
from google.oauth2.service_account import Credentials

# ===== Google Sheets 認証 =====
service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)

# ===== スプレッドシート設定 =====
SHEET_NAME = "スクレイピングテスト"
sheet = client.open(SHEET_NAME).sheet1

# ===== NHKニュースRSSを取得 =====
RSS_URL = "https://www3.nhk.or.jp/rss/news/cat0.xml"
feed = feedparser.parse(RSS_URL)

# ===== スプレッドシート書き込み =====
sheet.clear()
sheet.append_row(["タイトル", "リンク"])
for entry in feed.entries[:10]:
    sheet.append_row([entry.title, entry.link])

print(f"✅ {len(feed.entries[:10])} 件のニュースをスプレッドシートに出力しました！")

