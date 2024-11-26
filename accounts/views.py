from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.
# Show the registration form.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')

        # Check if passwords match
        if password == confirm_password:
            try:
                # Create a new user
                user = User.objects.create_user(username=username, password=password)
                user.email = email
                # user.first_name = first_name
                # user.last_name = last_name
                user.save()
                # Display success message
                messages.success(request, "Compassion beneficiary account successfully created")
                return redirect('myapp:about')  # Adjust 'myapp:about' to match your app's URL name
            except:
                # Display error if user creation fails
                messages.error(request, "Username already exists. Try again")
        else:
            # Display error if passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'accounts/register.html')


# Login
def login_view(request):
    """ Login view """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # Check if the user exists
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect("myapp:about")
        else:
            messages.error(request, "Invalid login credentials")
    return render(request, 'login.html')