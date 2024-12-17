from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save


class User(AbstractUser):
  
  username = models.CharField()
  username = models.CharField(
    _("username"),
      max_length=100,
      unique=True,
      help_text=_(
          "Required. 100 characters or fewer."
      ),
      error_messages={
          "unique": _("A user with that username already exists."),
      },
  )
  otp = models.CharField(unique=True, max_length=100)
  email = models.EmailField(unique=True, null=True, blank=True)
  full_name = models.CharField(unique=True, max_length=150, null=True, blank=True)


  def __str__(self):
    return self.email
  
  def save(self, *args, **kwargs):
    email_username, full_name = self.email.split("@")
    # breakpoint()
    if not self.full_name:
      self.full_name = email_username 
    
    if not self.username:
      self.username = email_username 

    super(User, self).save(*args, **kwargs)


class Profile(models.Model):

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = models.FileField(upload_to="user_folder", default="default-user.webp", null=True, blank=True)
  full_name = models.CharField(max_length=150)
  country = models.CharField(max_length=100, null=True, blank=True)
  about = models.TextField(null=True, blank=True)
  create_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    if self.full_name:
      return str(self.full_name)
    else:
      return str(self.user.full_name)
  
  def save(self, *args, **kwargs):
    if not self.full_name:
      self.full_name = self.user.full_name 

    super(Profile, self).save(*args, **kwargs)

  
def create_user_profile(sender, instance, created, **kwargs):
  # Create user to a profile
  if created:
    Profile.objects.create(user=instance)
  
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)