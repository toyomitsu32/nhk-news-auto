import os
import json
import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

# ===== Google Sheets 認証 =====
service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)

# ===== スプレッドシート設定 =====
SHEET_NAME = "スクレイピングテスト"
sheet = client.open(SHEET_NAME).sheet1

# ===== Yahooニュース取得 =====
URL = "https://news.yahoo.co.jp/"
res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")

titles = [a.get_text(strip=True) for a in soup.select("a.sc-esOvli")]
if not titles:
    titles = [a.get_text(strip=True) for a in soup.select("a.newsFeed_item_title")]

# ===== スプレッドシートに出力 =====
sheet.clear()
sheet.append_row(["Yahooニュース見出し"])
for t in titles[:10]:
    sheet.append_row([t])

print("✅ Yahooニュースの見出しをスプレッドシートに書き込みました！")

