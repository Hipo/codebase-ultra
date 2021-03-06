from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('Email'), unique=True, db_index=True)
    username = models.CharField(_('Username'), max_length=150, unique=True)
    first_name = models.CharField(_('First Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255, blank=True)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True, editable=False)
    is_active = models.BooleanField(verbose_name=_('Active Status'), default=True)
    is_staff = models.BooleanField(verbose_name=_('Staff Status'), default=False)
    codebase_id = models.IntegerField(null=True)
    projects = models.ManyToManyField('codebase.Project')
    company = models.CharField(_('Company'), max_length=255, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.first_name