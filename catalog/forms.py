# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 10:08:22 2020

@author: Private
"""

from django import forms

class InputForm(forms.Form):
	"""form that contains all of our questionnaire inputs"""

	#budget input
	player_name = forms.CharField(max_length=100)