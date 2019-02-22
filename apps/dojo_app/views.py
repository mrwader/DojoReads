from django.shortcuts import render, redirect
from .models import User, Book, Author, Review
import bcrypt
from django.contrib import messages
import datetime


def index(request):
    return render(request, "dojo_app/index.html")


def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        fname_from_form = request.POST['first_name']
        lname_from_form = request.POST['last_name']
        email_from_form = request.POST['email']
        password_from_form = request.POST['password']

        pw_hash = bcrypt.hashpw(password_from_form.encode(), bcrypt.gensalt())

        user = User.objects.create(
            first_name=fname_from_form, last_name=lname_from_form, email=email_from_form, password=pw_hash)

        if 'user' in request.session:
            request.session['user'] = user.email
        else:
            request.session['user'] = user.email
        return redirect("/books")


def login(request):

    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        email_from_form = request.POST['email']
        password_from_form = request.POST['password']
        user = User.objects.get(email=email_from_form)
        print(user)
        if bcrypt.checkpw(password_from_form.encode(), user.password.encode()):
            if 'user' in request.session:
                request.session['user'] = user.email
            else:
                request.session['user'] = user.email
            return redirect("/books")
        return redirect("/")
    
def display_books(request):
    if 'user' not in request.session:
        return redirect("/")
    
    last_three = Review.objects.all().order_by('-id')[:3]
    last_three_in_ascending_order = reversed(last_three)
    context = {
        "user": User.objects.get(email=request.session['user']),
        "books": Book.objects.all(),
        "last" : last_three_in_ascending_order
    }

    return render(request, "dojo_app/books.html", context)

def logout(request):
    del request.session['user']
    return redirect("/")

def add_book_page(request):
    context={
        "authors": Author.objects.all()
    }
    return render(request, "dojo_app/add_book.html", context)

def add_book(request):
    user = User.objects.get(email = request.session['user'])
    author = Author.objects.get(id= request.POST['author_id'])
    book = Book.objects.create(
        title=request.POST['title'], author = author)
    review = Review.objects.create(review = request.POST['review'], rating = request.POST['rating'], book = book, user =user)

    return redirect("/books")

def add_author(request):
    author = Author.objects.create(name = request.POST['author_name'])

    return redirect("/add_book_page")

def view_book(request, id):
    context={
        "book": Book.objects.get(id=id)  
    }
    return render(request, "dojo_app/view_book.html", context)

def add_review(request):
    book_id = request.POST['book_id']
    user = User.objects.get(email = request.session['user'])
    book = Book.objects.get(id=book_id)
    review = Review.objects.create(review = request.POST['review'], rating = request.POST['rating'], book = book, user =user)
    return redirect(f"/books/{book_id}")

def view_user(request, id):
    context={
        "user": User.objects.get(id=id)  
    }
    return render(request, "dojo_app/view_user.html", context)

def delete_review(request,id):
    review = Review.objects.get(id=id)
    book_id = review.book.id
    if request.session['user'] == review.user.email:
        review.delete()
    return redirect (f"/books/{book_id}")

