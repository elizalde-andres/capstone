import json
import datetime

from django import forms

from django.contrib import messages
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


def tests_view(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            tests = Test.objects.all().order_by("-timestamp")
            return render(request, "tests/tests.html", {
                "tests": tests
            })
        else:
            #TODO: add order_by
            tests = request.user.tests_assignments.all()
            assigned_tests = tests.filter(finished_date=None)
            finished_tests = tests.exclude(finished_date=None)
            return render(request, "tests/tests.html", {
                "assigned_tests": assigned_tests,
                "finished_tests": finished_tests
            })

def test_view(request, id):
    try:
        test = Test.objects.get(pk=id)
        test_parts = test.parts.order_by("part_number")

        assignments = TestAssignment.objects.all()
        assigned = [assignment.user for assignment in assignments.filter(test=test)]
        assigned_ids = [user.id for user in assigned]
        assignable = User.objects.exclude(pk__in=assigned_ids)
    except:
        return render(request, "tests/tests.html", {
            "message": "Invalid test part"
        })

    paginator = Paginator(test_parts,1)
    page_number = request.GET.get('part')
    parts = paginator.get_page(page_number)

    return render(request, "tests/test.html", {
        "test": test,
        "parts": parts,
        "assigned": assigned,
        "assignable": assignable
    })
    
class NewTestForm(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Title', 'autofocus': 'autofocus'}))
    categories = [(0, "")]
    categories += [(category.id, category.category) for category in Category.objects.all().order_by("category")]
    category = forms.ChoiceField(choices=categories, label="Category", widget=forms.Select(attrs = { 'class': 'form-control'}))

def new_test(request):
    if request.method == "POST":
        if request.user.is_authenticated and request.user.is_teacher:
            test_form = NewTestForm(request.POST)
            if test_form.is_valid():
                try:
                    title = request.POST["title"]
                    category_id = request.POST["category"]
                    test = Test(title=title, category=Category.objects.get(pk=category_id))
                    test.save()

                    parts_count = int(request.POST["parts_count"])
                    last_question_part = 0
                    for i in range(parts_count):
                        part_number = i+1
                        questions_count = int(request.POST[f"questions-count-{part_number}"]) - last_question_part

                        text_content = request.POST[f"text-content-{part_number}"]
                        max_score_per_answer = request.POST[f"max-score-per-answer-{part_number}"]
                        try:
                            content_img = request.POST[f"img-content-{part_number}"]
                        except:
                            content_img = None
                        try:
                            is_multiple_choice = request.POST[f"is-multiple-choice-{part_number}"]
                            is_multiple_choice = True if is_multiple_choice == 'on' else False
                        except:
                            is_multiple_choice = False
                        try:
                            audio = request.POST[f"part-audio-{part_number}"]
                        except:
                            audio = None

                        part = TestPart(test=test, part_number=part_number, content=text_content, content_img=content_img, is_multiple_choice=is_multiple_choice, max_score_per_answer=max_score_per_answer, audio=audio)
                        part.save()

                        for j in range(questions_count):
                            question_number = last_question_part + 1
                            correct_answers = request.POST[f"correct-answers-{part_number}-{question_number}"]
                            try:
                                audio = request.POST[f"question-audio-{part_number}-{question_number}"]
                            except:
                                audio = None
                            
                            question = Question(test_part=TestPart.objects.get(pk=part.pk), number=question_number, correct_answers=correct_answers)
                            question.save()
                            last_question_part += 1

                    return render(request, "tests/new_test.html")
                except:
                    return render(request, "tests/new_test.html", {
                        "message": "Error saving test"
                    })
    else:
        return render(request, "tests/new_test.html")

def abm_test_layout(request):
    # if request.GET.get('id'):
    #     test = Test.objects.filter(pk=id)
    #     # TODO: crear y rellenar los formularios, enviar todo
    #     return render(request, "tests/abm_test.html", {
    #         "form": {
    #             "title": test.title,
    #             "category": test.category,
    #             "parts": [ {
    #                 "number": part.part_number,
    #                 "text-content": part.content,
    #                 "is_multiple_choice": part.is_multiple_choice,
    #                 "max_score_per_answer": part.max_score_per_answer,
    #                 "part_audio": part.audio if test.category.category == 'Listening' else None,
    #                 "questions": [{
    #                     "number": question.number,
    #                     "correct_answers": question.correct_answers,
    #                     "audio": question.audio if test.category.category == 'Listening' else None,
    #                 } for question in part.questions] 
    #             } for part in test.parts],
    #         },
    #     })
    return render(request, "tests/abm_test_layout.html", {
        "test_form": NewTestForm()
    })

def abm_testpart_layout(request):
    
    category =request.GET.get('category')
    
    return render(request, "tests/abm_testpart_layout.html", {
        "category": category,
        "part_number": request.GET.get('part_number')
    })

def abm_question_layout(request):
    category = request.GET.get('category')
    return render(request, "tests/abm_question_layout.html", {
        "category": category,
        "question_number": request.GET.get('question_number'),
        "part_number": request.GET.get('part_number')
    })

def assign(request, id):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == "POST":
            try:
                user = User.objects.get(pk=int(request.POST["assign"]))
                test = Test.objects.get(pk=id)
                assigned_date = datetime.date.today()
                assignment = TestAssignment(user=user, test=test, assigned_date=assigned_date)
                assignment.save()
                messages.success(request, f'Test successfully assigned to {user.first_name} {user.last_name}')
                return HttpResponseRedirect(reverse("test", kwargs={'id': id}))
            except:
                return HttpResponseRedirect(reverse("index"))

def unassign(request, id):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == "POST":
            try:
                user = User.objects.get(pk=int(request.POST["remove"]))
                test = Test.objects.get(pk=id)
                # TODO: sacar los que ya finalizaron la tarea
            
                assignment = user.tests_assignments.get(test=test)
                assignment.delete()
                
                messages.success(request, f'Test successfully removed from {user.first_name} {user.last_name}.')
                return HttpResponseRedirect(reverse("test", kwargs={'id': id}))
            except:
                return HttpResponseRedirect(reverse("index"))
