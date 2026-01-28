from django.db import models

#Categories of Product
class Category(models.Model):
    name= models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    
    #This changes the name "Categorys" to "Categories" in DB.
    class Meta:
        verbose_name_plural = 'Categories'


#All of our products
class Product(models.Model):
    name= models.CharField(max_length=100,unique=True)
    price= models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category= models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
    description= models.CharField(max_length=250, default="", blank=True, null=True)
    image= models.ImageField(upload_to='product/')

    #add sales
    is_sale= models.BooleanField(default=False)
    sale_price= models.DecimalField(default=0, decimal_places=2, max_digits=10)
    out_of_stock= models.BooleanField(default=False)
    on_stock = models.PositiveIntegerField(default=0, help_text='Available quantity in stock')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.out_of_stock = self.on_stock == 0
        super().save(*args, **kwargs)
    

    @property
    def savings(self):
        return self.price - self.sale_price


# Homepage Models
class Carousel(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='carousel/')
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Carousels'
    
    def __str__(self):
        return self.title


class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'About Us'
    
    def __str__(self):
        return self.title


class Stat(models.Model):
    STAT_TYPE_CHOICES = [
        ('customers', 'Happy Customers'),
        ('products', 'Total Products'),
        ('delivered', 'Products Delivered'),
        ('experience', 'Years Experience'),
    ]
    
    stat_type = models.CharField(max_length=20, choices=STAT_TYPE_CHOICES, unique=True)
    value = models.IntegerField()
    label = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=50, default='bi bi-people', help_text='Bootstrap Icon class')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Stats'
    
    def __str__(self):
        return self.get_stat_type_display()


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Testimonials'
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Team Members'
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class Support(models.Model):
    title = models.CharField(max_length=200, default="Get Support")
    description = models.TextField(blank=True, help_text="Brief description about support")
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    working_hours = models.CharField(max_length=200, blank=True, help_text="e.g., Mon-Fri: 9AM-6PM")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Support Information'
    
    def __str__(self):
        return self.title


class KnowledgeBase(models.Model):
    """Simple knowledge base entries to be surfaced by the chatbot.

    - `title`: short human readable title
    - `content`: the HTML/text content to return to the user
    - `keywords`: comma-separated keywords to match against the user message
    - `is_active`: toggle visibility
    """
    title = models.CharField(max_length=200)
    content = models.TextField(help_text='The content that the chatbot will return (can include simple HTML).')
    keywords = models.CharField(max_length=300, blank=True, help_text='Comma-separated keywords to match user messages')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Knowledge Base'

    def __str__(self):
        return self.title
