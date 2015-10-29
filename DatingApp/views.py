from django.shortcuts import render
from django.http import HttpResponseRedirect
from DatingApp.models import (User,OnlineUser,Contact)
from django.contrib import auth
from multiprocessing import Process
from datetime import datetime
from django.db.models import F
import uuid,sys,asyncio,websockets,os
from django.db import connection
from OnlineDating import settings

# Create your views here.

#onlineUsers = []
#raise AssertionError()

def prepareHtml(username,password):
	htmlMessage='<a style="font-size:25px;" href="http://192.168.1.39:8000/confirmation/'+username+'" target=\'_blank\'>Click here for confirmation in Minion Finder</a><br>'
	htmlMessage += 'Username : '+ username + '<br>'
	htmlMessage += 'Password : ' + password + '<br>'
	
	return htmlMessage

def Login(request):
	templateName = ''
	if(request.POST):
		userName = request.POST['emailAddress']
		password = request.POST['password']

		user = auth.authenticate(username=userName,password=password)
		#user = User.objects.get(username=userName,isValidUser)

		if(user is not None):
			if(user.isValidUser == 0):
				return render(request,'DatingApp/Confirmation.html',{'confirmation':'check your mail and confirm registration'})
			else:
				auth.login(request,user)
				onlineUser = OnlineUser(user.username,user.name,user.gender,user.address,user.gender)
				return HttpResponseRedirect('/MainPage/')
				#templateName = 'DatingApp/MainPage.html'
		else:
			templateName = 'DatingApp/Login.html'

	elif(request.GET):
		if(bool(request.GET['signUp'])):
			return HttpResponseRedirect('registration')
		else:
			templateName = 'DatingApp/Login.html'
	else:
		templateName = 'DatingApp/Login.html'
	return render(request,templateName)


def Logout(request):
	if(request.user is not None):
		user = User.objects.get(username = request.user.username,uid=request.user.uid)
		user.logout_time = datetime.now().isoformat()
		user.save()
		auth.logout(request)
		return HttpResponseRedirect('/')


def Registration(request):
	if(request.POST):
		error = ''
		userName = request.POST['emailAddress']
		if(userName is not None and len(userName)>0):
			alreadyPresentUsers = User.objects.filter(username=userName)
			if(alreadyPresentUsers.count() == 0):
				try:
					firstName = request.POST['firstName']
					lastName = request.POST['lastName']
					fullName = firstName + " " + lastName
					gender = request.POST.get('gender')
					address = request.POST['location']
					password = request.POST['password']
					uid = uuid.uuid1()
					user = User.objects.create_user(username=userName,password=password,uid=uid)
					if(user is not None):
					#user.dob = request.POST['dob']
						user.address=address
						user.gender=gender
						user.name=fullName
						user.save()
						recipients = []
						recipients.append(userName)
						from django.core.mail import get_connection,send_mail
						emailConnection = get_connection(username=settings.EMAIL_HOST_USER,password=settings.EMAIL_HOST_PASSWORD)
						#htmlMessage='Emails/ConfirmationMail.html'			
						htmlMessage = prepareHtml(userName,password)
						
						result = send_mail(subject='confirmation mail',message='click on the below link to confirm your mail address',recipient_list=recipients,from_email=settings.EMAIL_HOST_USER,connection=emailConnection,html_message=htmlMessage)
						return render(request,'DatingApp/Confirmation.html',{'confirmation': 'check your mail and confirm registration'})
				except:
					raise
					#error = 'there is some problem' #sys.exc_info()[0]
			else:
				error = 'user already present'
		return render(request,'DatingApp/Registration.html',{'serverError': error})
	else:	
		return render(request,'DatingApp/Registration.html')

def Confirmation(request,emailId):
	if(len(emailId)>0):
		user = User.objects.get(username=emailId)
		if(user is not None):
			user.isValidUser = 1
			user.save()

	return render(request,'DatingApp/Confirmation.html',{'confirmation':'Thanks for confirmation ....!'})

def MainPage(request):
	#contacts = Contact.objects.all().order_by("-id")[:10]
	contacts = []
	cursor = connection.cursor()
	cursor.callproc('OnlineDating_Contact_User_Get')
	raw_Contacts = cursor.fetchall()
	cursor.close();
	if(raw_Contacts is not None):
		for raw_contact in raw_Contacts:
			contact = Contact()
			contact.name = raw_contact[0]
			contact.email = raw_contact[1]
			contact.id = raw_contact[2]
			contact.contact_uid = raw_contact[3]
			contact.phone = raw_contact[4]
			contact.hobbies = raw_contact[5]
			contact.interestedin = raw_contact[6]
			contact.currentstatus = raw_contact[7]
			contact.maritalstatus = raw_contact[8]
			contact.contact_of = raw_contact[9]
			contact.last_updated = raw_contact[10]
			contact.image = raw_contact[11]
			contacts.append(contact)
	onlineUsers = _getOnlineUsers()
	return render(request,'DatingApp/MainPage.html',{'user':request.user,'contacts':contacts,'onlineUsers':onlineUsers})

def ChangePassword(request):
	if(request.POST and request.user is not None):
		currentPassword = request.POST.get('currentPassword','')
		newPassword = request.POST.get('newPassword','')
		confirmPassword = request.POST.get('confirmPassword','')
		changePassword = True
		userName = request.user.username
		uid = request.user.uid
		errorMessage = ''
		user = User.objects.get(username=userName,uid=uid)
		try:
			if(len(currentPassword) == 0 or len(newPassword) == 0 or len(confirmPassword) == 0):
				changePassword = False
				errorMessage = 'Passwords cannot be empty'
			if(newPassword != confirmPassword):
				changePassword = False
				errorMessage = 'new password and re-entered passwords do not match'
			if(currentPassword == newPassword):
				changePassword = False
				errorMessage = 'current password and new password cannot be same'
			if(not user.check_password(currentPassword)):
				changePassword = False
				errorMessage = 'current password is not valid'
			if(changePassword):
				user.set_password(newPassword)
				user.save();
		except AttributeError as e:
			errorMessage = 'current password is invalid'
		
		if(not changePassword):
			pass

		return render(request,'DatingApp/DummyFile.html',{'error':errorMessage})

def ViewProfile(request):
	user = request.user
	contact = Contact.objects.filter(contact_uid=user.uid)[:1]
	return render(request,'DatingApp/ProfilePage.html',{'user':user,'name':str(user.name),'contact':contact})

def GetOnlineUsers(request):
	onlineUsers = _getOnlineUsers()
	return render(request,'DatingApp/GetOnlineUsers.html',{'users':onlineUsers})

def _getOnlineUsers():
	onlineUsers = []
	users = User.objects.filter(logout_time__lte=F('last_login'))[:10]
	for user in users:
		onlineUser = OnlineUser(user.username,user.name,user.gender,user.address,user.dob)
		onlineUsers.append(onlineUser)
	return onlineUsers

def UpdateUserDetails(request):
	error = ''
	success = 0
	templateName = 'DatingApp/ProfilePage.html'
	user = None
	line = 0
	image = None
	if(request.POST):
		try:
			if('img' in request.FILES):
				image = request.FILES['img']
			user = request.user
			name = request.POST.get('name') 
			dob = request.POST.get('dob')
			address = request.POST.get('address')
			gender = request.POST.get('gender')
			phone = request.POST.get('phone')
			hobbies = request.POST.get('hobbies')
			interestedIn = request.POST.get('interestedIn',-1)
			currentStatus = request.POST.get('currentStatus')
			maritalStatus = request.POST.get('maritalStatus',-1)
			user = User.objects.get(username=request.user.username,uid=request.user.uid)
			user.name = name
			user.dob = datetime.strptime(dob,'%Y-%m-%d').isoformat()
			user.address = address
			user.gender = gender
			user.save()
			
			contact = Contact.objects.filter(contact_uid=user.uid)[:1]

			if(contact is None):
				#fileName = request.POST.get('img')
				contact = Contact(phone=phone,hobbies=hobbies,currentstatus=currentStatus,interestedin=interestedIn,maritalstatus=maritalStatus,contact_uid=user.uid)
				
			else:
				contact.phone=phone
				contact.hobbies=hobbies
				contact.currentstatus=currentStatus
				contact.interestedin=interestedIn
				contact.maritalstatus=maritalStatus

			
				
			if(image is not None):
				imageName = SetProfilePic(image,contact)
				if(len(imageName)>0 and imageName is not None):
					contact.image = imageName
			contact.save()
			success = 1
		except:
			error = sys.exc_info[0]
			#return render(request,'DatingApp/ProfilePage.html',{'error':error})

		if(success == 1):
			return HttpResponseRedirect('/MainPage/')

	return render(request,'DatingApp/ProfilePage.html',{'error':error,'user':user,'contact':contact})

def SetProfilePic(image,contact):
	filename = ''
	try:
		name = image.name
		relativeFileName ='Profile_Pics\\' + contact.contact_uid +'_'+ name
		destinationFile = settings.MEDIA_ROOT + '\\' + relativeFileName
		if(not os.path.exists(destinationFile)):
			open(destinationFile,'x')
		imageFile = open(destinationFile, 'wb+')
		for chunk in image.chunks():
			imageFile.write(chunk)
		imageFile.close()

		filename = relativeFileName
	except Exception as e:
		print(e)
		filename = 'abc'
		return filename
	return filename