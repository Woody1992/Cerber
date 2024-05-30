from typing import Any, Type

from django import forms
from django.forms.utils import ErrorList

from parser.models import InstagramAccount, ACCOUNT_STATUS


class InstagramAccountForm(forms.ModelForm):

    class Meta:
        model = InstagramAccount
        fields = ['username', 'password', 'status']

    def __init__(self, *args, **kwargs):
        print("In form init: ")
        query_dict = args[0]
        query_dict._mutable = True
        print("query_dict: ", query_dict)
        query_dict['status'] = 'active' if query_dict.get('status') == 'on' else 'inactive'
        super().__init__(query_dict, *args, **kwargs)
