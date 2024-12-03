# IdolPass/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Concert,Ticket
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )

from django import forms
from .models import Concert

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['name', 'date', 'location', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del concierto'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ubicación del concierto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del concierto'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'type': 'file'
            })
        }


from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introduce tu contraseña'
        }),
        label='Contraseña'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        }),
        label='Confirmar Contraseña'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Introduce tu nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Introduce tu correo electrónico'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 1rem;'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 1rem;'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")

        return cleaned_data

from django import forms
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Introduce tu nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Introduce tu correo electrónico'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 1rem;'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 1rem;'
            }),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['concert', 'seat_number', 'price', 'is_sold', 'pdf_file']
        widgets = {
            'concert': forms.Select(attrs={
                'class': 'form-control',
            }),
            'seat_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de asiento',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio del ticket',
            }),
            'is_sold': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 1rem;'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'type': 'file',
            }),
        }