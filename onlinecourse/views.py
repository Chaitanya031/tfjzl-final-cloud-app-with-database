from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import (
    Course,
    Lesson,
    Enrollment,
    Question,
    Choice,
    Submission
)


def index(request):
    course_list = Course.objects.all()
    context = {
        'course_list': course_list
    }
    return render(
        request,
        'onlinecourse/course_list_bootstrap.html',
        context
    )


def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')

        return render(
            request,
            'onlinecourse/login.html',
            {'message': 'Invalid username or password'}
        )

    return render(request, 'onlinecourse/login.html')


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    return HttpResponseRedirect(
        reverse(
            'onlinecourse:course_details',
            args=(course.id,)
        )
    )


@login_required
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    lesson_list = Lesson.objects.filter(
        course=course
    ).order_by('order')

    question_list = Question.objects.filter(
        course=course
    )

    enrollment = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).first()

    context = {
        'course': course,
        'lesson_list': lesson_list,
        'question_list': question_list,
        'enrollment': enrollment,
    }

    return render(
        request,
        'onlinecourse/course_details_bootstrap.html',
        context
    )


@login_required
def submit(request, course_id):
    if request.method != 'POST':
        return HttpResponseRedirect(
            reverse(
                'onlinecourse:course_details',
                args=(course_id,)
            )
        )

    course = get_object_or_404(
        Course,
        pk=course_id
    )

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    questions = Question.objects.filter(
        course=course
    )

    for question in questions:
        choice_id = request.POST.get(
            'choice_' + str(question.id)
        )

        if choice_id:
            choice = Choice.objects.filter(
                pk=choice_id,
                question=question
            ).first()

            if choice:
                submission.choices.add(choice)

    return HttpResponseRedirect(
        reverse(
            'onlinecourse:show_exam_result',
            kwargs={
                'course_id': course.id,
                'submission_id': submission.id,
            }
        )
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(
        Course,
        pk=course_id
    )

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__user=request.user,
        enrollment__course=course
    )

    question_list = Question.objects.filter(
        course=course
    )

    selected_choices = submission.choices.all()

    total_score = 0
    possible_score = 0

    for question in question_list:
        possible_score += question.grade

        selected_choice_ids = selected_choices.filter(
            question=question
        ).values_list('id', flat=True)

        if question.is_get_score(selected_choice_ids):
            total_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'question_list': question_list,
        'choices': selected_choices,
        'total_score': total_score,
        'possible_score': possible_score,
        'grade': total_score,
        'possible': possible_score,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
