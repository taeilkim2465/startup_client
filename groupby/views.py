from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Recruit, Image, Tag, Employee 
from .models import Image
from django.utils import timezone
from django.http import Http404

def index(request):
    startup_list = Post.objects.order_by('-create_date')
    context = {'startup_list': startup_list}
    return render(request, 'groupby/startup_list.html', context)

def detail(request, startup_id):
    startup = get_object_or_404(Post, pk=startup_id)
    recruit_list = Recruit.objects.filter(post_id=startup_id)
    image_list = Image.objects.filter(post_id=startup_id)
    tag_list = Tag.objects.filter(post_id=startup_id)
    employee_list = Employee.objects.filter(post_id=startup_id)
    context = {'startup': startup, "recruit_list":recruit_list, "image_list":image_list, "tag_list":tag_list, "employee_list":employee_list}
    return render(request, 'groupby/startup_detail.html', context)

def startup_upload(request):
    return render(request, 'groupby/startup_upload.html')

def startup_upload_create(request):
    print(request.POST)
    post_form = Post()
    post_form.startup_name = request.POST['startup_name']
    post_form.thumbnail_image = request.FILES['thumbnail_image']
    post_form.short_introduce = request.POST['short_introduce']
    post_form.short_form_video = request.POST['short_form_video']
    post_form.startup_introduce = request.POST['startup_introduce']
    post_form.startup_culture = request.POST['startup_culture']
    post_form.startup_welfare = request.POST['startup_welfare']
    post_form.recruit_conference_video = request.POST['recruit_conference_video']
    post_form.create_date = timezone.localtime()
    post_form.save()

    for i in range(1,6):
        tag_form = Tag(post_id=post_form)
        try:
            tag_form.tag = request.POST['tag'+str(i)]
        except:
            continue
        tag_form.save()
   
    try:
        images = request.FILES.getlist('image')
    except:
        pass
    for image in images:
        #id 로 저장하는 방법 찾기
        image_form=Image(post_id=post_form, image=image)
        image_form.save()

    for i in range(1,4):
        employee_form = Employee(post_id=post_form)
        try:
            employee_form.name = request.POST['name'+str(i)]
            employee_form.introduce = request.POST['introduce'+str(i)]
        except:
            continue
        employee_form.save()

    for i in range(1,4):
        recruit_form = Recruit(post_id=post_form)
        try:
            recruit_form.is_recruiting = request.POST['is_recruiting'+str(i)]
            if recruit_form.is_recruiting == "":
                continue
        except:
            print("problem1")
        try:
            recruit_form.recruit_ending = request.POST['recruit_ending'+str(i)]
        except:
            print("problem2")
        try:
            recruit_form.recruit_position = request.POST['recruit_position'+str(i)]
        except:
            print("problem3")
        try:
            recruit_form.techstack = request.POST['techstack'+str(i)]
        except:
            print("problem4")
        try:
            recruit_form.career = request.POST['career'+str(i)]
        except:
            print("problem5")
        try:
            recruit_form.job_info = request.POST['job_info'+str(i)]
        except:
            print("problem6")
        try:
            recruit_form.qualification = request.POST['qualification'+str(i)]
        except:
            print("problem7")
        try:
            recruit_form.preference = request.POST['preference'+str(i)]
        except:
            print("problem8")
        recruit_form.save()
    
    return redirect('/groupby')  


    
    # Post(startup_name=request.POST.get('startup_name'), content=request.POST.get('content'), create_date=timezone.now())
    # return redirect('groupby:index')

def startup_upload_update(request, startup_id):
    startup = get_object_or_404(Post, pk=startup_id)
    recruit_list = Recruit.objects.filter(post_id=startup_id)
    image_list = Image.objects.filter(post_id=startup_id)
    tag_list = Tag.objects.filter(post_id=startup_id)
    employee_list = Employee.objects.filter(post_id=startup_id)
    context = {'startup': startup, "recruit_list":recruit_list, "image_list":image_list, "tag_list":tag_list, "employee_list":employee_list}
    return render(request, 'groupby/startup_update.html', context)

def startup_upload_update_create(request, startup_id):
    post_form=get_object_or_404(Post, pk=startup_id)
    post_form.startup_name = request.POST['startup_name']
    post_form.thumbnail_image = request.FILES['thumbnail_image']
    post_form.short_introduce = request.POST['short_introduce']
    post_form.short_form_video = request.POST['short_form_video']
    post_form.startup_introduce = request.POST['startup_introduce']
    post_form.startup_culture = request.POST['startup_culture']
    post_form.startup_welfare = request.POST['startup_welfare']
    post_form.recruit_conference_video = request.POST['recruit_conference_video']
    post_form.create_date = timezone.localtime()
    post_form.save()

    for i in range(1,6):
        tag_form = Tag(post_id=post_form)
        try:
            tag_form.tag = request.POST['tag'+str(i)]
        except:
            continue
        tag_form.save()
   
    try:
        images = request.FILES.getlist('image')
    except:
        pass
    for image in images:
        #id 로 저장하는 방법 찾기
        image_form=Image(post_id=post_form, image=image)
        image_form.save()

    for i in range(1,4):
        employee_form = Employee(post_id=post_form)
        try:
            employee_form.name = request.POST['name'+str(i)]
            employee_form.introduce = request.POST['introduce'+str(i)]
        except:
            continue
        employee_form.save()

    for i in range(1,4):
        recruit_form = Recruit(post_id=post_form)
        try:
            recruit_form.is_recruiting = request.POST['is_recruiting'+str(i)]
            if recruit_form.is_recruiting == "":
                continue
        except:
            print("problem1")
        try:
            recruit_form.recruit_ending = request.POST['recruit_ending'+str(i)]
        except:
            print("problem2")
        try:
            recruit_form.recruit_position = request.POST['recruit_position'+str(i)]
        except:
            print("problem3")
        try:
            recruit_form.techstack = request.POST['techstack'+str(i)]
        except:
            print("problem4")
        try:
            recruit_form.career = request.POST['career'+str(i)]
        except:
            print("problem5")
        try:
            recruit_form.job_info = request.POST['job_info'+str(i)]
        except:
            print("problem6")
        try:
            recruit_form.qualification = request.POST['qualification'+str(i)]
        except:
            print("problem7")
        try:
            recruit_form.preference = request.POST['preference'+str(i)]
        except:
            print("problem8")
        recruit_form.save()
    
    return redirect('/groupby')  


def startup_upload_delete(request, startup_id):
    startup = get_object_or_404(Post, pk=startup_id)
    startup.delete()
    return redirect('/groupby')