from django.db import models
from django.contrib.auth.models import(AbstractBaseUser,BaseUserManager)
from OnlineDating import settings
from swampdragon.models import SelfPublishModel
from DatingApp.serializers import ChatMessageSerializer
import uuid

# Create your models here.

def getUploadFileLocation(instance,filename):
	return "uploaded_files/%s"%(filename)

class CustomUserManager(BaseUserManager):
	def create_user(self,username,password,uid, **extra_fields):
		if(not username):
			raise ValueError('User name must be set')
		username = CustomUserManager.normalize_email(username)
		user = self.model(
				username = username,
				uid=uid,			
			)
		user.set_password(password)
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	uid = models.CharField(db_column='UId', max_length=36)
	name = models.CharField(db_column='Name', max_length=100, null=True)
	username = models.EmailField(db_column='Email', max_length=128, unique=True)
	#password = models.CharField(db_column='Password', max_length=128)
	dob = models.DateTimeField(db_column='DOB', blank=True, null=True)
	address = models.CharField(db_column='Address', max_length=500, blank=True, null=True)
	isValidUser = models.IntegerField(db_column='isValidUser', default=0)
	gender = models.IntegerField(db_column='Gender', default=0)
	created = models.DateTimeField(db_column='Created',auto_now_add=True)
	lastupdated = models.DateTimeField(db_column='LastUpdated',auto_now=True)
	logout_time = models.DateTimeField(db_column='Logout_Time',blank=True,null=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['name','password','isValidUser','gender','created','lastupdated']
	objects = CustomUserManager()
	class Meta:
		db_table = 'user'

class Contact(models.Model):
    id = models.IntegerField(primary_key=True)
    contact_uid = models.CharField(db_column='ContactUid', max_length=36, blank=True, null=True)
    image = models.CharField(db_column='Image', max_length=255, blank=True, null=True)
    phone = models.CharField(db_column='Phone', max_length=11, blank=True, null=True)
    hobbies = models.CharField(db_column='Hobbies', max_length=500, blank=True, null=True)
    interestedin = models.IntegerField(db_column='InterestedIn', blank=True, null=True)
    currentstatus = models.CharField(db_column='CurrentStatus', max_length=500, blank=True, null=True)
    maritalstatus = models.IntegerField(db_column='MaritalStatus', blank=True, null=True)
    contact_of = models.CharField(db_column='Contact_Of', max_length=36, blank=True, null=True)
    last_updated = models.DateTimeField(db_column='Last_Updated', blank=True, null=True,auto_now=True)
    name=''
    email = ''
    class Meta:
        db_table = 'contact'

class OnlineUser(object):
	def __init__(self,username,name,gender,address,dob):
		self.username = username
		self.name = name
		self.gender = gender
		self.address = address
		self.dob = dob

	def __str__(self):
		return (self.username)

	def __unicode__(self):
		return u'%s' %(self.username)

class ChatMessage(SelfPublishModel, models.Model):
	message = models.TextField()
	message_from = models.TextField()
	message_to = models.TextField()

	serializer_class = ChatMessageSerializer
	class Meta:
		db_table = 'ChatMessage'
		