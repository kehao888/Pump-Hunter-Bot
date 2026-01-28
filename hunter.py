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
    # 模拟请求包含详细指标的 API
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
    print("🔎 大师正在开启‘防收割’扫描模式...")
    tokens = fetch_live_signals()
    
    for token in tokens:
        # --- 大师级过滤标准 ---
        progress = token.get("progress", 0)
        dev_hold = token.get("dev_p", 100)  # 开发者持仓比例
        has_twitter = token.get("twitter_link", "") # 社交媒体
        smart_money_count = token.get("sw_count", 0) # 聪明钱人数

        # 1. 进度过滤：只看即将毕业的 (进度 > 85%)
        if progress < 85:
            continue
            
        # 2. 开发者持仓过滤：超过 10% 直接判定为‘收割盘’，剔除！
        if dev_hold > 10:
            print(f"⚠️ 剔除危险盘: {token['symbol']} (开发者持仓过高: {dev_hold}%)")
            continue
            
        # 3. 社交过滤：没有推特的项目大概率是‘三无产品’，剔除！
        if not has_twitter:
            print(f"⚠️ 剔除草台班子: {token['symbol']} (无社交媒体)")
            continue

        # 4. 聪明钱过滤：至少有 3 个聪明钱地址在里面才算‘有眼光’
        if smart_money_count < 3:
            continue

        # --- 通过所有过滤，正式报警 ---
        address = token["address"]
        gmgn_link = f"https://gmgn.ai/sol/token/{address}"
        
        alert_msg = (
            f"<b>🌟 发现【大师级】高胜率金狗！</b>\n\n"
            f"<b>代币：</b> ${token['symbol']}\n"
            f"<b>📈 进度：</b> <code>{progress}%</code>\n"
            f"<b>🛡️ 开发者：</b> 持仓 {dev_hold}% (安全)\n"
            f"<b>👥 聪明钱：</b> {smart_money_count} 位大牛已入场\n\n"
            f"👉 <a href='{gmgn_link}'>立即进入 GMGN 实时终端</a>\n\n"
            f"<i>大师提醒：该币种已通过防割扫描，符合‘低风险、高爆发’标准！</i>"
        )
        send_telegram(alert_msg)
        return # 每次只报一个最稳的，防止手机炸裂

if __name__ == "__main__":
    master_filter()
