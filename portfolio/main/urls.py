from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('certificates/', views.certificates, name='certificates'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    
    # API endpoints
    path('api/projects/', views.api_projects, name='api_projects'),
    path('api/skills/', views.api_skills, name='api_skills'),
]
