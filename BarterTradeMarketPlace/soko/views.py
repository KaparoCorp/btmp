from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Appraisal, Exchange, Rating, Category, User, ActivityLog, Notification, Message
from .forms import ItemForm, AppraisalForm, ExchangeForm, RatingForm, CategoryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import ProfileForm
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_item')
    else:
        form = AuthenticationForm()
    return render(request, 'soko/login.html', {'form': form})


def profile(request):
    return render(request, 'soko/profile.html', {'user': request.user})

def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'soko/edit_profile.html', {'form': form})


def list_item(request):
    def queryer(request):
        query = request.GET.get('q')
        category_id = request.GET.get('category')
        items = Item.objects.all()
        if query:
            items = Item.objects.filter(title__icontains=query)
        else:
            items = Item.objects.all()
        if category_id:
            items = items.filter(category_id=category_id)
        paginator = Paginator(items, 10)  # Show 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        categories = Category.objects.all()  # Fetch all categories for filtering
        return render(request, 'soko/list_items.html', {'page_obj': page_obj, 'query': query, 'categories': categories})
    
    if request.method == 'POST':
        #queryer(request)
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'soko/list_items.html', {'form': form})


def appraise_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = AppraisalForm(request.POST)
        if form.is_valid():
            appraisal = form.save(commit=False)
            appraisal.item = item
            appraisal.save()
            return redirect('item_detail', item_id=item.id)
    else:
        form = AppraisalForm()
    return render(request, 'soko/appraise_item.html', {'form': form, 'item': item})

def propose_exchange(request, item_from_id, item_to_id):
    item_from = get_object_or_404(Item, id=item_from_id)
    item_to = get_object_or_404(Item, id=item_to_id)
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.item_from = item_from
            exchange.item_to = item_to
            exchange.save()
            return redirect('exchange_detail', exchange_id=exchange.id)
    else:
        form = ExchangeForm()
    return render(request, 'soko/propose_exchange.html', {'form': form, 'item_from': item_from, 'item_to': item_to})

def rate_user(request, rated_user_id):
    rated_user = User.objects.get(id=rated_user_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.rated_user = rated_user
            rating.save()
            return redirect('user_profile', user_id=rated_user.id)
    else:
        form = RatingForm()
    return render(request, 'soko/rate_user.html', {'form': form, 'rated_user': rated_user})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_item')
    else:
        form = UserCreationForm()
    return render(request, 'soko/register.html', {'form': form})

def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'soko/notifications.html', {'notifications': user_notifications})

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            ActivityLog.objects.create(user=request.user, action=f'Created item: {item.title}')
            return redirect('list_item')
    else:
        form = ItemForm()
    return render(request, 'soko/create_item.html', {'form': form})

def activity_log(request):
    logs = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'soko/activity_log.html', {'logs': logs})

def propose_exchange(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.item_from = item
            exchange.save()
            Notification.objects.create(
                user=item.user,
                message=f"{request.user.username} has proposed an exchange for your item: {item.title}."
            )
            return redirect('list_item')
    else:
        form = ExchangeForm()
    return render(request, 'soko/propose_exchange.html', {'form': form, 'item': item})

def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.mark_as_read()
    return redirect('notifications')

def edit_rating_view(request, rating_id):
    rating = Rating.objects.get(id=rating_id, user=request.user)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating.edit_rating(form.cleaned_data['score'], form.cleaned_data['comment'])
            return redirect('list_item')
    else:
        form = RatingForm(instance=rating)
    return render(request, 'soko/edit_rating.html', {'form': form})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_item')
    else:
        form = CategoryForm()
    return render(request, 'soko/create_category.html', {'form': form})

def send_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect('list_item')
    return render(request, 'soko/send_message.html', {'recipient': recipient})

def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'soko/inbox.html', {'messages': messages})

def mark_message_read(request, message_id):
    message = Message.objects.get(id=message_id, recipient=request.user)
    message.mark_as_read()
    return redirect('inbox')

def logout_view(request):
    logout(request)
    return redirect('list_item')

