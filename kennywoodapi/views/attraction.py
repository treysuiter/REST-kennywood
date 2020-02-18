from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction

class AttractionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Attraction
        url = serializers.HyperlinkedIdentityField(
            view_name='attraction',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'area')

class Attractions(ViewSet):

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single attraction

        Returns:
          Response - JSON serialized instance
        """
        try:
            attraction = Attraction.objects.get(pk=pk)
            serializer = AttractionSerializer(attraction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to park attractions

        Returns:
          REsponse - JSON serialized list of park attraction

        """
        attractions = Attraction.objects.all()

        #How to declare a query parameter; returns default value of None if not there
        area = self.request.query_params.get('area', None)

        if area is not None:
            #how to access the id of a realted instance with dunders
            attractions = attractions.filter(area__id=area)

        serializer = AttractionSerializer(attractions, many=True, context={'request': request})
        return Response(serializer.data)

