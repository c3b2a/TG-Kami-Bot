from django.http import HttpResponse,FileResponse
from django.shortcuts import render,HttpResponseRedirect
from django.views.decorators import csrf
from django.contrib import messages
from threading import Thread
from pprint import pprint
import re,time,string,random,os,csv,xlwt
import numpy as np
import pandas as pd

from .__init__ import tokenData,util,random_string

def panel(request):
	tokenCookie = request.COOKIES.get('token')
	if (not tokenCookie) or (not tokenData().chkToken(tokenCookie)):
		return HttpResponseRedirect('/login')
	timeoutFlag,timeoutResponse = tokenData().cookieTimeout(request)
	if timeoutFlag:
		return timeoutResponse
	panelIndexRegExp = r'^/panel/?$'
	panelAdminRegExp = r'^/panel/admin/?$'
	panelBanRegExp   = r'^/panel/ban/?$'
	panelKamiRegExp  = r'^/panel/kami/?$'
	panelLogRegExp   = r'^/panel/log/?$'
	urlPath = request.path
	if re.match(panelIndexRegExp,urlPath):
		return render(request,'panel.html')
	elif re.match(panelAdminRegExp,urlPath):
		return adminManager(request,tokenCookie)
	elif re.match(panelBanRegExp,urlPath):
		return banManager(request,tokenCookie)
	elif re.match(panelKamiRegExp,urlPath):
		return kamiManager(request,tokenCookie)
	elif re.match(panelLogRegExp,urlPath):
		return logReader(request,tokenCookie)
	else:
		return render(request,'404.html')

def adminManager(request,tokenCookie):
	if tokenData().identityAuth(tokenData().getIdentity(tokenCookie),(0,1)):
		send_dict = {
			'showWebguiTable': True,
			'webguiList': tokenData().convertDict(),
			'showBotTable': True,
			'botAdminList': tokenData().getBotAdmin(),
			'Token': request.COOKIES.get('token'),
			'webguiAdminEditable': True if len(tokenData().convertDict()) > 1 else False,
			'botAdminEditable': True if len(tokenData().getBotAdmin()) > 1 else False,
		}
		if request.method == 'GET':
			return render(request,'admin.html',send_dict)
		elif request.method == 'POST':
			if ('webguiaddadmin' in request.POST) and ('webguiadminidentity' in request.POST):
				adminToken = request.POST['webguiaddadmin']
				adminIdentity = request.POST['webguiadminidentity']
				if adminToken and adminIdentity:
					if tokenData().identityAuth(adminIdentity,(0,1,2,3,4)):
						if not tokenData().chkToken(adminToken):
							tokenData().webguiWriteDetail(adminToken,adminIdentity)
							messages.success(request,'操作成功')
							return HttpResponseRedirect('/panel/admin')
						else:
							return render(request,'admin.html',{**{'webgui': 'Token重复'},**send_dict})
					else:
						return render(request,'admin.html',{**{'webgui': '输入类型不正确'},**send_dict})
				else:
					return render(request,'admin.html',{**{'webgui': 'Token为空'},**send_dict})
			elif 'botaddadmin' in request.POST:
				if request.POST['botaddadmin']:
					filterNum = ''.join(list(filter(str.isdigit,request.POST['botaddadmin'])))
					if not util.isAllDigit(request.POST['botaddadmin']):
						return render(request,'admin.html',{**{'bot': 'ID 只允许数字'},**send_dict})
					if tokenData().chkIDRepeat(filterNum):
						return render(request,'admin.html',{**{'bot': 'ID 重复'},**send_dict})
					tokenData().botWriteID(request.POST['botaddadmin'])
					messages.success(request,'操作成功')
					return HttpResponseRedirect('/panel/admin')
				else:
					return render(request,'admin.html',{**{'bot': 'ID 未输入'},**send_dict})
			elif 'webguidelete' in request.POST:
				tokenData().delWebguiAdmin(request.POST['editTokenSelect'])
				messages.success(request,'操作成功')
				return HttpResponseRedirect('/panel/admin')
			elif 'webguieditconfirm' in request.POST:
				if request.POST['ntoken']:
					tokenData().editWebguiAdmin(request.POST['editTokenSelect'],request.POST['ntoken'],request.POST['ntype'])
					messages.success(request,'操作成功')
					return HttpResponseRedirect('/panel/admin')
				else:
					return render(request,'admin.html',{**{'editwebguierr': '新 Token 为空'},**send_dict})
			elif 'botadmindelete' in request.POST:
				tokenData().delBotAdmin(request.POST['editBotAdminSelect'])
				messages.success(request,'操作成功')
				return HttpResponseRedirect('/panel/admin')
			elif 'botadmineditconfirm' in request.POST:
				if util.isAllDigit(request.POST['newtgid']):
					tokenData().editBotAdmin(request.POST['editBotAdminSelect'],request.POST['newtgid'])
					messages.success(request,'操作成功')
					return HttpResponseRedirect('/panel/admin')
				else:
					return render(request,'admin.html',{**{'editboterr': '只允许数字'},**send_dict})
			else:
				return render(request,'admin.html',{**{'head_notice': '未知错误'},**send_dict})
	else:
		return render(request,'denied.html')

def banManager(request,token):
	if tokenData().identityAuth(tokenData().getIdentity(token),(0,1,2)):
		send_dict = {
			'banList': util.getBan(),
			'adminList': util.getAdmin(),
			'identityList': tokenData().getBotAdmin(),
			'loginIdentity': tokenData().getIdentity(token),
		}
		if request.method == 'GET':
			return render(request,'ban.html',send_dict)
		elif request.method == 'POST':
			post_content = request.POST;
			if 'delselect' in post_content:
				delList = [False for i in range(len(send_dict['banList']))]
				delCount = 0
				for i in range(len(send_dict['banList'])):
					if send_dict['banList'][i] in post_content:
						delList[i] = True
						delCount += 1
				if delCount != 0:
					util.delBan(delList)
					messages.success(request,'操作成功')
					return HttpResponseRedirect('/panel/ban')
				else:
					return render(request,'ban.html',send_dict)
			elif 'submitAdd' in post_content:
				if post_content['addBanId']:
					if util.isAllDigit(post_content['addBanId']):
						if tokenData().getIdentity(token) == 'common-admin' and post_content['addBanId'] in util.getAdmin():
							return HttpResponseRedirect('/panel/ban')
						elif tokenData().getIdentity(token) == 'privileged-admin' and post_content['addBanId'] in util.getAdmin() and tokenData().getBotAdmin()[post_content['addBanId']] == 'super-admin':
							return HttpResponseRedirect('/panel/ban')
						util.addBan(post_content['addBanId'])
						messages.success(request,'操作成功')
						return HttpResponseRedirect('/panel/ban')
					return HttpResponseRedirect('/panel/ban')
			return render(request,'ban.html',send_dict)
		else:
			return HttpResponseRedirect('/panel')
	else:
		return render(request,'denied.html')

def kamiManager(request,token):
	if not tokenData().identityAuth(tokenData().getIdentity(token),(1,)):
		send_dict = {
			'loginIdentity': tokenData().getIdentity(token),
			'loginToken': token,
			'kamiList': util.getKami(),
		}
		if request.method == 'GET':
			return render(request,'kami.html',send_dict)
		elif request.method == 'POST':
			post_content = request.POST
			if 'deletekami' in post_content:
				if tokenData().identityAuth(tokenData().getIdentity(token),(0,2)):
					delList = [False for i in range(len(util.getKami()))]
					delCount = 0
					for i in range(len(util.getKami())):
						if ('checkbox' + str(i)) in post_content:
							delList[i] = True
							delCount += 1
					if delCount != 0:
						util.delKami(delList)
						messages.success(request,'操作成功')
						return HttpResponseRedirect('/panel/kami')
					else:
						return HttpResponseRedirect('/panel/kami')
				else:
					messages.info(request,'🐂🍺 ! 还会改 post 请求')
					return HttpResponseRedirect('/panel/kami')
			elif 'resetkami' in post_content:
				if tokenData().identityAuth(tokenData().getIdentity(token),(0,2)):
					resetList = [False for i in range(len(util.getKami()))]
					resetCount = 0
					for i in range(len(util.getKami())):
						if ('checkbox' + str(i)) in post_content:
							resetList[i] = True
							resetCount += 1
					if resetCount != 0:
						util.resetKami(resetList)
						messages.success(request,'操作成功')
						return HttpResponseRedirect('/panel/kami')
					else:
						return HttpResponseRedirect('/panel/kami')
				else:
					messages.info(request,'🐂🍺 ! 还会改 post 请求')
					return HttpResponseRedirect('/panel/kami')
			elif 'setkami' in post_content:
				if tokenData().identityAuth(tokenData().getIdentity(token),(0,2)):
					if post_content['nkamiinput'] and util.isLetterOrDigit(post_content['nkamiinput']):
						index = -1;
						counts = 0
						for i in range(len(util.getKami())):
							if ('checkbox' + str(i)) in post_content:
								index = i
								counts += 1
						if index != -1 and counts == 1:
							if util.setKami(index,post_content['nkamiinput']):
								messages.success(request,'操作成功')
							else:
								messages.error(request,'卡密重复')
							return HttpResponseRedirect('/panel/kami')
						else:
							return HttpResponseRedirect('/panel/kami')
					else:
						return HttpResponseRedirect('/panel/kami')
				else:
					messages.info(request,'🐂🍺 ! 还会改 post 请求')
					return HttpResponseRedirect('/panel/kami')
			elif 'setnum' in post_content:
				if tokenData().identityAuth(tokenData().getIdentity(token),(0,2)):
					if post_content['nkaminum'] and util.isAllDigit(post_content['nkaminum']):
						counts = 0
						changeList = [False for i in range(len(util.getKami()))]
						for i in range(len(util.getKami())):
							if ('checkbox' + str(i)) in post_content:
								changeList[i] = True
								counts += 1
						if counts != 0:
							util.setNum(changeList,int(post_content['nkaminum']))
							messages.success(request,'操作成功')
							return HttpResponseRedirect('/panel/kami')
						else:
							return HttpResponseRedirect('/panel/kami')
					else:
						return HttpResponseRedirect('/panel/kami')
				else:
					messages.info(request,'🐂🍺 ! 还会改 post 请求')
					return HttpResponseRedirect('/panel/kami')
			elif 'editkamidetails' in post_content:
				if tokenData().identityAuth(tokenData().getIdentity(token),(0,2)):
					newKami = post_content['editFormInputNewKami']
					newNum  = post_content['editFormInputNewNum']
					newTag  = post_content['editFormInputNewTag']
					newPs   = post_content['editFormInputNewPs']
					whichOne = request.COOKIES.get('editFormSelect').split(':')[0]
					isSuccess = util.editKami(newKami,newNum,newTag,newPs,whichOne)
					if isSuccess:
						messages.success(request,'操作成功')
						response = HttpResponseRedirect('/panel/kami')
						response.delete_cookie('editFormSelect')
						return response
					else:
						messages.info(request,'操作失败')
						return HttpResponseRedirect('/panel/kami')
				else:
					messages.info(request,'🐂🍺 ! 还会改 post 请求')
					return HttpResponseRedirect('/panel/kami')
			elif 'addkamidetails' in post_content:
				if tokenData().identityAuth(tokenData().getIdentity(token),(0,2,4)):
					newKami = post_content['akami']
					newNum  = post_content['anum']
					newTag  = post_content['atag']
					newPs   = post_content['aps']
					isSuccess = util.addKami(newKami,newNum,newTag,newPs)
					if isSuccess:
						messages.success(request,'操作成功')
						response = HttpResponseRedirect('/panel/kami')
						response.delete_cookie('addFormOpened')
						return response
					else:
						messages.info(request,'操作失败')
						return HttpResponseRedirect('/panel/kami')
				else:
					messages.info(request,'🐂🍺 ! 还会改 post 请求')
					return HttpResponseRedirect('/panel/kami')
			elif 'addInBulkInputHidden' in post_content:
				if tokenData().identityAuth(tokenData().getIdentity(token),(0,2,4)):
					addList = []
					addCounts = 0
					while True:
						if not (('addTableKami' + str(addCounts)) in post_content):
							break
						addList.append([
							post_content['addTableKami' + str(addCounts)],
							post_content['addTableNum' + str(addCounts)],
							post_content['addTableTag' + str(addCounts)],
							post_content['addTablePs' + str(addCounts)]])
						addCounts += 1
					errCounts = util.addKamiInBulk(addList)
					if errCounts == 0:
						messages.success(request,'操作成功')
					else:
						messages.info(request,str(errCounts) + ' 个添加失败')
					return HttpResponseRedirect('/panel/kami')
				else:
					messages.info(request,'🐂🍺 ! 还会改 post 请求')
					return HttpResponseRedirect('/panel/kami')
			elif 'file_import_submit_btn' in post_content:
				if tokenData().identityAuth(tokenData().getIdentity(token),(0,2,4)):
					upload_file = request.FILES.get('import_file',None)
					if upload_file:
						file_name = str(time.time()).replace('.','_') + '_' + random_string(16) + '.xlsx'
						with open('cache/' + file_name,'wb+') as bf:
							for chunk in upload_file.chunks():
								bf.write(chunk)
						two_dimensional_array_of_data = util.xlsx_to_2darray('cache/' + file_name)
						err_counts = util.add_kami_with_2d_array(two_dimensional_array_of_data)
						os.remove('cache/' + file_name)
						if err_counts == 0:
							messages.success(request,'操作成功')
						else:
							messages.info(request,str(err_counts) + ' 个添加失败')
					else:
						messages.info(request,'未选择文件')
					return HttpResponseRedirect('/panel/kami')
				else:
					messages.info(request,'🐂🍺 ! 还会改 post 请求')
					return HttpResponseRedirect('/panel/kami')
			elif 'export_kami' in post_content:
				if tokenData().identityAuth(tokenData().getIdentity(token),(0,2)):
					export_file_name = 'export_' + str(time.time()).replace('.','_') + '_' + random_string(16)
					kami_data = util.getKami()
					for i in range(len(kami_data)):
						kami_data[i][1] = int(kami_data[i][1])
						kami_data[i][2] = ':'.join(kami_data[i][2])
					send_data = np.array(kami_data)
					send_data = pd.DataFrame(send_data,columns = ['卡密','可用次数','Tag','备注'])
					send_data['可用次数'] = send_data['可用次数'].apply(pd.to_numeric,errors = 'ignore')
					send_data.to_excel('cache/' + export_file_name + '.xlsx',sheet_name = 'data',index = False)
					response = FileResponse(open('cache/' + export_file_name + '.xlsx','rb'))
					response['Content-Type'] = 'application/octet-stream'
					response['Content-Disposition'] = 'attachment;filename="kami.xlsx"'
					os.remove('cache/' + export_file_name + '.xlsx')
					return response
				else:
					messages.info(request,'🐂🍺 ! 还会改 post 请求')
					return HttpResponseRedirect('/panel/kami')
			else:
				return HttpResponseRedirect('/panel/kami')
		else:
			return HttpResponseRedirect('/panel/kami')
	else:
		return render(request,'denied.html')

def logReader(request,token):
	if tokenData().identityAuth(tokenData().getIdentity(token),(0,2)):
		send_dict = {
			'log': util.read_log(),
		}
		return render(request,'log.html',send_dict)
	else:
		return render(request,'denied.html')
