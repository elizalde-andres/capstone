from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BooleanField, CharField, DateField, DateTimeField, DecimalField, IntegerField, PositiveSmallIntegerField, TextField

from os.path import join as osjoin

# Create your models here.

class User(AbstractUser):
    last_name = CharField(max_length=128)
    first_name = CharField(max_length=128)
    is_teacher = BooleanField(default=False)

class Category(models.Model):
    category = CharField(max_length=64)
    def __str__(self) -> str:
        return self.category

class Test(models.Model):
    timestamp = DateTimeField(auto_now_add=True, editable=False)
    title = CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tests")

    def serialize(self):
        return {
            "title": self.title,
            "category_id": self.category.id,
            "category_name": self.category.category
        }

    def __str__(self) -> str:
        return self.title

class TestPart(models.Model):
    def get_upload_path(self, filename):
        return osjoin(str(self.test.title) + "-" +str(self.test.id), filename)

    timestamp = DateTimeField(auto_now_add=True, editable=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="parts")
    part_number = PositiveSmallIntegerField()
    content = TextField(blank=True)
    content_img = models.ImageField(blank=True, null=True, default=None, upload_to=get_upload_path)
    is_multiple_choice = BooleanField()
    max_score_per_answer = PositiveSmallIntegerField(default=1)
    audio = models.FileField(blank=True, null=True, default=None, upload_to=get_upload_path)

    def serialize(self):
        return {
            "part_number": self.part_number,
            "content": self.content,
            "content_img": self.content_img.url if self.content_img else "",
            "is_multiple_choice": self.is_multiple_choice,
            "max_score_per_answer": self.max_score_per_answer,
            "audio": self.audio.url if self.audio else ""
        }

    def __str__(self) -> str:
        return f"{self.test} - Part {self.part_number}"

    @property
    def get_questions(self):
        return self.questions.all().order_by("number")

    
class Question(models.Model):
    def get_upload_path(self, filename):
        return osjoin(str(self.test_part.test.title) + "-" +str(self.test_part.test.id), filename)

    test_part = models.ForeignKey(TestPart, on_delete=models.CASCADE, related_name="questions")
    number = IntegerField()
    correct_answers = CharField(max_length=256)
    audio = models.FileField(blank=True, null=True, default=None, upload_to=get_upload_path)

    def serialize(self):
        return {
            "question_number": self.number,
            "correct_answers": self.correct_answers,
            "audio": self.audio.url if self.audio else ""
        }

    def __str__(self) -> str:
        return f"{self.test_part} - {self.number}"

class TestAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tests_assignments")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="assignments")
    assigned_date = DateField()
    score = DecimalField(max_digits=4, decimal_places=1, default=None, null=True, blank=True)
    score_percent = DecimalField(max_digits=4, decimal_places=1, default=None, null=True, blank=True)
    finished_date = DateTimeField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.test}"
    
    def get_answer(self, question):
        try:
            answer = Answer.objects.get(test_assignment=self.id, question=question).answer
        except:
            answer = ""
        return answer
    
    def get_answer_id(self, question):
        try:
            answer_id = Answer.objects.get(test_assignment=self.id, question=question).id
        except:
            answer_id = None
        return answer_id

    def get_score(self, question):
        try:
            answer = Answer.objects.get(test_assignment=self.id, question=question).score.normalize()
        except:
            answer = ""
        return answer
       

class Answer(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
    answer = CharField(max_length=128, default=None, null=True, blank=True)
    score = DecimalField(max_digits=4, decimal_places=1, default=None, null=True, blank=True)
    test_assignment = models.ForeignKey(TestAssignment, on_delete=models.CASCADE, related_name="answers")