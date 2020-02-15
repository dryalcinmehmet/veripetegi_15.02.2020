# ./manage.py shell_plus --notebook
# ./manage.py shell_plus --notebook
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
from source.forms import SignUpForm
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
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
import datetime
import unidecode, re
import random
from django.utils import timezone
import glob
from passlib.hash import pbkdf2_sha256

avatar_list = glob.glob("static/img/avatar/*.png")
document_list = glob.glob("media/documents/load_document/*.csv")

fixed = ['True', 'False']
category = ['Futbol', 'Finans', 'Teknoloji']

job = ['Mühendis', 'Akademisyen', 'Bilim Adamı', 'Tarihçi', 'Arkeolog']
users = ['TestUser1', 'TestUser2', 'TestUser3', 'TestUser4', 'TestUser5', 'TestUser6', 'TestUser7', 'TestUser8',
         'TestUser9', 'TestUser9']
for i in range(1, 20):
    User.objects.create(username='TestUser%d' % i, email='test%d@gmail.com' % i)
    user = User.objects.get(username='TestUser%d' % i)
    user.set_password("gurban99")
    user.save()

for i in range(1, 20):
    CustomProfile.objects.create(user=User.objects.get(username='TestUser%d' % i), first_name='Tom',
                                 last_name='Bombadil', job=random.choice(job), avatar=random.choice(avatar_list))

    text = unidecode.unidecode("Story number %d" % i).lower()
    slug = re.sub(r'[\W_]+', '-', text)
    Post.objects.create(author=User.objects.get(username=random.choice(users)),
                        title="Story number %d" % i,
                        category=random.choice(category),
                        body="Integer nec consequat mi. In rhoncus in tellus nec congue. Phasellus vel interdum elit, a laoreet eros. Aenean egestas at libero ac dignissim.Integer nec consequat mi. In rhoncus in tellus nec congue. Phasellus vel interdum elit, a laoreet eros. Aenean egestas at libero ac dignissim.Integer nec consequat mi.",
                        slug=slug,
                        publish=timezone.now(),
                        type="Blog"
                        )
    data = pd.read_csv(random.choice(document_list))
    data = data.iloc[:5, :5]
    data_html = data.to_html(justify="center", border="0.1px")

    Document.objects.create(publisher=User.objects.get(username=random.choice(users)),
                            publish_date=timezone.now(),
                            file_name=random.choice(document_list)[30:],
                            dataset_title='Fifa Veriseti %d' % i,
                            path=random.choice(document_list),
                            first_5_row=data_html,
                            )

    QA.objects.create(author=User.objects.get(username=random.choice(users)),
                      publish=timezone.now(),
                      fixed=random.choice(fixed),
                      title='Python: How to get a value of datetime.today() that is “timezone aware”? %d' % i,
                      id=i + 10000,
                      body="""

                                    I am trying to subtract one date value from the value of datetime.today() to calculate how long ago something was. But it complains:

                                    TypeError: can't subtract offset-naive and offset-aware datetimes

                                    The value datetime.today() doesn't seem to be "timezone aware", while my other date value is. How do I get a value of datetime.today() that is timezone aware? Right now it's giving me the time in local time, which happens to be PST, i.e. UTC-8hrs. Worst case, is there a way I can manually enter a timezone value into the datetime object returned by datetime.today() and set it to UTC-8? Of course, the ideal solution would be for it to automatically know the timezone.
                                    """,
                      )
