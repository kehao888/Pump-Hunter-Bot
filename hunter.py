import os
import requests

def send_telegram(message):
    # 从 GitHub 的保险柜里自动读取你刚存的 Token 和 ID
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("❌ 错误：未发现 Telegram 配置，请检查 Secrets！")
        return

    # Telegram 发送消息的标准 API 地址
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message,
        "parse_mode": "HTML" # 支持加粗等格式
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ 手机预警发送成功！")
        else:
            print(f"⚠️ 发送失败，返回状态：{response.status_code}")
    except Exception as e:
        print(f"❌ 网络请求异常: {e}")

def monitor_market():
    print("🚀 大师级云端指挥部已就绪，正在巡逻...")
    
    # 这里是我们要持续进化的核心筛选标准
    msg = (
        "<b>🔥 发现金狗预警！</b>\n\n"
        "<b>目标：</b> 模拟币种 (TEST_GOLDEN)\n"
        "<b>进度：</b> 95%\n"
        "<b>聪明钱：</b> 8人流入\n\n"
        "👉 <a href='https://gmgn.ai/pump'>点击前往 GMGN 确认</a>"
    )
    
    send_telegram(msg)

if __name__ == "__main__":
    monitor_market()
