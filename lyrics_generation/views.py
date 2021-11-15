from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from .forms import LyricsForm
from django.views.decorators.cache import never_cache
from dotenv import load_dotenv
from pycantonese import characters_to_jyutping, parse_jyutping
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
            input_text = ""
            for char in form.cleaned_data['starting']:
                input_text += char
                input_text += " "
            output = query({
                "inputs": input_text,
                "parameters": {
                    "num_return_sequences": int(form.cleaned_data['number_of_sample']),
                    "max_new_tokens": int(form.cleaned_data['max_output_length']) if form.cleaned_data['max_output_length'] else None,
                    "top_k": int(form.cleaned_data['top_k']) if form.cleaned_data['top_k'] else None,
                    "top_p": float(form.cleaned_data['top_p']) if form.cleaned_data['top_p'] else None,
                    "temperature": float(form.cleaned_data['temperature']) if form.cleaned_data['temperature'] else 1.0,
                    "repetition_penalty": float(form.cleaned_data['repetition_penalty']) if form.cleaned_data['repetition_penalty'] else None,
                },
                "options": {
                    "use_cache": False,
                    "wait_for_model": True
                }
            })
            lyrics_list = []
            for lyrics in output:
                lyrics_word = lyrics['generated_text'].replace('\\ n', '\n')
                lyrics_tone = ""
                for char in lyrics_word:
                    jyutping = characters_to_jyutping(char)
                    if jyutping:
                        if jyutping[0][1]:
                            char_tone = parse_jyutping(jyutping[0][1])
                            for tone in char_tone:
                                lyrics_tone += tone.tone
                        else:
                            lyrics_tone += char
                    else:
                        lyrics_tone += char
                lyrics_list.append(
                    {
                        'lyrics': lyrics_word,
                        'tone': lyrics_tone
                    })
        else:
            form = LyricsForm()
            lyrics_list = []
    else:
        requests.post(API_URL, headers=headers)
        form = LyricsForm()
        lyrics_list = []

    return render(request, 'index.html', {'form': form, 'output': lyrics_list})
