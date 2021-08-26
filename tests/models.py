from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BooleanField, CharField, DateField, DateTimeField, DecimalField, IntegerField, TextField

from os.path import join as osjoin

# Create your models here.

class User(AbstractUser):
    last_name = CharField(max_length=128)
    first_name = CharField(max_length=128)

class Category(models.Model):
    category = CharField(max_length=64)
    def __str__(self) -> str:
        return self.category

class Test(models.Model):
    title = CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tests")
    assigned_students = models.ManyToManyField(User, blank=True, related_name="assigned_tests")
    finished_students = models.ManyToManyField(User, blank=True, related_name="finished_test")

    def __str__(self) -> str:
        return self.title

class TestPart(models.Model):
    def get_upload_path(self, filename):
        return osjoin(str(self.test.title), filename)

    timestamp = DateTimeField(auto_now_add=True, editable=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="test_parts")
    title = CharField(max_length=64)
    content = TextField(blank=True)
    content_img = models.ImageField(blank=True, upload_to=get_upload_path)
    multiple_choice = BooleanField()
    
    def __str__(self) -> str:
        return f"{self.test} - {self.title}"

    
class Question(models.Model):
    test_part = models.ForeignKey(TestPart, on_delete=models.CASCADE)
    number = IntegerField()
    question = CharField(blank=True, max_length=128)
    correct_answers = CharField(max_length=256)
    max_score = IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.test_part} - {self.number}"

class Answer(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
    answer = CharField(blank=True, max_length=128)
    score = DecimalField(blank=True, max_digits=4, decimal_places=1)

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_results")
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = DecimalField(max_digits=4, decimal_places=1)
    score_percent = DecimalField(max_digits=4, decimal_places=1)
    taken_date = DateTimeField(auto_now_add=True, editable=False)