from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    
    # Import and export Data
    path('import-data', views.import_data, name='import_data'),
    path('export-data', views.export_data, name='export_data'),
    
    # Account URLs
    path('login', views.login_page, name='login'),
    path('sign-up', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    
    # Celery Email Testing
    path('email-send', views.email_send)

]
