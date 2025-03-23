from django.db import models
from django.contrib.auth.models import AbstractUser
from django. urls import reverse



class User(AbstractUser):
   email = models.EmailField(null =True, unique=True, max_length=100)
   address=models.CharField(max_length=255,null=True,blank=True)
   date_registered = models.DateTimeField(auto_now_add=True, null=True)
   reffered_by = models.ForeignKey("self", on_delete= models.CASCADE, blank=True, related_name="refferals",null=True)
   referal_wallet = models.DecimalField(max_digits=10, decimal_places= 2, default= 0.00)
   image=models.ImageField(upload_to="images",null=True,blank=True,)
   
   def get_refferal_link(self):
    return f"http://127.0.0.1:8000/ref={self.username}"
#creating categories
class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name




#creating blog posts
class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    Genres_choices = (
         ("Gospel", "Gospel"),
         ("R&B", "R&B"),
         ("Pop", "Pop"),
         ("Rock", "Rock"),
         ("Jazz", "Jazz"),
         ("Country", "Country"),
         ("Reggae", "Reggae"),
         ("Blues", "Blues"),
         ("Others", "Others"),
         ("Electronic", "Electronic"),
         
         
    )
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=255,null=True,blank=True)
    body = models.TextField(null=True)
    published= models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories', null=True,blank=True) 
    image=models.ImageField(upload_to="images",null=True,blank=True,)
    slug = models.SlugField(default="",max_length=200,unique=True, blank=True)#slug for urls
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, 
       default='published')
    upload_song = models.FileField(upload_to="audio",null=True,blank=True)
    branded_dp = models.ImageField(upload_to="branded_dps/", blank=True, null=True)
    meta_keywords = models.CharField(max_length=255,help_text='Comma-delimited set of SEO keywords for meta tag',null=True) 
    meta_description = models.CharField(max_length=255,help_text='Content for description meta tag',null=True)
    genres = models.CharField(max_length=50,choices= Genres_choices, default="Others")
 
    class Meta: 
        verbose_name_plural="Posts"

    def __str__(self):
        return self.title
    #the slug to article details
    def get_absolute_url(self):
        return reverse("post_details", kwargs={"slug": self.slug})    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete= models.CASCADE, null=True, related_name="postcomment")
    name = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.name} commented on {self.post}"

class replycomment(models.Model):
    comment = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE, related_name="replycomm")
    name = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.name} reply on {self.comment} "
    
    #promoted songs
class promotedsongs(models.Model):
    post = models.ForeignKey(Post,on_delete= models.CASCADE, null=True, related_name="promotedsong")
    slug = models.SlugField(default="",max_length=200,unique=True)#slug for urls
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return f"{self.post.title} promoted"
    
#popular posts
class popularpost(models.Model):
    post = models.ForeignKey(Post,on_delete= models.CASCADE, null=True, related_name="popularposts")
    slug = models.SlugField(default="",max_length=200,unique=True)#slug for urls
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __(self):
        return f"{self.post} "

class trendingsongs(models.Model):
    post = models.ForeignKey(Post,on_delete= models.CASCADE, null=True, related_name="trendingsongs")
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.post}"
    
# newsletter subscription

class newsletter(models.Model):
    email = models.EmailField(null=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.email} subscribed to newsletter'
   
# SongPlay model to track the number of plays
class SongPlay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="usersongplay")
    song = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, related_name="songplay")
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} played {self.song.title} at {self.played_at}"
    
# SongDownload model to track the number of downloads
class SongDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="usersongdownload")
    song = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, related_name="songdownload")
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} downloaded {self.song.title} at {self.downloaded_at}"
    
# songlikes

class songlike(models.Model):
    song = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, related_name="songlike")
    like = models.BooleanField (default=False,null=True)
    
    def __str__(self):
        return f"{self.like} on {self.song}"
