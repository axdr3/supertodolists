from django.shortcuts import render, redirect
from .models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm
# Create your views here.


def home_page(request):

	return render(
		request,
		'lists/home.html',
		{'form': ItemForm()}
	)


def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	error = None
	if request.method == 'POST':
		try:
			item = Item(text=request.POST['text'], list=list_)
			item.full_clean()
			item.save()
			# return redirect(f'/lists/{list_.id}/')
			return redirect(list_)
		except ValidationError:
			error = "You can't have an empty list item"

	return render(request, 'lists/list.html', {'list': list_, 'error': error})


def new_list(request):
	# create method already saves list in db
	list_ = List.objects.create()
	item = Item(text=request.POST['text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"
		return render(request, 'lists/home.html', {'error': error})

	# return redirect('/lists/%d/' % (list_.id,))
	return redirect(list_)
