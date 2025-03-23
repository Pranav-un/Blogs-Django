from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Blogger, on_delete=models.CASCADE, related_name='posts')
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='blog_images/%Y/%m/%d/', blank=True, null=True)
    image_caption = models.CharField(max_length=200, blank=True, null=True)
    image_position = models.CharField(
        max_length=20,
        choices=[
            ('left', 'Left'),
            ('right', 'Right'),
            ('center', 'Center'),
            ('full', 'Full Width')
        ],
        default='center'
    )
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('LIKE', 'Like'),
        ('LOVE', 'Love'),
        ('WOW', 'Wow'),
    ]
    
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=4, choices=REACTION_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['post', 'user']

class Poll(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='polls')
    question = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    voters = models.ManyToManyField(User, related_name='voted_polls', blank=True)

    @property
    def total_votes(self):
        return sum(choice.votes for choice in self.choices.all())

    def __str__(self):
        return self.question

class PollChoice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
