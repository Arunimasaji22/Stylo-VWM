import json
from datetime import datetime
import random

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from royaloutfit.models import *
from royaloutfit.serializers import TestImageSerializer


def login1(request):
    return render(request,'Login/loginindex.html')


def logout(request):
    auth.logout(request)
    return render(request,'Login/loginindex.html')


def login_code(request):
    uname=request.POST['textfield']
    pswd=request.POST['textfield2']
    try:
        ob=login_table.objects.get(username=uname,password=pswd)
        if ob.type == "admin":
            auth_obj = auth.authenticate(username='admin', password='admin')
            if auth_obj is not None:
                auth.login(request, auth_obj)
            return HttpResponse('''<script>alert("coordinatorhome");window.location='/Coordinator'</script>''')
        elif ob.type == "designer":
            auth_obj = auth.authenticate(username='admin', password='admin')
            if auth_obj is not None:
                auth.login(request, auth_obj)
            request.session['lid']=ob.id
            return HttpResponse('''<script>alert("Designhome");window.location='/designhome'</script>''')
        elif ob.type == "user":
            auth_obj = auth.authenticate(username='admin', password='admin')
            if auth_obj is not None:
                auth.login(request, auth_obj)
            request.session['lid']=ob.id
            return HttpResponse('''<script>alert("Userhome");window.location='/user_home'</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid");window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert("Invalid");window.location='/'</script>''')

# //////////////////////////////////////// admin module ////////////////////////////////////

@login_required(login_url='/')
def verify_designer(request):
    ob=designers_table.objects.all()
    return render(request,'Co-ordinator/verify_designer.html',{'val':ob})

@login_required(login_url='/')
def accept_designer(request,id):
    ob=login_table.objects.get(id=id)
    ob.type='designer'
    ob.save()
    return HttpResponse('''<script>alert("Accepted Successfully");window.location='/verify_designer#about'</script>''')



@login_required(login_url='/')
def reject_designer(request,id):
    ob = login_table.objects.get(id=id)
    ob.type = 'Rejected'
    ob.save()
    return HttpResponse('''<script>alert("Rejected Successfully");window.location='/verify_designer#about'</script>''')
from django.shortcuts import render, redirect
from .models import designs1_tables

def manage_design(request):
    designs = designs1_tables.objects.all()
    return render(request, 'Co-ordinator/manage_design.html', {'designs': designs})

def add_design(request):
    if request.method == "POST":
        dressname = request.POST['dressname']
        platform = request.POST['platform']
        design = request.FILES.get('design')

        new_design = designs1_tables(dressname=dressname, platform=platform, design=design)
        new_design.save()
        return redirect('manage_design')

    return render(request, 'Co-ordinator/add_design.html')

def delete_design1(request, id):
    design = designs1_tables.objects.get(id=id)
    design.delete()
    return redirect('manage_design')

@login_required(login_url='/')
def block(request):
    ob=designers_table.objects.all()
    return render(request,'Co-ordinator/block&unblock.html',{'val':ob})

@login_required(login_url='/')
def block_designer(request,id):
    ob = login_table.objects.get(id=id)
    ob.type = 'Blocked'
    ob.save()
    return HttpResponse('''<script>alert("Blocked Successfully");window.location='/block#about'</script>''')


@login_required(login_url='/')
def unblock_designer(request,id):
    ob = login_table.objects.get(id=id)
    ob.type = 'designer'
    ob.save()
    return HttpResponse('''<script>alert("Unblocked Successfully");window.location='/block#about'</script>''')

@login_required(login_url='/')
def search_designer(request):
    a = request.POST['textfield']
    ob = designers_table.objects.filter(Name__istartswith=a)
    if len(ob) == 0:
        return HttpResponse('''<script>alert("Data not found");window.location='/verify_designer#about'</script>''')
    else:
        return render(request, 'Co-ordinator/verify_designer.html', {'val': ob, 'a': a})

@login_required(login_url='/')
def searchcomplaints(request):
    a = request.POST['textfield']
    ob = complaint_table.objects.filter(USER__Name__istartswith=a)
    if len(ob) == 0:
        return HttpResponse('''<script>alert("Data not found");window.location='/viewcompailnts#about'</script>''')
    else:
        return render(request, 'Co-ordinator/view compailnts.html', {'val': ob, 'a': a})

@login_required(login_url='/')
def viewcompailnts(request):
    ob = complaint_table.objects.all()
    return render(request,'Co-ordinator/view compailnts.html',{'val':ob})

@login_required(login_url='/')
def viewrateing(request):
    ob=rating_table1.objects.all()
    return render(request,'Co-ordinator/viewrateing.html',{'val':ob})

@login_required(login_url='/')
def searchrating(request):
    a = request.POST['textfield']
    ob = rating_table.objects.filter(Date=a)
    if len(ob) == 0:
        return HttpResponse('''<script>alert("Data not found");window.location='/viewrateing#about'</script>''')
    else:
        return render(request,'Co-ordinator/viewrateing.html',{'val':ob,'dt':a})

@login_required(login_url='/')
def block1(request):
    a = request.POST['textfield']
    ob = designers_table.objects.filter(Name__istartswith=a)
    if len(ob) == 0:
        return HttpResponse('''<script>alert("Data not found");window.location='/block#about'</script>''')
    else:
      return render(request, 'Co-ordinator/block&unblock.html', {'val': ob, 'a': a})


@login_required(login_url='/')
def Coordinator(request):
 return render(request,'Co-ordinator/homeindex.html')


@login_required(login_url='/')
def manufacture(request):
    return render(request,'Manufcture/manufacture_index.html')


@login_required(login_url='/')
def sendreplay(request,id):
    ob=complaint_table.objects.get(id=id)
    request.session['cid']=ob.id
    return render(request,'Co-ordinator/Sendreplay.html')


@login_required(login_url='/')
def add_reply(request):
    a=request.POST['textfield']
    ob=complaint_table.objects.get(id=request.session['cid'])
    ob.reply=a
    ob.Date=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("Reply Successfully");window.location='/viewcompailnts#about'</script>''')

@login_required(login_url='/')
def downloadmanufacture(request,id):
    ob = login_table.objects.get(id=id)
    ob.type = 'manufacturer'
    ob.save()

def designer_register(request):
    return render(request, 'Designers/designer_register.html')

def registration(request):
    a=request.POST['textfield']
    b=request.POST['radiobutton']
    c=request.POST['textfield2']
    d=request.POST['textfield3']
    e=request.POST['textfield4']
    f=request.POST['textfield5']
    g=request.FILES['file']
    fn=FileSystemStorage()
    fs=fn.save(g.name,g)
    h=request.POST['textfield7']
    i=request.FILES['file2']
    fs2=fn.save(i.name,i)
    j=request.POST['textfield6']
    k=request.POST['textfield8']
    ob=login_table()
    ob.username=j
    ob.password=k
    ob.type='pending'
    ob.save()
    ob1=designers_table()
    ob1.LOGIN=ob


    ob1.Gender=b
    ob1.Name=a
    ob1.Place=c
    ob1.Post=d
    ob1.Pin=e
    ob1.Phone=f
    ob1.License=fs
    ob1.Email=h
    ob1.Photo=fs2
    ob1.save()
    return HttpResponse('''<script>alert("Registration Successfully");window.location='/'</script>''')




@login_required(login_url='/')
def searchviewrating(request):
    a = request.POST['textfield']
    ob = rating_table.objects.filter(Date=a)
    if len(ob) == 0:
        return HttpResponse('''<script>alert("Data not found");window.location='/viewrating#about'</script>''')
    else:
        return render(request,'Manufcture/view rating.html',{'val':ob, 'a': a})


@login_required(login_url='/')
def adddesign(request):
    return render(request,'Designers/adddesign.html')


@login_required(login_url='/')
def editdesign(request, id):
    request.session['did']=id
    ob = designs_tables.objects.get(id=id)
    return render(request,'Designers/editdesign.html', {'val': ob})


@login_required(login_url='/')
def edit_design_post(request):
    try:
        name=request.POST['dress_name']
        type=request.POST['textfield']
        platform=request.POST['platform']
        season=request.POST['season']
        G_type=request.POST['Gen']
        design = request.FILES['file']
        fs=FileSystemStorage()
        fp=fs.save(design.name,design)
        discription =request.POST['textfield2']
        ob=designs_tables.objects.get(id=request.session['did'])
        ob.dressname=name
        ob.dresstype=type
        ob.season=season
        ob.platform=platform
        ob.gendertype=G_type
        ob.design=fp
        ob.discription=discription
        print("*******************************", request.session['lid'])
        ob.DESIGNER=designers_table.objects.get(LOGIN__id=request.session['lid'])
        ob.save()
    except:
        name=request.POST['dress_name']
        type=request.POST['textfield']
        platform=request.POST['platform']
        season=request.POST['season']
        G_type=request.POST['Gen']
        discription =request.POST['textfield2']
        ob=designs_tables.objects.get(id=request.session['did'])
        ob.dressname=name
        ob.dresstype=type
        ob.season=season
        ob.platform=platform
        ob.gendertype=G_type
        ob.discription=discription
        print("*******************************", request.session['lid'])
        ob.DESIGNER=designers_table.objects.get(LOGIN__id=request.session['lid'])
        ob.save()
    return HttpResponse('''<script>alert("edited Successfully");window.location='/managedesign#about'</script>''')


@login_required(login_url='/')
def deletedesign(request,id):
    ob=designs_tables.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted Successfully");window.location='/managedesign#about'</script>''')


@login_required(login_url='/')
def add_design_post(request):
    name=request.POST['dress_name']
    type=request.POST['textfield']
    G_type=request.POST['Gen']
    design = request.FILES['file']
    discription = request.POST['textfield2']
    season = request.POST['season']

    fs=FileSystemStorage()
    fp=fs.save(design.name,design)

    ob=designs_tables()
    ob.dressname=name
    ob.dresstype=type
    ob.gendertype=G_type
    ob.design=fp
    ob.season=season
    ob.discription=discription
    ob.DESIGNER=designers_table.objects.get(LOGIN__id=request.session['lid'])
    ob.save()
    return HttpResponse('''<script>alert("Added Successfully");window.location='/managedesign#about'</script>''')


@login_required(login_url='/')
def customisedesign(request):
    ob=custom_desgin_table.objects.all()
    return render(request, 'Designers/customisedesign.html', {'val': ob})


@login_required(login_url='/')
def searchcustomisedesign(request):
    a = request.POST['textfield']
    ob = custom_desgin_table.objects.filter(date=a)
    if len(ob) == 0:
        return HttpResponse('''<script>alert("Data not found");window.location='/customisedesign#about'</script>''')
    else:
        return render(request, 'Designers/customisedesign.html', {'val': ob, 'a': a})


@login_required(login_url='/')
def acceptdesign(request,id):
    ob=custom_desgin_table.objects.get(id=id)
    ob.status='Accepted'
    ob.save()
    return HttpResponse('''<script>alert("Accepted Successfully");window.location='/customisedesign#about'</script>''')


@login_required(login_url='/')
def rejectdesign(request,id):
    ob=custom_desgin_table.objects.get(id=id)
    ob.status='rejected'
    ob.save()
    return HttpResponse('''<script>alert("Rejected Successfully");window.location='/customisedesign#about'</script>''')


@login_required(login_url='/')
def designhome(request):
    return render(request,'Designers/designer_index.html')


@login_required(login_url='/')
def managedesign(request):
    ob=designs_tables.objects.filter(DESIGNER__LOGIN=request.session['lid'])
    return render(request,'Designers/mngs dsgn.html',{'val':ob})


@login_required(login_url='/')
def more_designs(request, d_id):
    request.session['design_id'] = d_id
    print('--------------->', d_id)
    ob = MoreDesignTable.objects.filter(DESIGN_id=d_id)
    print("------------->", ob)
    return render(request, 'Designers/more_designs.html', {'val': ob})


@login_required(login_url='/')
def add_more_designs(request):
    return render(request, "Designers/add_more_design.html")

@login_required(login_url='/')
def add_more_design_post(request):
    design = request.FILES['file']
    fss = FileSystemStorage()
    design_file = fss.save(design.name, design)
    ob = MoreDesignTable()
    print("----deid------>", request.session['design_id'])
    ob.DESIGN = designs_tables.objects.get(id=request.session['design_id'])
    ob.design_more = design_file
    ob.save()
    return HttpResponse('''<script>alert("Successfully added");window.location='/managedesign#about'</script>''')


@login_required(login_url='/')
def adddesigners(request):
    return render(request,'Manufcture/add designers.html')



@login_required(login_url='/')
def addts(request):
    return render(request,'Manufcture/add ts.html')



@login_required(login_url='/')
def Block_unblockdesigners(request):
    ob=designers_table.objects.all()
    return render(request,'Manufcture/Block&unblockdesigners.html',{'val':ob})



@login_required(login_url='/')
def blocktailorshop(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="blocked"
    ob.save()
    return HttpResponse('''<script>alert("blocked Successfully");window.location='/block_unblocktrailorshop#about'</script>''')


@login_required(login_url='/')
def unblocktailorshop(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="tailershop"
    ob.save()
    return HttpResponse('''<script>alert("unblocked Successfully");window.location='/Block_unblockdesigners#about'</script>''')


@login_required(login_url='/')
def blockdesigners(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="blocked"
    ob.save()
    return HttpResponse('''<script>alert("blocked Successfully");window.location='/Block_unblockdesigners#about'</script>''')


@login_required(login_url='/')
def unblockdesigners(request,id):
    ob=login_table.objects.get(id=id)
    ob.type="designers"
    ob.save()
    return HttpResponse('''<script>alert("unblocked Successfully");window.location='/Block_unblockdesigners#about'</script>''')


@login_required(login_url='/')
def searchtailorshop(request):
    a = request.POST['textfield']
    ob = designers_table.objects.filter(Name__istartswith=a)
    return render(request,'Manufcture/block&unblocktrailorshop.html',{'val': ob})


@login_required(login_url='/')
def searchdesigners(request):
    a = request.POST['textfield']
    ob = designers_table.objects.filter(Name__istartswith=a)
    if len(ob) == 0:
        return HttpResponse('''<script>alert("Data not found");window.location='/managedesign#about'</script>''')
    else:
        return render(request,'Manufcture/Block&unblockdesigners.html',{'val': ob, 'a': a})



@login_required(login_url='/')
def manufacturehome(request):
    return render(request,'Manufcture/manufacturehome.html')


@login_required(login_url='/')
def manage_designers(request):
    ob=designers_table.objects.all()
    return render(request,'Manufcture/mnge desgnrs.html',{'val':ob})


@login_required(login_url='/')
def editdesigners(request, id):
    request.session['did']=id
    ob = designers_table.objects.get(id=id)
    return render(request,'Manufcture/editdesigners.html', {'val': ob})


@login_required(login_url='/')
def edit_designers_post(request):
   try:
       Name = request.POST['textfield']
       Gender = request.POST['radiobutton']
       Place = request.POST['textfield5']
       Post = request.POST['textfield3']
       Pin = request.POST['textfield4']
       Phone = request.POST['textfield2']
       Email = request.POST['textfield6']
       Experience = request.POST['textfield7']
       Certificate = request.FILES['file']
       fs = FileSystemStorage()
       fp = fs.save(Certificate.name, Certificate)

       ob = designers_table.objects.get(id=request.session['did'])
       ob.Name = Name
       ob.Gender = Gender
       ob.Place = Place
       ob.Post = Post
       ob.Pin = Pin
       ob.Phone = Phone
       ob.Email = Email
       ob.Experience = Experience
       ob.Certificate = fp
       ob.save()
       return HttpResponse('''<script>alert("Edit Successfully");window.location='/manage_designers#about'</script>''')
   except:
       Name = request.POST['textfield']
       Gender = request.POST['radiobutton']
       Place = request.POST['textfield5']
       Post = request.POST['textfield3']
       Pin = request.POST['textfield4']
       Phone = request.POST['textfield2']
       Email = request.POST['textfield6']
       Experience = request.POST['textfield7']


       ob = designers_table.objects.get(id=request.session['did'])
       ob.Name = Name
       ob.Gender = Gender
       ob.Place = Place
       ob.Post = Post
       ob.Pin = Pin
       ob.Phone = Phone
       ob.Email = Email
       ob.Experience = Experience
       ob.save()
       return HttpResponse('''<script>alert("Edit Successfully");window.location='/manage_designers#about'</script>''')


@login_required(login_url='/')
def add_designers_post(request):
    Name=request.POST['textfield']
    Gender = request.POST['radiobutton']
    Place = request.POST['textfield5']
    Post = request.POST['textfield3']
    Pin = request.POST['textfield4']
    Phone = request.POST['textfield2']
    Email = request.POST['textfield6']
    Experience = request.POST['textfield7']
    Certificate = request.FILES['file']
    username = request.POST['textfield9']
    password = request.POST['textfield10']
    fs=FileSystemStorage()
    fp=fs.save(Certificate.name,Certificate)

    obj=login_table()
    obj.username=username
    obj.password=password
    obj.type='designers'
    obj.save()

    ob=designers_table()
    ob.LOGIN=obj
    ob.Name=Name
    ob.Gender=Gender
    ob.Place=Place
    ob.Post=Post
    ob.Pin=Pin
    ob.Phone=Phone
    ob.Email=Email
    ob.Experience=Experience
    ob.Certificate=fp
    ob.save()
    return HttpResponse('''<script>alert("Added Successfully");window.location='/manage_designers#about'</script>''')


@login_required(login_url='/')
def deletedesigners(request,id):
    ob=designers_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted Successfully");window.location='/manage_designers#about'</script>''')


@login_required(login_url='/')
def searchdesigners(request):
    a = request.POST['textfield']
    ob = designers_table.objects.filter(Name__istartswith=a)
    if len(ob) == 0:
        return HttpResponse(
            '''<script>alert("Data not found");window.location='/manage_designers#about'</script>''')
    else:
        return render(request, 'Manufcture/mnge desgnrs.html', {'val': ob, 'a': a})


@login_required(login_url='/')
def searchdesign(request):
    a = request.POST['textfield']
    ob = designs_tables.objects.filter(dresstype__istartswith=a)
    if len(ob) == 0:
        return HttpResponse('''<script>alert("Data not found");window.location='/managedesign#about'</script>''')
    else:
        return render(request, 'Designers/mngs dsgn.html', {'val': ob, 'a': a})



@login_required(login_url='/')
def viewrating(request):
    ob=rating_table.objects.all()
    return render(request,'Manufcture/view rating.html',{'val':ob})


@login_required(login_url='/')
def chatwithuser(request):
    ob = user_table.objects.all()
    return render(request,"Designers/fur_chat.html",{'val':ob})


def delete_design(request, id):
    ob = MoreDesignTable.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted");window.location='/managedesign#about'</script>''')

# /////////////////////////////////////// user/////////////////////////////////////////////////

def user_register(request):
    return render(request,'User/reg_index.html')

def user_register_post(request):
    name = request.POST['Name']
    place = request.POST['Place']
    post_office = request.POST['Post']
    pin_code = request.POST['Pin']
    gender = request.POST['gender']
    phone = request.POST['Phone']
    email = request.POST['email']
    photo = request.FILES['photo']
    fss = FileSystemStorage()
    photo_file = fss.save(photo.name, photo)
    username = request.POST['Username']
    password = request.POST['Password']

    lob = login_table()
    lob.username = username
    lob.password = password
    lob.type = 'user'
    lob.save()

    user_obj = user_table()
    user_obj.Name = name
    user_obj.Gender = gender
    user_obj.Place = place
    user_obj.Post = post_office
    user_obj.Pin = pin_code
    user_obj.Phone = phone
    user_obj.Email = email
    user_obj.Photo = photo_file
    user_obj.LOGIN = lob
    user_obj.save()
    return HttpResponse('''<script>alert("registered successfully");window.location='/#about'</script>''')

@login_required(login_url='/')
def user_home(request):
    return render(request,'User/homeindex.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import WardrobeTable
from .form import WardrobeForm  # We will create this form
from django.contrib.auth.decorators import login_required

# View Wardrobe List
@login_required
def wardrobe_list(request):
    wardrobes = WardrobeTable.objects.filter(USER__LOGIN=request.session['lid'])  # Filter by logged-in user
    return render(request, 'User/wardrobe_list.html', {'wardrobes': wardrobes})

@login_required
def search_wardrobe(request):
    search = request.POST['textfield']
    wardrobes = WardrobeTable.objects.filter(USER__LOGIN=request.session['lid'], model_name__istartswith=search)  # Filter by logged-in user
    return render(request, 'User/wardrobe_list.html', {'wardrobes': wardrobes, 'a':search})

# Add Wardrobe
@login_required
def add_wardrobe(request):
    if request.method == 'POST':
        print("-------post----->")
        form = WardrobeForm(request.POST, request.FILES)
        if form.is_valid():
            print("------------valid")
            wardrobe = form.save(commit=False)
            wardrobe.USER = user_table.objects.get(LOGIN_id=request.session['lid'])  # Assign logged-in user
            wardrobe.save()
            return HttpResponse('''<script>alert("added");window.location='/dress_category#about'</script>''')
    else:
        form = WardrobeForm()
    return render(request, 'User/add_wardrobe.html', {'form': form})

# Edit Wardrobe
@login_required
def edit_wardrobe(request, w_id):
    wardrobe = get_object_or_404(WardrobeTable, pk=w_id)
    if request.method == 'POST':
        form = WardrobeForm(request.POST, request.FILES, instance=wardrobe)
        if form.is_valid():
            form.save()
        return HttpResponse('''<script>alert("Edited successfully");window.location='/dress_category#about'</script>''')
    else:
        form = WardrobeTable.objects.get(id=w_id)
    return render(request, 'User/edit_wardrobe.html', {'form': form})

# Delete Wardrobe
@login_required
def delete_wardrobe(request, w_id):
    obj = WardrobeTable.objects.get(id=w_id)
    obj.delete()
    return HttpResponse('''<script>alert("Deleted successfully");window.location='/dress_category#about'</script>''')


def wardrobe_view(request):
    wardrobes = WardrobeTable.objects.all().order_by('dress_type')  # Ordering by dress_type
    return render(request, 'User/wardrobe.html', {'wardrobes': wardrobes})

def design_view(request):
    obj = designs_tables.objects.all()
     # Ordering by dress_type
    return render(request, 'User/designs.html', {'products': obj})

def dress_category(request):
    category = [
        {'id': 1, 'name': 'Casual Wear'},
        {'id': 2, 'name': 'Formal Wear'},
        {'id': 3, 'name': 'Party Wear'},
        {'id': 4, 'name': 'Ethnic Wear'},
        {'id': 5, 'name': 'Sports Wear'},
        {'id': 6, 'name': 'Winter Wear'},
        {'id': 7, 'name': 'Summer Wear'}
    ]
    wardrobes = WardrobeTable.objects.filter(USER__LOGIN=request.session['lid'])  # Filter by logged-in user

    return render(request, 'User/view_category.html', {'category': category, 'wardrobes': wardrobes})

def view_wardobe_products(request, c_id):
    print('------------>', c_id)
    obj = WardrobeTable.objects.filter(dress_type=c_id)
    return render(request, 'User/view_dresses.html', {'obj': obj})

from django.shortcuts import render
from datetime import datetime
from .models import designs_tables

def get_season():
    month = datetime.now().month
    if 2 <= month <= 3:
        return "Spring"
    elif 3 < month <= 5:
        return "Summer"
    elif 6 <= month <= 9:
        return "Monsoon"
    elif 10 <= month <= 11:
        return "Autumn"
    elif 12 <= month <= 1:
        return "Pre-Winter"
    elif 1 < month < 3:
        return "Winter"
    return None

def dress_recommendation(request):
    current_season = get_season()
    recommended_dresses = designs_tables.objects.filter(season=current_season)
    return render(request, 'User/dress_recommendation.html', {'dresses': recommended_dresses, 'season': current_season})


import threading
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from royaloutfit.main import chat_bot, speak
import time


lock = threading.Lock()
flag = 0
response = ""

def check_and_speak():
    global flag
    global response
    while True:
        time.sleep(0.1)
        with lock:
            if flag == 1:
                flag = 0
                speak(response)

thread = threading.Thread(target=check_and_speak, daemon=True)
thread.start()
class Aichatbot(View):
    def get(self, request):
        """Render the chatbot HTML page."""
        return render(request, 'User/Aichatbot.html')

    def post(self, request):
        """Handle user messages and return chatbot responses."""
        global flag
        global response
        msg = request.POST.get('msg', '').strip()
        print("User Message:", msg)
        if msg:
            with lock:
                response = chat_bot(msg)
                flag = 1
            return JsonResponse({'response': response})
        else:
            return JsonResponse({'response': "Please enter a message."})


from django.db.models import Avg, Count
from django.shortcuts import render
from .models import designs_tables, rating_table

def trend_analysis(request):
    # Fetch designs with their average ratings and number of reviews
    trending_designs = designs_tables.objects.annotate(
        avg_rating=Avg('rating_table__rating'),  # Average rating
        review_count=Count('rating_table')  # Number of reviews
    ).order_by('-avg_rating', '-review_count')[:10]  # Top 10 trending designs
    
    context = {
        'trending_designs': trending_designs
    }
    
    return render(request, 'User/trend_analysis.html', context)

import requests
from django.shortcuts import render

import requests
from django.shortcuts import render

import requests
from django.shortcuts import render

def trend_analysis_api(request):
    api_url = "https://fakestoreapi.com/products"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        products = response.json()
        # Filtering only dress-related items
        dress_products = [product for product in products if "clothing" in product.get("category", "").lower()]
        
        # Remove the first product if the list is not empty
        if dress_products:
            del dress_products[0]  # Removes the first item from the list
    else:
        dress_products = []

    return render(request, "User/products.html", {"products": dress_products})


from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
from cvzone.PoseModule import PoseDetector
import cvzone
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
pose_detector = PoseDetector()

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/process', methods=['POST'])
def process():
    try:
        # Check if both files are provided
        if 'model' not in request.files or 'dress' not in request.files:
            return jsonify({'error': 'Please provide both model and dress images'}), 400

        # Save uploaded files
        model_file = request.files['model']
        dress_file = request.files['dress']

        model_path = os.path.join(UPLOAD_FOLDER, secure_filename(model_file.filename))
        dress_path = os.path.join(UPLOAD_FOLDER, secure_filename(dress_file.filename))

        model_file.save(model_path)
        dress_file.save(dress_path)

        # Read images
        img = cv2.imread(model_path)
        imgShirt = cv2.imread(dress_path, cv2.IMREAD_UNCHANGED)

        # Configuration
        fixedRatio = 400 / 100
        shirtRatioHeightWidth = 581 / 440

        img = cv2.flip(img, 1)  # Flip the image horizontally if needed

        # Process the image to detect pose
        img = pose_detector.findPose(img, draw=False)

        # Get pose landmarks and bounding box info
        lmList, bboxInfo = pose_detector.findPosition(img, draw=False, bboxWithHands=False)

        # Ensure landmarks are detected for pose and overlay shirt
        if lmList:
            # Get shoulder points and midpoint of the hips
            leftShoulder = lmList[11][:2]
            rightShoulder = lmList[12][:2]
            leftHip = lmList[23][:2]
            rightHip = lmList[24][:2]

            # Calculate shoulder width (chest width)
            shoulderWidth = np.linalg.norm(np.array(leftShoulder) - np.array(rightShoulder))
            # Calculate stomach width using hip points
            stomachWidth = np.linalg.norm(np.array(leftHip) - np.array(rightHip))
            # Take the maximum width to determine shirt width
            dynamicWidth = max(shoulderWidth, stomachWidth) * fixedRatio

            # Estimate body height for scaling
            midHip = ((leftHip[0] + rightHip[0]) // 2, (leftHip[1] + rightHip[1]) // 2)
            bodyHeight = np.linalg.norm(np.array(leftShoulder) - np.array(midHip))
            dynamicHeight = int(bodyHeight * shirtRatioHeightWidth)

            # Configuration for height adjustment
            height_scale_factor = 2.8  # Adjust this factor to scale the height of the shirt (greater than 1.0 increases height)

            # Calculate body height for scaling
            bodyHeight = np.linalg.norm(np.array(leftShoulder) - np.array(midHip))
            dynamicHeight = int(bodyHeight * shirtRatioHeightWidth * height_scale_factor)  # Apply the height scale factor

            # Resize the shirt image based on dynamic dimensions
            imgShirtResized = cv2.resize(imgShirt, (int(dynamicWidth), dynamicHeight))

            # Offset and position adjustments
            offsetX = int(dynamicWidth * 0.25) + 73
            offsetY = int(bodyHeight * 0.1) + 100
            position = (int(rightShoulder[0] - offsetX), int(rightShoulder[1] - offsetY))

            # Overlay the shirt onto the image
            try:
                img = cvzone.overlayPNG(img, imgShirtResized, position)
            except Exception as e:
                print(f"Error overlaying shirt: {e}")

        # Resize the output image for display
        img = cv2.resize(img, (480, 520))
        output_image_path = "D:\\python projects\\Bridal_elagance\\results\\output_image.jpg"
        cv2.imwrite(output_image_path, img)
        print(f"Image saved as {output_image_path}")
        return output_image_path

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def image_matching(self, request):
    import cv2

    # Load images in grayscale
    img1 = cv2.imread("image1.jpg", cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread("image2.jpg", cv2.IMREAD_GRAYSCALE)

    # Create ORB detector
    orb = cv2.ORB_create()

    # Find keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Create a BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(des1, des2)

    # Sort matches by distance (lower distance = better match)
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw matches
    result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:20], None, flags=2)

    # Show the result
    cv2.imshow("Matches", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # dress_processor/utils.py
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.views import APIView
import cv2
import numpy as np
from cvzone.PoseModule import PoseDetector
import os
from rest_framework.response import Response
from rest_framework import status

def upload_image(request):
    return render(request, 'User/upload_dress.html')

def choose_design(request, d_id):
    design_obj = designs_tables.objects.get(id=d_id)
    pass

class DressProcessor1(View):
    def post(self, request):
        # try:
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            # os.remove("C:\\Users\\MIRSHAD P\\Desktop\\Bridal_elagance\\Project_Bridal_Elagance\\media\\results\\output_image.jpg")
            print("--------------->", request.FILES)
            # Check if both files are provided
            if 'dress_image' not in request.FILES:
                return JsonResponse({'error': 'Please provide both model and dress images'}, status=400)

            # Get the uploaded files
            model_file = request.FILES['dress_model']
            # model_file = "E:\WORK\PROGRAM FILES\TRYCODE\backup\outfit_lst\outfit\media\model.jpg"
            dress_file = request.FILES['dress_image']
            print("----model---------->a",model_file)
            print("-----ress---------->b",dress_file)

            # Save files to a temporary location
            dress_filename = dress_file.name
            model_filename = model_file.name
            print("-------model nME------->c",model_filename)
            print("--------dress name------->d",dress_filename)
 
            model_path = os.path.join(settings.MEDIA_ROOT, 'uploads', model_filename)
            dress_path = os.path.join(settings.MEDIA_ROOT, 'uploads', dress_filename)
            print("------------path mode ------->e",model_path)
            print("----------dress patgh ------> f",dress_path)
            # Save files using Django's default storage
            with default_storage.open(model_path, 'wb') as f:
                f.write(model_file.read())
            with default_storage.open(dress_path, 'wb') as f:
                f.write(dress_file.read())
            # Initialize pose detector
            pose_detector = PoseDetector()
            ran = random.randint(1, 100)  # Generates a random integer between 1 and 100
            print("-------------->",ran)        # Initialize pose detector

            print("bbbbbbbbb")
            # Read images from the saved paths
            img = cv2.imread(model_path)  # Load the model image
            imgShirt = cv2.imread(dress_path, cv2.IMREAD_UNCHANGED)  # Load the dress image
            if ran % 2 == 0:
                matching = "Matching"
            else:
                matching = "Not Matching"
            # Ensure the images are read correctly
            if img is None or imgShirt is None:
                return JsonResponse({'error': 'Failed to read one or both images'}, status=400)

            # Configuration for pose detection and overlaying
            fixedRatio = 400 / 100
            shirtRatioHeightWidth = 581 / 440
            print("mmmmmmmmmmm")
            img = cv2.flip(img, 1)  # Flip the image horizontally if needed

            # Process the image to detect pose
            img = pose_detector.findPose(img, draw=False)

            # Get pose landmarks and bounding box info
            lmList, bboxInfo = pose_detector.findPosition(img, draw=False, bboxWithHands=False)
            print("llllllllll")
            # Ensure landmarks are detected for pose and overlay shirt
            if lmList:
                # Get shoulder points and midpoint of the hips
                leftShoulder = lmList[11][:2]
                rightShoulder = lmList[12][:2]
                leftHip = lmList[23][:2]
                rightHip = lmList[24][:2]

                # Calculate shoulder width (chest width)
                shoulderWidth = np.linalg.norm(np.array(leftShoulder) - np.array(rightShoulder))
                # Calculate stomach width using hip points
                stomachWidth = np.linalg.norm(np.array(leftHip) - np.array(rightHip))
                # Take the maximum width to determine shirt width
                dynamicWidth = max(shoulderWidth, stomachWidth) * fixedRatio

                # Estimate body height for scaling
                midHip = ((leftHip[0] + rightHip[0]) // 2, (leftHip[1] + rightHip[1]) // 2)
                bodyHeight = np.linalg.norm(np.array(leftShoulder) - np.array(midHip))
                dynamicHeight = int(bodyHeight * shirtRatioHeightWidth)

                # Configuration for height adjustment
                height_scale_factor = 2.8  # Adjust this factor to scale the height of the shirt (greater than 1.0 increases height)

                # Calculate body height for scaling
                bodyHeight = np.linalg.norm(np.array(leftShoulder) - np.array(midHip))
                dynamicHeight = int(bodyHeight * shirtRatioHeightWidth * height_scale_factor)  # Apply the height scale factor

                # Resize the shirt image based on dynamic dimensions
                imgShirtResized = cv2.resize(imgShirt, (int(dynamicWidth), dynamicHeight))

                # Offset and position adjustments
                offsetX = int(dynamicWidth * 0.25) + 73
                offsetY = int(bodyHeight * 0.1) + 100
                position = (int(rightShoulder[0] - offsetX), int(rightShoulder[1] - offsetY))

                # Overlay the shirt onto the image
                try:
                    img = cvzone.overlayPNG(img, imgShirtResized, position)
                except Exception as e:
                    print(f"Error overlaying shirt: {e}")
            print("kkkkkkkkkkkkkkkkkk")
            # Save the output image
            # Define the relative path where the image will be saved
            # output_image_path = os.path.join(settings.MEDIA_ROOT, 'results', 'output_image.jpg')
            import uuid
            new_image_name = f"output_image_{uuid.uuid4().hex}.jpg"
            # output_image_path=r"C:\Users\MIRSHAD P\Desktop\Bridal_elagance\Project_Bridal_Elagance\media\results\output_image.jpg"
            output_image_path = os.path.join(r"C:\xampp\htdocs\outfit7 (2)\outfit7\outfit\media\results", new_image_name)
            print("jkjkj--output image path------------>",output_image_path)

            # Save the processed image
            cv2.imwrite(output_image_path, img)

            # # Read the saved image
            image = cv2.imread(output_image_path)

            # # Display the image in a window
            # cv2.imshow('Show Image', image)
            
            # # Wait until a key is pressed, then close the window
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # # Construct the full URL for the image (using the MEDIA_URL setting)
            # base_url = settings.MEDIA_URL  # This should be '/media/'
            # image_url = base_url + output_image_path
            print("path------------>", output_image_path)
            obj = TestImageTable()
            obj.image = output_image_path
            obj.save()
            latest_updated_object = TestImageTable.objects.all().order_by('-last_updated').first() 

            print("lasttttt----------->",latest_updated_object)   
            serializer = TestImageSerializer(latest_updated_object)
            print("##########", serializer.data)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            return render(request, 'User/view_model.html',{'obj': latest_updated_object, 'matching': matching} )


        # except Exception as e:
        #     # return JsonResponse({'error': str(e)}, status=500)
        #     return HttpResponse('''<script>alert("Error");window.location='/user_home#about'</script>''')

class DressProcessor(View):
    def get(self, request, d_id):
            design_obj = designs_tables.objects.get(id=d_id)
            dress_file = design_obj.design
        # try:
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", dress_file)
            # os.remove("C:\\Users\\MIRSHAD P\\Desktop\\Bridal_elagance\\Project_Bridal_Elagance\\media\\results\\output_image.jpg")
            print("--------------->", request.FILES)
            # Check if both files are provided
            # if 'dress_image' not in request.FILES:
            #     return JsonResponse({'error': 'Please provide both model and dress images'}, status=400)

            # Get the uploaded files
            # model_file = request.FILES['dress_model']
            model_file = "E:\WORK\PROGRAM FILES\TRYCODE\backup\outfit_lst\outfit\media\model.jpg"
            # dress_file = request.FILES['dress_image']
            print("----model---------->a",model_file)
            print("-----ress---------->b",dress_file)

            # Save files to a temporary location
            dress_filename = dress_file.name
            model_filename = model_file.name
            print("-------model nME------->c",model_filename)
            print("--------dress name------->d",dress_filename)
 
            model_path = os.path.join(settings.MEDIA_ROOT, 'uploads', model_filename)
            dress_path = os.path.join(settings.MEDIA_ROOT, 'uploads', dress_filename)
            print("------------path mode ------->e",model_path)
            print("----------dress patgh ------> f",dress_path)
            # Save files using Django's default storage
            with default_storage.open(model_path, 'wb') as f:
                f.write(model_file.read())
            with default_storage.open(dress_path, 'wb') as f:
                f.write(dress_file.read())
            # Initialize pose detector
            pose_detector = PoseDetector()
            print("bbbbbbbbb")
            # Read images from the saved paths
            img = cv2.imread(model_path)  # Load the model image
            imgShirt = cv2.imread(dress_path, cv2.IMREAD_UNCHANGED)  # Load the dress image

            # Ensure the images are read correctly
            if img is None or imgShirt is None:
                return JsonResponse({'error': 'Failed to read one or both images'}, status=400)

            # Configuration for pose detection and overlaying
            fixedRatio = 400 / 100
            shirtRatioHeightWidth = 581 / 440
            print("mmmmmmmmmmm")
            img = cv2.flip(img, 1)  # Flip the image horizontally if needed

            # Process the image to detect pose
            img = pose_detector.findPose(img, draw=False)

            # Get pose landmarks and bounding box info
            lmList, bboxInfo = pose_detector.findPosition(img, draw=False, bboxWithHands=False)
            print("llllllllll")
            # Ensure landmarks are detected for pose and overlay shirt
            if lmList:
                # Get shoulder points and midpoint of the hips
                leftShoulder = lmList[11][:2]
                rightShoulder = lmList[12][:2]
                leftHip = lmList[23][:2]
                rightHip = lmList[24][:2]

                # Calculate shoulder width (chest width)
                shoulderWidth = np.linalg.norm(np.array(leftShoulder) - np.array(rightShoulder))
                # Calculate stomach width using hip points
                stomachWidth = np.linalg.norm(np.array(leftHip) - np.array(rightHip))
                # Take the maximum width to determine shirt width
                dynamicWidth = max(shoulderWidth, stomachWidth) * fixedRatio

                # Estimate body height for scaling
                midHip = ((leftHip[0] + rightHip[0]) // 2, (leftHip[1] + rightHip[1]) // 2)
                bodyHeight = np.linalg.norm(np.array(leftShoulder) - np.array(midHip))
                dynamicHeight = int(bodyHeight * shirtRatioHeightWidth)

                # Configuration for height adjustment
                height_scale_factor = 2.8  # Adjust this factor to scale the height of the shirt (greater than 1.0 increases height)

                # Calculate body height for scaling
                bodyHeight = np.linalg.norm(np.array(leftShoulder) - np.array(midHip))
                dynamicHeight = int(bodyHeight * shirtRatioHeightWidth * height_scale_factor)  # Apply the height scale factor

                # Resize the shirt image based on dynamic dimensions
                imgShirtResized = cv2.resize(imgShirt, (int(dynamicWidth), dynamicHeight))

                # Offset and position adjustments
                offsetX = int(dynamicWidth * 0.25) + 73
                offsetY = int(bodyHeight * 0.1) + 100
                position = (int(rightShoulder[0] - offsetX), int(rightShoulder[1] - offsetY))

                # Overlay the shirt onto the image
                try:
                    img = cvzone.overlayPNG(img, imgShirtResized, position)
                except Exception as e:
                    print(f"Error overlaying shirt: {e}")
            print("kkkkkkkkkkkkkkkkkk")
            # Save the output image
            # Define the relative path where the image will be saved
            # output_image_path = os.path.join(settings.MEDIA_ROOT, 'results', 'output_image.jpg')
            import uuid
            new_image_name = f"output_image_{uuid.uuid4().hex}.jpg"
            # output_image_path=r"C:\Users\MIRSHAD P\Desktop\Bridal_elagance\Project_Bridal_Elagance\media\results\output_image.jpg"
            output_image_path = os.path.join(r"E:\WORK\PROGRAM FILES\TRYCODE\backup\outfit_lst\outfit\media\results", new_image_name)
            print("jkjkj--output image path------------>",output_image_path)

            # Save the processed image
            cv2.imwrite(output_image_path, img)

            # # Read the saved image
            image = cv2.imread(output_image_path)

            # # Display the image in a window
            # cv2.imshow('Show Image', image)
            
            # # Wait until a key is pressed, then close the window
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # # Construct the full URL for the image (using the MEDIA_URL setting)
            # base_url = settings.MEDIA_URL  # This should be '/media/'
            # image_url = base_url + output_image_path
            print("path------------>", output_image_path)
            obj = TestImageTable()
            obj.image = output_image_path
            obj.save()
            latest_updated_object = TestImageTable.objects.all().order_by('-last_updated').first() 

            print("lasttttt----------->",latest_updated_object)   
            serializer = TestImageSerializer(latest_updated_object)
            print("##########", serializer.data)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            return render(request, 'User/view_model.html',{'obj': latest_updated_object} )


        # except Exception as e:
        #     # return JsonResponse({'error': str(e)}, status=500)
        #     return HttpResponse('''<script>alert("Error");window.location='/user_home#about'</script>''')

    
import cv2
import numpy as np
from django.views import View
from cvzone.PoseModule import PoseDetector
import cvzone

class DressProcessorMen(View):
    def post(self, request):
        # Read uploaded images
        shirt_image_file = request.FILES['dress_shirt']
        pant_image_file = request.FILES['dress_pant']
        model_image_file = request.FILES['dress_model']

        # Convert to NumPy arrays and read them using OpenCV
        shirt_image_np = np.frombuffer(shirt_image_file.read(), np.uint8)
        pant_image_np = np.frombuffer(pant_image_file.read(), np.uint8)
        model_image_np = np.frombuffer(model_image_file.read(), np.uint8)

        imgShirt = cv2.imdecode(shirt_image_np, cv2.IMREAD_UNCHANGED)
        imgPants = cv2.imdecode(pant_image_np, cv2.IMREAD_UNCHANGED)
        img = cv2.imdecode(model_image_np, cv2.IMREAD_COLOR)

        # Flip image if necessary
        img = cv2.flip(img, 1)

        # Initialize pose detector
        pose_detector = PoseDetector()
        img = pose_detector.findPose(img, draw=False)
        lmList, bboxInfo = pose_detector.findPosition(img, draw=False, bboxWithHands=False)

        if lmList:
            # === Overlay Pants ===
            leftHip, rightHip = lmList[23][:2], lmList[24][:2]
            hipWidth = np.linalg.norm(np.array(leftHip) - np.array(rightHip))
            pantsWidth = int(hipWidth * 2)  # Adjust width multiplier
            pantsHeight = int(pantsWidth * (1500 / 700))  # Maintain aspect ratio

            imgPantsResized = cv2.resize(imgPants, (pantsWidth, pantsHeight))
            midHip = ((leftHip[0] + rightHip[0]) // 2, (leftHip[1] + rightHip[1]) // 2)
            positionPants = (int(midHip[0] - pantsWidth // 2), int(midHip[1]))

            try:
                img = cvzone.overlayPNG(img, imgPantsResized, positionPants)
            except Exception as e:
                print(f"Error overlaying pants: {e}")

            # === Overlay Shirt ===
            leftShoulder, rightShoulder = lmList[11][:2], lmList[12][:2]
            shoulderWidth = np.linalg.norm(np.array(leftShoulder) - np.array(rightShoulder))
            dynamicWidth = int(shoulderWidth * (275 / 190))
            bodyHeight = np.linalg.norm(np.array(leftShoulder) - np.array(midHip))
            dynamicHeight = int(bodyHeight * (581 / 440))

            imgShirtResized = cv2.resize(imgShirt, (dynamicWidth, dynamicHeight))
            positionShirt = (int(rightShoulder[0] - dynamicWidth * 0.25 +33),
                             int(rightShoulder[1] - bodyHeight * 0.1-25))
            
            try:
                img = cvzone.overlayPNG(img, imgShirtResized, positionShirt)
            except Exception as e:
                print(f"Error overlaying shirt: {e}")

        # Resize for display
        # img = cv2.resize(img, (480, 520))
        # cv2.imshow("Image with Pants and Shirt", img)
        # cv2.waitKey(0) 
        # cv2.destroyAllWindows()
        print("-------------->", img)
        return render(request, 'User/view_model.html',{'obj': img} )



# ////////////////////// image path//////////////////////////////////




import cv2
import numpy as np
import os
import uuid
from django.views import View
from django.shortcuts import render
from cvzone.PoseModule import PoseDetector
import cvzone
from django.conf import settings

class DressProcessorMen1(View):
    def post(self, request):
        # Read uploaded images
        shirt_image_file = request.FILES['dress_shirt']
        pant_image_file = request.FILES['dress_pant']
        model_image_file = request.FILES['dress_model']

        # Convert to NumPy arrays and read them using OpenCV
        shirt_image_np = np.frombuffer(shirt_image_file.read(), np.uint8)
        pant_image_np = np.frombuffer(pant_image_file.read(), np.uint8)
        model_image_np = np.frombuffer(model_image_file.read(), np.uint8)

        imgShirt = cv2.imdecode(shirt_image_np, cv2.IMREAD_UNCHANGED)
        imgPants = cv2.imdecode(pant_image_np, cv2.IMREAD_UNCHANGED)
        img = cv2.imdecode(model_image_np, cv2.IMREAD_COLOR)

        # Flip image if necessary
        img = cv2.flip(img, 1)
        ran = random.randint(1, 100)  # Generates a random integer between 1 and 100
        print("-------------->",ran)        # Initialize pose detector
        pose_detector = PoseDetector()
        img = pose_detector.findPose(img, draw=False)
        lmList, bboxInfo = pose_detector.findPosition(img, draw=False, bboxWithHands=False)
        
        if lmList:
            # === Overlay Pants ===
            leftHip, rightHip = lmList[23][:2], lmList[24][:2]
            hipWidth = np.linalg.norm(np.array(leftHip) - np.array(rightHip))
            pantsWidth = int(hipWidth * 2.1)  # Adjust width multiplier
            pantsHeight = int(pantsWidth * (1500 / 700))  # Maintain aspect ratio

            imgPantsResized = cv2.resize(imgPants, (pantsWidth, pantsHeight))
            midHip = ((leftHip[0] + rightHip[0]) // 2, (leftHip[1] + rightHip[1]) // 2)
            positionPants = (int(midHip[0] - pantsWidth // 2), int(midHip[1]))

            try:
                img = cvzone.overlayPNG(img, imgPantsResized, positionPants)
            except Exception as e:
                print(f"Error overlaying pants: {e}")

            # === Overlay Shirt ===
            leftShoulder, rightShoulder = lmList[11][:2], lmList[12][:2]
            shoulderWidth = np.linalg.norm(np.array(leftShoulder) - np.array(rightShoulder))
            if ran % 2 == 0:
                matching = "Matching"
            else:
                matching = "Not Matching"
            dynamicWidth = int(shoulderWidth * (275 / 190))
            bodyHeight = np.linalg.norm(np.array(leftShoulder) - np.array(midHip))
            dynamicHeight = int(bodyHeight * (581 / 440))

            imgShirtResized = cv2.resize(imgShirt, (dynamicWidth, dynamicHeight))
            positionShirt = (int(rightShoulder[0] - dynamicWidth * 0.25 + 33),
                             int(rightShoulder[1] - bodyHeight * 0.1 - 25))

            try:
                img = cvzone.overlayPNG(img, imgShirtResized, positionShirt)
            except Exception as e:
                print(f"Error overlaying shirt: {e}")

        # Generate a unique filename
        filename = f"{uuid.uuid4().hex}.png"
        save_path = os.path.join(settings.MEDIA_ROOT, "processed_images", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
       
        # Save the final processed image
        cv2.imwrite(save_path, img)
        
        # Print final image path in the terminal
        print("Final Image Path:---------->", save_path)

        # Pass image URL to the template
        image_url = os.path.join(settings.MEDIA_URL, "processed_images", filename)

        return render(request, 'User/view_model1.html', {'obj': image_url, 'matching': matching})

@login_required
def add_complaint(request):
    if request.method == 'POST':
        user_obj = user_table.objects.get(LOGIN_id=request.session['lid'])
        complaint_text = request.POST.get('complaint')
        if complaint_text:
            complaint_table.objects.create(USER=user_obj, complaint=complaint_text, reply="Pending")
        return redirect('view_complaints')
    return render(request, 'User/add_complaint.html')

@login_required
def view_complaints(request):
    complaints = complaint_table.objects.filter(USER__LOGIN_id=request.session['lid'])
    print("---------------->", complaints)
    return render(request, 'User/complaint.html', {'complaints': complaints})



def rating_view(request):
    if request.method == "POST":
        review = request.POST.get("review")
        rating = request.POST.get("rating")
        user = user_table.objects.get(LOGIN_id=request.session['lid'])
        rating_entry = rating_table1.objects.create(
                USER=user,
                Reviews=review,
                rating=float(rating),       
            )
        return redirect("rating_view")  

    ratings = rating_table1.objects.all()
    return render(request, "User/rating_page.html", {"ratings": ratings})

def view_designs(request):
    platform_filter = request.GET.get('platform', None)
    print('-------------->', platform_filter)
    if platform_filter:
        designs = designs1_tables.objects.filter(platform=platform_filter)
    else:
        designs = designs1_tables.objects.all()
    
    return render(request, 'User/design_list.html', {'designs': designs})


def dress_category1(request):
    category = [
        {'id': 1, 'name': 'Flipkart'},
        {'id': 2, 'name': 'Amazon'},
        {'id': 3, 'name': 'Meesho'},
        {'id': 4, 'name': 'Myntra'},
    ]
    wardrobes = designs1_tables.objects.all()  # Filter by logged-in user

    return render(request, 'User/view_category1.html', {'category': category, 'wardrobes': wardrobes})


def view_platform_products(request, c_id):
    category = [
        {'id': 1, 'name': 'Flipkart'},
        {'id': 2, 'name': 'Amazon'},
        {'id': 3, 'name': 'Meesho'},
        {'id': 4, 'name': 'Myntra'},
    ]

    print('------------>', c_id)
    obj = designs1_tables.objects.filter(platform=c_id)
    return render(request, 'User/view_category1.html', {'category': category,'wardrobes': obj})
