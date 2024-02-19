from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    """Custom user model with additional fields for user type and profile (optional)."""

    USER_TYPE_CHOICES = (
        ('provider', 'Service Provider'),
        ('consumer', 'Service Consumer'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    profile_image = models.ImageField(upload_to='profiles/', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Token-related fields
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    token_expiration = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.username


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='provider_profile')
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    id_photograph = models.ImageField(upload_to='provider_id_photos/')
    self_photograph = models.ImageField(upload_to='provider_self_photos/')
    service_type = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='consumer_profile')
    full_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='consumer_photos/', blank=True)

    def __str__(self):
        return self.user.username