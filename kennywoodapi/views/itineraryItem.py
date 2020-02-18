from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction, ParkArea, Itinerary, Customer


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for itineraries

    Arguments:
        serializers
    """
    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction')
        depth = 2

class ItineraryItems(ViewSet):

    """
    Itinerary stuff
    """

    def create(self, request):

        """
        Itinerary create
        """
        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data['starttime']
        new_itinerary_item.customer_id = request.auth.userid
        new_itinerary_item.attraction_id = request.data['attraction_id']

        new_itinerary_item.save()

        serializer = ItinerarySerializer(new_itinerary_item, context={'request': request})
        return Response(serializer.data)
