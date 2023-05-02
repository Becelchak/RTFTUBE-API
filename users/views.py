from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Переназначение в случае успеха
            return redirect('main')
        else:
            # Ошибка при неверном логине/пароле
            messages.success(request, ('Ошибка при входе в аккаунт. Проверьте корректность данных.'))
            return redirect('login_user')
    else:
        return render(request,'authentication/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('Произведен выход из аккаунта.'))
    return redirect('login_user')