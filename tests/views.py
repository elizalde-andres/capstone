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
from django.utils import timezone
from django.urls import reverse

import sys
import traceback

from .models import *

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': 'autofocus'}))
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    first_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

def index(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            tests = Test.objects.all().order_by("-timestamp")
            return render(request, "tests/tests.html", {
                "tests": tests
            })
        else:
            tests = request.user.tests_assignments.all()
            assigned_tests = tests.filter(finished_date=None).order_by("-assigned_date")
            finished_tests = tests.exclude(finished_date=None).order_by("-finished_date")

            return render(request, "tests/tests.html", {
                "assigned_tests": assigned_tests,
                "finished_tests": finished_tests
            })
    else:
        return HttpResponseRedirect(reverse("login"))

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
            tests = request.user.tests_assignments.all()
            assigned_tests = tests.filter(finished_date=None).order_by("-assigned_date")
            finished_tests = tests.exclude(finished_date=None).order_by("-finished_date")

            return render(request, "tests/tests.html", {
                "assigned_tests": assigned_tests,
                "finished_tests": finished_tests
            })

def test_view(request, id, assignment_id = None):
    try:
        test = Test.objects.get(pk=id)
        test_parts = test.parts.order_by("part_number")

        assignments = TestAssignment.objects.all()
        assigned = [assignment.user for assignment in assignments.filter(test=test)]

        assignable = User.objects.exclude(pk__in=[user.id for user in assigned])
    except:
        return render(request, "tests/tests.html", {
            "message": "Invalid test part"
        })

    assignment = None
    if assignment_id:
        assignment = TestAssignment.objects.get(pk=assignment_id)
    
    paginator = Paginator(test_parts,1)
    page_number = request.GET.get('part')
    parts = paginator.get_page(page_number)

    
    return render(request, "tests/test.html", {
        "test": test,
        "parts": parts,
        "assigned": assigned,
        "assignable": assignable,
        "assignment": assignment
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
                            content_img = request.FILES[f"img-content-{part_number}"]
                        except:
                            content_img = None
                        try:
                            is_multiple_choice = request.POST[f"is-multiple-choice-{part_number}"]
                            is_multiple_choice = True if is_multiple_choice == 'on' else False
                        except:
                            is_multiple_choice = False
                        try:
                            audio = request.FILES[f"part-audio-{part_number}"]
                        except:
                            audio = None

                        part = TestPart(test=test, part_number=part_number, content=text_content, content_img=content_img, is_multiple_choice=is_multiple_choice, max_score_per_answer=max_score_per_answer, audio=audio)
                        part.save()

                        for j in range(questions_count):
                            question_number = last_question_part + 1
                            correct_answers = request.POST[f"correct-answers-{part_number}-{question_number}"]
                            try:
                                audio = request.FILES[f"question-audio-{part_number}-{question_number}"]
                            except:
                                audio = None
                            
                            question = Question(test_part=TestPart.objects.get(pk=part.id), number=question_number, correct_answers=correct_answers, audio=audio)
                            question.save()
                            last_question_part += 1

                    return render(request, "tests/new_test.html")
                except:
                    return render(request, "tests/new_test.html", {
                        "message": "Error saving test"
                    })
    else:
        return render(request, "tests/new_test.html")


def edit_test(request, id):
    if request.method == "POST":
        if request.user.is_authenticated and request.user.is_teacher:
            test_data = request.POST
            # try:
            title = test_data["title"]
            test = Test.objects.get(pk=id)
            test.title = title
            test.save()

            assignments = test.assignments.all()

            for part_number in range(int(test_data["parts_count"])):
                part_number += 1
                part = test.parts.get(part_number=int(part_number))
                part.content = test_data[f"text-content-{part_number}"]
                part.max_score_per_answer = test_data[f"max-score-per-answer-{part_number}"]
                
                if f"img-content-{part_number}" in request.FILES:
                    part.content_img = request.FILES[f"img-content-{part_number}"]
                if f"is-multiple-choice-{part_number}" in test_data:
                    part.is_multiple_choice = True
                if f"part-audio-{part_number}" in request.FILES:
                    part.audio = request.FILES[f"part-audio-{part_number}"]
                part.save()

                for i in range(len(test_data.getlist(f"questions-count-{part_number}"))):
                    question_number = test_data.getlist(f"questions-count-{part_number}")[i]
                    question = part.questions.get(number=question_number)
                    question.correct_answers = test_data[f"correct-answers-{part_number}-{question_number}"]

                    if f"question-audio-{part_number}-{question_number}" in request.FILES:
                        question.audio = request.FILES[f"question-audio-{part_number}-{question_number}"]
                    question.save()


                    for assignment in assignments:
                        if assignment.finished_date:
                            # Calculate answer score
                            correct_answers = question.correct_answers.lower()
                            correct_answers = correct_answers.split(";")
                            correct_answers = [answer.strip() for answer in correct_answers]

                            answer = Answer.objects.get(question=question, test_assignment=assignment)
                            
                            if answer.answer.lower() in correct_answers:
                                answer.score = part.max_score_per_answer

                            answer.save()
                            # Calculate assignment score
                            assignment.score = 0
                            for answer in assignment.answers.all():
                                assignment.score += answer.score

                            max_test_score = 0
                            for test_part in assignment.test.parts.all():
                                max_test_score += test_part.max_score_per_answer * test_part.questions.count()
                            
                            assignment.score_percent = assignment.score / max_test_score *100

                            assignment.save()
            return HttpResponseRedirect(reverse("test", kwargs={'id': id}))
    else:
        messages.error(request, f'Error saving test.')
        return HttpResponseRedirect(reverse("test", kwargs={'id': id}))


def get_test(request):
    try: 
        id = request.GET.get('id')
        test = Test.objects.get(pk=id)
        test_dict = test.serialize()
        
        test_dict["parts"] = [ part.serialize() for part in test.parts.all()]
        
        for part in test_dict["parts"]:
            part["questions"] = [question.serialize() for question in test.parts.get(part_number=part["part_number"]).questions.all()]
        
        return JsonResponse(test_dict, safe=False)
    except:
        return JsonResponse({"error": "Invalid test id."}, status=400)


def answer(request, assignment_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("finish") is not None:
            assignment = TestAssignment.objects.get(pk=int(assignment_id))
            test_part = TestPart.objects.get(test=assignment.test, part_number=data.get("part_number"))
            
            for k in data.get("answers"):
                question = Question.objects.get(test_part=test_part, number=int(k))
                try:
                    answer = Answer.objects.get(question=question, test_assignment=assignment)
                except:
                    answer = Answer(question=question, test_assignment=assignment)
                answer.answer = data.get("answers")[k]
                
                # Calculate answer score
                correct_answers = question.correct_answers.lower()

                correct_answers = correct_answers.split(";")
                correct_answers = [answer.strip() for answer in correct_answers]
                if answer.answer.lower() in correct_answers:
                    answer.score = test_part.max_score_per_answer
                else:
                    answer.score = 0

                answer.save()

            if data.get("finish") == True:
                # Mark as finished
                assignment.finished_date = timezone.now()

                # Calculate assignment score
                assignment.score = 0
                for answer in assignment.answers.all():
                    assignment.score += answer.score

                max_test_score = 0
                for part in assignment.test.parts.all():
                    max_test_score += part.max_score_per_answer * part.questions.count()
                
                assignment.score_percent = assignment.score / max_test_score *100

                assignment.save()
                return HttpResponse(status=200)
            return HttpResponse(status=200)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)

def update_score(request, assignment_id, answer_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        new_score = data.get("new_score")
        if new_score is not None:
            assignment = TestAssignment.objects.get(pk=int(assignment_id))
            answer = assignment.answers.get(pk=int(answer_id))
            answer.score = float(new_score)
            answer.save()

            # Calculate assignment score
            assignment.score = 0
            for answer in assignment.answers.all():
                assignment.score += answer.score

            max_test_score = 0
            for part in assignment.test.parts.all():
                max_test_score += part.max_score_per_answer * part.questions.count()
            
            assignment.score_percent = assignment.score / max_test_score *100
            assignment.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=500) 
    else:
        return HttpResponse(status=500) 

def teacher_results(request, test_id):
    test_assignments = Test.objects.get(pk=test_id).assignments.all().order_by("-finished_date")

    paginator = Paginator(test_assignments,2)
    page_number = request.GET.get('part')
    assignments = paginator.get_page(page_number)

    return render(request, "tests/teacher_results.html", {
        "assignments": assignments
    })

def abm_test_layout(request):
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
                messages.error(request, f'You must select a student.')
                return HttpResponseRedirect(reverse("test", kwargs={'id': id}))
def unassign(request, id):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == "POST":
            try:
                user = User.objects.get(pk=int(request.POST["remove"]))
                test = Test.objects.get(pk=id)
            
                assignment = user.tests_assignments.get(test=test)
                assignment.delete()
                
                messages.success(request, f'Test successfully removed from {user.first_name} {user.last_name}.')
                return HttpResponseRedirect(reverse("test", kwargs={'id': id}))
            except:
                messages.error(request, f'You must select a student.')
                return HttpResponseRedirect(reverse("test", kwargs={'id': id}))
