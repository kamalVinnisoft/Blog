from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login,authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# Create your views here.
def SignUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_pic = request.FILES.get('profile_pic')

        if not(email and username and password1 and password2):
            messages.error(request,"email,username and password required")

        if '@' not in email:   
            messages.error(request,"enter valid email.")

        if  CustomUser.objects.filter(email=email,username=username).exists():
            messages.error(request,"user already exist.")

        if password1 !=  password2:
            messages.error(request,"passwords doesnot match.")

        user = CustomUser.objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password1)
        # user.password = make_password(password1)
        if profile_pic :
            print(profile_pic)
            user.profile_pic =profile_pic
        user.save()
        print(user.password)
        return redirect('/signin')
    return render(request,'signup.html')


def SignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not (email and  password):
            messages.error(request,"email and password required")

        user = authenticate(email=email,password=password)
    
        if not user:
            messages.error(request,"invalid credentials.")
        login(request,user)

        refresh = RefreshToken.for_user(user)
        print(refresh.access_token)

        return redirect('/blog/')
    return render(request,'signin.html')


@login_required(login_url="/signin")
def users_listing(request):
    users =  CustomUser.objects.exclude(id=request.user.id)
    user_requests = UserFollowingRequest.objects.filter(requested_to_id=request.user.id,accepted=False)
    
    #users requested by request.user
    userss=UserFollowingRequest.objects.filter(requested_by_id=request.user.id,accepted=False).values_list('requested_to', flat=True)
    requested = CustomUser.objects.filter(id__in=userss)

    #user followed by request.user
    frnds = UserFollowingRequest.objects.filter(Q(requested_by_id=request.user.id)& Q(accepted=True)).values_list('requested_to', flat=True)
    frnds = CustomUser.objects.filter(id__in=frnds)
    
    if 'req_id' in request.POST:
        id=request.POST.get('req_id')
        req,created = UserFollowingRequest.objects.get_or_create(requested_by_id=request.user.id,requested_to_id=id)
        if created:
            req.save()

    if 'accept_id' in request.POST:
        print(request.POST)
        id=request.POST.get('accept_id')
        req = UserFollowingRequest.objects.filter(requested_by_id=id,requested_to_id=request.user.id).first()
        if req:
            req.accepted =True
            req.save()
    return render(request,"user_listings.html",{'users':users,'user_requests':user_requests,'requested':requested,'frnds':frnds})

