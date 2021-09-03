from tests.models import TestAssignment
from django import template

register = template.Library()

@register.filter(name='load_answer')
def load_answer(assignment, question):
    try:
        assignment = TestAssignment.objects.get(id=int(assignment.id))
    except:
        print("**************************************+")
        print(TestAssignment.objects.filter(id=int(assignment.id)))
    return assignment.get_answer(question)