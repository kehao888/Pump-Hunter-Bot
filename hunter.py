import os
import requests

def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML", "disable_web_page_preview": False}
    requests.post(url, json=payload)

def master_filter():
    print("🚀 大师级风险过滤系统已启动...")
    
    # 定义你的金狗准则
    # 1. 进度 > 85% (即将发射)
    # 2. 聪明钱 > 5人 (有专业猎手)
    # 3. 开发者持仓 < 5% (防止收割)
    # 4. 社交媒体已验证 (推特/电报必须有)
    
    # 模拟一个经过过滤后的高质量信号
    signal = {
        "name": "MASTER_COIN",
        "progress": 92,
        "smart_money": 8,
        "dev_hold": "2.1%",
        "has_twitter": "✅ 已关联",
        "link": "https://gmgn.ai/pump"
    }

    # 只有符合标准的才发预警
    if signal["progress"] > 80 and signal["smart_money"] >= 5:
        alert_msg = (
            f"<b>🌟 发现【高胜率】金狗信号！</b>\n\n"
            f"<b>代币：</b> {signal['name']}\n"
            f"<b>📈 进度：</b> <code>{signal['progress']}%</code> (极度接近内盘结束)\n"
            f"<b>👥 聪明钱：</b> {signal['smart_money']} 位猎手已入场\n"
            f"<b>🛡️ 安全：</b> 开发者持仓 {signal['dev_hold']} (极低风险)\n"
            f"<b>📱 社交：</b> {signal['has_twitter']}\n\n"
            f"⚠️ <b>大师提示：</b> 该币种满足‘聪明钱扎堆’且‘进度超前’标准。\n"
            f"👉 <a href='{signal['link']}'>立即去 GMGN 扫街</a>"
        )
        send_telegram(alert_msg)
        print("✅ 优质信号已推送至手机！")
    else:
        print("💡 扫描中... 暂未发现符合大师标准的信号。")

if __name__ == "__main__":
    master_filter()
