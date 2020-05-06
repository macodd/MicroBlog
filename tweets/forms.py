from django import forms

from .models import Tweet


class TweetModelForm(forms.ModelForm):
    content = forms.CharField(label="",
                              widget=forms.Textarea(
                                  attrs={'placeholder': 'Que fuego deseas iniciar?',
                                         'class': 'form-control'}))

    class Meta:
        model = Tweet
        fields = [
            'content'
        ]

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 320:
            raise forms.ValidationError("Muy largo")
        return content
