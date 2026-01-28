name: Auto-Hunter-Clock

on:
  schedule:
    # 每 5 分钟自动运行一次
    - cron: '*/5 * * * *'
  workflow_dispatch:
    # 支持你随时手动点击按钮运行

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - name: 检查代码内容
        uses: actions/checkout@v2

      - name: 安装 Python 环境
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: 安装依赖插件 (修复报错的关键)
        run: pip install requests  #

      - name: 执行巡逻脚本
        run: python hunter.py
