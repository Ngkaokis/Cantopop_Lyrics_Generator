from django import forms


class LyricsForm(forms.Form):
    starting = forms.CharField(label="starting sentence", max_length=200)
    number_of_sample = forms.IntegerField(
        label="number of sample (max 5)", max_value=5, min_value=1)
    max_output_length = forms.IntegerField(
        label="max output length", required=False)
    top_k = forms.IntegerField(
        label="top_k", required=False)
    top_p = forms.FloatField(
        label="top_p", required=False)
    temperature = forms.FloatField(
        label="temperature", required=False)
    repetition_penalty = forms.FloatField(
        label="repetition_penalty", required=False)
