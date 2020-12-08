from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account
import json
from django.http import JsonResponse
import os
import sqlite3
from django.http import HttpRequest





def createData():
	db = \
	"""
	PRAGMA foreign_keys=OFF;
	BEGIN TRANSACTION;
	CREATE TABLE UsersByPass (
    	id varchar(200),
    	password varchar(200)
	);
	INSERT INTO UsersByPass VALUES('sars','sarsssss');
	INSERT INTO UsersByPass VALUES('sars','saasasas');
	INSERT INTO UsersByPass VALUES('ster','sters');
	COMMIT;
	"""
 
	if os.path.exists('UserGetter.sqlite'):
		print('UserGetter.sqlite already exists')
	else:
		print("Database has been created")
		conn = sqlite3.connect('UserGetter.sqlite')
		conn.cursor().executescript(db)
		conn.commit()





@csrf_exempt
@login_required
def homePageView(request):
	createData()
#	tasks = Account.objects.get(user_id=request.user.id)
#	accounts = Account.objects.get(user_id=request.user.id)
#	return render(request, 'pages/tasks.html')
	accounts = Account.objects.get(user_id=request.user.id)

	return render(request, 'pages/passwords.html', {'username':accounts.user.username})
#	return render(request, 'pages/tasks.html')

#	accounts = Account.objects.exclude(user_id=request.user.id)
#	return render(request, 'pages/index.html', {'accounts': accounts})
@csrf_exempt
def submitNewLogin(request):
	username = request.POST.get('username')
	email = request.POST.get('email')
	password = request.POST.get('password')
	user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password)
	Account.objects.create(user=user)
	return render(request, 'pages/addNewLogin.html')
def addNewLogin(request):
	return render(request, 'pages/addNewLogin.html')
	
@csrf_exempt
@login_required
def passwordsView(request):
	return JsonResponse({'passwords' : [{'name': t} for t in passwords]})
@csrf_exempt

def passwordListView(request):
	createData()
	username = request.GET.get('username')
	passwords = []
	conn = sqlite3.connect('UserGetter.sqlite')
	c = conn.cursor()
	c.execute('select password FROM UsersByPass WHERE id=?',(username,))
	rows = c.fetchall()
	for row in rows:
		row = str(row)[2:]
		row = row[:-3]
		passwords.append(row)	
	return render(request, 'pages/passwordList.html', {'passwords':passwords,'username':username})
@csrf_exempt

def addPassWord(request):
	username = request.GET.get('username')
	addedPass = request.GET.get('addedPassWord')
	conn = sqlite3.connect('UserGetter.sqlite')
	c = conn.cursor()
	c.execute("INSERT INTO UsersByPass (id, password) VALUES (?, ?)", (username, addedPass))
	conn.commit()
	otherRequest = HttpRequest()
	otherRequest.method = 'GET'
	otherRequest.GET = {'username': username}
	return (passwordListView(otherRequest))
@csrf_exempt

def testIfThereIsUser(request):
	username = request.GET.get('username')
	conn = sqlite3.connect('UserGetter.sqlite')
	c = conn.cursor()
	c.execute('select * FROM UsersByPass WHERE id=?',(username,))
	rows = c.fetchall()
	for row in rows:
		val = row
		return passwordListView(request)
	accounts = Account.objects.get(user_id=request.user.id)	
	return render(request, 'pages/passwords.html', {'username':accounts.user.username})
@csrf_exempt

def deletePassWord(request):
	username = request.GET.get('username')
	conn = sqlite3.connect('UserGetter.sqlite')
	c = conn.cursor()
	c.execute("DELETE FROM UsersByPass WHERE id = ?", (username, ))
	conn.commit()
	return passwordListView(request)
@csrf_exempt

def deleteAll(request):
	conn = sqlite3.connect('UserGetter.sqlite')
	c = conn.cursor()
	c.execute("DELETE FROM UsersByPass WHERE 1=1")
	conn.commit()
	accounts = Account.objects.get(user_id=request.user.id)	
	return render(request, 'pages/passwords.html', {'username':accounts.user.username})

@csrf_exempt

def addUserPassWord(request):
	username = request.GET.get('username')
	conn = sqlite3.connect('UserGetter.sqlite')
	c = conn.cursor()
	c.execute("INSERT INTO UsersByPass (id, password) VALUES (?, ?)", (username, ""))
	conn.commit()
	accounts = Account.objects.get(user_id=request.user.id)	
	return render(request, 'pages/passwords.html', {'username':accounts.user.username})