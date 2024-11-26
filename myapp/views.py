from urllib import request
import requests
import json
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
#import the log_in required
from django.contrib.auth.decorators import login_required

from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .models import Forms
from .models import Child
#XAMPP
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage


# Create your views here.
def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html", {})


def team(request):
    return render(request, "team.html")


def testimonials(request):
    return render(request, "testimonials.html")


def blog(request):
    return render(request, "blog.html")


def pricing(request):
    return render(request, "pricing.html")


def portfolio(request):
    return render(request, "portfolio.html")


def form(request):
    return render(request, "form.html")


def show_appointments(request):
    return render(request, "show_appointments.html")


def show_sponsorship(request):
    sponsorships = Child.objects.all()
    return render(request, "show_sponsorship.html", {'sponsorships': sponsorships})


#function to push appointments
def contact(request):
    #check if it's a post method
    if request.method == "POST":
        appointment = Forms(
            #List the input fields here
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            date=request.POST["date"],
            message=request.POST["message"],
        )
        #save the variable
        appointment.save()
        #redirect to a page
        return redirect('myapp:index')
    else:
        return render(request, "contact.html")


#Retrieve all appointments
def retrieve_appointments(request):
    #Create a variable to store these appointments
    appointments = Forms.objects.all()
    context = {"appointments": appointments}
    return render(request, 'show_appointments.html', context)


#delete
def delete_appointments(request, id):
    appointment = Forms.objects.get(id=id)
    appointment.delete()
    return redirect('myapp:show_appointments')


#Update
def edit_appointments(request, appointment_id):
    # update the appoitnments
    # Retrieve the appointment object or return a 404 error
    appointment = get_object_or_404(Forms, id=appointment_id)
    # Put the condition for the form to update
    # Check if the request method is POST (form submission)
    if request.method == "POST":
        appointment.name = request.POST.get("name")
        appointment.email = request.POST.get("email")
        appointment.phone = request.POST.get("phone")
        appointment.date = request.POST.get("date")
        appointment.message = request.POST.get("message")
        appointment.save()
        return redirect('myapp:show_appointments')
    context = {"appointment": appointment}
    return render(request, 'edit_appointments.html', context)


#Functions to push sponsorship
def sponsorship_form(request):
    if request.method == "POST":
        sponser = Child(
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            gender=request.POST["gender"],
            Religion=request.POST["religion"],
            address=request.POST["address"],
            age=request.POST["age"],
        )
        sponser.save()
        return redirect('myapp:show_sponsorship')
    else:
        return render(request, 'sponsorship_form.html')

    #Retrieve all the sponsorship


def retrieve_sponsorship(request):
    sponsorship = Child.objects.all()
    context = {"sponsorship": sponsorship}
    return render(request, 'edit_sponsorship.html', context)


#Delete
def delete_sponsorship(request, id):
    sponsor = Child.objects.get(id=id)
    sponsor.delete()
    return redirect('myapp:show_sponsorship')


#Update
def edit_sponsorship(request, sponsor_id):
    sponsor = get_object_or_404(Child, id=sponsor_id)
    if request.method == "POST":
        sponsor.name = request.POST.get("name")
        sponsor.email = request.POST.get("email")
        sponsor.phone = request.POST.get("phone")
        sponsor.age = request.POST.get("age")
        sponsor.gender = request.POST.get("gender")
        sponsor.Religion = request.POST.get("religion")
        sponsor.address = request.POST.get("address")
        sponsor.save()
        return redirect('myapp:show_sponsorship')
    context = {"sponsor": sponsor}
    return render(request, 'edit_sponsorship.html', context)


#XAMPP
def upload_image(request):
    if request.method == "POST":
        title = request.POST["title"]
        uploaded_file = request.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        image = UploadedImage.objects.create(title=title, image=filename)
        image.save()
        return render (request,'upload_success.html',{'file_url':file_url})
    return render(request,'upload_image.html')





#Adding Mpesa functions
#Display the payment form
def pay(request):
   """ Renders the form to pay """
   return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'tSYOLLPWdDBXQBjIZYj9jc7m7UGVQCprRKMEmJJZ39O7zJqp'
    consumer_secret = 'E37iguUH3ePe6WU62QzWIJKKNIpiGc0EfBjLMLlqNP8jYAuTsnZzPBrQ4cZ8EA3f'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")


