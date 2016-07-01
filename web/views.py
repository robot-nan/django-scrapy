
from django.core import serializers
from web.models import GoldAdvice
from django.http import JsonResponse, HttpResponse

def glod_advice(request):
    last_team_flag =  GoldAdvice.objects.latest('id').show_team
    haha=  GoldAdvice.objects.filter(show_team=last_team_flag)
    json_data = serializers.serialize('json', haha)
    return HttpResponse(json_data)