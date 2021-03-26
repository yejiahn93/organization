from django.db import models
from datetime import datetime
import re, bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['last_name'] = "Name must be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Name must be at least 2 characters long."
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be less than 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['match'] = "Passwords do not match."
        if len(postData['email']) < 6:
            errors['email'] = "email is too short"
        EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Email in wrong format"
        users_with_email = User.objects.filter(email=postData['email'])
        if len(users_with_email) >= 1:
            errors['dup'] = "Email taken, use another"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()

class OrganizationManager(models.Manager):
    def organization_validator(self, postData):
        errors = {}
        if len(postData['name']) < 5:
            errors['name'] = "organization name should be more than 5 characters"
        if len(postData['description']) < 5:
            errors['description'] = "Description should be more than 10 characters"

        return errors

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="has_created_org", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_org")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = OrganizationManager()