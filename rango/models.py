from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, False)
    website = models.URLField(blank=True)
    picture = models.ImageField(blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'

    def fetchuserprofile(self, userx):
        user = User.objects.get(username=userx)

        try:
            userprofile = UserProfile.objects.get(user=user)
        except:
            userprofile = None

        return user, userprofile


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Page(models.Model):
    category = models.ForeignKey(Category, False)
    title = models.CharField(max_length=128, unique=True)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'pages'
