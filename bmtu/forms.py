from django import forms

class FollowForm(forms.Form):
    handler = forms.CharField()
