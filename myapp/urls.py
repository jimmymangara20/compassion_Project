from django.urls import path
from . import views
app_name = 'myapp'
urlpatterns = [
    path('', views.index,name='index'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('sponsorship_form/', views.sponsorship_form,name='sponsorship_form'),
    path('services/', views.services,name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('team/', views.team,name='team'),
    path('blog/',views.blog,name='blog'),
    path('pricing/',views.pricing,name='pricing'),
    path('testimonials/',views.testimonials,name='testimonials'),

    #Appointments
    path('show_appointments/',views.retrieve_appointments,name='show_appointments'),
    path('appo/delete/<int:id>',views.delete_appointments,name='delete_appointments'),
    path('appo/edit/<int:appointment_id>',views.edit_appointments,name='edit_appointments'),

    #Sponsorship
    path('show_sponsorship/', views.show_sponsorship,name='show_sponsorship'),
    path('spon/delete/<int:id>',views.delete_sponsorship,name='delete_sponsorship'),
    path('spo/edit/<int:sponsor_id>',views.edit_sponsorship,name='edit_sponsorship'),
    path('upload/',views.upload_image,name='upload_image'),

]