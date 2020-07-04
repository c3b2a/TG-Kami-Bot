就一个 kami.py 别告诉我不会用

需要安装 telepot 和 watchdog

pip3 install telepot watchdog

此项目会持续更新

[Telegram 更新频道](https://t.me/kamibotchannel)

卡密 Bot Developed By [c3b2a](https://t.me/c3b2abot)

第一次运行前请把 kami.py 中的 Token 替换为自己的 Bot 的 Token

第一次运行时，会自动创建 kamifile.txt admin.txt ban.txt searchLog.txt

kamifile.txt:
存储卡密的文件，格式为:
[卡密] [次数] [Tag] [备注]
[卡密] [次数] [Tag] [备注]
...
备注中的换行以空格进行存储

admin.txt:
存储管理员的 Telegram ID，一行一个 ID，文件必须以换行结尾

ban.txt:
存储被封禁的账号的 ID，一行一个 ID，一样必须以换行结尾

searchLog.txt:
卡密搜索日志，格式为:
[用户 ID] [时间戳] [卡密]
[用户 ID] [时间戳] [卡密]
...