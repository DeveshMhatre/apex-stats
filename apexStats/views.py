from django.shortcuts import render

from .forms import StatForm
def landing(request):
    if request.method == 'POST':
        form = StatForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    
    form = StatForm()

    context = {
        'form': form
    }
        
    return render(request, 'apexStats/landing.html', context)
