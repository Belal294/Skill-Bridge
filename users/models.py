from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='buyer', **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = (
#         ('buyer', 'Buyer'),
#         ('seller', 'Seller'),
#     )
    
#     email = models.EmailField(unique=True)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email



class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)  
    first_name = models.CharField(max_length=30, blank=True, null=True)  
    last_name = models.CharField(max_length=30, blank=True, null=True)  
    address = models.CharField(max_length=255, blank=True, null=True) 
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email