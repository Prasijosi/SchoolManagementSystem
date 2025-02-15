from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.contrib.auth import logout
from django.core.mail import send_mail

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/index.html')

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/adminclick.html')

def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/teacherclick.html')

def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/studentclick.html')

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'school/adminsignup.html',{'form':form})

def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        
        else:
            print("form1 errors",form2.errors)
            print("form2 errors",form2.errors)
            
        return HttpResponseRedirect('studentlogin')
    return render(request,'school/studentsignup.html',context=mydict)

def teacher_signup_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':  
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request,'school/teachersignup.html',context=mydict)

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval=models.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request,'school/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.Student.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'school/student_wait_for_approval.html')
        
def logout_view(request):
    logout(request)
    return redirect('')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.Teacher.objects.all().filter(status=True).count()
    pendingteachercount=models.Teacher.objects.all().filter(status=False).count()
    studentcount=models.Student.objects.all().filter(status=True).count()
    pendingstudentcount=models.Student.objects.all().filter(status=False).count()
    teachersalary=models.Teacher.objects.filter(status=True).aggregate(Sum('salary'))
    pendingteachersalary=models.Teacher.objects.filter(status=False).aggregate(Sum('salary'))
    studentfee=models.Student.objects.filter(status=True).aggregate(Sum('fee',default=0))
    pendingstudentfee=models.Student.objects.filter(status=False).aggregate(Sum('fee'))

    notice=models.Notice.objects.all()

    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

        'teachersalary':teachersalary['salary__sum'],
        'pendingteachersalary':pendingteachersalary['salary__sum'],

        'studentfee':studentfee['fee__sum'],
        'pendingstudentfee':pendingstudentfee['fee__sum'],

        'notice':notice

    }

    return render(request,'school/admin_dashboard.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'school/admin_teacher.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-teacher')
    return render(request,'school/admin_add_teacher.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=models.Teacher.objects.all().filter(status=True)
    return render(request,'school/admin_view_teacher.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    teachers=models.Teacher.objects.all().filter(status=False)
    return render(request,'school/admin_approve_teacher.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect(reverse('admin-approve-teacher'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-approve-teacher')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherForm(request.POST,instance=teacher)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-teacher')
    return render(request,'school/admin_update_teacher.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_salary_view(request):
    teachers=models.Teacher.objects.all()
    return render(request,'school/admin_view_teacher_salary.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'school/admin_student.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            return HttpResponseRedirect('admin-student')
    return render(request,'school/admin_add_student.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.Student.objects.all().filter(status=True)
    return render(request,'school/admin_view_student.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentForm(request.POST,instance=student)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-student')
    return render(request,'school/admin_update_student.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students=models.Student.objects.all().filter(status=False)
    return render(request,'school/admin_approve_student.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    students=models.Student.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('admin-approve-student'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_fee_view(request):
    students=models.Student.objects.all()
    return render(request,'school/admin_view_student_fee.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request,'school/admin_attendance.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_take_attendance_view(request,level):
    students=models.Student.objects.all().filter(level=level)
    form=forms.AttendanceForm(request.POST)
    if request.method=='POST':
        if form.is_valid():
            date=form.cleaned_data['date']
            for key, value in request.POST.items():
                if key.startswith('attendance_'):
                    student_id = key.split('_')[1]
                    present_status = value
                    AttendanceModel = models.Attendance()
                    AttendanceModel.level = level
                    AttendanceModel.date = date
                    AttendanceModel.present_status = present_status
                    AttendanceModel.roll_no = students.get(id=student_id).roll_no
                    AttendanceModel.save()
                    
            return redirect('admin-attendance')
        else:
            print('form invalid')
    return render(request,'school/admin_take_attendance.html',{'students':students,'aform':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_attendance_view(request,level):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,level=level)
            studentdata=models.Student.objects.all().filter(level=level)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/admin_view_attendance_page.html',{'level':level,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/admin_view_attendance_ask_date.html',{'level':level,'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fee_view(request):
    return render(request,'school/admin_fee.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_fee_view(request,level):
    feedetails=models.Student.objects.all().filter(level=level)
    return render(request,'school/admin_view_fee.html',{'feedetails':feedetails,'level':level})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('admin-dashboard')
    return render(request,'school/admin_notice.html',{'form':form})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.Teacher.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'salary':teacherdata[0].salary,
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].joindate,
        'notice':notice
    }
    return render(request,'school/teacher_dashboard.html',context=mydict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request,'school/teacher_attendance.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,level):
    students=models.Student.objects.all().filter(level=level)
    form=forms.AttendanceForm(request.POST)
    if request.method=='POST':
        if form.is_valid():
            date=form.cleaned_data['date']
            for key, value in request.POST.items():
                if key.startswith('attendance_'):
                    student_id = key.split('_')[1]
                    present_status = value
                    AttendanceModel = models.Attendance()
                    AttendanceModel.level = level
                    AttendanceModel.date = date
                    AttendanceModel.present_status = present_status
                    AttendanceModel.roll_no = students.get(id=student_id).roll_no
                    AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request,'school/teacher_take_attendance.html',{'students':students,'aform':form})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,level):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,level=level)
            studentdata=models.Student.objects.all().filter(level=level)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/teacher_view_attendance_page.html',{'level':level,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/teacher_view_attendance_ask_date.html',{'level':level,'form':form})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'school/teacher_notice.html',{'form':form})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.Student.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'roll_no':studentdata[0].roll_no,
        'mobile':studentdata[0].mobile,
        'fee':studentdata[0].fee,
        'notice':notice
    }
    return render(request,'school/student_dashboard.html',context=mydict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            studentdata=models.Student.objects.all().filter(user_id=request.user.id,status=True)
            attendancedata=models.Attendance.objects.all().filter(date=date,level=studentdata[0].level,roll_no=studentdata[0].roll_no)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/student_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/student_view_attendance_ask_date.html',{'form':form})

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']

            send_mail(
                f"{name} || {email}", 
                message,  
                settings.EMAIL_HOST_USER,
                [email],  
                fail_silently=False,
            )
            return render(request, 'school/contactussuccess.html')
    return render(request, 'school/contactus.html', {'form': sub})
