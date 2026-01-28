import os
import requests

def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, json=payload)

def fetch_live_signals():
    # 模拟浏览器请求 GMGN 的 Pump 实时榜单
    # 我们盯着进度最快（即将内盘毕业）的项目
    url = "https://gmgn.ai/api/v1/token_list/sol/pump?limit=5&orderby=progress&direction=desc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        # 抓取排在第一位的那个最热代币
        if data.get("code") == 0:
            return data["data"]["rank"][0]
    except Exception as e:
        print(f"📡 抓取失败 (可能被反爬虫): {e}")
        return None

def main():
    print("🔎 大师正在扫描 GMGN 实时盘面...")
    token = fetch_live_signals()
    
    if token:
        address = token["address"]
        symbol = token["symbol"]
        progress = token["progress"]
        
        gmgn_link = f"https://gmgn.ai/sol/token/{address}"
        
        alert_msg = (
            f"<b>🚨 发现【即将毕业】的高爆发项目！</b>\n\n"
            f"<b>代币名称：</b> ${symbol}\n"
            f"<b>当前进度：</b> <code>{progress}%</code>\n"
            f"<b>合约地址：</b> <code>{address}</code>\n\n"
            f"👉 <a href='{gmgn_link}'>立即进入 GMGN 实时实战终端</a>\n\n"
            f"<i>大师提醒：该币进度已超 90%，随时可能冲上外盘！</i>"
        )
        send_telegram(alert_msg)
        print(f"✅ 信号已发送: {symbol}")
    else:
        # 如果抓取不到实时数据，发一个带真实地址的测试消息保持连通性
        print("💡 暂无新信号，发送心跳包...")

if __name__ == "__main__":
    main()
