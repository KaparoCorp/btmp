from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default=" ")

class Tags(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default=" ")

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='item_photos/')
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2)
    suggestions = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    description = models.TextField()
    appraisal_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    #tags = models.ForeignKey(Tags, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):

        return self.photo, f"{self.category} - {self.price} Ksh"

class Appraisal(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    market_trend_value = models.DecimalField(max_digits=10, decimal_places=2)
    community_votes = models.IntegerField(default=0)
    admin_input = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Exchange(models.Model):
    item_from = models.ForeignKey(Item, related_name='item_from', on_delete=models.CASCADE)
    item_to = models.ForeignKey(Item, related_name='item_to', on_delete=models.CASCADE)
    proposed_value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])
    created_at = models.DateTimeField(auto_now_add=True)

class Escrow(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    item_held = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_user = models.ForeignKey(User, related_name='rated_user', on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def edit_rating(self, score, comment):
        self.score = score
        self.comment = comment
        self.save()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)