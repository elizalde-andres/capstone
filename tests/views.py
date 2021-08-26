import json

from django import forms

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models.fields import EmailField
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse

import sys
import traceback

from .models import *
# Create your views here.

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': 'autofocus'}))
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    first_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

def index(request):
    return render(request, "tests/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tests/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tests/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":

        form = RegisterForm(request.POST)
        if form.is_valid():
            # Ensure password matches confirmation
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]
            if password != confirmation:
                return render(request, "tests/register.html", {
                    "message": "Passwords must match.",
                    "form": form
                })

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            last_name = form.cleaned_data["last_name"]
            first_name = form.cleaned_data["first_name"]

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password, last_name=last_name, first_name=first_name)
                user.save()
            except IntegrityError:
                return render(request, "tests/register.html", {
                    "message": "Username already taken.",
                    "form": form
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            message = ''
            for field in form:
                    message += field.errors.as_text()
            # If the form is invalid, re-render the page with existing information.
            return render(request, "tests/register.html", {
                "message": message,
                "form": form
            })
    else:
        return render(request, "tests/register.html", {
            "form": RegisterForm()
        })


# def tests_view(request):
#     return render(request, "tests/tests.html")

def tests_view(request):
    img = TestPart.objects.get(pk=1).content_img.url
    return render(request, "tests/uoe_test.html", {
        "img": img
    })