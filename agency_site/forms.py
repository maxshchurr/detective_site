from django.forms import forms, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Clients, Orders, Employees, Tasks
import datetime


class ExtendedUserCreationForm(UserCreationForm):

    username = forms.CharField(label='Username', max_length=30, required=True)
    email = forms.EmailField(max_length=50, required=True)


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=True)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class ClientProfileForm(ModelForm):

    class Meta:
        model = Clients
        fields = ('full_name', 'tel_number')


class TestClientLogin(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class TestCreateOrder(ModelForm):
    class Meta:
        model = Orders
        fields = ['client_comment', 'type_of_order']


class AcceptOrder(ModelForm):
    class Meta:
        model = Orders
        fields = ['rate', 'status']


class ManagerTakeOrder(ModelForm):
    class Meta:
        model = Orders
        fields = ['rate']


class DateInput(forms.DateInput):
    input_type = 'date'


class CalculateIncomeForPeriod(forms.Form):
    current_date = datetime.date.today()
    start_date = forms.DateField(widget=DateInput(), required=True)
    end_date = forms.DateField(widget=DateInput(), required=True)


class DetectiveAssignTask(ModelForm):
    assistant = forms.ModelChoiceField(queryset=Employees.objects.filter(position='Assistant'),
                                       label='Выберите помощника:')

    class Meta:
        model = Tasks
        fields = ['task_description']


