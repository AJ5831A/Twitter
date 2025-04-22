from django.db import models # djangos module for building database models (tables)
from django.contrib.auth.models import User
# Create your models here.


#We're creating a Tweet model.
#It will become a table in our database named tweet_tweet (appname_modelname).
#Each class attribute becomes a column, and each instance becomes a row.
class Tweet(models.Model): 

    # User is the built-in Django user model.
    # ForeignKey creates a link to another table.
    user = models.ForeignKey(User , on_delete=models.CASCADE)


    text = models.TextField(max_length=240)

    # upload_to='photos/': Uploaded files will go to /media/photos/
    # blank=True: You can leave it empty in forms.
    # null=True: You can store NULL in the database.
    photo = models.ImageField(upload_to='photos/' , blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
    # This method defines the string representation of the model.
    # When you print a Tweet object (or view it in Django admin), it will show:
    # username - first 10 chars of tweet