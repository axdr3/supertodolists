from django.http import HttpResponse
from lists.models import List, Item
from .forms import ExistingListItemForm
from lists.forms import (
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
)
import json
from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueTogetherValidator


# Serializers are DRF’s way of converting from Django database models to JSON
# (or possibly other formats) that you can send over the wire:
class ItemSerializer(serializers.ModelSerializer):

    text = serializers.CharField(
        allow_blank=False, error_messages={'blank': EMPTY_ITEM_ERROR}
    )

    class Meta:
        model = Item
        fields = ('id', 'list', 'text')
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=('list', 'text'),
                message=DUPLICATE_ITEM_ERROR
            )
        ]


class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, source='item_set')

    class Meta:
        model = List
        fields = ('id', 'items',)


# A ModelViewSet is DRF’s way of defining all the different ways you can
# interact with the objects for a particular model via your API. Once you tell
# it which models you’re interested in (via the queryset attribute) and how to
# serialize them (serializer_class), it will then do the rest—​automatically
# building views for you that will let you list, retrieve, update, and even
# delete objects.
class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


# A router is DRF’s way of building URL configuration automatically, and
# mapping them to the functionality provided by the ViewSet.
router = routers.SimpleRouter()
router.register(r'lists', ListViewSet)
router.register(r'items', ItemViewSet)


# Own REST api onwards
def list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(
                json.dumps({'error': form.errors['text'][0]}),
                content_type='application/json',
                status=400
            )
    item_dicts = [
        {'id': item.id, 'text': item.text}
        for item in list_.item_set.all()
    ]
    return HttpResponse(
        json.dumps(item_dicts),
        content_type='application/json'
    )
