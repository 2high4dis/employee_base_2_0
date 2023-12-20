from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('table/', views.table_view, name='employee_flat'),
    path('load/', views.employee_load, name='employee_load'),
    path('change/', views.page_change, name='page_change'),
    path('swap/', views.swap_bosses, name='swap_bosses'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(),
         name='employee_update'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(),
         name='employee_delete'),
    path('', views.EmployeeListView.as_view(), name='employee_list'),
]
