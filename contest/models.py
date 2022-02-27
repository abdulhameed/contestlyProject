from datetime import datetime

import pytz
from django.db import models
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=26)
    tag = models.CharField(max_length=200, default='none')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contest-list')

    class Meta:
        verbose_name_plural = 'Categories'


class Contest(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField(default='contest_art/default.png', upload_to='contest_art')
    brief_post = models.TextField(blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    cash_vote = models.BooleanField(default=False)
    vote_cost = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contest:results', kwargs={'pk': self.pk})

    @property
    def days_left(self):
        tz = pytz.timezone('Africa/Lagos')
        today = datetime.now(tz=tz)
        ed = self.end_date
        days_left = today - ed
        if ed is None:
            return '0'
        else:
            return days_left.days

    @property
    def has_expired(self):
        tz = pytz.timezone('Africa/Lagos')
        today = datetime.now(tz=tz)
        ed = self.end_date
        if ed is None:
            return '0'
        else:
            if today > ed:
                return True
            else:
                return False


class Contestant(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='participating_contest')
    name = models.CharField(max_length=30, blank=True, null=True)
    photo = models.ImageField(default='contestant_art/default.png', upload_to='contestant_art')
    title = models.CharField(max_length=50, blank=True, null=True)
    brief_post = models.TextField(blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    votes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contest:contestant-detail', kwargs={'pk': self.pk})

