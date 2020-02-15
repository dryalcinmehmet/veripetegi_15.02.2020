# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from blog.models import Post, Document, AuthorApply, QA, QAnswer, CustomProfile
import datetime
from django.views.generic import TemplateView
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import *

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import pandas as pd
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
import unidecode
from django.http import HttpResponseRedirect
import operator
from django.db.models import Q
from functools import reduce
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.template import RequestContext
from django.template import loader
from django.views.generic import ListView, DateDetailView



class SearchListView(TemplateView):
    ql=''
    template_name = 'search.html'
    post_filter = Post.objects.all()
    document_filter = Document.objects.all()
    paginate_by = 10

    def get(self, request, *args, **kwargs):


        query = self.request.GET.get('q')
        if query:
            query_list = query.split()

            self.post_filter = Post.objects.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(body__icontains=q) for q in query_list))
            )
            self.document_filter = Document.objects.filter(
                reduce(operator.and_,
                       (Q(dataset_title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(file_name__icontains=q) for q in query_list))
            )

        return render(request, self.template_name, {'post_filter': self.post_filter,'document_filter':self.document_filter,'query':query})


class JupyterView(TemplateView):
    template_name = 'dataset/jupyter.html'
    time=timezone.now()

    def get(self, request, *args, **kwargs):
            return render(request,self.template_name,{'embed':'http://0.0.0.0:8890/notebooks/load_data.ipynb'})

class DatasetDetailView(TemplateView):
    template_name = 'dataset/dataset_detail.html'
    time=timezone.now()

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('filename')
        if query:
            document = Document.objects.filter(file_name=query)
            data = pd.read_csv('media/documents/%s'%query)
            # data = data.iloc[:5, :5]
            # table_id = "%s" % post.file_name.split('.')[0]
            data_html = data.to_html(justify="center", border="0.1px")



        return render(request,self.template_name,{'document_list':document,'data_html':data_html})

class DatasetListView(TemplateView):
    template_name = 'dataset/dataset_list.html'
    documents = Document.objects.all().order_by('-publish_date')
    time=timezone.now()

    def get(self, request, *args, **kwargs):

        page = request.GET.get('page', 1)
        paginator = Paginator(self.documents, 5)
        try:
            document = paginator.page(page)
        except PageNotAnInteger:
            document = paginator.page(1)
        except EmptyPage:
            document = paginator.page(paginator.num_pages)

        return render(request,self.template_name,{'document_list':document,'time':self.time,'new_title':'new'})

    def post(self, request):
        if request.method == 'POST':
            category_select=request.POST.getlist('myselect')
            q_objects = Q()
            for item in category_select:
                q_objects.add(Q(category=item), Q.OR)
            print(q_objects)
            documents = Document.objects.filter(q_objects)
            return render(request,self.template_name,{'document_list':documents,'selected_category':category_select})
        else:
            return render(request,self.template_name,{'document_list':self.documents})

class AddDocumentView(TemplateView):
    template_name = 'dataset/add_dataset.html'


    def get(self, request, *args, **kwargs):
        form = DocumentForm()
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)

            if form.is_valid():
                post = form.save(commit=False)

                try:
                    exist_file = Document.objects.get(dataset_title=form.cleaned_data['dataset_title'])
                    return render(request, self.template_name, {'exist_file': exist_file, 'form': form})

                except Document.DoesNotExist:

                    post.publisher = request.user
                    post.publish_date = timezone.now()
                    post.file_name = form.cleaned_data['document'].name
                    post.dataset_title = form.cleaned_data['dataset_title']
                    post.path = 'media/documents/%s'%post.file_name
                    import os
                    data = pd.read_csv(request.FILES["document"] )
                    data = data.iloc[:5, :5]
                    # table_id = "%s" % post.file_name.split('.')[0]
                    data_html = data.to_html(justify="center",border="0.1px")
                    post.first_5_row = data_html
                    # post.document = form.cleaned_data['document']
                    form.save()
                    DatasetListView.as_view()(self.request)
                    return redirect('dataset-list')


        else:
            form = DocumentForm()
        return render(request,self.template_name,{'form':form})

class PostListView(TemplateView):
    template_name = 'blog/post_list_filter.html'
    object_list = Post.objects.all().order_by('-publish')
    time=timezone.now()

    def get(self, request, *args, **kwargs):

        page = request.GET.get('page', 1)
        paginator = Paginator(self.object_list, 10)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        return render(request,self.template_name,{'object_list':object_list,'time':self.time,'new_title':'new'})

    def post(self, request):
        if request.method == 'POST':
            category_select=request.POST.getlist('myselect')
            q_objects = Q()
            for item in category_select:
                q_objects.add(Q(category=item), Q.OR)
            print(q_objects)
            object_list = Post.objects.filter(q_objects)
            return render(request,self.template_name,{'object_list':object_list,'selected_category':category_select})
        else:
            return render(request,self.template_name,{'object_list':self.object_list})

class AddPostView(TemplateView):
    template_name = 'blog/send_post.html'


    def get(self, request, *args, **kwargs):
        form = PostForm()
        edit_or_delete = self.request.GET.get('edit_or_delete')
        title = self.request.GET.get('title')

        if edit_or_delete == 'Düzenle':
            post= Post.objects.filter(author=request.user,title=title)
            return render(request, self.template_name, {'object_list':post,'post_form': form,'edit': True, 'first_title':title})
        elif edit_or_delete == 'Sil':
            post = Post.objects.filter(author=request.user, title=title)
            return render(request, self.template_name,
                          {'object_list': post, 'post_form': form, 'delete': True, 'first_title': title})
        else:
            return render(request, self.template_name,
                          {'post_form': form})


    def post(self, request):
        args = {}
        if request.method == 'POST':
            edit_control= self.request.POST.get('control')
            first_title = self.request.POST.get('first_title')
            form = PostForm(request.POST)
            print(form.is_valid())

            if form.is_valid():
                post = form.save(commit=False)

                if edit_control == "edit":
                    post = Post.objects.get(author=request.user,title=first_title)
                    post.title = form.cleaned_data['title']
                    post.category = form.cleaned_data['category']
                    post.body = form.cleaned_data['body']
                    post.allow_comments = form.cleaned_data['allow_comments']
                    text = unidecode.unidecode(post.title).lower()
                    post.slug = re.sub(r'[\W_]+', '-', text)
                    post.save(update_fields=['title','category','body','allow_comments','slug'])
                    PostListView.as_view()(self.request)
                    return HttpResponseRedirect(post.get_absolute_url())

                elif edit_control == "delete":
                    Post.objects.get(author=request.user,title=first_title).delete()
                    PostListView.as_view()(self.request)
                    return render(request, self.template_name, {'delete_info':True,'first_title':first_title})

                # add-post alanı
                try:
                    exist_blog=Post.objects.get(title=form.cleaned_data['title'])
                    return render(request, self.template_name, {'exist_blog':exist_blog,'post_form': form})

                except Post.DoesNotExist:

                    post.author = request.user
                    post.publish = timezone.now()
                    post.title = form.cleaned_data['title']
                    post.category = form.cleaned_data['category']
                    post.body = form.cleaned_data['body']
                    post.allow_comments = form.cleaned_data['allow_comments']
                    text = unidecode.unidecode(post.title).lower()
                    post.slug=re.sub(r'[\W_]+', '-', text)
                    form.save()
                    PostListView.as_view()(self.request)
                    return HttpResponseRedirect(post.get_absolute_url())

                #

            else:
                print(form.errors)
        else:
            pass
        return PostListView.as_view()(self.request)


class AddQAView(TemplateView):
    template_name = 'q&a/send_question.html'


    def get(self, request, *args, **kwargs):
        form = QAForm()
        edit_or_delete = self.request.GET.get('edit_or_delete')
        title = self.request.GET.get('title')
        id = self.request.GET.get('id')

        if edit_or_delete == 'Düzenle':
            object = QA.objects.get(author=request.user, title=title, id=id)
            return render(request, self.template_name,
                          {'object': object, 'qa_form': form, 'edit': True})
        elif edit_or_delete == 'Sil':
            object = QA.objects.get(author=request.user, title=title, id=id)
            return render(request, self.template_name,
                          {'object': object, 'qa_form': form, 'delete': True})
        else:
            return render(request, self.template_name, {'qa_form': form})





    def post(self, request):
        if request.method == 'POST':

            form = QAForm(request.POST)
            id = self.request.POST.get('id')
            edit_or_save = self.request.POST.get('edit_or_save')

            if form.is_valid():

                if edit_or_save == "edit":

                    post = QA.objects.get(author=request.user, id=id)
                    post.author = request.user
                    post.edit_time = timezone.now()
                    post.title = form.cleaned_data['title']
                    post.body = form.cleaned_data['body']
                    post.fixed = form.cleaned_data['fixed']
                    post.save(update_fields=['author', 'edit_time', 'body', 'title', 'fixed'])
                    return redirect('q&a-list')

                elif edit_or_save == "delete":
                    qa = QA.objects.get(author=request.user,id=id)
                    qa.delete()
                    return render(request, self.template_name, {'delete_info':True,'title':qa.title,'author':qa.author})
                else:
                    post = form.save(commit=False)
                    post.author = request.user
                    post.publish = timezone.now()
                    post.title = form.cleaned_data['title']
                    post.body = form.cleaned_data['body']
                    post.fixed = form.cleaned_data['fixed']
                    form.save()
                    return redirect('q&a-list')
        else:
            form = QAForm()
        return redirect('q&a-list')


class QAListView(TemplateView):
    template_name = 'q&a/QA_list.html'
    object_list = QA.objects.all().order_by('-publish')
    time = timezone.now()

    def get(self, request, *args, **kwargs):

        page = request.GET.get('page', 1)
        paginator = Paginator(self.object_list, 10)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'object_list': object_list})



class QAView(TemplateView):
    template_name = 'q&a/qa-detail.html'


    def get(self, request, *args, **kwargs):
        form = QAnswerForm()
        query_question = self.request.GET.get('title')
        query_id = self.request.GET.get('id')
        object_list = QA.objects.filter(title=query_question)
        answer_list = QAnswer.objects.filter(compare_id=query_id)


        return render(request, self.template_name, {'object_list': object_list, 'form': form, 'answer_list': answer_list})

    def post(self, request):
        query_question = self.request.GET.get('title')
        query_id = self.request.GET.get('id')
        edit_or_save = self.request.POST.get('edit_or_save')
        answer_unique = self.request.POST.get('unique')
        print(query_question,query_id,edit_or_save,answer_unique)
        if request.method == 'POST':
            form = QAnswerForm(request.POST)
            print(form.is_valid())
            print(form.errors)
            if form.is_valid():
                print(edit_or_save,answer_unique)
                if edit_or_save == "save":
                    post = QAnswer.objects.get(author=request.user, compare_id=query_id, unique= answer_unique)
                    post.author = request.user
                    post.edit_time = timezone.now()
                    post.body = form.cleaned_data['body']
                    post.save(update_fields=['author', 'edit_time', 'body'])
                    object_list = QA.objects.filter(title=query_question,id=query_id)
                    answer_list = QAnswer.objects.filter(compare_id=query_id)
                    return HttpResponseRedirect('')
                elif edit_or_save == "delete":
                    print(request.user,query_id, answer_unique)
                    post = QAnswer.objects.get(author=request.user, compare_id=query_id, unique= answer_unique)
                    post.delete()
                    object_list = QA.objects.filter(title=query_question, id=query_id)
                    answer_list = QAnswer.objects.filter(compare_id=query_id)
                    return HttpResponseRedirect('')

                else:
                    post = form.save(commit=False)
                    post.author = request.user
                    post.publish = timezone.now()
                    post.compare_id = query_id
                    post.body = form.cleaned_data['body']
                    form.save()

                    object_list = QA.objects.filter(title=query_question)
                    answer_list = QAnswer.objects.filter(compare_id=query_id)

                    return HttpResponseRedirect('')
        else:

            form = DocumentForm()

        object_list = QA.objects.filter(title=query_question)
        answer_list = QAnswer.objects.filter(compare_id=query_id)

        return render(request, self.template_name,{'object_list': object_list, 'form': form, 'answer_list': answer_list})


class PasswordChangeView(TemplateView):
    template_name = 'registration/password_change_form.html'
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {
            'form': form
        })
    def post(self,request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Şifreniz başarıyla değiştirildi!')
                return redirect('password_reset_complete')
            else:
                messages.error(request, 'Lütfen hataları düzeltin.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {
            'form': form
        })



class ProfilePageView(TemplateView):
    template_name = 'registration/profile.html'
    import glob
    avatar_list=glob.glob("static/img/avatar/*.png")
    avatar_list=avatar_list[:-1]
    # avatar_list=[i[18:] for i in avatar_list]
    time = timezone.now()


    def get(self, request, *args, **kwargs):
        edit_control = self.request.GET.get('edit')
        edit_or_save=False
        if edit_control=='go-edit':
            edit_or_save=True
        else:
            edit_or_save=False

        object_list = Post.objects.filter(author=request.user).order_by('-publish')
        object_list_document = Document.objects.filter(publisher=request.user).order_by('-publish_date')
        object_list_qa = QA.objects.filter(author=request.user).order_by('-publish')
        page = request.GET.get('page', 1)
        paginator = Paginator(object_list, 10)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        profile = CustomProfile.objects.filter(user=request.user)

        return render(request, self.template_name, {'edit_or_save':edit_or_save,'profile':profile,'object_list_qa':object_list_qa,'object_list':object_list,'object_list_document':object_list_document,'avatar_list':self.avatar_list})


    def post(self, request):
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                # post = form.save(commit=False)
                post=CustomProfile.objects.get(user=request.user)
                post.first_name = form.cleaned_data['first_name']
                post.last_name = form.cleaned_data['last_name']
                post.job = form.cleaned_data['job']
                post.uni = form.cleaned_data['uni']
                post.location = form.cleaned_data['location']

                post.talents = form.cleaned_data['talents']
                post.avatar = form.cleaned_data['avatar']
                post.save(update_fields=['first_name','last_name','job','uni','location','talents','avatar'])
                return redirect('profile')
        else:
            form = DocumentForm()
        return redirect('profile')


class AuthorApplyView(TemplateView):
    template_name = 'blog/author-apply.html'
    form = AuthorApplyForm()
    approve_wait=False
    # <!--{% if request.user|has_group:"Yazar" %}-->

    def get(self, request, *args, **kwargs):
        object = CustomProfile.objects.get(user=request.user)
        try:
            author_apply = AuthorApply.objects.get(author=request.user)
            return render(request, self.template_name, {'post_form': self.form, 'object': object,'author_apply':author_apply})
        except:
            return render(request, self.template_name, {'post_form': self.form,'object':object})

    def post(self, request):
        if request.method == 'POST':
            form = AuthorApplyForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.apply_date = timezone.now()
                post.name = form.cleaned_data['name']
                post.surname = form.cleaned_data['surname']
                post.job = form.cleaned_data['job']
                post.job_talents = form.cleaned_data['job_talents']
                post.rustudent = form.cleaned_data['rustudent']
                post.text = form.cleaned_data['text']
                form.save()
                self.approve_wait=True
                return render(request, self.template_name, {'approve_wait': self.approve_wait})
        else:
            form = DocumentForm()
        return redirect('homepage')


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                success_register=False

                try:
                    User.objects.get(email=email)
                    return render(request, self.template_name,
                                  {'login_error': 'E-Mail adresiniz zaten sistemimizde kayıtlı!'})
                except:
                    try:
                        form.save()
                        user = authenticate(username=username, password=raw_password)
                        login(request, user)
                        username2=User.objects.get(username=username)
                        CustomProfile.objects.create(user=username2,first_name=username2.first_name,last_name=username2.last_name)
                        return render(request, self.template_name,
                                      {'success_register': True})

                    except:
                        return render(request, self.template_name,
                                      {'login_error': 'Bilgiler hatalı, lütfen tekrar deneyiniz!'})


        else:
            form = SignUpForm()
        return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def post(self, request, *args, **kwargs):
        template_name = 'registration/login.html'

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            UserModel = get_user_model()

            try:
                username = UserModel.objects.get(email=email)
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect('homepage')
                    else:
                        return HttpResponse("Your account was inactive.")
                else:
                    return render(request, self.template_name,
                                  {'login_error': 'Bilgiler hatalı, lütfen tekrar deneyiniz!'})
            except:
                return render(request, self.template_name,
                              {'login_error': '%s e-maili ile ilişkili kullanıcı bulunmamaktadır. Önce siteye kayıt olunuz!'%email})



        else:
            return render(request, self.template_name, {})


class HomepageView(TemplateView):
    template_name = "home.html"
    object_list = Post.objects.all().order_by('-publish')[:10]
    form=DocumentForm()
    documents = Document.objects.all().order_by('-publish_date')[:10]
    questions = QA.objects.all().order_by('-publish')[:10]
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'object_list':self.object_list,'form':self.form,'document_list':self.documents,'questions':self.questions})

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                       kwargs={'year': self.publish.year,
                               'month': self.publish.strftime('%b'),
                               'day': self.publish.strftime('%d'),
                               'slug': self.slug})




