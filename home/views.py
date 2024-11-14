from django.shortcuts import render

def index(request):
    return render(request, 'pages/landing.html')

def checkresult(request):
    return render(request, 'pages/checkresult.html')
