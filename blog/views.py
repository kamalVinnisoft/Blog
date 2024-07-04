from django.shortcuts import render,redirect
from .models import *
from user_authentication.models import *
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import  login,authenticate
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib import messages
@login_required(login_url="/signin")
def Home(request):
    user = CustomUser.objects.get(id=request.user.id)

    #followings list followed by user
    followings = UserFollowingRequest.objects.filter(Q(requested_by=user) & Q(accepted=True)).values_list('requested_to', flat=True)

    posts = Blog.objects.filter(Q(created_by=user) | Q(created_by_id__in=followings))

    for i in posts:
        i.total_likes = Like.objects.filter(post_id=i.id).count()
        i.liked= Like.objects.filter(liked_by_id=request.user.id,post=i).exists()
        i.comments = Comment.objects.filter(post_id=i.id)
        i.total_comments = i.comments.count()

    return render(request,"home.html",{'posts':posts})
@login_required(login_url="/signin")
def CreatePost(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        if title or image:
            print("dfghfduglsdfkl;sdkfljfdkgsdjdlfkgjsdl;gksd",image)
            post= Blog.objects.create(title=title,created_by_id=request.user.id)
            if image :
                print(image)
                post.image= image
            post.save()
            return redirect('/blog/')
    return render(request,"createpost.html")


@login_required(login_url="/signin")
def UpdatePost(request,id):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        if not (title or image):
            messages.error(request,"atleast one field required.")
        try:
            post= Blog.objects.get(id=id)
            if post.created_by_id != request.user.id:
                messages.success(request,"you have no access to update this Post .")

            post.title = title
            if image :
                post.image= image
            post.save()
            messages.success(request,"Post updated successfully.")
            
            return redirect('/blog/')
        except:
            messages.error(request,"post doesnot exist.")
    return render(request,"createpost.html")

@login_required(login_url="/signin")
def DeletePost(request,id):
    try:
        post= Blog.objects.get(id=id)

        if post.created_by != request.user:
            messages.success(request,"you have no access to delete this Post .")

        post.delete()
        messages.success(request,"Post deleted successfully.")

        return redirect('/blog/')
    except:
        messages.error(request,"Post doesnot exist.")

                
@login_required(login_url="/signin")
def LikePost(request):
    if request.method == 'POST':
        print(request.POST)
        p_id = request.POST.get('p_id')
        if p_id:
            l=Like.objects.filter(Q(post_id=p_id) & Q(liked_by_id=request.user.id)).first()
            if l:
                l.delete()
                change_txt="like"
            else:
                l = Like.objects.create(post_id=p_id,liked_by_id=request.user.id)
                l.save()
                change_txt="unlike"
            likes= Like.objects.filter(post_id=p_id).count()
            return JsonResponse({'total_likes':likes,'change_txt':change_txt})
       
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CommentPost(request):
    if request.method == 'POST':
        user = request.user
        c_text = request.POST.get('c_text')
        p_id = request.POST.get('p_id')
        c_id = request.POST.get('c_id','')
        print(c_text,p_id,">>>",c_id,user)
        if not p_id or not c_text:
            return JsonResponse({'error': 'Post ID and comment text are required.'}, status=400)
        try:
            c = Comment.objects.create(post_id=p_id, comment_by_id=user.id, c_text=c_text)
            print(c)
            if c_id !='':
                comment=Comment.objects.filter(id=c_id).first()
                if c_id:
                    print("here")
                    c.recomment = comment
            c.save()
            comments = Comment.objects.filter(post_id=p_id).count()
            # recomments = list(Comment.objects.filter(post_id=p_id,recomment_id=c_id).values())
            
            return JsonResponse({'total_comments': comments}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
