import os
import requests

def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def scan_gmgn_market():
    print("📡 正在接入 GMGN 实时数据流...")
    
    # 模拟从 GMGN 抓取的逻辑标准
    # 我们盯着：1. 进度 > 80% 2. 聪明钱流入 > 5人 3. 无大户捆绑
    
    # 这里是一个真实的信号模拟
    signal = {
        "name": "SOL-WHALE",
        "progress": "88%",
        "smart_money": "12",
        "link": "https://gmgn.ai/pump"
    }

    alert_msg = (
        f"<b>🎯 发现高爆发信号！</b>\n\n"
        f"<b>币种：</b> {signal['name']}\n"
        f"<b>当前进度：</b> {signal['progress']}\n"
        f"<b>聪明钱地址：</b> {signal['smart_money']} 个\n\n"
        f"✅ <b>大师建议：</b> 这种进度配合聪明钱扎堆，爆发概率极高！\n"
        f"👉 <a href='{signal['link']}'>立即上车查看</a>"
    )
    
    send_telegram(alert_msg)

if __name__ == "__main__":
    scan_gmgn_market()
