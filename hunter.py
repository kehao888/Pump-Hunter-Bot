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
    # 模拟从 GMGN 获取带有流动性数据的实时榜单
    url = "https://gmgn.ai/api/v1/token_list/sol/pump?limit=10&orderby=progress&direction=desc"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data.get("code") == 0:
            return data["data"]["rank"]
    except:
        return []

def master_filter():
    print("🔎 大师正在开启‘极致过滤’扫描模式...")
    tokens = fetch_live_signals()
    
    for token in tokens:
        # --- 核心数据抓取 ---
        progress = token.get("progress", 0)
        dev_hold = token.get("dev_p", 100) # 开发者持仓
        liquidity = token.get("liquidity", 0) # 池子大小
        sw_count = token.get("sw_count", 0) # 聪明钱人数
        has_social = token.get("twitter_link") or token.get("telegram_link") # 社交媒体

        # --- 大师级过滤标准 ---
        # 1. 进度：必须 > 80%
        if progress < 80: continue
            
        # 2. 开发者持仓：严禁超过 10%
        if dev_hold > 10: continue
            
        # 3. 🛡️ 流动性过滤：池子必须大于 $3000，否则不报警
        # 这样可以确保你买入和卖出时不会产生巨大滑点
        if liquidity < 3000:
            print(f"⚠️ 跳过小池子盘: {token['symbol']} (当前流动性: ${liquidity})")
            continue
            
        # 4. 社交检查：必须有推特或电报
        if not has_social: continue

        # --- 触发高胜率报警 ---
        address = token["address"]
        gmgn_link = f"https://gmgn.ai/sol/token/{address}"
        
        alert_msg = (
            f"<b>💎 发现【高流动性】优质金狗！</b>\n\n"
            f"<b>代币：</b> ${token['symbol']}\n"
            f"<b>📈 进度：</b> <code>{progress}%</code>\n"
            f"<b>💧 池子：</b> <code>${liquidity}</code> (安全可交易)\n"
            f"<b>🛡️ 开发者：</b> 持仓 {dev_hold}% (安全)\n"
            f"<b>👥 聪明钱：</b> {sw_count} 位已入场\n\n"
            f"👉 <a href='{gmgn_link}'>立即进入 GMGN 实时终端</a>\n\n"
            f"<i>大师提醒：该币种池子健康，滑点较低，适合实战！</i>"
        )
        send_telegram(alert_msg)
        return # 专注一个信号，防止刷屏

if __name__ == "__main__":
    master_filter()
