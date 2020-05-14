from django import forms


class ContactForm(forms.Form):
    subject   = forms.CharField(label="Nombre Completo", max_length=140)
    email       = forms.EmailField(widget=forms.EmailInput)
    message     = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea,
        max_length=200
    )

    def clean(self):
        data = self.cleaned_data
        subject = data.get('subject')
        from_email = data.get('email')
        message = data.get('message')
        if subject and message and from_email:
            return data
        else:
            raise forms.ValidationError('Todos los campos son requeridos.')