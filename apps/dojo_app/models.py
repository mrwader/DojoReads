from django.db import models
import re
from datetime import datetime, date

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class BlogManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['email']) < 5:
            errors['email'] = "Invalid email!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Passwords should match!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email!"
        if User.objects.filter(email=postData['email']).count() > 0:
            errors['email'] = "This email already exists!"

        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['email'] = "Invalid email!"
        if User.objects.filter(email=postData['email']).count() < 1:
            errors['email'] = "This email doesnt exist!"
        if len(postData['password']) < 1:
            errors["password"] = "Password should be at least 8 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email!"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Author(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Review(models.Model):
    review = models.TextField(max_length =500)
    rating = models.IntegerField(default =0)
    book = models.ForeignKey(Book, related_name="book_reviews")
    user = models.ForeignKey(User, related_name="reviews") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()
    


# class Book(models.Model):
#     title = models.CharField(max_length=45)
#     description = models.CharField(max_length=45)
#     uploaded_by = models.ForeignKey(User, related_name ="books_uploaded")
#     users_who_like = models.ManyToManyField(User, related_name="liked_books", default=None)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = BlogManager()
