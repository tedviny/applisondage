from collections import Counter

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd


# Create your views here.

def base(request):
    return render(request, 'base.html')


def index(request):
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def readfile(filename):
    global rows, columns, data, my_file, missing_values
    # read the missing data - checking if there is a null
    missingvalue = ['?', '0', '--']

    my_file = pd.read_csv(filename, sep='[:;,|_]', na_values=missingvalue, engine='python')

    data = pd.DataFrame(data=my_file, index=None)
    print(data)

    rows = len(data.axes[0])
    columns = len(data.axes[1])

    null_data = data[data.isnull().any(axis=1)]  # find where is the missing data #na null =['x1','x13']
    missing_values = len(null_data)

def account(request):
    global attribute
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        attribute = request.POST.get('attributeid')
        print(attribute)
        # print(uploaded_file)
        if uploaded_file.name.endswith('.csv'):
            # save file in media
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)
            # know where to save the file
            d = os.getcwd()
            file_directory = d + '\media\\' + name
            readfile(file_directory)
            request.session['attribute'] = attribute
            message = 'Present ' + str(rows) + ' lignes et ' + str(columns) + ' colonnes. Donnes absentes: ' + str(missing_values)
            messages.warning(request, message)
            dashboard = []  # ['A11','A11',A'122',]
            for x in data[attribute]:
                dashboard.append(x)

            my_dashboard = dict(Counter(dashboard))  # {'A121': 282, 'A122': 232, 'A124': 154, 'A123': 332}

            print(my_dashboard)

            keys = my_dashboard.keys()  # {'A121', 'A122', 'A124', 'A123'}
            values = my_dashboard.values()

            listkeys = []
            listvalues = []

            for x in keys:
                listkeys.append(x)

            for y in values:
                listvalues.append(y)

            print(listkeys)
            print(listvalues)

            context = {
                'listkeys': listkeys,
                'listvalues': listvalues,
            }
        else:
            messages.warning(request, 'Choisir un fichier avec l\'extension csv')

    return render(request, 'account.html', context)
