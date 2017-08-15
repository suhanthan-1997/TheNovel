from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..models import login
from ..models import newsfeed
from ..models import admin
from ..models import count
from ..models import report
from ..models import blocklist
from sqlalchemy import desc
import datetime
import time
import hashlib
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )
user = 'Administrator'
@view_config(route_name='home', renderer='../templates/p/home.pt')
def home(request):
	user='Administrator'
	return{}
@view_config(route_name='signup', renderer='../templates/p/signup.pt')
def signup(request):
	return{}
@view_config(route_name='signup1')
def signup1(request):
	global user
	user=request.params['username']
	pwd=request.params['password']
	hash_obj = hashlib.md5(pwd)	
	m=hash_obj.hexdigest()
	obj=request.dbsession.query(login).filter(login.username==user).all()
	length=len(obj)
	if length:
		return render_to_response('../templates/p/signup11.pt',{'message':'Username '+user+' is occupied. Try another name.'},request=request)
	else:
		obj=login(username=user,password=m)
		request.dbsession.add(obj)
		countobj=count(username=user,times=1)
		request.dbsession.add(countobj)
		reportobj=report(username=user, reportcount=0)
		request.dbsession.add(reportobj)
		return render_to_response('../templates/p/signup1.pt',{'message':'Registered succesfully!!'},request=request)
@view_config(route_name='signupf', renderer='../templates/p/login1.pt')
def signupf(request):
	global user
	return {'name':user, 'message':'logged in'}

@view_config(route_name='login1')
def login1(request):
	global user
	user=request.params['username']
	pwd=request.params['password']
	hash_obj = hashlib.md5(pwd.encode())	
	m=hash_obj.hexdigest()
	obj=request.dbsession.query(login).filter(login.username==user,login.password==m).first()
	if obj is None:
		return render_to_response('../templates/p/home11.pt',{'message':'Access denied!!!Incorrect username or password'},request=request)
	else:
		blockeduser=request.dbsession.query(blocklist).filter(blocklist.username==user).first()
		if blockeduser is None:
			countobj=request.dbsession.query(count).filter(count.username==user).first()
			countobj.times+=1
			request.dbsession.add(countobj)
			return render_to_response('../templates/p/login1.pt',{'message':'logged in','name':user},request=request)
		else:
			return render_to_response('../templates/p/home1.pt',{'message':'You are blocked!!Please contact admin@tce.edu to resolve this.','name':user},request=request)
@view_config(route_name='update', renderer='../templates/p/update.pt')
def update(request):
 	return {'name':user}

@view_config(route_name='adhome', renderer='../templates/p/adhome.pt')
def adhome(request):
	return {}

@view_config(route_name='admenu')
def admenu(request):
	adminpass=request.params['adminpass']
	obj=request.dbsession.query(admin).filter().first()
	if adminpass==obj.password:
		return render_to_response('../templates/p/admenu.pt',{},request=request)
	else:
		return render_to_response('../templates/p/adhome1.pt',{'message':'Access denied!!!Incorrect password'},request=request)

@view_config(route_name='admenuf', renderer='../templates/p/admenu.pt')
def admenuf(request):
	return {}


@view_config(route_name='topusers', renderer='../templates/p/topusers.pt')
def topusers(request):
	obj=request.dbsession.query(count).filter().order_by(desc(count.times)).all()	
	return {'obj':obj}

@view_config(route_name='update1')
def update1(request):
	global user
	ab=request.params['about']
	cont = request.params['content']
	tdy = datetime.date.today()
	localtime = time.asctime(time.localtime(time.time()))
	#if user is None:
	#	obj=newsfeed(username='admin',about=ab,content=cont,submitted_date=tdy,submitted_time=localtime)
	#else:
	#dup=request.dbsession.query(newsfeed).filter(newsfeed.content==cont).first()
	#if dup is None:
	obj=newsfeed(username=user,about=ab,content=cont,submitted_date=tdy,submitted_time=localtime)
	request.dbsession.add(obj)
	if user=='Administrator':
		return render_to_response('../templates/p/adminupdate1.pt',{'message':'Updated succesfully!!','name':user},request=request)
	else:
		return render_to_response('../templates/p/update1.pt',{'message':'Updated succesfully!!','name':user},request=request)
	#else:
	#	if user=='Administrator':
	#		return render_to_response('../templates/p/adminupdate1.pt',{'message':'Same idea is already posted by '+dup.username,'name':user},request=request)
	#	else:
	#		return render_to_response('../templates/p/update1.pt',{'message':'Same idea is already posted by '+dup.username,'name':user},request=request)
		

@view_config(route_name='tomenu', renderer='../templates/p/login1.pt')
def tomenu(request):
	global user
	return {'name':user, 'message':'logged in'}

@view_config(route_name='toadmenu', renderer='../templates/p/admenu.pt')
def toadmenu(request):
	global user
	return {'name':user, 'message':'logged in'}

@view_config(route_name='adminnews', renderer='../templates/p/adminnews.pt')
def adminnews(request):
	global user
	user='Administrator'
	obj=request.dbsession.query(newsfeed).filter().order_by(desc(newsfeed.submitted_time)).all()
	return {'length':len(obj),'obj':obj,'name':user}

@view_config(route_name='adminnews1', renderer='../templates/p/adminnews1.pt')
def adminnews1(request):
	global user
	obj=request.dbsession.query(newsfeed).filter().order_by(desc(newsfeed.submitted_time)).all()
	return {'length':len(obj),'obj':obj,'name':user}

@view_config(route_name='adminnews2', renderer='../templates/p/adminnews2.pt')
def adminnews2(request):
	obj=request.dbsession.query(newsfeed).filter().order_by(desc(newsfeed.submitted_time)).all()
	return {'length':len(obj),'obj':obj,'name':user}


@view_config(route_name='news', renderer='../templates/p/news.pt')
def news(request):
	obj=request.dbsession.query(newsfeed).filter().order_by(desc(newsfeed.submitted_time)).all()
	return {'length':len(obj),'obj':obj,'name':user}

@view_config(route_name='news1', renderer='../templates/p/news1.pt')
def news1(request):
	obj=request.dbsession.query(newsfeed).filter().order_by(desc(newsfeed.submitted_time)).all()
	return {'length':len(obj),'obj':obj,'name':user}

@view_config(route_name='news2', renderer='../templates/p/news2.pt')
def news2(request):
	obj=request.dbsession.query(newsfeed).filter().order_by(desc(newsfeed.submitted_time)).all()
	return {'length':len(obj),'obj':obj,'name':user}


@view_config(route_name='toreport', renderer='../templates/p/toreport.pt')
def toreport(request):
	return {'name':user}

@view_config(route_name='userreported', renderer='../templates/p/toreport1.pt')
def userreported(request):
	global user
	reporteduser=request.params['reporteduser']
	reportobj=request.dbsession.query(report).filter(report.username==reporteduser).first()
	if reportobj is None:
		return {'name':user,'message':'There is no user like '+reporteduser}
	else:
		if reportobj.username==user:
			return {'name':user,'message':'You cannott report yourself'}	
		else:
			reportobj.reportcount+=1
			request.dbsession.add(reportobj)
			return {'name':user,'message':'Reported the user '+reporteduser+' .'}

@view_config(route_name='reportedusers', renderer='../templates/p/reportedusers.pt')
def reportedusers(request):
	reportobj=request.dbsession.query(report).filter(report.reportcount >= 3).order_by(desc(report.reportcount)).all()
	return {'obj':reportobj}

@view_config(route_name='action', renderer='../templates/p/action.pt')
def action(request):
	return {'name':user}

@view_config(route_name='block', renderer='../templates/p/action1.pt')
def block(request):
	blockeduser=request.params['blist']
	bl=request.dbsession.query(blocklist).filter(blocklist.username==blockeduser).first()
	if bl is None:
		obj=blocklist(username=blockeduser)
		request.dbsession.add(obj)
		return {'name':user,'msg':'Blocked the user '+blockeduser}
	else:
		return {'name':user,'msg':'Already the user '+blockeduser+' is in blockedlist'}

@view_config(route_name='unblock', renderer='../templates/p/action1.pt')
def unblock(request):
	unblockeduser=request.params['blist']
	bl=request.dbsession.query(blocklist).filter(blocklist.username==unblockeduser).first()
	if bl is None:
		return {'msg':'The user '+unblockeduser+' is not in the blockedlist'}
	else:	
		obj=blocklist(username=unblockeduser)
		request.dbsession.query(blocklist).filter(blocklist.username==unblockeduser).delete()
		return {'msg':'Unblocked the user '+unblockeduser}

@view_config(route_name='adminupdate', renderer='../templates/p/adminupdate.pt')
def adminupdate(request):
 	return {'name':'Administrator'}

@view_config(route_name='about', renderer='../templates/p/about.pt')
def about(request):
 	return {}





