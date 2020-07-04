import telepot,os,time,string,random,sys
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space,per_chat_id,create_open
from telepot.namedtuple import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler,FileSystemEventHandler

Token = ''

arr = ['' for i in range(10000)]
ps = ['' for i in range(10000)]
status = [0 for i in range(10000)]
tag = [[0] * 10 for i in range(10000)]
tagDepth = [0 for i in range(10000)]
realKamiCount = 0

admin = []

owner = ''

kamifn = "kamifile.txt"

banuser = ['' for i in range(10000)]
banusercount = 0

fileExist = os.path.exists(kamifn)

if fileExist:
    File = open(kamifn,"r+")
else:
    File = open(kamifn,"w+")

if not os.path.exists("ban.txt"):
    TmpNew = open('ban.txt','w')
    TmpNew.close()

if not os.path.exists("searchLog.txt"):
    TmpNew = open('searchLog.txt','w')
    TmpNew.close()

if not os.path.exists("admin.txt"):
    TmpNew = open('admin.txt','w')
    TmpNew.close()

BanFile = open('ban.txt','r+')

searchLog = open('searchLog.txt','r+')

AdminFile = open('admin.txt','r+')

def searchLogEnd():
    while(1):
        if not searchLog.readline():
            break

def loadfile():
    File.seek(0,0)
    global realKamiCount
    realKamiCount = 0
    ln = int(os.popen('wc -l ' + str(kamifn)).read().split()[0])
    print('File Lines Count : ' + str(ln))
    for i in range(ln):
        strlist = File.readline().split()
        arr[i] = strlist[0]
        status[i] = int(strlist[1])
        tagTmp = strlist[2].split(':')
        pstmp = strlist[3]
        tag[i] = tagTmp
        tagDepth[i] = len(tagTmp)
        for j in range(len(strlist) - 4):
            pstmp += ' ' + strlist[4 + j]
        ps[i] = pstmp
        realKamiCount += 1
        print(len(strlist),arr[i],status[i],tag[i],ps[i])
    print(realKamiCount)

def loadban():
    BanFile.seek(0,0)
    global banusercount
    banusercount = 0
    ln = int(os.popen('wc -l ban.txt').read().split()[0])
    print('Ban File Lines Count : ' + str(ln))
    for i in range(ln):
        string = BanFile.readline()
        banuser[i] = string
        print(banuser[i])
        banusercount += 1
    print('Ban User Count : ' + str(banusercount))

def loadadmin():
    global admin,owner
    del admin
    admin = []
    Count = 0
    AdminFile.seek(0,0)
    while True:
        string = AdminFile.readline()
        if not string:
            break
        elif len(string.split()) == 1:
            if Count == 0:
                admin.append(string.split()[0])
                owner = string.split()[0]
            else:
                admin.append(string.split()[0])
            print(Count,admin[Count])
            Count += 1

def chkbaned(chat_id):
    ret = False
    for i in range(banusercount):
        if int(chat_id) == int(banuser[i]):
            ret = True
            break
    return ret

def chkadmin(chat_id):
    ret = False
    for i in range(len(admin)):
        if str(chat_id) == admin[i]:
            ret = True
            break
    return ret

def searchkami(string,chat_id):
    ret = False
    for i in range(realKamiCount):
        if arr[i] == string and status[i] != 0:
            ret = True
            break
    return ret

def findindex(string):
    for i in range(realKamiCount):
        if arr[i] == string and status[i] != 0:
            return i

def addkami(getMsg,chat_id):
    statusTmp = int(getMsg[1])
    tagTmp = getMsg[2].split(':')
    print('addTag : ',end = '')
    print(tagTmp)
    psTmp = getMsg[3]
    for i in range(len(getMsg) - 4):
        psTmp += ' ' + getMsg[4 + i]
    print('ps : ' + psTmp)
    print('num : ' + str(statusTmp))
    if len(tagTmp) > 10:
        print('tag gt 10')
        bot.sendMessage(chat_id,'*Tag 必须小于等于 10 个*',parse_mode = 'Markdown')
        return 0
    else:
        print('tag le 10')
        mark_up = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = '是'),KeyboardButton(text = '否')]],one_time_keyboard = True,resize_keyboard = True)
        dpstr = 'Tag : `' + '`, `'.join(tagTmp) + '`\n' + '备注 : \n' + psTmp.replace(' ','\n') + '\n' + '次数 : ' + str(statusTmp) + '\n\n' + '确认是否添加'
        bot.sendMessage(chat_id,dpstr,reply_markup = mark_up,parse_mode = 'Markdown')
    return 1

def random_string(length):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits,length))
    return ran_str

def refresh_file():
    starttime = time.time()
    File.seek(0,0)
    File.truncate()
    for i in range(realKamiCount):
        File.write(arr[i] + ' ' + str(status[i]) + ' ' + ':'.join(tag[i]) + ' ' + ps[i] + '\n')
    File.flush()
    print('\n\nfile rewrote , time use ' + str(time.time() - starttime) + '\n\n')

class MultiProcess:
    def __init__(self):
        self._running = True
    def esc(self):
        self._running = False
    def run(self,chat_id):
        nowtime = time.time()
        while self._running:
            if(time.time() - nowtime) >= 30:
                print('timeout')
                bot.sendMessage(chat_id,'*时间到*',parse_mode = 'Markdown')
                break
            time.sleep(0.1)

class msgProcess(telepot.helper.ChatHandler):
    def __init__(self,*args,**kwargs):
        super(msgProcess,self).__init__(*args, **kwargs)
        self.indicator = None
        self.lastmsg = None
        self.authstr = None
        self.timeout = time.time()
        self.authstart = None
        self.multi = None
        self.difficulty = 0
        self.lastsearch = time.time()
        self.fscount = 0
        self.searchban = None
        self.usedkami = ['' for i in range(100)]
        self.usednum = 0
    def on_chat_message(self,msg):
        content_type,chat_type,chat_id = telepot.glance(msg)
        print(content_type,chat_type,chat_id)
        print(chkbaned(chat_id))
        if chkbaned(chat_id):
            bot.sendMessage(chat_id,'*您已被此 Bot 封禁*',parse_mode = 'Markdown')
            print('baned user')
        else:
            if self.difficulty > 9:
                self.difficulty = 9;
            if self.difficulty != 0 and (time.time() - self.lastsearch >= 3600):
                self.difficulty = 0
                print('difficulty reset')
            if self.indicator == 'searchauth' and (time.time()) - self.authstart >= 30:
                self.indicator = None
            if self.fscount >= 3:
                if not chkadmin(chat_id):
                    print('search auto ban')
                    bot.sendMessage(chat_id,'*您使用 /search 指令的频率过快，已自动封禁，若是误封，请联系* @kamibanshensu_bot',parse_mode = 'Markdown')
                    bot.sendMessage(owner,'自动封禁 ' + str(chat_id))
                    BanFile.write(str(chat_id) + '\n')
                    BanFile.seek(0,0)
                    loadban()
            if content_type == 'text':
                print('time : ' + str(time.time()))
                print(msg['text'])
                getMsg = msg['text'].split()
                lenOfMsg = len(getMsg)
                print(lenOfMsg)
                for i in range(lenOfMsg):
                    print(getMsg[i])
                if self.indicator != None:
                    if self.indicator == 'confirm':
                        if msg['text'] == '是':
                            global realKamiCount
                            self.indicator = None
                            print(self.lastmsg['text'])
                            info = self.lastmsg['text'].split()
                            statusTmp = int(info[1])
                            tagTmp = info[2].split(':')
                            psTmp = info[3]
                            for i in range(len(info) - 4):
                                psTmp += ' ' + info[4 + i]
                            status[realKamiCount] = statusTmp
                            arr[realKamiCount] = random_string(16)
                            tag[realKamiCount] = tagTmp
                            ps[realKamiCount] = psTmp
                            File.write(arr[realKamiCount] + ' ' + str(status[realKamiCount]) + ' ' + ':'.join(tag[realKamiCount]) + ' ' + ps[realKamiCount] + '\n')
                            File.flush()
                            print('卡密 : ' + arr[realKamiCount])
                            realKamiCount += 1
                            print('added successfully')
                            bot.sendMessage(chat_id,'成功添加',reply_markup = ReplyKeyboardRemove())
                        else:
                            self.indicator = None
                            print('cancel')
                            bot.sendMessage(chat_id,'取消添加',reply_markup = ReplyKeyboardRemove())
                    if self.indicator == 'bulk':
                        if msg['text'] == '是':
                            self.indicator = None
                            print(self.lastmsg['text'])
                            stringList = self.lastmsg['text'].split('\n')
                            for var in range(len(stringList) - 1):
                                index = var + 1
                                stringTmp = stringList[index].split()
                                statusTmp = int(stringTmp[0])
                                tagTmp = stringTmp[1].split(':')
                                psTmp = stringTmp[2]
                                for var2 in range(len(stringTmp) - 3):
                                    psTmp += ' ' + stringTmp[3 + var2]
                                status[realKamiCount] = statusTmp
                                arr[realKamiCount] = random_string(16)
                                tag[realKamiCount] = tagTmp
                                ps[realKamiCount] = psTmp
                                File.write(arr[realKamiCount] + ' ' + str(status[realKamiCount]) + ' ' + ':'.join(tag[realKamiCount]) + ' ' + ps[realKamiCount] + '\n')
                                print('卡密 : ' + arr[realKamiCount])
                                realKamiCount += 1
                            File.flush()
                            print('added successfully')
                            bot.sendMessage(chat_id,'成功添加',reply_markup = ReplyKeyboardRemove())
                        else:
                            self.indicator = None
                            print('cancel')
                            bot.sendMessage(chat_id,'取消添加',reply_markup = ReplyKeyboardRemove())
                    if self.indicator == 'searchauth':
                        if (time.time() - self.authstart) >= 30:
                            self.indicator = None
                        else:
                            self.multi.esc()
                            self.multi = None
                            self.indicator = None
                            if msg['text'] == self.authstr:
                                self.lastsearch = time.time()
                                self.difficulty += 1
                                print('search activate')
                                smsg = self.lastmsg.split()[1]
                                bot.sendMessage(chat_id,'验证成功')
                                searchLog.write(str(chat_id) + ' ' + str(time.time()) + ' ' + smsg + '\n')
                                searchLog.flush()
                                ans = searchkami(smsg,chat_id)
                                Used = False
                                for i in range(self.usednum):
                                    if self.usedkami[i] == smsg:
                                        Used = True
                                        break
                                print(ans)
                                if not ans:
                                    bot.sendMessage(chat_id,'*卡密不存在*',parse_mode = 'Markdown')
                                if ans:
                                    if not Used:
                                        self.usedkami[self.usednum] = smsg
                                        self.usednum += 1
                                        getIndex = findindex(smsg)
                                        tmpstr = ps[getIndex]
                                        status[getIndex] -= 1
                                        refresh_file()
                                        tmpstr = tmpstr.replace(' ','\n')
                                        dp = 'Tag : `' + '`, `'.join(tag[getIndex]) + '`\n\n' + '备注 : \n' + tmpstr
                                        print(dp.replace('备注','note').replace('\n\n','\n'))
                                        bot.sendMessage(chat_id,dp,parse_mode = 'Markdown')
                                    else:
                                        print('used')
                                        bot.sendMessage(chat_id,'*您已搜索过此卡密*',parse_mode = 'Markdown')
                            else:
                                print('auth failed')
                                bot.sendMessage(chat_id,'*验证失败*',parse_mode = 'Markdown')
                    if self.indicator == 'editconfirm':
                        self.indicator = None
                        if msg['text'] == '是':
                            msgSplit = self.lastmsg.split()
                            destKami = msgSplit[1]
                            statusTmp = msgSplit[2]
                            tagTmp = msgSplit[3].split(':')
                            psTmp = msgSplit[4]
                            for i in range(len(msgSplit) - 5):
                                psTmp += ' ' + msgSplit[5 + i]
                            print(destKami,statusTmp,tagTmp,psTmp)
                            Index = -1
                            for i in range(realKamiCount):
                                if destKami == arr[i]:
                                    Index = i
                                    break
                            status[Index] = int(statusTmp)
                            tag[Index] = tagTmp
                            ps[Index] = psTmp
                            refresh_file()
                            bot.sendMessage(chat_id,'成功更改',reply_markup = ReplyKeyboardRemove())
                        else:
                            print('cancel edit')
                            bot.sendMessage(chat_id,'取消更改',reply_markup = ReplyKeyboardRemove())
                    if self.indicator == 'rekamitag':
                        self.indicator = None
                        sendStr = '更新成功 : \n\n'
                        if msg['text'] == '是':
                            msgSplit = self.lastmsg.split(' ')
                            tagSplit = msgSplit[1].split(':')
                            for i in range(realKamiCount):
                                flag = True
                                for j in range(len(tagSplit)):
                                    if not tagSplit[j] in tag[i]:
                                        flag = False
                                        break
                                if flag:
                                    arr[i] = random_string(16)
                            refresh_file()
                            bot.sendMessage(chat_id,'更新成功',reply_markup = ReplyKeyboardRemove())
                        else:
                            print('cancel')
                            bot.sendMessage(chat_id,'操作已取消',reply_markup = ReplyKeyboardRemove())
                else:
                    if getMsg[0] == '/search':
                        if lenOfMsg == 2:
                            if self.searchban != None and (time.time() - self.searchban) >= 5:
                                self.searchban = time.time()
                                self.fscount = 0
                            if self.searchban == None:
                                self.searchban = time.time()
                            self.fscount += 1
                            print('auth activate')
                            basicString = random_string(24 + self.difficulty * 4)
                            symbol = ['!','@','#','$','%','^','&','*','(',')',',','.','<','>','-','=','+','_','[',']']
                            snum = random.randint(6,10) + self.difficulty * 2
                            for i in range(int(snum)):
                                basicString += symbol[random.randint(0,len(symbol) - 1)]
                            listStr = list(basicString)
                            random.shuffle(listStr)
                            dpString = '`' + ''.join(listStr) + '`'
                            bot.sendMessage(chat_id,'请将下列字符串中的特殊符号删去然后发送以完成验证（ 限时 30s ）')
                            print('difficulty : ',self.difficulty)
                            bot.sendMessage(chat_id,dpString,parse_mode = 'Markdown')
                            self.indicator = 'searchauth'
                            tmpFilter = filter(str.isalnum,dpString)
                            self.authstr = ''.join(list(tmpFilter))
                            self.authstart = time.time()
                            self.lastmsg = msg['text']
                            self.multi = MultiProcess()
                            t = Thread(target = self.multi.run,args = (chat_id,))
                            t.start()
                        else:
                            print('format err')
                            bot.sendMessage(chat_id,"*格式错误*",parse_mode = 'Markdown')
                    if getMsg[0] == '/amiadmin':
                        print('chkadmin activate')
                        ans = chkadmin(chat_id)
                        print(ans)
                        bot.sendMessage(chat_id,str(ans))
                    if getMsg[0] == '/add':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg < 4:
                            print('format err')
                            bot.sendMessage(chat_id,"*格式错误*",parse_mode = 'Markdown')
                        else:
                            print('add activate')
                            setornot = addkami(getMsg,chat_id)
                            if setornot:
                                self.indicator = 'confirm'
                                self.lastmsg = msg
                    if getMsg[0] == '/list':
                        print('list activate')
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg > 2:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            sendMsg = ''
                            if lenOfMsg == 1:
                                for i in range(realKamiCount):
                                    sendMsg += str(i + 1) + ':\n' + '卡密 : `' + arr[i] + '`\n' + 'Tag : `' + '`, `'.join(tag[i]) + '`\n' + '备注 : \n' + ps[i].replace(' ','\n') + '\n' + '次数 : ' + str(status[i]) + '\n\n'
                            else:
                                tagSplit = getMsg[1].split(':')
                                for i in range(realKamiCount):
                                    flag = True
                                    for j in range(len(tagSplit)):
                                        if not tagSplit[j] in tag[i]:
                                            flag = False
                                            break
                                    if flag:
                                        sendMsg += str(i + 1) + ':\n' + '卡密 : `' + arr[i] + '`\n' + 'Tag : `' + '`, `'.join(tag[i]) + '`\n' + '备注 : \n' + ps[i].replace(' ','\n') + '\n' + '次数 : ' + str(status[i]) + '\n\n'
                            if not sendMsg:
                                sendMsg = '无卡密'
                            bot.sendMessage(chat_id,sendMsg,parse_mode = 'Markdown')
                            print('list sent')
                    if getMsg[0] == '/ck':
                        print('keyboard removed')
                        bot.sendMessage(chat_id,'键盘已清除',reply_markup = ReplyKeyboardRemove())
                    if getMsg[0] == '/addbulk':
                        print('add in bulk activate')
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif len(msg['text'].split('\n')[0].split()) != 1:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            if len(msg['text'].split('\n')) < 2:
                                print('format err')
                                bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                            flag = True
                            for var in range(len(msg['text'].split('\n')) - 1):
                                if(len(msg['text'].split('\n')[1 + var].split()) < 3):
                                    print('format err')
                                    bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                                    flag = False
                                    break
                            if flag:
                                print('command verified')
                                stringList = msg['text'].split('\n')
                                print(stringList)
                                dpstr = ''
                                for var in range(len(stringList) - 1):
                                    index = var + 1
                                    stringTmp = stringList[index].split()
                                    print(str(index) + ' : ',end = '')
                                    print(stringTmp)
                                    statusTmp = stringTmp[0]
                                    tagTmp = stringTmp[1].split(':')
                                    psTmp = stringTmp[2]
                                    for var2 in range(len(stringTmp) - 3):
                                        psTmp += ' ' + stringTmp[3 + var2]
                                    dpstr += 'Tag : `' + '`, `'.join(tagTmp) + '`\n' + '备注 : \n' + psTmp.replace(' ','\n') + '\n次数 : ' + statusTmp + '\n\n'
                                self.indicator = 'bulk'
                                self.lastmsg = msg
                                dpstr += '\n\n\n确认添加吗？'
                                mark_up = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = '是'),KeyboardButton(text = '否')]],one_time_keyboard = True,resize_keyboard = True)
                                bot.sendMessage(chat_id,dpstr,reply_markup = mark_up,parse_mode = 'Markdown')
                    if getMsg[0] == '/ban':
                        if chkadmin(chat_id) or int(chat_id) == int(owner):
                            if(not chkadmin(getMsg[1])) or (int(chat_id) == int(owner)):
                                BanFile.write(getMsg[1] + '\n')
                                BanFile.seek(0,0)
                                loadban()
                            print('Ban ' + str(getMsg[1]))
                            bot.sendMessage(chat_id,'Ban ' + str(getMsg[1]))
                    if getMsg[0] == '/unban':
                        if chkadmin(chat_id) or int(chat_id) == int(owner):
                            BanFile.seek(0,0)
                            BanFile.truncate()
                            BanFile.flush()
                            for i in range(banusercount):
                                if(int(banuser[i]) != int(getMsg[1])):
                                    BanFile.write(str(banuser[i]))
                            BanFile.seek(0,0)
                            loadban()
                            print('Unban ' + str(getMsg[1]))
                            bot.sendMessage(chat_id,'Unban ' + str(getMsg[1]))
                    if getMsg[0] == '/difficulty':
                        print('difficulty : ' + str(self.difficulty))
                        bot.sendMessage(chat_id,'验证难度 : ' + str(self.difficulty))
                    if getMsg[0] == '/num':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg != 3:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            Kami = getMsg[1]
                            Count = getMsg[2]
                            Index = -1
                            for i in range(realKamiCount):
                                if Kami == arr[i]:
                                    Index = i
                                    break
                            if Index == -1:
                                print('not found')
                                bot.sendMessage(chat_id,'未找到此卡密')
                            else:
                                status[Index] = int(Count)
                                refresh_file()
                                bot.sendMessage(chat_id,'成功更新 : \n卡密 : `' + arr[Index] + '`\nTag : `' + '`, `'.join(tag[Index]) + '`\n备注 : \n' + ps[Index] + '\n次数 : ' + str(status[Index]),parse_mode = 'Markdown')
                    if getMsg[0] == '/numtag':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg != 3:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            tagTmp = getMsg[1].split(':')
                            numOfTag = len(tagTmp)
                            Count = getMsg[2]
                            dpLog = '已更新 : \n\n'
                            updateCount = 0
                            for i in range(realKamiCount):
                                iAvail = True
                                for j in range(numOfTag):
                                    if not (tagTmp[j] in tag[i]):
                                        iAvail = False
                                        break
                                if iAvail:
                                    updateCount += 1
                                    print('update ' + arr[i])
                                    status[i] = int(Count)
                                    dpLog += '卡密 : `' + arr[i] + '`\nTag : `' + '`, `'.join(tag[i]) + '`\n备注 : \n' + ps[i] + '\n次数 : ' + str(status[i]) + '\n\n'
                            if updateCount != 0:
                                dpLog += '\n共更新 ' + str(updateCount) + ' 个'
                                bot.sendMessage(chat_id,dpLog,parse_mode = 'Markdown')
                                refresh_file()
                            else:
                                bot.sendMessage(chat_id,'未更新')
                    if getMsg[0] == '/edit':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'您无权进行此操作')
                        elif lenOfMsg < 5:
                            print('format err')
                            bot.sendMessage(chat_id,'格式错误')
                        else:
                            Index = -1
                            for i in range(realKamiCount):
                                if getMsg[1] == arr[i]:
                                    Index = i
                                    break
                            if Index != -1:
                                self.indicator = 'editconfirm'
                                self.lastmsg = msg['text']
                                mark_up = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = '是'),KeyboardButton(text = '否')]],one_time_keyboard = True,resize_keyboard = True)
                                psTmp = getMsg[4]
                                for i in range(lenOfMsg - 5):
                                    psTmp += ' ' + getMsg[5 + i]
                                dpStr = '卡密 : `' + getMsg[1] + '`\nTag : `' + '`, `'.join(getMsg[3].split(':')) + '`\n备注 : \n' + psTmp.replace(' ','\n') + '\n次数 : ' + getMsg[2] + '\n\n确认更改吗？'
                                bot.sendMessage(chat_id,dpStr,reply_markup = mark_up,parse_mode = 'Markdown')
                            else:
                                print('kami not found')
                                bot.sendMessage(chat_id,'卡密未找到')
                    if getMsg[0] == '/help':
                        if int(chat_id) == int(owner):
                            helpMenu = '''
/ck - 清除键盘
用法 : /ck

/cl - 清除搜索限制
用法 : /cl

/difficulty - 查看当前验证难度
用法 : /difficulty

/sd - 设置验证难度
用法 : /sd [难度]

/add - 添加卡密 ( 卡密自动生成 )
用法 : /add [次数] [Tag] [备注]

/addbulk - 批量添加卡密
用法 : /addbulk
[次数] [Tag] [备注]
[次数] [Tag] [备注]
......

/delzero - 删除所有次数为 0 的卡密
用法 : /delzero

/edit - 编辑卡密
用法 : /edit [卡密] [次数] [Tag] [备注]

/rekami - 重新生成卡密
用法 : /rekami [原卡密]

/rekamitag - 按 Tag 重新生成卡密
用法 : /rekamitag [Tag]

/gen - 生成卡密
用法 : /gen

/setkami - 手动设置卡密
用法 : /setkami [原卡密] [新卡密]

/num - 编辑次数
用法 : /num [卡密] [次数]

/numtag - 编辑拥有此 Tag 的所有卡密的次数
用法 : /numtag [Tag] [次数]

/list - 列出所有卡密
用法 : /list [Tag](可选)

/search - 搜索卡密
用法 : /search [卡密]

/addadmin - 添加管理员
用法 : /addadmin [Telegram ID]

/deladmin - 删除管理员
用法 : /deladmin [Telegram ID]'''
                            bot.sendMessage(chat_id,helpMenu)
                        elif chkadmin(chat_id):
                            helpMenu = '''
/ck - 清除键盘
用法 : /ck

/cl - 清除搜索限制
用法 : /cl

/difficulty - 查看当前验证难度
用法 : /difficulty

/sd - 设置验证难度
用法 : /sd [难度]

/add - 添加卡密 ( 卡密自动生成 )
用法 : /add [次数] [Tag] [备注]

/addbulk - 批量添加卡密
用法 : /addbulk
[次数] [Tag] [备注]
[次数] [Tag] [备注]
......

/delzero - 删除所有次数为 0 的卡密
用法 : /delzero

/edit - 编辑卡密
用法 : /edit [卡密] [次数] [Tag] [备注]

/rekami - 重新生成卡密
用法 : /rekami [原卡密]

/rekamitag - 按 Tag 重新生成卡密
用法 : /rekamitag [Tag]

/gen - 生成卡密
用法 : /gen

/setkami - 手动设置卡密
用法 : /setkami [原卡密] [新卡密]

/num - 编辑次数
用法 : /num [卡密] [次数]

/numtag - 编辑拥有此 Tag 的所有卡密的次数
用法 : /numtag [Tag] [次数]

/list - 列出所有卡密
用法 : /list [Tag](可选)

/search - 搜索卡密
用法 : /search [卡密]'''
                            bot.sendMessage(chat_id,helpMenu)
                        else:
                            helpMenu = '''
/ck - 清除键盘

/difficulty - 查看当前验证难度

/search - 搜索卡密
用法 : /search [卡密]
'''
                            bot.sendMessage(chat_id,helpMenu)
                    if getMsg[0] == '/start':
                        bot.sendMessage(chat_id,'欢迎使用此 Bot\n发送 /help 以获得指令帮助\n\n注意！请勿高频发送 /search 指令，若发送频率过快，将会自动封禁\n若滥用 /search，发现直接永久封禁')
                    if getMsg[0] == '/delzero':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'您无权进行此操作')
                        else:
                            startTime = time.time()
                            File.seek(0,0)
                            File.truncate()
                            for i in range(realKamiCount):
                                if(status[i] != 0):
                                    File.write(arr[i] + ' ' + str(status[i]) + ' ' + ':'.join(tag[i]) + ' ' + ps[i] + '\n')
                            File.seek(0,0)
                            loadfile()
                            print('Time used : ' + str(time.time() - startTime))
                            bot.sendMessage(chat_id,'删除成功')
                    if getMsg[0] == '/rekami':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg != 2:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            Index = -1
                            for i in range(realKamiCount):
                                if getMsg[1] == arr[i]:
                                    Index = i
                                    break
                            if Index == -1:
                                print('not found')
                                bot.sendMessage(chat_id,'卡密未找到')
                            else:
                                tmpArr = arr[Index]
                                arr[Index] = random_string(16)
                                refresh_file()
                                bot.sendMessage(chat_id,'成功更新\n\n原卡密 : `' + tmpArr + '`\nTag : `' + '`, `'.join(tag[Index]) + '`\n备注 : \n' + ps[Index] + '\n次数 : ' + str(status[Index]) + '\n\n新卡密 : `' + arr[Index] + '`',parse_mode = 'Markdown')
                    if getMsg[0] == '/rekamitag':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg != 2:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            tagTmp = getMsg[1].split(':')
                            dpStr = ''
                            ans = 0
                            for i in range(realKamiCount):
                                flag = True
                                for j in range(len(tagTmp)):
                                    if not tagTmp[j] in tag[i]:
                                        flag = False
                                        break
                                if flag:
                                    dpStr += '卡密 : `' + arr[i] + '`\nTag : `' + '`, `'.join(tag[i]) + '`\n备注 : \n' + ps[i] + '\n次数 : ' + str(status[i]) + '\n\n'
                                    ans += 1
                            dpStr += '共需更新 ' + str(ans) + ' 个\n\n确认吗？'
                            mark_up = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = '是'),KeyboardButton(text = '否')]])
                            bot.sendMessage(chat_id,dpStr,reply_markup = mark_up,parse_mode = 'Markdown')
                            self.indicator = 'rekamitag'
                            self.lastmsg = msg['text']
                    if getMsg[0] == '/setkami':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg != 3:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            Index = -1
                            for i in range(realKamiCount):
                                if getMsg[1] == arr[i]:
                                    Index = i
                                    break
                            if Index == -1:
                                print('not found')
                                bot.sendMessage(chat_id,'未找到原卡密')
                            else:
                                sendStr = '原卡密 : `' + arr[Index] + '`\nTag : `' + '`, `'.join(tag[Index])  + '`\n备注 : \n' + ps[Index] + '\n次数 : ' + str(status[Index]) + '\n\n新卡密 : `' + getMsg[2] + '`'
                                arr[Index] = getMsg[2]
                                refresh_file()
                                bot.sendMessage(chat_id,sendStr,parse_mode = 'Markdown')
                    if getMsg[0] == '/gen':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        else:
                            bot.sendMessage(chat_id,'`' + random_string(16) + '`',parse_mode = 'Markdown')
                    if getMsg[0] == '/sd':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg != 2:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            self.difficulty = int(getMsg[1])
                            bot.sendMessage(chat_id,'操作成功')
                    if getMsg[0] == '/cl':
                        if not chkadmin(chat_id):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        else:
                            self.usednum = 0
                            bot.sendMessage(chat_id,'*操作成功*',parse_mode = 'Markdown')
                    if getMsg[0] == '/addadmin':
                        if int(chat_id) != int(owner):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg != 2:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            AdminFile.write(getMsg[1] + '\n')
                            AdminFile.flush()
                            loadadmin()
                            bot.sendMessage(chat_id,'操作成功')
                    if getMsg[0] == '/deladmin':
                        if int(chat_id) != int(owner):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        elif lenOfMsg != 2:
                            print('format err')
                            bot.sendMessage(chat_id,'*格式错误*',parse_mode = 'Markdown')
                        else:
                            AdminFile.seek(0,0)
                            AdminFile.truncate()
                            for i in admin:
                                if int(i) != int(getMsg[1]):
                                    AdminFile.write(i + '\n')
                            AdminFile.flush()
                            loadadmin()
                            bot.sendMessage(chat_id,'操作成功')
                    if getMsg[0] == '/lsadmin':
                        if int(chat_id) != int(owner):
                            print('no permission')
                            bot.sendMessage(chat_id,'*您无权进行此操作*',parse_mode = 'Markdown')
                        else:
                            dpStr = ''
                            for i in admin:
                                dpStr += i + '\n\n'
                            bot.sendMessage(chat_id,dpStr)
        print('')

class LoggingEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        pass

    def on_created(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        super(LoggingEventHandler, self).on_modified(event)
        what = 'directory' if event.is_directory else 'file'
        if what == 'file':
            print(time.asctime(time.localtime(time.time())),what,event.src_path)
            print(len(event.src_path))
            if event.src_path == './ban.txt':
                loadban()
            elif event.src_path == './admin.txt':
                loadadmin()
            elif event.src_path == './kamifile.txt':
                loadfile()

searchLogEnd()
loadfile()
loadban()
loadadmin()

print(admin,owner)

print('\n')

bot = telepot.DelegatorBot(Token,[pave_event_space()(per_chat_id(),create_open,msgProcess,timeout = 86400),])

MessageLoop(bot).run_as_thread()

path = sys.argv[1] if len(sys.argv) > 1 else '.'
event_handler = LoggingEventHandler()
observer = Observer()
observer.schedule(event_handler,path,recursive = True)
observer.start()

while(1):
    time.sleep(0.01)
