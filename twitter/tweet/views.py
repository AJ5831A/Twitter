from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm , UserRegistrationForm
from django.shortcuts import redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def index(request):
    return render(request , 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request , 'tweet_list.html' , {'tweets' : tweets})
#   'tweets'	Variable name available inside the template
#   tweets	Actual TweetForm object being passed from the view



@login_required
def tweet_create(request):
    if request.method == "POST": 
        form = TweetForm(request.POST , request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False) # create the tweet but not add it to the database
            tweet.user = request.user # set the user
            tweet.save() # save the tweet
            return redirect('tweet_list') # redirect to tweet list
    else:
        form = TweetForm() # create an empty form
    return render(request , 'tweet_form.html' , {'form' : form}) # renders the form template
#request: contains the HTTP request info (like method, user, etc.)
#'tweet_form.html': the HTML template to render
#{'form': form}: context dictionary → makes form available as a variable inside the template


@login_required
def tweet_edit(request , tweet_id):
    tweet = get_object_or_404(Tweet , pk=tweet_id , user = request.user)
    if request.method == "POST":
        form = TweetForm(request.POST , request.FILES , instance=tweet)
        if form.is_valid():
            tweet = form.save()
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request , 'tweet_form.html' , {'form' : form})
#When you initialize a form with instance=tweet, you're telling Django:
#"Here is an existing object. Use its current field values to fill in the form fields, and when saving, update this object instead of creating a new one."


@login_required
def tweet_delete(request , tweet_id):
    tweet = get_object_or_404(Tweet , pk = tweet_id , user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request , 'tweet_confirm_delete.html' , {'tweet' : tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request , user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request , 'registration/register.html' , {'form' : form})

