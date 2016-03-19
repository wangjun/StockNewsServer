#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"

from django import forms
from django.utils.translation import ugettext as _


class SingInForm(forms.Form):
    username = forms.CharField(max_length=16, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': _('用户名')}))
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': _("密码")}))

    def clean(self):
        cleaned_data = super(SingInForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return cleaned_data
            else:
                raise forms.ValidationError(_("The password is valid, but the account has been disabled!"))
        else:
            raise forms.ValidationError(_("The username and password were incorrect."))