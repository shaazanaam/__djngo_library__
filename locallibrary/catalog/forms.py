# To create  a forms we impor the forms library
# forms data is stored in the application's forms.py file

from django import forms

import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# remember  from the testing perspective 
# this form has one field which will have a label and the help text which 
# we will need to verify
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        ## this is the step that gets the  data already converted 
        # to a python data object datatime.
        # datetime object by
        ## the Django form system called the DateField widget
        ## the cleaned data is stored in the cleaned_data dictionary
        ## then we call the value of the dictionary as below
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
