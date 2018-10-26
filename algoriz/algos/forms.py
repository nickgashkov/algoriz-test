from django import forms
from django.apps import apps


class AlgoForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('algos.Algo')
        fields = (
            'name',
            'signal',
            'ticker',
            'trade',
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.update_algo_result()

        if commit:
            instance.save()

        return instance
