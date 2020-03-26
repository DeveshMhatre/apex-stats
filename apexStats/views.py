from django.shortcuts import render, redirect

import requests

from .forms import StatForm

TRACKER_SITE = 'https://public-api.tracker.gg/v2/apex/standard/profile'
TRACKER_SITE_AUTH = '8ebcd8b1-2cd9-470d-9476-58bd6f313a08'

def landing(request):
    if request.method == 'POST':
        form = StatForm(request.POST)
        if form.is_valid():
            request.session['platform'] = form.cleaned_data['platform']
            request.session['alias'] = form.cleaned_data['alias']
            return redirect('apex:results')
    
    form = StatForm()

    context = {
        'form': form
    }
        
    return render(request, 'apexStats/landing.html', context)

def tracker_results(request):
    response = requests.get(
        f"{TRACKER_SITE}/{request.session['platform']}/{request.session['alias']}",
        headers={'TRN-Api-Key': TRACKER_SITE_AUTH}
    )

    stats = response.json()['data']


    context = {}

    if stats['platformInfo']['platformSlug'] == 'origin':
        context['platform'] = 'PC'
    elif stats['platformInfo']['platformSlug'] == 'xb1':
        context['platform'] = 'Xbox One'
    else:
        context['platform'] = 'PS4'
    player = stats['platformInfo']['platformUserId']
    context['player'] = player
    banner = stats['segments'][1]['metadata']['tallImageUrl']
    context['banner'] = banner
    legend = stats['metadata']['activeLegendName']
    context['legend'] = legend
    level = stats['segments'][0]['stats']['level']['displayValue']
    context['level'] = level
    if stats['segments'][0]['stats']['kills']['displayValue']:
        kills = stats['segments'][0]['stats']['kills']['displayValue']
        context['kills'] = kills
    if stats['segments'][0]['stats']['season4Wins']['displayValue']:
        wins = stats['segments'][0]['stats']['season4Wins']['displayValue']
        context['wins'] = wins
    if stats['segments'][1]['stats']['kills']['displayValue']:
        killsAs = stats['segments'][1]['stats']['kills']['displayValue']
        context['killsAs'] = killsAs
    if stats['segments'][1]['stats']['season4Wins']['displayValue']:
        winsAs = stats['segments'][1]['stats']['season4Wins']['displayValue']
        context['winsAs'] = winsAs

    return render(request, 'apexStats/results.html', context)
