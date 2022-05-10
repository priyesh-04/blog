from django.core.validators import RegexValidator
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.views.generic.edit import CreateView

from django.http import JsonResponse

from django.contrib.auth import login, logout
from accounts.forms import UserLoginForm, UserCreationForm
from accounts.models import MyUser


# class RegisterView(CreateView):
#     form_class = UserCreationForm
#     template_name = 'accounts/register.html'
#     success_url = '/login/'

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect('/')
#         return super(RegisterView, self).get(request, *args, **kwargs)


# def login_view(request, *args, **kwargs):
#     form = UserLoginForm(request.POST or None)
#     if request.user.is_authenticated:
#         return HttpResponseRedirect("/")
#     else:
#         if form.is_valid():
#             user_obj = form.cleaned_data.get('user_obj')
#             login(request, user_obj)
#             print('loggedin successfully')
#             return HttpResponseRedirect("/")
#     return render(request, "accounts/login.html", {"form": form})


# Ajax Authentication

def register_view(request, *args, **kwargs):
    form = UserCreationForm()
    context = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == "POST" and request.is_ajax():
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        input_email = MyUser.objects.filter(email=email).first()
        input_mobile_number = MyUser.objects.filter(mobile_number=mobile_number).first()
        input_username = MyUser.objects.filter(username=username).first()
        if input_email:
            context['error_email'] = "User with this Email address already exists."
            return JsonResponse(context)
        if mobile_number:
            try:
                pattern = RegexValidator("^[6-9]\d{9}$")
                pattern(mobile_number)
            except:
                context['error_mobile_number'] = "Enter a valid mobile number."
                return JsonResponse(context)
        if input_mobile_number:
            context['error_mobile_number'] = "User with this Mobile number already exists."
            return JsonResponse(context)
        if input_username:
            context['error_username'] = "User with this username already exists."
            return JsonResponse(context)    
        if (password1 and password2) and (password1 != password2):
            context['error_password'] = "Passwords don't match"
            return JsonResponse(context)
        try:
            user = MyUser.objects.create(email=email,
                                        mobile_number=mobile_number,
                                        username=username,)
            user.set_password(password1)
            user.save()
            context['status'] = 200
            context['redirect_url'] = '/login/'
            return JsonResponse(context)
        except:
            pass
    else:
        pass
    return render(request, "accounts/register.html", {"form": form})

def login_view(request, *args, **kwargs):
    form = UserLoginForm()
    context = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    elif request.method == "POST" and request.is_ajax():
        query = request.POST.get('query')
        password = request.POST.get('password')
        user_qs_final = MyUser.objects.filter(
                Q(mobile_number__iexact=query)|
                Q(email__iexact=query)
            ).distinct()

        # user = authenticate(request, email=username, password=password)
        if not user_qs_final.exists() and user_qs_final.count() != 1:
            context['error'] = "Invalid credentials -- user does not exists"
            return JsonResponse(context)

        user_obj = user_qs_final.first()

        if not user_obj.check_password(password):
            context['error'] = "Invalid credentials"
            return JsonResponse(context)

        if user_qs_final.exists():
            login(request, user_obj)
            print('loggedin successfully')
            context['loggedIn'] = True
            context['status'] = 200
            context['redirect_url'] = '/'
            return JsonResponse(context)
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/")
