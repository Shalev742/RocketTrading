import asyncio
import httpx
from datetime import datetime
from supabase import create_client
from groq import Groq

METAAPI_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJjYmQyZTAyYzFhMmU0MjkyOTVkZmIzOWE2ZTVlODA1MCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOjlmYTc0NjAxLTk0ZjAtNGNkZi1hMDczLTM2OGM3Y2IxNmQ0NiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6OWZhNzQ2MDEtOTRmMC00Y2RmLWEwNzMtMzY4YzdjYjE2ZDQ2Il19LHsiaWQiOiJtZXRhYXBpLXJwYy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDo5ZmE3NDYwMS05NGYwLTRjZGYtYTA3My0zNjhjN2NiMTZkNDYiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDo5ZmE3NDYwMS05NGYwLTRjZGYtYTA3My0zNjhjN2NiMTZkNDYiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6OWZhNzQ2MDEtOTRmMC00Y2RmLWEwNzMtMzY4YzdjYjE2ZDQ2Il19LHsiaWQiOiJyaXNrLW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJyaXNrLW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOjlmYTc0NjAxLTk0ZjAtNGNkZi1hMDczLTM2OGM3Y2IxNmQ0NiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiY2JkMmUwMmMxYTJlNDI5Mjk1ZGZiMzlhNmU1ZTgwNTAiLCJpYXQiOjE3NzMxNzI5MDF9.ZTVIJvvm_pSEShNi_zBfA6IT0kQFzZEDgDKu3XyCgbKyGGEa_lHrAVRRNVeni4LhP3NDC3nXdbWlaFYzIlNL9nIVKbn_KX2N63w_DS78sMqaWgXaZuMcujjBR4qGbX77ds6h9CFSzybH51c-wpqw37UuHfILj5wkdbJs89ZDGV0LpmkftTJW4M4PN_r6TiP9b6I_6bcFFqwIIchUozWay_yeGslRYUTge_prz_EcQbs97Gs-azsHB9nFlyxL1ABfcUwC2WVhoEIO_sSISlzs9KtkgKquPkHt6ZAmavEmWnSPoRwbw7GRcEPKEXMqk2PKdsAZVH-bs0AbRMG6GwKk5mh1LpokT9Er80TJVN5rKysCu8SvUbVCfmfCe-nzHzi6tPV3d22mt6PGaoDVaceS-5P3YZJbJdE8id7tKOstDqOu_sr9A8PI1aVYHOqqfDeXhDLhxMaWOczZrO9YAXJyIt1N9YiGXtrs1OJsrBGFkv5AcUzJ3VGNSWIMA-u9t-d0NDPbGbGRjTMarlm8qTC7bfEljtfqop1pACsYhbGY1HbeX7C9z5fRFT7ZcmRqLlp6_zMQxYWKG1MRf6E3A1YV3288pkJQlDm9wzhpyDa6LGz-aZx5aGJJfFsxTTnXsNxvF1ukeinG2x3rNgiUG2gyvP61Hg6VouokOv7R_9o5OdU"
METAAPI_ACCOUNT_ID = "9fa74601-94f0-4cdf-a073-368c7cb16d46"
SUPABASE_URL = "https://fibgicgcuirtuvnnisbc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpYmdpY2djdWlydHV2bm5pc2JjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMxNzI1NTIsImV4cCI6MjA4ODc0ODU1Mn0.5IhNawBBj17m2exMl0ywSRI9jcJNmCYrRmWp3J61cj0"
GROQ_API_KEY = "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"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

async def get_open_trades():
    url = f"https://mt-client-api-v1.london.agiliumtrade.ai/users/current/accounts/{METAAPI_ACCOUNT_ID}/positions"
    headers = {"auth-token": METAAPI_TOKEN}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return []

async def get_trade_history():
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    url = f"https://mt-client-api-v1.london.agiliumtrade.ai/users/current/accounts/{METAAPI_ACCOUNT_ID}/history-deals/time/2024-01-01T00:00:00.000Z/{now}"
    headers = {"auth-token": METAAPI_TOKEN}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return []

def group_trades(trades):
    closed = [t for t in trades if t.get("entryType") == "DEAL_ENTRY_OUT"]
    groups = {}
    for trade in closed:
        symbol = trade.get("symbol")
        close_price = trade.get("price")
        close_time = trade.get("time", "")
        if not symbol or not close_price:
            continue
        key = str(symbol) + "_" + str(round(float(close_price), 4)) + "_" + str(close_time)[:16]
        if key not in groups:
            groups[key] = []
        groups[key].append(trade)
    result = []
    for key, group in groups.items():
        total_profit = sum(t.get("profit", 0) or 0 for t in group)
        total_volume = sum(t.get("volume", 0) or 0 for t in group)
        first = group[0]
        result.append({
            "group_id": key,
            "symbol": first.get("symbol"),
            "type": first.get("type"),
            "open_time": first.get("time"),
            "close_time": first.get("time"),
            "close_price": first.get("price"),
            "total_volume": total_volume,
            "total_profit": total_profit,
            "trade_count": len(group)
        })
    return result

def save_grouped_trade(group):
    try:
        supabase.table("grouped_trades").upsert(group, on_conflict="group_id").execute()
        print("קבוצה נשמרה: " + str(group.get("symbol")) + " | " + str(group.get("trade_count")) + " עסקאות | רווח: " + str(round(group.get("total_profit", 0), 2)))
    except Exception as e:
        print("שגיאה: " + str(e))

def save_trade(trade, analysis=None):
    data = {
        "trade_id": trade.get("id"),
        "symbol": trade.get("symbol"),
        "type": trade.get("type"),
        "open_price": trade.get("price"),
        "volume": trade.get("volume"),
        "profit": trade.get("profit"),
        "open_time": trade.get("time"),
        "ai_analysis": analysis,
        "created_at": datetime.now().isoformat()
    }
    try:
        supabase.table("trades").upsert(data, on_conflict="trade_id").execute()
    except Exception as e:
        print("שגיאה: " + str(e))

def get_all_grouped_trades():
    try:
        result = supabase.table("grouped_trades").select("*").execute()
        return result.data
    except Exception as e:
        print("שגיאה: " + str(e))
        return []

def generate_weekly_insights(trades_data):
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": "נתח את נתוני המסחר ותן תובנות בעברית:\n" + trades_data}],
        max_tokens=800
    )
    return response.choices[0].message.content

def run_weekly_report():
    print("מייצר דוח שבועי...")
    trades = get_all_grouped_trades()
    if not trades:
        print("אין עסקאות עדיין")
        return
    total_profit = sum(t.get("total_profit", 0) or 0 for t in trades)
    summary = "סהכ עסקאות: " + str(len(trades)) + "\nסהכ רווח/הפסד: $" + str(round(total_profit, 2))
    insights = generate_weekly_insights(summary)
    print("תובנות:\n" + insights)

async def main():
    print("המערכת מתחילה...")
    open_trades = await get_open_trades()
    history = await get_trade_history()
    print("היסטוריה: " + str(len(history)) + " עסקאות גולמיות")
    if history:
    supabase.table("debug_log").insert({"data": str(history[0])}).execute()
    print("נשמרה דוגמא ל-Supabase")
    print("פתוחות: " + str(len(open_trades)))
    for trade in history:
        save_trade(trade)
    grouped = group_trades(history)
    print("קבוצות עסקאות: " + str(len(grouped)))
    for group in grouped:
        save_grouped_trade(group)
    run_weekly_report()
    print("סיום!")

asyncio.run(main())
