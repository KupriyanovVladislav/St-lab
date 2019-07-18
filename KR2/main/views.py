from django.shortcuts import render, redirect
from django.urls import reverse
from django import views
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView

from .models import Teacher, Student


class IndexView(views.View):
    def get(self, request):
        students = Student.objects.all()
        teachers = Teacher.objects.all()
        return render(request, 'index.html', context={'students': students, 'teachers': teachers})


class StudentCreate(CreateView):
    template_name = 'student_add.html'
    model = Student
    fields = ['name', 'surname', 'birthdate']

    def form_valid(self, form):
        self.object = Student(**form.cleaned_data)
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class TeacherCreate(CreateView):
    template_name = 'teacher_add.html'
    model = Teacher
    fields = ['name', 'surname', 'birthdate']

    def form_valid(self, form):
        self.object = Teacher(**form.cleaned_data)
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class StudentDelete(DeleteView):
    model = Student
    template_name = 'student_delete.html'
    pk_url_kwarg = 'student_id'

    def get_success_url(self):
        return reverse('index')


class StudentUpdate(UpdateView):
    model = Student
    template_name = 'student_update.html'
    fields = ['name', 'surname', 'birthdate']
    pk_url_kwarg = 'student_id'

    def form_valid(self, form):
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class TeacherUpdate(UpdateView):
    model = Teacher
    template_name = 'teacher_update.html'
    fields = ['name', 'surname', 'birthdate']
    pk_url_kwarg = 'teacher_id'

    def form_valid(self, form):
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class TeacherDelete(DeleteView):
    model = Teacher
    template_name = 'teacher_delete.html'
    pk_url_kwarg = 'teacher_id'

    def get_success_url(self):
        return reverse('index')


class StudentInfoView(DetailView):
    model = Student
    template_name = 'student_information.html'
    pk_url_kwarg = 'student_id'


class TeacherInfoView(DetailView):
    model = Teacher
    template_name = 'teacher_information.html'
    pk_url_kwarg = 'teacher_id'


class DisabledView(TemplateView):
    template_name = 'disabled.html'
