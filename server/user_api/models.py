from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
class Roles(models.Model):
    role_id = models.CharField(primary_key=True,max_length=20)
    role_name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'roles'
        ordering = ['role_id']

    def __str__(self):
        return self.role_name
    
class Clients(models.Model):
    client_id = models.CharField(primary_key=True,max_length=20)
    client_name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'clients'
        ordering = ['client_id']

    def __str__(self):
        return self.client_name
    
class Projects(models.Model):
    project_id = models.CharField(primary_key=True,max_length=20)
    project_name = models.CharField(max_length=100, null=False, blank=False)
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)

    class Meta:
        db_table = 'projects'
        ordering = ['project_id']

    def __str__(self):
        return self.project_name 
    
class UserCredentialsManager(BaseUserManager):
    def create_user(self, user_id, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(user_id=user_id, username=username, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(user_id, username, password, **extra_fields)
    
class UserCredentials(AbstractUser):
    user_id = models.CharField(max_length=20, null=False, blank=False,unique=True)
    username = models.CharField(max_length=100, null=False, blank=False,unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)

    USERNAME_FIELD = 'username'
    PASSWORD_FIELD = 'password'

    objects = UserCredentialsManager() 

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='usercredentials_set',  # Custom related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='usercredentials_set',  # Custom related name
        blank=True
    )
    class Meta:
        db_table = 'user_credentials'
        ordering = ['user_id']

    def __str__(self):
        return self.username
    
class Users(models.Model):
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE,)
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE,null=True)
    user_id = models.OneToOneField(UserCredentials,on_delete=models.CASCADE, primary_key=True,to_field='user_id')

    class Meta:
        db_table = 'users'
        ordering = ['user_id']

    def __str__(self):
        return self.username