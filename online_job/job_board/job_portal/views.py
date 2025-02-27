from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import ApplyForm

def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'company'):
            try:
                company = Company.objects.get(user=request.user)
                candidates = Candidate.objects.filter(company=company)  # Filter candidates based on the company
                context = {
                    'candidates': candidates,
                }
                return render(request, 'job_portal/hr.html', context)
            except Company.DoesNotExist:
                messages.error(request, "Company not found.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('login')
        else:
            messages.error(request.user, "You are not authorized to view this page.")
            return redirect('login')
    else:
        companies = Company.objects.all()
        context = {
            'companies': companies,
        }
        return render(request, 'job_portal/Jobseeker.html', context)


def applyPage(request):
    form = ApplyForm()
    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('home')  # Redirect to home page after successful application
        else:
            messages.error(request, "Error submitting application. Please check the form and try again.")

    # If method is not POST or form is not valid, render the apply page with the form
    return render(request, 'job_portal/apply.html', context={'form': form})

def logoutUser(request):
    logout(request)
    return redirect('login')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        return render(request, 'job_portal/login.html')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        Form = UserCreationForm()
        if request.method == 'POST':
            Form = UserCreationForm(request.POST)

            if Form.is_valid():
                currUser = Form.save()
                Company.objects.create(user=currUser, name=currUser.username)
                return redirect('login')
        context = {
            'form': Form
        }
        return render(request, 'job_portal/register.html', context)
