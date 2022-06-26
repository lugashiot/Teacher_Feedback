from django import forms
import sys
#sys.path.append('/home/pi/Feedback/API')
from SQL_Dataclasses import Question


def format_anwer_opts(question_answer_opts: list) -> list[list[str]]:
    out = []
    for i in range(len(question_answer_opts)):
        out.append([f"{i+1}", question_answer_opts[i]])
    return out


class RatingForm1(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question: Question = kwargs.pop('question')
        super(RatingForm1, self).__init__(*args, **kwargs)
        answer_opts = format_anwer_opts(self.question.question_answer_opts)
        self.fields['rating_1'] = forms.CharField(label=self.question.question_text, required=True)
        if self.question.question_id == 0:
            self.fields['rating_1'].required = False
        self.fields['rating_1'].widget = forms.RadioSelect(choices=answer_opts)


class RatingForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm2, self).__init__(*args, **kwargs)
        answer_opts = format_anwer_opts(self.question.question_answer_opts)
        self.fields['rating_2'] = forms.CharField(label=self.question.question_text, required=True)
        if self.question.question_id == 0:
            self.fields['rating_2'].required = False
        self.fields['rating_2'].widget = forms.RadioSelect(choices=answer_opts)
        
    
class RatingForm3(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm3, self).__init__(*args, **kwargs)
        answer_opts = format_anwer_opts(self.question.question_answer_opts)
        self.fields['rating_3'] = forms.CharField(label=self.question.question_text, required=True)
        if self.question.question_id == 0:
            self.fields['rating_3'].required = False
        self.fields['rating_3'].widget = forms.RadioSelect(choices=answer_opts)


class RatingForm4(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm4, self).__init__(*args, **kwargs)
        answer_opts = format_anwer_opts(self.question.question_answer_opts)
        self.fields['rating_4'] = forms.CharField(label=self.question.question_text, required=True)
        if self.question.question_id == 0:
            self.fields['rating_4'].required = False
        self.fields['rating_4'].widget = forms.RadioSelect(choices=answer_opts)


class RatingForm5(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm5, self).__init__(*args, **kwargs)
        answer_opts = format_anwer_opts(self.question.question_answer_opts)
        self.fields['rating_5'] = forms.CharField(label=self.question.question_text, required=True)
        if self.question.question_id == 0:
            self.fields['rating_5'].required = False
        self.fields['rating_5'].widget = forms.RadioSelect(choices=answer_opts)


class RatingForm6(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(RatingForm6, self).__init__(*args, **kwargs)
        answer_opts = format_anwer_opts(self.question.question_answer_opts)
        self.fields['rating_6'] = forms.CharField(label=self.question.question_text, required=True)
        if self.question.question_id == 0:
            self.fields['rating_6'].required = False
        self.fields['rating_6'].widget = forms.RadioSelect(choices=answer_opts)


class Textfield_Form(forms.Form):
    text_field = forms.CharField(label=f'', required=False, widget=forms.Textarea(attrs={'class': "form-control", 'rows': 3}))
