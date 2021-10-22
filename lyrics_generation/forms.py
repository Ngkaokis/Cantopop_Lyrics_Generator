from django import forms


class LyricsForm(forms.Form):
    starting = forms.CharField(label="starting sentence", max_length=200)
    number_of_sample = forms.CharField(
        label="number of sample (max 5)", max_length=5)
