from django import forms

from .models import Tweet


class TweetModelForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = [
            'content'
        ]

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content == "":
            raise forms.ValidationError("Can't be empty")
        return content
