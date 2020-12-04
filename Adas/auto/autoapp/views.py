from django.shortcuts import render,redirect

from django.http import HttpResponse

import os

from django.urls import path

# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from .forms import registerForm,loginForm,uploadForm

from .models import auto_users,upload


def home(request):

    return render(request,'pages/home.html')


def register(request):
    if request.method == 'POST':
        registerform = registerForm(request.POST)

        if registerform.is_valid():

            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            uname = request.POST['uname']
            pwd = request.POST['pwd']
            cpwd= request.POST['cpwd']
            if pwd != cpwd:
                registerform = registerForm()

                matcherror = "Passwords don't match"

                context = {'registerform': registerform,'merror':matcherror}

                return render(request,'pages/register.html',context)
            else:
               new_user=auto_users(fname=fname,lname=lname,email=email,uname=uname,pwd=pwd)
               new_user.save()
               return redirect('login')

    else:

       registerform = registerForm()

       context = {'registerform':registerform}

       return render(request,'pages/register.html',context)


def login(request):

    if request.method == 'POST':

        loginform = loginForm(request.POST)

        if loginform.is_valid():

            emailuname= request.POST['emailuname']

            pwd = request.POST['pwd']

            try:

                if auto_users.objects.filter(uname=emailuname, pwd=pwd):

                    my_info = auto_users.objects.get(uname=emailuname, pwd=pwd)

                    request.session['user_id'] = my_info.id

                    request.session['fname'] = my_info.fname

                    request.session['lname'] = my_info.lname

                    request.session['uname'] = my_info.uname

                    request.session['email'] = my_info.email

                    fname = my_info.fname

                    lname = my_info.lname

                    uname = my_info.uname

                    my_datasets = upload.objects.filter(user_id_id=my_info.id)

                    context = {'fname':fname,'lname':lname,'uname':uname,'my_datasets':my_datasets}

                    return render(request,'pages/user_dashboard.html',context)

                elif auto_users.objects.filter(email=emailuname, pwd=pwd):

                    my_info = auto_users.objects.get(email=emailuname, pwd=pwd)

                    request.session['user_id'] = my_info.id

                    request.session['fname'] = my_info.fname

                    request.session['lname'] = my_info.lname

                    request.session['uname'] = my_info.uname

                    request.session['email'] = my_info.email

                    fname = my_info.fname

                    lname = my_info.lname

                    uname = my_info.uname

                    my_datasets = upload.objects.filter(user_id_id=my_info.id)

                    context = {'fname': fname, 'lname': lname, 'uname': uname, 'my_datasets': my_datasets}

                    return render(request,'pages/user_dashboard.html', context)
                else:
                     loginform = loginForm()

                     errormessage = "Incorrect credentials"

                     context = {'loginform': loginform, 'error': errormessage}

                     return render(request,'pages/login.html',context)

            except:

                loginform = loginForm()

                errormessage = "Incorrect credentials"

                context = {'loginform': loginform, 'error': errormessage}

                return render(request, 'pages/login.html', context)

        else:
            loginform = loginForm()

            errormessage = "Incorrect credentials"

            context = {'loginform': loginform, 'error': errormessage}

            return render(request, 'pages/login.html', context)
    else:
        loginform = loginForm()

        context = {'loginform': loginform}

        return render(request, 'pages/login.html', context)


def user_dashboard(request):

    try:

        if request.session.get('user_id',True):

           user_id = request.session['user_id']

           my_datasets =  upload.objects.filter(user_id_id=user_id).order_by('-upload_date')

           fname = request.session['fname']

           lname = request.session['lname']

           uname = request.session['uname']

           context = {'fname':fname,'lname':lname,'uname':uname,'my_datasets':my_datasets}

           return render(request,'pages/user_dashboard.html',context)
        else:
            return render(request, 'pages/error_message.html')

    except:

       return render(request, 'pages/error_message.html')


def uploadfunc(request):

    if request.method == 'POST' and request.FILES['filename']:

        uploadform = uploadForm(request.POST,request.FILES)

        if uploadform.is_valid():

            file_path = request.FILES['filename']

            file_name = file_path.name

            file_name = str(file_name)

            if file_name.endswith(".csv"):
                file_name = file_name.rstrip('.csv')

                user_id = request.session['user_id']

                new_file = upload(filepaths=file_path, filename=file_name, user_id_id=user_id)

                new_file.save()

                return redirect('user_dashboard')

            elif file_name.endswith(".json"):

                file_name = file_name.rstrip('.csv')

                user_id = request.session['user_id']

                new_file = upload(filepaths=file_path, filename=file_name, user_id_id=user_id)

                new_file.save()

                return redirect('user_dashboard')
            else:
                upladform = uploadForm()

                format_message="Unsupported format";

                return render(request,'pages/upload_dataset.html',{'fmsg':format_message,'uploadform':upladform})

        else:
            return redirect('upload')

    upladform = uploadForm()

    context = {'uploadform':upladform}

    return render(request,'pages/upload_dataset.html',context)


def logout(request):
    del request.session['user_id']
    return redirect('home')


def deleteuploaded(request):

    if request.method == 'POST':

        data_id = request.POST['delete_up']

        data_selected = upload.objects.get(id=data_id)

        if data_selected:

            data_selected.delete()

            fname = request.session['fname']

            lname = request.session['lname']

            uname = request.session['uname']

            return redirect('user_dashboard')
        else:
            return render(request, 'user_dashboard')
    else:
         return render(request,'user_dashboard')


def viewuploaded(request):

    if request.method=='POST':

        data_id = request.POST['view_up']

        data_selected = upload.objects.get(id=data_id)

        data_path = data_selected.filepaths

        if data_path:

            import pandas as pd

            dataFrame = pd.read_csv(data_path)

            dataFrame = dataFrame.head(10)

            dataFrame  = dataFrame.to_html()

            fname=request.session['fname']

            file_name = str(data_selected.filename)

            file_name = file_name.replace('_',' ')

            file_name = file_name.upper()

            lname = request.session['lname']

            uname=request.session['uname']

            context = {'fname': fname, 'lname': lname, 'uname': uname, 'df' : dataFrame,'dataset':file_name }

            return render(request,'pages/view_uploads.html',context)
        else:

            return redirect('user_dashboard')

    else:

        return redirect('user_dashboard')

def analyse(request):

    if request.method == 'POST':

        data_id = request.POST['analyse']

        data_selected = upload.objects.get(id=data_id)

        data_path = data_selected.filepaths

        file_name = str(data_selected.filename)

        file_name = file_name.replace('_', ' ')

        file_name = file_name.upper()

        if data_path:

            import pandas as pd

            import numpy as np

            import matplotlib as mpl

            #import seaborn as ab

            #import matplotlib.pyplot as plt

            #from matplotlib import style


            if str(data_path).endswith(".csv"):

                dataFrame = pd.read_csv(data_path)

                datacolumns = dataFrame.columns

                colsdtypes = dataFrame.dtypes

                colsdtypes = list(colsdtypes)

                datacolumns = list(datacolumns)

                datasize = dataFrame.size

                tnullvalues = dataFrame.isnull().sum()

                tnullvalues = list(tnullvalues)

                colsnull = zip(datacolumns, tnullvalues)

                datashape = np.array(dataFrame.shape)

                rows = datashape[0]

                cols = datashape[1]

                datacolumns = dataFrame.columns

                colsdtypes = dataFrame.dtypes

                colsdtypes = list(colsdtypes)

                datacolumns = list(datacolumns)

                newcols = []

                newdtype = []

                for n in datacolumns:
                    newcols.append(n)
                    newdtype.append(dataFrame[n].dtype)

                zip_colstype = zip(newcols, newdtype)

                dataFrame_described = dataFrame.describe()

                dataFrame_described = dataFrame_described.to_html()

                fname = request.session['fname']

                lname = request.session['lname']

                uname = request.session['uname']

                # nullvalues = dataFrame[dataFrame.isnull()]

                nullvalues = dataFrame.isnull().head(10)

                nullvalues = nullvalues.to_html()

                context = {'fname': fname, 'lname': lname, 'uname': uname, 'dataset': file_name,
                           'dataFrame_described': dataFrame_described, 'dsize': datasize,
                           'cols': cols, 'rows': rows, 'datacols': datacolumns, 'zipped': zip_colstype,
                           'somenull': nullvalues, 'nullcols_value': colsnull}

                return render(request, 'pages/analyse_data.html', context)

            elif str(data_path).endswith(".html"):

                dataFrame = pd.read_html(data_path)

                datacolumns = dataFrame.columns

                colsdtypes = dataFrame.dtypes

                colsdtypes = list(colsdtypes)

                datacolumns = list(datacolumns)

                datasize = dataFrame.size

                tnullvalues = dataFrame.isnull().sum()

                tnullvalues = list(tnullvalues)

                colsnull = zip(datacolumns, tnullvalues)

                datashape = np.array(dataFrame.shape)

                rows = datashape[0]

                cols = datashape[1]

                datacolumns = dataFrame.columns

                colsdtypes = dataFrame.dtypes

                colsdtypes = list(colsdtypes)

                datacolumns = list(datacolumns)

                newcols = []

                newdtype = []

                for n in datacolumns:
                    newcols.append(n)
                    newdtype.append(dataFrame[n].dtype)

                zip_colstype = zip(newcols, newdtype)

                dataFrame_described = dataFrame.describe()

                dataFrame_described = dataFrame_described.to_html()

                fname = request.session['fname']

                lname = request.session['lname']

                uname = request.session['uname']

                # nullvalues = dataFrame[dataFrame.isnull()]

                nullvalues = dataFrame.isnull().head(10)

                nullvalues = nullvalues.to_html()

                context = {'fname': fname, 'lname': lname, 'uname': uname, 'dataset': file_name,
                           'dataFrame_described': dataFrame_described, 'dsize': datasize,
                           'cols': cols, 'rows': rows, 'datacols': datacolumns, 'zipped': zip_colstype,
                           'somenull': nullvalues, 'nullcols_value': colsnull}

                return render(request, 'pages/analyse_data.html', context)
            elif str(data_path).endswith(".json"):

                dataFrame = pd.read_json(data_path)

                datacolumns = dataFrame.columns

                colsdtypes = dataFrame.dtypes

                colsdtypes = list(colsdtypes)

                datacolumns = list(datacolumns)

                datasize = dataFrame.size

                tnullvalues = dataFrame.isnull().sum()

                tnullvalues = list(tnullvalues)

                colsnull = zip(datacolumns, tnullvalues)

                datashape = np.array(dataFrame.shape)

                rows = datashape[0]

                cols = datashape[1]

                datacolumns = dataFrame.columns

                colsdtypes = dataFrame.dtypes

                colsdtypes = list(colsdtypes)

                datacolumns = list(datacolumns)

                newcols = []

                newdtype = []

                for n in datacolumns:
                    newcols.append(n)
                    newdtype.append(dataFrame[n].dtype)

                zip_colstype = zip(newcols, newdtype)

                dataFrame_described = dataFrame.describe()

                dataFrame_described = dataFrame_described.to_html()

                fname = request.session['fname']

                lname = request.session['lname']

                uname = request.session['uname']

                # nullvalues = dataFrame[dataFrame.isnull()]

                nullvalues = dataFrame.isnull().head(10)

                nullvalues = nullvalues.to_html()

                context = {'fname': fname, 'lname': lname, 'uname': uname, 'dataset': file_name,
                           'dataFrame_described': dataFrame_described, 'dsize': datasize,
                           'cols': cols, 'rows': rows, 'datacols': datacolumns, 'zipped': zip_colstype,
                           'somenull': nullvalues, 'nullcols_value': colsnull}

                return render(request, 'pages/analyse_data.html', context)
            else:
                return HttpResponse("Not supported format")

        else:

            return redirect('user_dashboard')

    else:

        return redirect('user_dashboard')

def clean(request):

    if request.method == 'POST':
        data_id = request.POST['clean']

        data_selected = upload.objects.get(id=data_id)

        request.session["data_id"] = data_selected.id

        data_path = data_selected.filepaths

        file_name = str(data_selected.filename)

        file_name = file_name.replace('_', ' ')

        file_name = file_name.upper()

        fname = request.session['fname']

        lname = request.session['lname']

        uname = request.session['uname']

        fname = request.session['fname']

        lname = request.session['lname']

        uname = request.session['uname']

        import pandas as pd

        import numpy as np

        #import matplotlib as mpl

        #import seaborn as ab

        #import matplotlib.pyplot as plt

        #from matplotlib import style

        str_data_path=str(data_path)

        if str_data_path.endswith('.csv'):

            getdata=pd.read_csv(data_path)

            colomns_names=getdata.columns.values

            context = {'fname': fname, 'lname': lname, 'dataset': file_name, 'dataid': data_id,'colsnames':colomns_names}

            return render(request, 'pages/clean_data.html', context)



        context = {'fname':fname,'lname':lname,'dataset':file_name,'dataid':data_id}

        return render(request,'pages/clean_data.html',context)

def rename(request):

    if request.method == 'POST':

        data_id = request.POST['clean']

        old_name = request.POST['old_name']

        new_name = request.POST['new_name']

        data_selected = upload.objects.get(id=data_id)

        request.session["data_id"] = data_selected.id

        data_path = data_selected.filepaths

        file_name = str(data_selected.filename)

        file_name = file_name.replace('_', ' ')

        file_name = file_name.upper()

        fname = request.session['fname']

        lname = request.session['lname']

        uname = request.session['uname']

        fname = request.session['fname']

        lname = request.session['lname']

        uname = request.session['uname']

        import pandas as pd

        import numpy as np

        import matplotlib as mpl

        import seaborn as ab

        import matplotlib.pyplot as plt

        from matplotlib import style

        str_data_path=str(data_path)

        if str_data_path.endswith('.csv'):

            getdata=pd.read_csv(data_path)

            colomns_names=getdata.columns.values

            if new_name:
                for i in colomns_names:
                    if i==old_name:
                         getdata.rename(columns={old_name:new_name},inplace=True)
                         colomns_names = getdata.columns.values
                         context = {'fname': fname, 'lname': lname, 'dataset': file_name, 'dataid': data_id,
                        'colsnames': colomns_names}
                         return render(request, 'pages/clean_data.html', context)


            context = {'fname': fname, 'lname': lname, 'dataset': file_name, 'dataid': data_id,'colsnames':colomns_names}

            return render(request, 'pages/clean_data.html', context)



        context = {'fname':fname,'lname':lname,'dataset':file_name,'dataid':data_id}

        return render(request,'pages/clean_data.html',context)


def removedup(request):

    if request.method == 'POST':

       if request.POST['duplicate']:
           data_id_dup = request.session["data_id"]

           data_selected = upload.objects.get(id=data_id_dup)

           data_path = data_selected.filepaths

           file_name = str(data_selected.filename)

           file_name = file_name.replace('_', ' ')

           file_name = file_name.upper()

           fname = request.session['fname']

           lname = request.session['lname']

           uname = request.session['uname']

           fname = request.session['fname']

           lname = request.session['lname']

           uname = request.session['uname']

           if data_path:
              import pandas as pd

              dataFrame = pd.read_csv(data_path)

              noOfdup = dataFrame.duplicated().sum()

              dataFrame = dataFrame.drop_duplicates(keep='first', inplace=True)

              # dataFrame.to_csv(file_name+"clean.csv", index=False, encoding='utf8')

              user_id = request.session['user_id']

              # new_file = clean(filepaths=path.join(BASE_DIR,file_name+"clean.csv"), filename=file_name+"clean", user_id_id=user_id)

              # new_file.save()

              context = {'fname': fname, 'lname': lname, 'dataset': file_name, 'dupid': data_id_dup,'nodup':noOfdup}

              return render(request, 'pages/clean_data.html', context)

