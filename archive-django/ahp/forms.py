from django import forms


class CriteriaSelection(forms.Form):
    CRITERIA_LIST = (('summer_high', 'Summer high'),
                     ('winter_low', 'Winter low'),
                     ('pollen', 'Pollen'),
                     ('humidity', 'Humidity'),
                     ('unemployment', 'Unemployment'),
                     ('crime_rate', 'Crime rate'),
                     ('median_income', 'Median income'),
                     ('walkability', 'Walkability'),
                     ('parkland', 'Parkland'))
    criteria = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=CRITERIA_LIST)
