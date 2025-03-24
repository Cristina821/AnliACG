# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import random
import re

from django.contrib.auth.decorators import login_required

from django.shortcuts import render,redirect
from django.http import HttpResponse

from myapp.models import Users
from myapp.models import Animate_data
from myapp.models import Article
from myapp.models import Comment

from django.http import HttpResponseRedirect

from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

#跳转函数
def jump(request):
	request.session['is_login']=0
	return redirect(reverse("loginpage"))

#用户信息界面
def indexUsers(request):
	
	state=request.session.get('is_login')
	if state:
		if state==2:
			try:
				ulist=Users.objects.all()
				context={"userslist":ulist}
				return render(request,"myapp/users/index.html",context)
			except:
				return HttpResponse("没有找到用户信息")
		else:
			context={"error":"请先进行登录管理员账号才能进行页面访问!"}
			return render(request,"myapp/error/error_message.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#加载注册表单
def addUsers(request):
	return render(request,"myapp/show/regist.html")

#执行用户信息注册
def insertUsers(request):
	if len(str(request.POST['telephone']))==11:
		phone_check=Users.objects.filter(phone=request.POST['telephone']).first()
		name_check=Users.objects.filter(name=request.POST['username']).first()
		if phone_check:
			context={"info":"该号码已被注册!"}
		else:
			if name_check:
				context={"info":"该昵称已被占用!"}
			else:
				ob=Users()
				ob.name=request.POST['username']
				ob.password=request.POST['password']
				ob.Email=request.POST['Email']
				ob.phone=request.POST['telephone']
				ob.save() #执行保存
				context={"info":"注册成功"}
	else:
		context={"info":"注册不符合规范，请重新检查"}
	return render(request,"myapp/error/error_message.html",context)

#用户信息删除
def delUsers(request,uid=0):
	state=request.session.get('is_login')
	if state:
		if state==2:
			try:
				ob=Users.objects.get(id=uid)
				ob.delete()#执行删除
				context={"info":"删除成功"}
				return render(request,"myapp/users/info.html",context)
			except:
				context={"info":"删除失败"}
				return render(request,"myapp/users/info.html",context)
		else:
			context={"error":"请先进行登录管理员账号才能进行页面访问!"}
			return render(request,"myapp/error/error_message.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#执行用户登录及身份判断
def loginpage(request):
	if request.method == 'POST':
		key = request.POST.get('key')
		password = request.POST.get('password')
		if key and password:
			user_check=Users.objects.filter(phone=key,password=password).first()
			user=Users.objects.filter(phone=key,password=password)
			for message in user:
				username=message.name
			if user_check:
				if key=='18382820359':
					request.session['username']=username
					request.session['key']=key
					request.session['is_login']=2
					request.session.set_expiry(3600)
					return render(request,"myapp/users/manager.html")
				else:
					request.session['username']=username
					request.session['key']=key
					request.session['is_login']=1
					request.session.set_expiry(3600)
					context={"user":username}
					return render(request,"myapp/menu/menu.html",context)
			else:
				return HttpResponse('账号或密码错误，登录失败')
		else:
			return HttpResponse('非法的信息')
	#return render(request,"myapp/show/loginpage.html")
	return render(request,"myapp/show/loginpage.html")

#执行用户登出
def logoutpage(request):
	request.session.flush()
	return render(request,"myapp/show/loginpage.html")

#显示主界面
def menu(request):
	state=request.session.get('is_login')
	if state:
		if state==1 or 2:
			user=request.session.get('username')
			context={"user":user}
			return render(request,"myapp/menu/menu.html",context)
		else:
			context={"warning":"请先进行登录才能进行页面访问!"}
			return render(request,"myapp/show/loginpage.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#展示作品数据库中的数据
def animate_manage(request):
	state=request.session.get('is_login')
	if state:
		if state==2:
			alist=Animate_data.objects.all()
			context={"animatelist":alist}
			return render(request,"myapp/animate_data/animate_manage.html",context)
		else:
			context={"warning":"请先进行登录才能进行页面访问!"}
			return render(request,"myapp/show/loginpage.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#执行作品的数据爬取与更新
def animate_update(request):
	state=request.session.get('is_login')
	if state:
		if state==2:
			name = []
			picture = []
			score = []
			rank = []

			i = 0
			count = 0
			if request.method == 'POST':
				user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
							"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
							"Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
							"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
							"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
							"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
							"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
							"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
							]
				head = {'User-Agent': random.choice(user_agent_list)}
				for i in range(10):
					response = requests.get('https://bangumi.tv/anime/browser?sort=rank&page='+str(i+1), headers = head)
					response.encoding="utf-8"
					soup = BeautifulSoup(response.text, "html.parser")
					message_h3 = soup.findAll("h3")
					for select1 in message_h3:
						message_name = select1.findAll("a")
						for names in message_name:
							name.append(names.string)
							count += 1
							rank.append(str(count))
					message_score = soup.findAll("small", attrs={"class":"fade"})
					for scores in message_score:
						score.append(scores.string)
					message_img = soup.findAll("img")
					for pictures in message_img:
						picture.append(pictures.get('src'))
					for j in range(count):
						animate_check=Animate_data.objects.filter(aname=name[j]).first()
						if animate_check:
							pass
						else:
							try:
								ob=Animate_data()
								ob.aname=name[j]
								ob.aimg=picture[j]
								ob.ascore=score[j]
								ob.arank=rank[j]
								ob.save() #执行保存
								context={"info":"添加成功"}
							except:
								context={"info":"添加失败"}
			else:
				HttpResponse("error")
			return render(request,"myapp/users/info.html")
		else:
			context={"warning":"请先进行登录才能进行页面访问!"}
			return render(request,"myapp/show/loginpage.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)
	
	
#执行作品单项删除
def animate_delete(request,aid=0):
	state=request.session.get('is_login')
	if state:
		if state==2:
			try:
				ob=Animate_data.objects.get(id=aid)
				ob.delete()#执行删除
				context={"info":"删除成功"}
			except:
				context={"info":"删除失败"}
		else:
			context={"warning":"请先进行登录才能进行页面访问!"}
			return render(request,"myapp/show/loginpage.html",context)
		return render(request,"myapp/users/info.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#执行数据全部删除
def animate_delall(request):
	aid=1
	for aid in range(1,10000):
		animate_check=Animate_data.objects.filter(arank=aid).first()
		if animate_check:
			ob=Animate_data.objects.get(arank=aid)
			ob.delete()#执行删除
		else:
			break
	context={"info":"删除成功"}
	return render(request,"myapp/users/info.html",context)

#执行作品搜索筛选
def animate_search(request):
	state=request.session.get('is_login')
	if state:
		if state==1:
			search_name= request.POST.get('search_name')
			if not search_name:
				context={"error":"请输入关键词"}
				return render(request,"myapp/error/error_message.html",context)

			consequence_check=Animate_data.objects.raw("SELECT * FROM myapp_animate_data WHERE aname LIKE '%%{}%%';".format(search_name))
			if consequence_check:
				consequence=Animate_data.objects.raw("SELECT * FROM myapp_animate_data WHERE aname LIKE '%%{}%%';".format(search_name))
				context={"consequence_list":consequence}
				return render(request,"myapp/show/consequence.html",context)
			else:
				context={"error":"未找到相关信息"}
				return render(request,"myapp/error/error_message.html",context)
		else:
			context={"warning":"请先进行登录才能进行页面访问!"}
			return render(request,"myapp/show/loginpage.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)


#文章页主界面调用，展示文章数据
def article_homepage(request):
	state=request.session.get('is_login')
	if state:
		if state==1 or 2:
			try:
				artlist=Article.objects.all()
				context={"all_article_list":artlist}
				return render(request,"myapp/communication/article_homepage.html",context)
			except:
				return HttpResponse("没有找到文章信息")
			return render(request,"myapp/communication/article_homepage.html")
		else:
			context={"warning":"请先进行登录才能进行页面访问!"}
			return render(request,"myapp/show/loginpage.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#调取文章发布页
def article_writing(request):
	state=request.session.get('is_login')
	if state:
		if state==1 or 2:
			return render(request,"myapp/communication/article_writing.html")
		else:
			context={"warning":"请先进行登录才能进行页面访问!"}
			return render(request,"myapp/show/loginpage.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#执行文章上传存储
def article_insert(request):
	state=request.session.get('is_login')
	if state:
		if state==1 or 2:
			ob=Article()
			ob.title=request.POST['title']
			ob.content=request.POST['content']
			ob.author=request.session.get('username')
			ob.save() #执行保存
			context={"info":"发布成功"}
		else:
			context={"warning":"请先进行登录才能进行发表文章!"}
			return render(request,"myapp/show/loginpage.html",context)
		return render(request,"myapp/communication/article_writing.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#显示文章详情页
def article_detail(request,article_id):
	state=request.session.get('is_login')
	request.session['target']=article_id
	request.session['target_id']=0
	if state:
		if state==1 or 2:
			article = Article.objects.get(id=article_id)    #从数据库找出id=article_id的文章对象
			comment_list = Comment.objects.filter(article_id=article_id)  #从数据库找出该文章的评论数据对象
			context = {
				'article': article,
				'comment_list': comment_list
			}
			return render(request,"myapp/communication/article_detail.html",context)  #返回对应文章的详情页面
		else:
			context={"warning":"请先进行登录才能进行查看文章!"}
			return render(request,"myapp/show/loginpage.html",context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#执行评论存储
def artcommon_insert(request):
	now_url=request.session.get('target')
	state=request.session.get('is_login')
	if state:
		if state==1 or 2:
			if request.session['target_id']==0:
				ob=Comment()
				ob.comment_content=request.POST['comment']
				ob.comment_author=request.session.get('username')
				ob.article_id=now_url
				ob.save() #执行保存
				article = Article.objects.get(id=now_url)    #从数据库找出id=article_id的文章对象
				comment_list = Comment.objects.filter(article_id=now_url)  #从数据库找出该文章的评论数据对象
				context = {
					'article': article,
					'comment_list': comment_list
				}
			else:
				ob=Comment()
				ob.comment_content=request.POST['comment']
				ob.comment_author=request.session.get('username')
				ob.article_id=now_url
				ob.pre_comment_id=request.session['target_id']
				ob.save() #执行保存
				article = Article.objects.get(id=now_url)    #从数据库找出id=article_id的文章对象
				comment_list = Comment.objects.filter(article_id=now_url)  #从数据库找出该文章的评论数据对象
				context = {
					'article': article,
					'comment_list': comment_list
				}
				request.session['target_id']=0
		else:
			context={"warning":"请先进行登录才能评论!"}
			return render(request,"myapp/show/loginpage.html",context)
		return render(request,'myapp/communication/article_detail.html',context)
	else:
		context={"warning":"请先进行登录才能进行页面访问!"}
		return render(request,"myapp/show/loginpage.html",context)

#辅助函数，用于判断是否为二级评论
def target_check(request):
	state=request.session.get('is_login')
	o=100
	if state==1 or 2:
		if request.method=='POST':
			content= request.POST['pre_id']
			request.session['target_id']=content
			return HttpResponse(content)
	else:
		context={"warning":"请先进行登录才能进行发表评论!"}
		return render(request,"myapp/show/loginpage.html",context)