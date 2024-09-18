from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404notfound.html', status=404)
