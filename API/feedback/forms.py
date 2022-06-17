from django import forms

placeholder_question = [['1', 'Placeholder'], ['2', 'Placeholder'], ['3', 'Placeholder'], ['4', 'Placeholder'], ['5', 'Placeholder']]


class RatingForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm1, self).__init__(*args, **kwargs)
        self.fields['rating_1'].widget = forms.RadioSelect(choices=self.question)
    rating_1 = forms.CharField(label=f'Wie gut findest du den Unterricht von dieser Lehrperson?', required=True)

class RatingForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm2, self).__init__(*args, **kwargs)
        self.fields['rating_2'].widget = forms.RadioSelect(choices=self.question)
    rating_2 = forms.CharField(label=f'Wie gut kommst du im Unterricht von dieser Lehrperson mit?', required=True)
    
class RatingForm3(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm3, self).__init__(*args, **kwargs)
        self.fields['rating_3'].widget = forms.RadioSelect(choices=self.question)
    rating_3 = forms.CharField(label=f'Wie verständlich ist der im Unterricht behandelte Stoff?', required=True)

class RatingForm4(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm4, self).__init__(*args, **kwargs)
        self.fields['rating_4'].widget = forms.RadioSelect(choices=self.question)
    rating_4 = forms.CharField(label=f'Wie hoch ist dein (Zeit-)Aufwand zuhause um im Unterricht dabei zu bleiben? (Lernen + Hü)', required=True)

class RatingForm5(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm5, self).__init__(*args, **kwargs)
        if self.question == None:
            self.fields['rating_5'] = forms.CharField(label=f'Placeholder?', required=False)
            self.fields['rating_5'].widget = forms.RadioSelect(choices=placeholder_question)
            return
        
        self.fields['rating_5'] = forms.CharField(label=f'Frage 5 Text?', required=True)
        self.fields['rating_5'].widget = forms.RadioSelect(choices=self.question)

class RatingForm6(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm6, self).__init__(*args, **kwargs)
        if self.question == None:
            self.fields['rating_6'] = forms.CharField(label=f'Placeholder?', required=False)
            self.fields['rating_6'].widget = forms.RadioSelect(choices=placeholder_question)
            return

        self.fields['rating_6'] = forms.CharField(label=f'Frage 6 Text?', required=True)
        self.fields['rating_6'].widget = forms.RadioSelect(choices=self.question)

class Textfield_Form(forms.Form):
    text_field = forms.CharField(label=f'', required=False, widget=forms.Textarea(attrs={'class': "form-control", 'rows': 3}))
    