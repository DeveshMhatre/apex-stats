from django import forms

class StatForm(forms.Form):
    PLATFORMS = (
        ('origin', 'PC'),
        ('xb1', 'Xbox'),
        ('psn', 'PS4'),
    )

    platform = forms.ChoiceField(
        choices=PLATFORMS,
        label='Platform:',
        widget=forms.Select(
            attrs={
                'class': 'form__input--field'
            }
        )
        )

    alias = forms.CharField(
        max_length=16,
        label='Alias:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your account id',
                'class': 'form__input--field'
            }
        )
    )
