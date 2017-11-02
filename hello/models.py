# -*- coding: utf-8 -*-
from django.contrib.auth.models import User as StdUser

# Import the basic Django ORM models library
from django.db import models

from django.utils.translation import ugettext_lazy as _

class User(StdUser):

    def __unicode__(self):
        return self.username