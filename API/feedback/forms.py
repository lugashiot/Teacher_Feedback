from django import forms

rates_gut = [('1', 'sehr gut'), ('2', 'gut'), ('3', 'ok'), ('4', 'weniger gut'), ('5', 'nicht gut')]
rates_verst = [('1', 'sehr leicht verständlich'), ('2', 'gut verständlich'), ('3', 'verständlich'), ('4', 'schwer verständlich'), ('5', 'nicht verständlich')]
rates_aufw = [('1', 'sehr gering'), ('2', 'gering'), ('3', 'akzeptabel'), ('4', 'übermäßig'), ('5', 'zu viel')]


class RatingForm1(forms.Form):
    rating_1 = forms.CharField(label=f'Wie gut findest du den Unterricht von dieser Lehrperson?', widget=forms.RadioSelect(choices=rates_gut), required=True)

class RatingForm2(forms.Form):
    rating_2 = forms.CharField(label=f'Wie gut kommst du im Unterricht von dieser Lehrperson mit?', widget=forms.RadioSelect(choices=rates_gut), required=True)
    
class RatingForm3(forms.Form):
    rating_3 = forms.CharField(label=f'Wie verständlich ist der im Unterricht behandelte Stoff?', widget=forms.RadioSelect(choices=rates_verst), required=True)

class RatingForm4(forms.Form):
    rating_4 = forms.CharField(label=f'Wie hoch ist dein (Zeit-)Aufwand zuhause um im Unterricht dabei zu bleiben? (Lernen + Hü)', widget=forms.RadioSelect(choices=rates_aufw), required=True)

class Textfield_Form(forms.Form):
    text_field = forms.CharField(label=f'', required=False, widget=forms.Textarea(attrs={'class': "form-control", 'rows': 3}))