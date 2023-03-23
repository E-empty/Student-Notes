from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
                messages.error(request, "Nazwa użytkownika jest już zajęta.")
                return redirect('home')
            
        if User.objects.filter(email=email).exists():
                messages.error(request, "Adres e-mail jest już zarejestrowany.")
                return redirect('home')
            
        if len(username)>20:
                messages.error(request, "Nazwa użytkownika musi zawierać poniżej 20 znaków!!")
                return redirect('home')
            
        if pass1 != pass2:
                messages.error(request, "Hasło nie pasuje!!")
                return redirect('home')
            
        if not username.isalnum():
                messages.error(request, "Nazwa użytkownika może zawierać tylko znaki alfanumeryczne!!")
                return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        
        messages.success(request, "Twoje konto zostało poprawnie założone!!")
            
            
        return redirect('signin')
            
            
    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło")
            return redirect('home')
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Zostałeś poprawnie wylogowany")
    return redirect('home')
    