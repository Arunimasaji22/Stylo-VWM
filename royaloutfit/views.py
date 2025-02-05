import json
from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from royaloutfit.models import *


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
    ob=rating_table.objects.all()
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
        type=request.POST['textfield']
        design = request.FILES['file']
        fs=FileSystemStorage()
        fp=fs.save(design.name,design)
        discription =request.POST['textfield2']
        ob=designs_tables.objects.get(id= request.session['did'])
        ob.type=type
        ob.design=fp
        ob.discription=discription
        print("*******************************", request.session['lid'])
        ob.DESIGNER=designers_table.objects.get(LOGIN__id=request.session['lid'])
        ob.save()
    except:
        type = request.POST['textfield']

        discription = request.POST['textfield2']
        ob=designs_tables.objects.get(id= request.session['did'])
        ob.type = type
        ob.discription = discription
        print("*******************************", request.session['lid'])
        ob.DESIGNER = designers_table.objects.get(LOGIN__id=request.session['lid'])
        ob.save()
    return HttpResponse('''<script>alert("edited Successfully");window.location='/managedesign#about'</script>''')


@login_required(login_url='/')
def deletedesign(request,id):
    ob=designs_tables.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted Successfully");window.location='/managedesign#about'</script>''')


@login_required(login_url='/')
def add_design_post(request):
    type=request.POST['textfield']
    design = request.FILES['file']
    discription = request.POST['textfield2']
    season = request.POST['season']

    fs=FileSystemStorage()
    fp=fs.save(design.name,design)

    ob=designs_tables()
    ob.type=type
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
def more_designs(request, id):
    request.session['design_id'] = id
    ob = MoreDesignTable.objects.filter(DESIGN_id=id)
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
    ob = designs_tables.objects.filter(type__istartswith=a)
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
        form = WardrobeForm(request.POST, request.FILES)
        if form.is_valid():
            wardrobe = form.save(commit=False)
            wardrobe.USER = user_table.objects.get(LOGIN_id=request.session['lid'])  # Assign logged-in user
            wardrobe.save()
        return HttpResponse('''<script>alert("added");window.location='/wardrobe#about'</script>''')
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
        return HttpResponse('''<script>alert("Edited successfully");window.location='/wardrobe#about'</script>''')
    else:
        form = WardrobeTable.objects.get(id=w_id)
    return render(request, 'User/edit_wardrobe.html', {'form': form})

# Delete Wardrobe
@login_required
def delete_wardrobe(request, w_id):
    obj = WardrobeTable.objects.get(id=w_id)
    obj.delete()
    return HttpResponse('''<script>alert("Deleted successfully");window.location='/wardrobe#about'</script>''')

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
