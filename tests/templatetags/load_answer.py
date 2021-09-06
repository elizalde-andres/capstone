from tests.models import TestAssignment
from django import template

register = template.Library()

@register.filter(name='load_answer')
def load_answer(assignment, question):
    return TestAssignment.objects.get(id=int(assignment.id)).get_answer(question)

@register.filter(name='load_answer_id')
def load_answer(assignment, question):
    return TestAssignment.objects.get(id=int(assignment.id)).get_answer_id(question)

@register.filter(name='load_score')
def load_score(assignment, question):
    return TestAssignment.objects.get(id=int(assignment.id)).get_score(question)

