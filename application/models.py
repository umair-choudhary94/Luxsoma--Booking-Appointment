from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='services/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"

class Appointment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    )

    COMPLETION_STATUS_CHOICES = (
        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    completion_status = models.CharField(max_length=20, choices=COMPLETION_STATUS_CHOICES, default='Incomplete')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.price = self.service.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment for {self.user.username} - {self.service.title}"

class StripeToken(models.Model):
    token_id = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class CreditCard(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    exp_month = models.CharField(max_length=2)
    exp_year = models.CharField(max_length=4)
    cvc = models.CharField(max_length=4)


