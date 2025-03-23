
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from .models import (User,Post,Comment,Category, replycomment,promotedsongs,popularpost,newsletter,SongDownload,SongPlay,
                     songlike, trendingsongs)
from .forms import (PasswordResetRequestForm, CustomSetPasswordForm)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.core.paginator import Paginator

from django.http import JsonResponse

FRAME_PATH = "media/images/wanjos.jpg"

def index(request):
    #display ten recent post
    recentposts = Post.objects.all().order_by("-published")[:10]
    #trending songs
    trending = trendingsongs.objects.all().order_by("-date_added")[:10]
    # display five promoted songs
    promotedsongsdisplay = promotedsongs.objects.all().order_by("-date_added")[:10]
     # display five popular songs
    popularsongsdisplay = popularpost.objects.all().order_by("-date_added")[:10]
    context ={"recentposts":recentposts, "promotedsongs":promotedsongsdisplay,"popularsongsdisplay":popularsongsdisplay,
              "trending":trending
    }
    return render(request, "index.html", context)


def register_view(request):
    referal_username = request.GET.get("ref") # getting username from
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
       
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email = email,
            address = address,
          
           
        )
        #encript password
        user.set_password(password)
        if referal_username:
            try:
                referer = User.objects.get(username= referal_username)
                user.reffered_by = referer
            except User.DoesNotExist:
                messages.error(request, "Invalid Referal Link")
        
        #save user
        user.save()
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/login/')
    
    # Render the registration page template (GET request)
    return render(request, 'user/register.html', {"referal_username": referal_username})

# logiin user
def login_view(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('login')
        user = authenticate(username=username, password=password) 
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('login')
        else:
            login(request,user)
            return redirect("index")
    return render(request, 'user/login.html')
# logout user

def logout_view(request):
    logout(request)
    return redirect('/login/')

#fogort password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'user/change_password.html', {'form': form})

def password_change_done(request):
    return render(request, 'user/change_password_done.html')

# Password reset request view
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    subject = "Password Reset Requested"
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    domain = get_current_site(request).domain
                    reset_link = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
                    reset_url = f'https://{domain}{reset_link}'
                    message = f"Click the link below to reset your password: {reset_url}"
                    send_mail(subject, message, 'josephwandiyahyel3@gmail.com', [email])
                return redirect("password_reset_done")
            else:
                return HttpResponse("Please you are not our User")
    else:
        form = PasswordResetRequestForm()
    return render(request, "user/password_reset_request.html", {"form": form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(get_user_model(), pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect("password_reset_complete")
        else:
            form = CustomSetPasswordForm(user)
        return render(request, "user/password_reset_confirm.html", {"form": form})
    else:
        return render(request, "user/password_reset_invalid.html")
    
def password_reset_complete(request):
    return render(request, "user/password_reset_complete.html") 

def password_reset_done(request):
    return render(request, "user/password_reset_done.html")  

#get post by user

def userposts(request):
    user = request.user
    userpost = Post.onjects.filter(user=user)
    context = {"userpost":userpost}
    return render (request, "user/posts.html",context)

#get post by category

def postbycategory(request, category ):
    
    categoryposts = Post.objects.filter(categories = category)
    context ={"categoryposts":categoryposts}
    return render(request, "categorypost.html", context)
#get all posts

def allposts(request):
    allpost = Post.objects.all()
    paginator = Paginator(allpost, 10) #number of songs per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context ={"allpost":page_obj}
    return render(request, "allposts.html",context)
# get post details
def postdetails(request, slug):
    postde = Post.objects.get(slug = slug)
    postdetail = Post.objects.filter(slug = slug)
    pastecomments = Comment.objects.filter(post =postde).order_by("-date_added")[:10]
    related_songs = Post.objects.filter(title__icontains = postdetail)[:5]
    context = {"postdetail":postde,"pastecomments":pastecomments,"related_songs":related_songs}
     # collect and store comments on each post
    if request.method =="POST":
        post_id = request.POST.get("post_id") #get the post id
        name = request.POST.get("name")
        comment = request.POST.get("comment")
        savecomment = Comment.objects.create(post_id =post_id, name = name, content = comment)
        savecomment.save()
        messages.info(request, "Comment added Successfully")
    
    return render(request, "postdetails.html", context)


# save reply comment

def savereply(request,pk):
    commentid = Comment.objects.get(pk = pk)
    getcommentreply = replycomment.objects.filter(comment =commentid) .order_by("-date_added") 
    if request.method =="POST":
       comment_id = request.POST.get("commentid") #get the comment id
       name = request.POST.get("name")
       email = request.POST.get("email")
       comment = request.POST.get("comment")
       savereplycomment = replycomment.objects.create(comment_id = comment_id, name = name, email = email,content = comment)
       savereplycomment.save()
       messages.info(request, " Replied Successfully")
    context = {"getcommentreply":getcommentreply} 
    return render(request, "postdetails.html", context)

# search posts, user, artist, description and category
def search(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        searched = Post.objects.filter(title__icontains = searched)
        return render(request, "search.html",{"searched":searched})
    else:
        return render(request, "search.html")

#new letter subscriptions

def newsletterView(request):
    if request.method =="POST":
        email = request.POST.get("email")
        saveemail = newsletter.objects.create(email=email)
        saveemail.save()
        messages.info(request, "succesfullt subscribed to newsletter")
        subject = "Simnawa King News Letter Subscription"
        message = f" {email} Thanks for Subscribing to our Newsletter \n Just stay calmed and wait on our daily Music releases."
        send_mail(subject, message, "josephwandiyahyel3@gmail.com", [email])
    return render(request, "newsletter.html")

#send songs updates to newsletter subscribers

def sendmailtosubscribers(request):
    
    return ""

#allow musician to upload their songs

def musicianuploadsong(request):
    user = request.user
    ref = User.objects.get(username = user)
    referer = ref.reffered_by #GET REFERAL USERNAME
    referal_bonus = 500  
    if request.method == "POST":
       title = request.POST.get("title")  
       body = request.POST.get("body")
       image = request.FILES.get("image")
       song = request.FILES.get("song")
       meta_keywords = request.POST.get("meta_keywords")
       meta_description = request.POST.get("meta_description")
       genres = request.POST.get("genres")
       # add payment gateway here before uploading the song
       savesong = Post.objects.create(user=user,title=title,body=body,image=image, upload_song=song,meta_keywords=meta_keywords, meta_description = meta_description,genres=genres)
       savesong.save()
       referer.referal_wallet += referal_bonus #adding 500 naira to referer
       referer.save()  # save the bonus to the referer
       messages.success(request,"Song uploaded Successfully")
    return render(request, "user/uploadsong.html")

#list of user uploaded songs

def songs(request, username):
    user = User.objects.get(username=username)
    getallsongs = Post .objects.filter(user= user)
    context ={"getallsongs": getallsongs }
    return render(request, "user/songs.html", context)

# Contact us 

def contact_us(request):
    if request.method =="POST":
        subject = request.POST.get("subject")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get(email)
        message = request.POST.get("message")
        send_mail(subject, message, "{email}",["josephwandiyahyel3@gmail.com"])
        messages.info(request, f"Thank you {firstname} {lastname} for contacting Simnawa King! Be calmed as Our agents will reply you to the email you've provided.")
    return render(request, "contactus.html")  
# View for playing a song
@login_required
def play_song(request, song_id):
    song = get_object_or_404(Post, id=song_id)
    # Record the play event
    SongPlay.objects.create(user=request.user, song=song)
    
    # You would have additional logic to play the song (e.g., using a media player)
    return HttpResponse(f"Playing {song.title}...")

# View for downloading a song
@login_required
def download_song(request, song_id):
    song = get_object_or_404(Post, id=song_id)
    # Record the download event
    SongDownload.objects.create(user=request.user, song=song)
    
    # You would have additional logic to serve the file
    response = HttpResponse(song.upload_song, content_type="audio/mpeg")
    response['Content-Disposition'] = f'attachment; filename="{song.title}.mp3"'
    return response



def user_song_stats(request):
    user = request.user
    songs = Post.objects.all()

    song_stats = []
    for song in songs:
        play_count = SongPlay.objects.filter(user=user, song=song).count()
        download_count = SongDownload.objects.filter(user=user, song=song).count()
        song_stats.append({
            'song': song,
            'play_count': play_count,
            'download_count': download_count
        })
    
    return render(request, 'song.html', {'song_stats': song_stats})

#user to like a song

def songslike(request):
    if request.method =="POST":
       songid = request.POST.get("song_id")
       like = request.POST.get("like")
       savelike = songlike.objects.create(song_id = songid,like = like)
    likes = songlike.objects.filter(Post).count()
    print(likes)
    return render(request, "postdetails.html")
@login_required()
def artistprofile(request):
    getuserdetails = User.objects.get(username = request.user)
    # referal_link = get_refferal_link()
    context ={"userdetails":getuserdetails}


    return render(request, "user/profile.html", context)




