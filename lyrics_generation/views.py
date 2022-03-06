from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from .forms import LyricsForm
from django.views.decorators.cache import never_cache
from dotenv import load_dotenv
from pycantonese import characters_to_jyutping, parse_jyutping
import os
from .needleman_wunsch import *
from transformers import BertTokenizer, BartForConditionalGeneration
from transformers import Text2TextGenerationPipeline
from django.templatetags.static import static
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/Takalo/bart-tone2cantopop"
headers = {"Authorization": os.getenv("huggingface_token")}


def tone_accuracy(list1, list2):
    correct = 0
    list1 = list1.strip().replace("\u200b", "").split()
    list2 = list2.strip().replace("\u200b", "").split()
    print(list1)
    print(list2)
    for tone1, tone2 in zip(list1, list2):
        if tone1 == tone2:
            correct += 1
    return correct/len(list1)


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def preload():
    tokenizer = BertTokenizer(vocab_file='model/vocab.txt')
    model = BartForConditionalGeneration.from_pretrained(
        "model/checkpoint-54000")
    text_generator = Text2TextGenerationPipeline(model, tokenizer)
    return tokenizer, model, text_generator


def index(request):
    tokenizer, model, text_generator = preload()
    if request.method == 'POST':
        form = LyricsForm(request.POST)
        if form.is_valid():
            input_text = ""
            for char in form.cleaned_data['tone']:
                if(char == '\r'):
                    continue
                if(char == '\n'):
                    input_text += "\\ n "
                else:
                    input_text += char
                    input_text += " "
            input_tone = ' '.join(input_text.split()).replace('\\ n ', '\n')
            output = [text_generator([input_text], do_sample=True) for i in range(
                int(form.cleaned_data['number_of_sample']))]
            """ output = [query({
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
            }) for i in range(int(form.cleaned_data['number_of_sample']))] """
            lyrics_list = []
            #accuracy = []
            for lyrics in output:
                lyrics_word = lyrics[0]['generated_text'].replace(
                    '\\ n ', '\n').replace("\\ n", "\n")
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
                        'tone': lyrics_tone,
                        'accuracy': tone_accuracy(input_tone, lyrics_tone)

                    })
                print(tone_accuracy(input_tone, lyrics_tone))
                #accuracy.append(tone_accuracy(input_tone, lyrics_tone))
        else:
            form = LyricsForm()
            lyrics_list = []
    else:
        #requests.post(API_URL, headers=headers)
        form = LyricsForm()
        lyrics_list = []
        input_tone = []

 
    return render(request, 'index.html', {'form': form, 'output': lyrics_list, 'input': input_tone})
