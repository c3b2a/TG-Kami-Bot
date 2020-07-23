<h1>ReadMe</h1>

就一个 kami.py 别告诉我不会用

<h2>依赖</h2>

需要安装 telepot 和 watchdog

```bash
pip3 install telepot watchdog
```

<h2>更新频道</h2>

此项目将会持续更新

[Telegram 更新频道](https://t.me/kamibotchannel)

卡密 Bot Developed By [c3b2a](https://t.me/c3b2abot)

<h2>运行注意事项⚠️</h2>

第一次运行前请把 kami.py 中的 Token 替换为自己的 Bot 的 Token

第一次运行时，会自动创建 kamifile.txt admin.txt ban.txt searchLog.txt

<h2>数据存储格式</h2>

kamifile.txt:
存储卡密的文件，格式为:<br>
[卡密] [次数] [Tag] [备注]<br>
[卡密] [次数] [Tag] [备注]<br>
...<br>
备注中的换行以空格进行存储

admin.txt:
存储管理员的 Telegram ID，一行一个 ID，文件必须以换行结尾

ban.txt:
存储被封禁的账号的 ID，一行一个 ID，一样必须以换行结尾

searchLog.txt:
卡密搜索日志，格式为:<br>
[用户 ID] [时间戳] [卡密]<br>
[用户 ID] [时间戳] [卡密]<br>
...<br>

<h2>Webgui 使用</h2>
<h3>1、依赖</h3>

```bash
pip3 install django numpy
```

<h3>2、Token</h3>

Token.txt 储存格式:<br>
[Token] [类型]

类型分为: global-admin, privileged-admin, common-admin, readonly, writeonly

<h3>2、运行</h3>

运行前请先配置好 bot

```bash
python3 manage.py runserver 0.0.0.0:8000
```
