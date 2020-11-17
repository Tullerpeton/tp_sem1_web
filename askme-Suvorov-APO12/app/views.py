from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import random
from app.models import Question, Tag, Answer, Profile
from itertools import chain

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    return paginator.get_page(page)


def right_column(count_tags=10, count_members=10):
    tags = Tag.objects.get_top_tags(count_tags)
#    members = Profile.objects.get_best_members(count_members)
    return {
        'tags': tags,
        'members': [],
    }


def new_questions(request):
    questions = paginate(Question.objects.new_questions(), request, 20)
    column = right_column()
    return render(request, 'index.html', {
        'questions': questions,
        'tags': column['tags'],
        'members': column['members'],
    })


def hot_questions(request):
    questions = paginate(Question.objects.hot_questions(), request, 20)
    column = right_column()
    return render(request, 'index.html', {
        'questions': questions,
        'tags': column['tags'],
        'members': column['members'],
    })


def tag_page(request, tag):
    questions = paginate(Question.objects.get_questions_by_tag(tag), request, 20)
    column = right_column()
    return render(request, 'tag_page.html', {
        'tag': tag,
        'questions': questions,
        'tags': column['tags'],
        'members': column['members'],
    })


def question_page(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = paginate(Answer.objects.get_answers_of_question(question_id), request, 30)
    column = right_column()
    return render(request, 'question_page.html', {
        'question': question,
        'answers': answers,
        'tags': column['tags'],
        'members': column['members'],
    })


def login_page(request):
    column = right_column()
    return render(request, 'login_page.html', {
        'tags': column['tags'],
        'members': column['members'],
    })


def signup_page(request):
    column = right_column()
    return render(request, 'signup_page.html', {
        'tags': column['tags'],
        'members': column['members'],
    })


def ask_page(request):
    column = right_column()
    return render(request, 'ask_page.html', {
        'tags': column['tags'],
        'members': column['members'],
    })

def settings_page(request):
    column = right_column()
    return render(request, 'settings_page.html', {
        'tags': column['tags'],
        'members': column['members'],
    })

