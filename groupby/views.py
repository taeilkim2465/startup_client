from django.shortcuts import render, get_object_or_404, redirect
from .models import CareerType, Position, Startup, StartupPosition, StartupImage, StartupPt, StartupTag, StartupMember, TechStack 
from django.utils import timezone
from django.http import Http404
import re

def index(request):
    startup_list = Startup.objects.order_by('id')
    context = {'startup_list': startup_list}
    return render(request, 'groupby/startup_list.html', context)

def detail(request, startup_id):
    startup = get_object_or_404(Startup, pk=startup_id)
    position_list = StartupPosition.objects.filter(startup=startup_id)
    image_list = StartupImage.objects.filter(startup=startup_id)
    tag_list = StartupTag.objects.filter(startup=startup_id)
    member_list = StartupMember.objects.filter(startup=startup_id)
    pt_list = StartupPt.objects.filter(startup=startup_id)
    techstack_list = []
    for position in position_list:
        techstack = position.techStacks.all()
        techstack_list.append(techstack)
    context = {'startup': startup, "position_list":position_list, "image_list":image_list, "tag_list":tag_list, \
        "member_list":member_list, "techstack_list":techstack_list, "pt_list":pt_list}
    return render(request, 'groupby/startup_detail.html', context)

def startup_upload(request):
    position_name_list = Position.objects.all()
    career_type_list = CareerType.objects.all()
    techstack_list = TechStack.objects.all()
    context = {'position_name_list': position_name_list, 'career_type_list': career_type_list, \
        'techstack_list': techstack_list}
    return render(request, 'groupby/startup_upload.html', context)

def html_tag_processor(str):
    str_list = str.split("\r\n")
    in_ol = False
    in_ul = False
    for i, str in enumerate(str_list):
        str = str.strip()
        if in_ol:
            if str[0:2] == "- ":
                in_ol = False
                in_ul =True
                str = "</ol>"+"<ul>"+"<li>"+str[2:]+"</li>"
                str_list[i] = str            

            elif len(re.findall(r"^(\d+. )", str)) != 0:
                in_ol = True
                in_ul = False
                print(re.sub(r"^(\d+. )", "", str))
                str = "<li>"+re.sub(r"^(\d+. )", "", str)+"</li>"
                str_list[i] = str
            
            else: 
                in_ol = False
                in_ul = False
                str = "</ol>"+str+"<br>"
                str_list[i] = str

        elif in_ul:
            if str[0:2] == "- ":
                in_ol = False
                in_ul = True
                str = "<li>"+str[2:]+"</li>"
                str_list[i] = str            

            elif len(re.findall(r"^(\d+. )", str)) != 0:
                in_ol = True
                in_ul = False
                print(re.sub(r"^(\d+. )", "", str))
                str = "</ul>"+"<ol>"+"<li>"+re.sub(r"^(\d+. )", "", str)+"</li>"
                str_list[i] = str
            
            else: 
                in_ol = False
                in_ul = False
                str = "</ul>"+str+"<br>"
                str_list[i] = str

        else:
            if str[0:2] == "- ":
                in_ol = False
                in_ul = True
                str = "<ul>"+"<li>"+str[2:]+"</li>"
                str_list[i] = str            

            elif len(re.findall(r"^(\d+. )", str)) != 0:
                in_ol = True
                in_ul = False
                print(re.sub(r"^(\d+. )", "", str))
                str = "<ol>"+"<li>"+re.sub(r"^(\d+. )", "", str)+"</li>"
                str_list[i] = str
            
            else: 
                in_ol = False
                in_ul = False
                str = str+"<br>"
                str_list[i] = str
        

    result = "".join(str_list)
    if in_ol:
        result += "</ol>"
    elif in_ul:
        result += "</ul>"
    else:
        result = result[:-4]

    return result

def hashtag_parser(str):
    tag_list = re.findall(r'#[^\s]+', str)
    for i in range(len(tag_list)):
        if tag_list[i][0] == "#":
            tag_list[i] = tag_list[i][1:]
    return tag_list

def startup_upload_create(request):
    print(request.POST)
    startup_form = Startup()
    startup_form.name = request.POST['name']
    startup_form.thumbnail = request.FILES['thumbnail']
    startup_form.briefIntro = request.POST['brief_intro']
    startup_form.pitch = request.POST['pitch']
    startup_form.intro = html_tag_processor(request.POST['intro'])
    startup_form.culture = html_tag_processor(request.POST['culture'])
    startup_form.benefit = html_tag_processor(request.POST['benefit'])
    startup_form.save()

    
    tag_list = hashtag_parser(request.POST['tag_name'])
    print("tag_list: ", tag_list)
    for i in range(len(tag_list)):
        print(tag_list[i])
        tag_form  = StartupTag(startup=startup_form, name=tag_list[i])
        tag_form.save()

    
    pt_list = []
    for key in request.POST.keys():
        if "pt_url" in key:
            pt_list.append(key)
    for i in range(len(pt_list)):
        pt_form  = StartupPt(startup=startup_form, url=request.POST[pt_list[i]])
        pt_form.save()


    try:
        images = request.FILES.getlist('image_url')
    except:
        pass
    for image in images:
        image_form=StartupImage(startup=startup_form, url=image)
        image_form.save()


    member_name_list = []
    member_role_list = []
    member_career_list = []
    member_intro_list = []
    for key in request.POST.keys():
        if "member_name" in key:
            member_name_list.append(key)
        elif "member_role" in key:
            member_role_list.append(key)
        elif "member_career" in key:
            member_career_list.append(key)
        elif "member_intro" in key:
            member_intro_list.append(key)

    for i in range(len(member_name_list)):
        member_form = StartupMember(startup=startup_form, name=request.POST[member_name_list[i]], role=request.POST[member_role_list[i]], career=request.POST[member_career_list[i]], intro=html_tag_processor(request.POST[member_intro_list[i]]))
        member_form.save()


    position_name_list = []
    position_qualification_list = []
    position_preferred_list = []
    position_due_date_list = []
    position_task_list = []
    position_position_list = []
    position_career_type_list = []
    position_techstacks_list = []
    for key in request.POST.keys():
        if "position_name" in key:
            position_name_list.append(request.POST[key])
        elif "position_qualification" in key:
            position_qualification_list.append(request.POST[key])
        elif "position_preferred" in key:
            position_preferred_list.append(request.POST[key])
        elif "position_due_date" in key:
            position_due_date_list.append(request.POST[key])
        elif "position_task" in key:
            position_task_list.append(request.POST[key])
        elif "position_position" in key:
            position_position_list.append(request.POST[key])
        elif "position_career_type" in key:
            position_career_type_list.append(request.POST[key])
        elif "position_techstacks" in key:
            position_techstacks_list.append(request.POST.getlist(key))

    for i in range(len(position_name_list)):
        position_form  = StartupPosition(startup=startup_form, name=position_name_list[i], \
            qualification=html_tag_processor(position_qualification_list[i]), preferred=html_tag_processor(position_preferred_list[i]),\
            dueDate=position_due_date_list[i], task=html_tag_processor(position_task_list[i]), \
            position=Position.objects.get(id=position_position_list[i]),\
            careerType=CareerType.objects.get(id=position_career_type_list[i]))
        
        position_form.save()
        print("position_techstacks_list[i]:", position_techstacks_list[i])
        ts_list = position_techstacks_list[i]
        print("ts_list:", ts_list)
        for j in range(len(ts_list)):
            ts=TechStack.objects.get(id=ts_list[j])
            print("ts:", ts)
            print("type(ts):", type(ts))
            position_form.techStacks.add(ts.id)    
        print(position_form.techStacks.all())
    return redirect('/groupby')  


    
    # Startup(name=request.POST.get('name'), content=request.POST.get('content'), create_date=timezone.now())
    # return redirect('groupby:index')

def startup_upload_update(request, startup_id):
    startup = get_object_or_404(Startup, pk=startup_id)
    position_list = StartupPosition.objects.filter(startup=startup_id)
    image_list = StartupImage.objects.filter(startup=startup_id)
    tag_list = StartupTag.objects.filter(startup=startup_id)
    member_list = StartupMember.objects.filter(startup=startup_id)
    pt_list = StartupPt.objects.filter(startup=startup_id)
    position_name_list = Position.objects.all()
    career_type_list = CareerType.objects.all()
    techstack_list = TechStack.objects.all()
    context = {'startup': startup, "position_list":position_list, "image_list":image_list, "tag_list":tag_list, "member_list":member_list,\
        'position_name_list': position_name_list, 'career_type_list': career_type_list, 'techstack_list': techstack_list, "pt_list": pt_list}
    return render(request, 'groupby/startup_update.html', context)

def startup_upload_update_create(request, startup_id):
    print(request)
    startup_form=get_object_or_404(Startup, pk=startup_id)
    startup_form.name = request.POST['name']
    startup_form.thumbnail = request.FILES['thumbnail']
    startup_form.briefIntro = request.POST['briefIntro']
    startup_form.pitch = request.POST['pitch']
    startup_form.intro = request.POST['intro']
    startup_form.culture = request.POST['culture']
    startup_form.benefit = request.POST['benefit']
    startup_form.save()

    tag_list = hashtag_parser(request.POST['tag_name'])
    print("tag_list: ", tag_list)
    for i in range(len(tag_list)):
        print(tag_list[i])
        tag_form  = StartupTag(startup=startup_form, name=tag_list[i])
        tag_form.save()

    
    pt_list = []
    for key in request.POST.keys():
        if "pt_url" in key:
            pt_list.append(key)
    for i in range(len(pt_list)):
        pt_form  = StartupPt(startup=startup_form, url=request.POST[pt_list[i]])
        pt_form.save()


    try:
        images = request.FILES.getlist('image_url')
    except:
        pass
    for image in images:
        image_form=StartupImage(startup=startup_form, url=image)
        image_form.save()


    member_name_list = []
    member_role_list = []
    member_career_list = []
    member_intro_list = []
    for key in request.POST.keys():
        if "member_name" in key:
            member_name_list.append(key)
        elif "member_role" in key:
            member_role_list.append(key)
        elif "member_career" in key:
            member_career_list.append(key)
        elif "member_intro" in key:
            member_intro_list.append(key)

    for i in range(len(member_name_list)):
        member_form = StartupMember(startup=startup_form, name=request.POST[member_name_list[i]], role=request.POST[member_role_list[i]], career=request.POST[member_career_list[i]], intro=html_tag_processor(request.POST[member_intro_list[i]]))
        member_form.save()


    position_name_list = []
    position_qualification_list = []
    position_preferred_list = []
    position_due_date_list = []
    position_task_list = []
    position_position_list = []
    position_career_type_list = []
    position_techstacks_list = []
    for key in request.POST.keys():
        if "position_name" in key:
            position_name_list.append(request.POST[key])
        elif "position_qualification" in key:
            position_qualification_list.append(request.POST[key])
        elif "position_preferred" in key:
            position_preferred_list.append(request.POST[key])
        elif "position_due_date" in key:
            position_due_date_list.append(request.POST[key])
        elif "position_task" in key:
            position_task_list.append(request.POST[key])
        elif "position_position" in key:
            position_position_list.append(request.POST[key])
        elif "position_career_type" in key:
            position_career_type_list.append(request.POST[key])
        elif "position_techstacks" in key:
            position_techstacks_list.append(request.POST.getlist(key))

    for i in range(len(position_name_list)):
        position_form  = StartupPosition(startup=startup_form, name=position_name_list[i], \
            qualification=html_tag_processor(position_qualification_list[i]), preferred=html_tag_processor(position_preferred_list[i]),\
            dueDate=position_due_date_list[i], task=html_tag_processor(position_task_list[i]), \
            position=Position.objects.get(id=position_position_list[i]),\
            careerType=CareerType.objects.get(id=position_career_type_list[i]))
        
        position_form.save()
        print("position_techstacks_list[i]:", position_techstacks_list[i])
        ts_list = position_techstacks_list[i]
        print("ts_list:", ts_list)
        for j in range(len(ts_list)):
            ts=TechStack.objects.get(id=ts_list[j])
            print("ts:", ts)
            print("type(ts):", type(ts))
            position_form.techStacks.add(ts.id)    
        print(position_form.techStacks.all())
    
    return redirect('/groupby')  


def startup_upload_delete(request, startup_id):
    startup = get_object_or_404(Startup, pk=startup_id)
    startup.delete()
    return redirect('/groupby')