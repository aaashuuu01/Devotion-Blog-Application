from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.text import slugify

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('bhagavad_gita', 'Bhagavad Gita Thoughts'),
        ('krishna_lila', 'Krishna Lila'),
        ('bhajans', 'Bhajans and Prayers'),
        ('festivals', 'Festivals and Celebrations')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True) 
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)
    gita_reference = models.CharField(max_length=100, blank=True, null=True) 
    featured_image = models.ImageField(upload_to='images/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager() 
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug =  slugify(self.title) 
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.title)  
        unique_slug = slug
        counter = 1
        
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug

    def __str__(self):
        return self.title
