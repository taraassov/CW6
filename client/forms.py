from django import forms

from client.models import Client, Mailing, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('email', 'fullname', 'comment')


class MailingForm(StyleFormMixin, forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(queryset=None)
    message = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Mailing
        fields = ['period', 'status', 'time', 'next_run', 'clients', 'message']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)
        # self.initial['user'] = user


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ('title', 'content')
