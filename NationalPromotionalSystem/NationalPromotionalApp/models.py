from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Media(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]
    
    file = models.FileField(upload_to='media/')
    title = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def str(self):
        return self.title or self.file.name

class brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField(unique=True, region="",blank=True)
    def str(self):
        return self.name

class product(models.Model):
    
    name = models.CharField(max_length=200)
    features = models.TextField()
    benefits = models.TextField()
    product_url = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    identityNo = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f" - {self.name}"

class service(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=100, blank=True, null=True)
    price_range = models.CharField(max_length=100, blank=True, null=True)
    service_type = models.CharField(max_length=100, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, region="",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.brand.name} - {self.name}"


    

class News(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    content = models.TextField()
    source = models.CharField(max_length=255, blank=True, null=True)
    published_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    

    def str(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    target_audience = models.CharField(max_length=255, blank=True, null=True)  # e.g. 'Developers', 'Designers',specific woreda users....
    valid_until = models.DateField(blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   

    def str(self):
        return self.title
class Event(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('hackathon', 'Hackathon'),
        ('recognition', 'Recognition Program'),
    ]

    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField()
    start_date = models.DateTimeField()
    
    deadline= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    target_audience = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    registration_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.title} ({self.event_type})"
class CompetitionDetail(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='competition_detail')
    judging_criteria = models.TextField(blank=True, help_text="Criteria used to judge the competition")
    prize = models.CharField(max_length=255, blank=True, null=True, help_text="Prize awarded to the winner(s)")
    winner_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the winner or winning team")
    winner_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Final score or rating of the winner")
    announcement_date = models.DateField(blank=True, null=True, help_text="Date when the winner was announced")

    def str(self):
        return f"Competition Details - {self.event.title}"

    
class JobAnnouncement(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
    ]

    title = models.CharField(max_length=255)
    company = models.ForeignKey(brand, on_delete=models.SET_NULL, null=True, blank=True)  # optional external brand
    department = models.CharField(max_length=150, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPES, default='full_time')
    description = models.TextField()
    requirements = models.TextField()
    no_of_vacancies= models.IntegerField(blank=True,null=True)
    gender= models.CharField(max_length=50,default='both')
    position = models.TextField(blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    application_link = models.URLField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    media = models.ManyToManyField(Media, blank=True, related_name='job_media')

    def str(self):
        return f"{self.title} - {self.company.name if self.company else 'Teamwork IT'}"

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=255, blank=True, null=True)
    post_caption = models.TextField(blank=True, null=True)
    time_limit= models.IntegerField(default=10)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    media = models.ManyToManyField(Media, related_name='posts', blank=True)
    status = models.CharField(max_length=20, default='draft')

    is_fixed = models.BooleanField(default=False)   
    fixed_until = models.DateTimeField(blank=True, null=True)  

    def str(self):
        return f"Post: {self.content_type} - {self.user.username}"

    class Meta:
        ordering = ['-is_fixed', '-post_date']  
    
class PostView(models.Model):
    post = models.ForeignKey('post', on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"View on {self.post.id} by {self.user or self.ip_address}"
    
class PostComment(models.Model):
    post = models.ForeignKey('post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Comment by {self.user} on {self.post}"

class PostReaction(models.Model):
    REACTION_TYPES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    post = models.ForeignKey('post', on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES, default='like')
    reacted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # One reaction per user per post

    def str(self):
        return f"{self.user} reacted {self.reaction_type} on {self.post.id}"

class PostShare(models.Model):
    post = models.ForeignKey('post', on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    shared_to = models.CharField(max_length=100, blank=True, null=True)  # e.g. 'Facebook', 'Telegram', 'Internal'
    shared_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user} shared {self.post} to {self.shared_to or 'Internal'}"

class PostRating(models.Model):
    post = models.ForeignKey('post', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5 stars
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Each user can rate a post only once
        indexes = [
            models.Index(fields=['post']),
        ]

    def str(self):
        return f"{self.user.username} rated {self.post.id} - {self.rating}★"




class PostAnalytics(models.Model):
    post = models.OneToOneField('post', on_delete=models.CASCADE, related_name='analytics')
    total_views = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    total_reactions = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    
    last_updated = models.DateTimeField(auto_now=True)

    def update_stats(self):
        # Count all
        self.total_views = self.post.views.count()
        self.total_comments = self.post.comments.count()
        self.total_reactions = self.post.reactions.count()
        self.total_shares = self.post.shares.count()
        self.total_ratings = self.post.ratings.count()

        # Calculate average rating
        ratings = self.post.ratings.all().values_list('rating', flat=True)
        self.average_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0.0
        self.save()

    def str(self):
        return f"Analytics for {self.post.id}"
      
class ChatRoom(models.Model):
    ROOM_TYPES = [
        ('private', 'Private Chat'),
        ('group', 'Group Chat'),
        ('announcement', 'Announcement Channel'),
    ]
    
    name = models.CharField(max_length=255, blank=True, null=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='private')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_rooms')
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        if self.room_type == 'private':
            return f"Private Chat {self.id}"
        return self.name or f"Group {self.id}"