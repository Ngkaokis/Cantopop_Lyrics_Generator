from django import forms


class LyricsForm(forms.Form):
    tone = forms.CharField(
        widget=forms.Textarea(
            attrs={'style': 'height: 20rem; width: 20rem', 'label': "tone", 'max_length': 200}))
    number_of_sample = forms.IntegerField(
        label="number of sample (max 5)", max_value=5, min_value=1)
    """ top_k = forms.IntegerField(
        label="top_k", required=False)
    top_p = forms.FloatField(
        label="top_p", required=False)
    temperature = forms.FloatField(
        label="temperature", required=False)
    repetition_penalty = forms.FloatField(
        label="repetition_penalty", required=False)
 """
