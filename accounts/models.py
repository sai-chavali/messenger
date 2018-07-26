from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations=True

    def _create_user(self,username,email,password,**extrafields):
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        user=self.model(username=username,email=email,**extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,username,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username,email, password, **extra_fields)

    def create_superuser(self, username,email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email,password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=254,unique=True, null=True)
    email=models.EmailField(unique=True,null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'username'
    EMAIL_FIELD='email'
    objects = UserManager()
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
