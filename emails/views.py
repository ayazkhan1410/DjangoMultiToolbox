from django.shortcuts import render, redirect
from .forms import EmailForm
from .models import *
from django.contrib import messages
from automation.helpers import send_email_notification_bulk
from django.conf import settings
from .tasks import celery_bulk_email_send
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone

def send_email(request):
    if request.method == "POST":
        email_list_id = request.POST.get('email_list')
        body = request.POST.get('body')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')  

        try:
            email_list = List.objects.get(id=email_list_id)   
            
            email_obj = Email.objects.create(
                email_list=email_list,
                body=body,
                message=message,
                attachment=attachment if attachment else None
            )
            email_obj.save()
        
            # Recipients List
            to_email = []
            try:
                sample = Subscriber.objects.filter(email_list = email_list)
                to_email = [item.email_address for item in sample]
            except Exception as e:
                messages.error(request, str(e))

            # Get email id
            email_id = email_obj.id
            
            # Send Email
            if not to_email:
                messages.error(request, "No recipients found in the selected email list. Please ensure that the email list has subscribers.")
            else:
                # Handover task to celery
                celery_bulk_email_send.delay(body, message, to_email, attachment,email_id)
                messages.success(request, "Email sent successfully!")
             
            return redirect('send_email')
        except List.DoesNotExist:
            messages.error(request, "Invalid email list selected.")
    else:       
        email_list = List.objects.only("email_list")
        context = {
            'email_list': email_list
        }
        return render(request, 'emails/send_email.html', context)

def track_click(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        url = request.GET.get("url")
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)
    except Exception as e:
       return HttpResponse("Something went WRONG")
  
def track_open(request, unique_id):
    # Logic to store the tracking info
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # Check if the opened_at field is already set or not
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse("Email opened successfully!")
        else:
            print('Email already opened')
            return HttpResponse('Email already opened')
    except:
        return HttpResponse('Email tracking record not found!')

def email_tracking_dashboard(request):
    email_obj = Email.objects.select_related('email_list').order_by('-send_at')
    total_email_sent = email_obj.count()

    # Calculate total opens and total clicks across all emails
    total_opens = EmailTracking.objects.filter(opened_at__isnull=False).count()
    total_clicks = EmailTracking.objects.filter(clicked_at__isnull=False).count()

    context = {
        'email_obj': email_obj,
        'total_email_sent': total_email_sent,
        'total_opens': total_opens,
        'total_clicks': total_clicks,
    }
    return render(request, 'emails/dashboard.html', context)

def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    email_list = email.email_list
    names = Subscriber.objects.filter(email_list=email_list)
    total_sent = names.count()
    
    # Fetch tracking data and map it to email addresses
    tracking_data = EmailTracking.objects.filter(email=email)
    
    # Check if opened_at is not null
    total_opens = tracking_data.filter(opened_at__isnull=False).count()
    #Check if opened_at is not null
    total_clicks = tracking_data.filter(clicked_at__isnull=False).count()
                    
    tracking_dict = {
        tracking.subscriber.email_address: (tracking.opened_at, tracking.clicked_at)
        for tracking in tracking_data
    }

    # Prepare a list with subscriber and their opened_at and clicked_at status
    subscribers_with_status = [
        (subscriber, tracking_dict.get(subscriber.email_address, (None, None)))
        for subscriber in names
    ]

    context = {
        'email': email,
        'subscribers_with_status': subscribers_with_status,
        'total_sent':total_sent,
        "total_opens":total_opens,
        "total_clicks":total_clicks
    }
    return render(request, 'emails/track_stats.html', context)