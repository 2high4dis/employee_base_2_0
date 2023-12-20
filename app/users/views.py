from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.views.generic import DetailView


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
