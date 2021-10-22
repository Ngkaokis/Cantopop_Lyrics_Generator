from django.shortcuts import render
import requests
from .forms import LyricsForm
from django.views.decorators.cache import never_cache
from dotenv import load_dotenv
import os
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/Takalo/cantopop-model"
headers = {"Authorization": os.getenv("huggingface_token")}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def index(request):
    if request.method == 'POST':
        form = LyricsForm(request.POST)
        if form.is_valid():
            output = query({
                "inputs": form.cleaned_data['starting'],
                "parameters": {
                    "num_return_sequences": int(form.cleaned_data['number_of_sample'])
                }})
            lyrics_list = []
            for lyrics in output:
                lyrics_list.append(
                    lyrics['generated_text'].replace('\\ n', '\n'))
    else:
        form = LyricsForm()
        lyrics_list = []

    return render(request, 'index.html', {'form': form, 'output': lyrics_list})
