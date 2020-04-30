from django import forms

from .models import Tweet


class TweetModelForm(forms.ModelForm):
    content = forms.CharField(label="",
                              widget=forms.Textarea(
                                  attrs={'placeholder': 'Your message',
                                         'class': 'form-control'}))

    class Meta:
        model = Tweet
        fields = [
            'content'
        ]

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 140:
            raise forms.ValidationError("Too long")
        return content
