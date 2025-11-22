from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
class Media(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ] 
    file = models.FileField(upload_to='media/',blank=True,null=True)
    title = models.CharField(max_length=255, blank=True,null=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES,blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
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
    def __str__(self):
        return self.name
from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=200)
    features = models.TextField()
    benefits = models.TextField()
    product_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)  # when product should expire
    def __str__(self):
        return self.name

    @property
    def is_expired(self):
        """Check if product is expired."""
        return self.expires_at and timezone.now() > self.expires_at
class service(models.Model):   
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=100, blank=True, null=True)
    price_range = models.CharField(max_length=100, blank=True, null=True)
    service_type = models.CharField(max_length=100, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, region="",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.brand.name} - {self.name}"
class News(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField(null=True,blank=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    published_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)   
    def __str__(self):
        return self.title
# class Announcement(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     category = models.CharField(max_length=100, blank=True, null=True)
#     target_audience = models.CharField(max_length=255, blank=True, null=True)  # e.g. 'Developers', 'Designers',specific woreda users....
#     valid_until = models.DateField(blank=True, null=True)
#     posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  
    def __str__(self):
        return self.title
class Event(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('hackathon', 'Hackathon'),
        ('recognition', 'Recognition Program'),
    ]
    title = models.CharField(max_length=255,blank=True,null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    start_date = models.DateTimeField(null=True)
    deadline= models.DateTimeField(auto_now_add=False,null=True,blank=True)
    target_audience = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    registration_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.event_type})"
class CompetitionDetail(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='competition_detail')
    judging_criteria = models.TextField(blank=True, help_text="Criteria used to judge the competition")
    prize = models.CharField(max_length=255, blank=True, null=True, help_text="Prize awarded to the winner(s)")
    winner_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the winner or winning team")
    winner_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Final score or rating of the winner")
    # announcement_date = models.DateField(blank=True, null=True, help_text="Date when the winner was announced")
    winner_picture=models.ImageField(upload_to='winner_picture',blank=True,null=True)
    def __str__(self):
        return f"Competition Details - {self.event.title}"   
class JobAnnouncement(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        # ('temporary', 'Temporary'),
    ]

    title = models.CharField(max_length=255)
    # company = models.ForeignKey(brand, on_delete=models.SET_NULL, null=True, blank=True)  # optional external brand
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

    def __str__(self):
        return f"{self.title} - {self.company.name if self.company else 'Teamwork IT'}"

# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey
# class post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
#     post_date = models.DateTimeField(auto_now_add=True)
#     post_title = models.CharField(max_length=255, blank=True, null=True)
#     post_caption = models.TextField(blank=True, null=True)
#     time_limit= models.IntegerField(default=10)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     media = models.ManyToManyField(Media, related_name='posts', blank=True)
#     status = models.CharField(max_length=20, default='draft')
#     is_fixed = models.BooleanField(default=False)   
#     fixed_until = models.DateTimeField(blank=True, null=True)  

#     def __str__(self):
#         return f"Post: {self.content_type} - {self.user.username}"

#     class Meta:
#         ordering = ['-is_fixed', '-post_date']  