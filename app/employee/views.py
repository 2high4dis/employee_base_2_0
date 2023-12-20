from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import EmployeeForm
from .models import Employee


class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'employee/list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(level__lte=1)
        return qs


@require_POST
def employee_load(request: HttpRequest):
    employee_id = request.POST.get('employee_id')
    try:
        employee = get_object_or_404(Employee, pk=employee_id)
    except Http404:
        return JsonResponse({'status': 404})

    employees = employee.get_children()

    out = render_to_string('employee/list_load.html',
                           {'employees': employees, 'user': request.user})

    return JsonResponse({'status': 200, 'out': out})


class EmployeeDetailView(DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employee/detail.html'


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = 'employee/form.html'
    form_class = EmployeeForm


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'employee/form.html'
    context_object_name = 'employee'
    form_class = EmployeeForm


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee/delete_confirmation.html'
    context_object_name = 'employee'
    success_url = '/'


def table_view(request: HttpRequest):
    employees = Employee.objects.all().order_by('pk')
    paginator = Paginator(employees, 250)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    template_name = 'employee/table.html'

    return render(request, template_name, {'page_obj': page_obj})


@require_POST
def page_change(request: HttpRequest):
    sorting = request.POST.get('sorting', 'pk')
    page_number = request.POST.get('page', 1)
    q = request.POST.get('q', None)

    employees = Employee.objects.all().order_by(sorting)

    if q:
        post_reverse = dict((v.upper(), k)
                            for k, v in Employee.PostChoice.choices)

        employees = employees.filter(Q(pk=int(q)) if q.isdigit() else (Q(full_name__icontains=q) | Q(hire_date__icontains=q) |
                                     Q(email__icontains=q) | Q(post=post_reverse.get(q.upper(), None))))

    paginator = Paginator(employees, 250)
    page_obj = paginator.get_page(page_number)

    out = render_to_string('employee/table_load.html',
                           {'page_obj': page_obj})

    paginator = render_to_string('employee/paginator_load.html',
                                 {'page_obj': page_obj})

    return JsonResponse({'status': 200, 'out': out, 'paginator': paginator})


@require_POST
@login_required
def swap_bosses(request: HttpRequest):
    child_id = request.POST.get('child_id')
    parent_id = request.POST.get('parent_id')
    if parent_id:
        try:
            child = get_object_or_404(Employee, pk=child_id)
            parent = get_object_or_404(Employee, pk=parent_id)
        except Http404:
            return JsonResponse({'status': 404})
        child.move_to(parent)
    else:
        try:
            child = get_object_or_404(Employee, pk=child_id)
        except Http404:
            return JsonResponse({'status': 404})
        child.move_to(None)

    child.save()

    return JsonResponse({'status': 200})
