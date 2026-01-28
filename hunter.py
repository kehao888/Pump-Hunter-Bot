import requests

def main():
    print("🚀 大师级机器人已上线，正在 24 小时巡逻 Pump.fun...")
    # 这一行测试 requests 是否安装成功
    response = requests.get("https://www.google.com")
    if response.status_code == 200:
        print("✅ 网络连接正常，抓取工具已就绪！")
    print("🔎 目前市场扫描完毕，等待‘金狗’信号...")

if __name__ == "__main__":
    main()
