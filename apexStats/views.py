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
    elif stats['platformInfo']['platformSlug'] == 'xbl':
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

    kills = stats['segments'][0]['stats'].get('kills')
    get_stats(kills, 'kills', context)
    damage = stats['segments'][0]['stats'].get('damage')
    get_stats(damage, 'damage', context)
    killsAs = stats['segments'][1]['stats'].get('kills')
    get_stats(killsAs, 'killsAs', context)
    damageAs = stats['segments'][1]['stats'].get('damage')
    get_stats(damageAs, 'damageAs', context)

    return render(request, 'apexStats/results.html', context)

def get_stats(element, criteria, context):
    if element:
        context[criteria] = element['displayValue']
    else:
        context[criteria] = 0