from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from blog.models import Document, Post, AuthorApply, QAnswer, CustomProfile, QA




class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomProfile
        fields = ('location', 'job','uni','talents','first_name','last_name','avatar')



class QAForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = ('title', 'body','fixed')


class QAnswerForm(forms.ModelForm):
    class Meta:
        model = QAnswer
        fields = ('body',)


class AuthorApplyForm(forms.ModelForm):
    class Meta:
        model = AuthorApply
        fields = ('name','surname','job','job_talents','uni','rustudent','text')



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body','allow_comments','category')



        # def __init__(self, *args, **kwargs):
        #     super(DocumentForm, self).__init__(*args, **kwargs)
        #     self.fields['document'].widget.attrs.update({'class': 'custom-file-input'})
        #     self.fields['category'].widget.attrs.update({'class': 'custom-select'})




class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('category', 'document','dataset_title','file_name','first_5_row','path' )

        # def __init__(self, *args, **kwargs):
        #     super(DocumentForm, self).__init__(*args, **kwargs)
        #     self.fields['document'].widget.attrs.update({'class': 'custom-file-input'})
        #     self.fields['category'].widget.attrs.update({'class': 'custom-select'})


class SignInForm(UserCreationForm):
    kullanici_adi = forms.CharField(max_length=30, required=True, help_text='Gerekli.')
    email = forms.EmailField(max_length=254, help_text='Gerekli. ')
    term_agree = forms.BooleanField(error_messages={'required': ("Site kurallarını kabul etmelisiniz.")})
    class Meta:
        model = User
        fields = ('username','email','password')



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opsiyonel.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opsiyonel.')
    email = forms.EmailField(max_length=254, help_text='Gerekli. ')
    term_agree = forms.BooleanField(error_messages={'required': ("Site kurallarını kabul etmelisiniz.")})
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','term_agree' )