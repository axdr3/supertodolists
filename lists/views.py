from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


def home_page(request):

	return render(
		request,
		'lists/home.html',
		{'form': ItemForm()}
	)


def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	form = ExistingListItemForm(for_list=list_)
	if request.method == 'POST':
		form = ExistingListItemForm(for_list=list_, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(list_)
	return render(
		request,
		'lists/list.html',
		{
		 	'list': list_,
	 		'form': form
	 	}
	)


def new_list2(request):
	form = ItemForm(data=request.POST)
	if form.is_valid():
		list_ = List()
		if request.user.is_authenticated:
			list_.owner = request.user
		list_.save()
		form = ExistingListItemForm(for_list=list_, data=request.POST)
		form.save()
		# TODO:IMPROVE should it be like this?
		return redirect(str(list_.get_absolute_url()))
	else:
		return render(request, 'lists/home.html', {"form": form})


def new_list(request):
	form = NewListForm(data=request.POST)
	if form.is_valid():
		list_ = form.save(owner=request.user)
		return redirect(str(list_.get_absolute_url()))
	return render(request, 'lists/home.html', {'form': form})


def my_lists(request, email):
	owner = User.objects.get(email=email)
	return render(request, 'lists/my_lists.html', {'owner': owner})


def share_list(request, list_id):
	if request.method == 'POST':
		email = request.POST.get('sharee')
		lista = List.objects.get(id=list_id)
		try:
			user = User.objects.all().get(email=email)
			lista.shared_with.add(user)
		except User.DoesNotExist:
			print(f'User does not exist.')
			pass
		return redirect(str(lista.get_absolute_url()))
