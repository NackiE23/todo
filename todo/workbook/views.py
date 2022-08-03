from django.http import HttpResponse
from django.shortcuts import render


def main(request):
    return HttpResponse('<a href="swagger-ui"><h1>Swagger-ui</h1></a>')
