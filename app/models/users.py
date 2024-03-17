# from typing import Any, Iterable, Sequence
# from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
# from django.db import models
# from django.utils import timezone

# class CustomUserManager(UserManager):
#     def _create_user(self, email, password, **extra_field):
#         if not email:
#             raise ValueError('The Email field must be set')
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_field)
#         user.set_password(password)
#         user.save(using=self._db)
        
#         return user
    
#     def create_user(self, email: str | None, password: str | None, **extra_fields : Any) -> Any:
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(email, password, **extra_fields)
    
#     def create_superuser(self, email: str | None, password: str | None, **extra_fields: Any) -> Any:
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self._create_user(email, password, **extra_fields)
    
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=255, blank=True)
#     last_name = models.CharField(max_length=255, blank=True)
    
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)

#     date_joined = models.DateTimeField(default=timezone.now)
#     last_login = models.DateTimeField(blank=True, null=True)

#     objects = CustomUserManager()
    
#     USERNAME_FIELD = "email"
#     EMAIL_FIELD = "email"
#     REQUIRED_FIELDS = []

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
    
#     def __str__(self) -> str:
#         return self.email
    
#     def get_full_name(self) -> str:
#         return f"{self.first_name} {self.last_name}"
    
#     def get_short_name(self) -> str:
#         return self.first_name
    