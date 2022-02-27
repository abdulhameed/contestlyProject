from django import forms
from django.forms import DateInput

from contest.models import Contestant, Contest, Category

# category_choices = Category.objects.all().values_list('name', 'name')
#
# category_choices_list = []
#
# for item in category_choices:
#     category_choices_list.append(item)


class DateInput(forms.DateInput):
    input_type = 'date'


class VoteForm(forms.ModelForm):
    # vote_count = forms.IntegerField(label='Vote')
    class Meta:
        model = Contestant
        fields = ['votes']


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['name', 'photo', 'brief_post', 'post', 'cash_vote', 'vote_cost', 'category', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            # 'category': forms.Select(choices=category_choices_list, attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].widget = DateInput()
        self.fields["end_date"].widget = DateInput()


class ContestantForm(forms.ModelForm):
    class Meta:
        model = Contestant
        fields = ['name', 'title', 'brief_post', 'post', 'photo']
