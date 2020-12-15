from django.shortcuts import render, redirect
from django.contrib import messages
from first_app.models import Student, Staff, Admin, Core_course, Calc_fees, Salary, Contact
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse


# Page Redirect Functions


def home(request):
    return render(request, 'index.html')


def login_staff(request):
    return render(request, 'login_staff.html')


def login_student(request):
    return render(request, 'login_student.html')


def login_admin(request):
    return render(request, 'login_admin.html')


def staffregistration(request):
    return render(request, 'register.html')


def student_register_page_fn(request):
    all_course = Core_course.objects.all()
    return render(request, 'student_register_page.html', {"course": all_course})


def admin_register_page_fn(request):
    return render(request, 'admin_register_page.html')


# Student


def student_reg_fn(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            dob = request.POST['dob']
            gender = request.POST['gender']
            mobile_no = request.POST['mobile_no']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            username = request.POST['username']
            email = request.POST['email']
            profile_picture = request.FILES['image']
            course_id = request.POST['course_id']
            temp_date = datetime.datetime.strptime(dob, '%Y-%m-%d')
            today = date.today()
            age = today.year - temp_date.year - ((today.month, today.day) < (temp_date.month, temp_date.day))
            course_id = int(course_id)

            if password1 == password2:
                if Student.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists!')
                    return redirect('student_reg_fn')

                elif Student.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists!')
                    return redirect('student_reg_fn')

                elif Student.objects.filter(mobile_no=mobile_no).exists():
                    messages.info(request, 'Mobile Number already exists!')
                    return redirect('student_reg_fn')

                elif len(str(mobile_no)) != 10:
                    messages.info(request, 'Enter a valid Mobile Number!')
                    return redirect('student_reg_fn')

                elif age < 18:
                    messages.info(request, 'Age doesn\'t match the requirements!')
                    return redirect('student_reg_fn')

                else:
                    student_object = Student(name=name, dob=dob, gender=gender, mobile_no=mobile_no, password=password1,
                                             username=username, profile_pic=profile_picture, email=email,
                                             course_id=course_id)
                    student_object.save()
                    print("Student Created")

            else:
                messages.info(request, 'Password not matching!')
                return redirect('student_reg_fn')

            messages.info(request, "Student Registered!")
            return render(request, 'index.html')
        else:
            return render(request, 'student_register_page.html')
    except Exception as error:
        messages.info(request, error)
        return redirect('student_reg_fn')


def student_login_fn(request):
    try:
        if request.method == 'POST':
            username = request.POST['student_username']
            password = request.POST['student_password']
            student_loglist = Student.objects.get(username=username)
            if password == student_loglist.password:
                request.session['user_id'] = student_loglist.student_id
                return render(request, 'student.html', {'user': student_loglist})

    except:
        return render(request, 'login_student.html', {'student_login_error': "please check the password"})


def student_logout_fn(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    HttpResponse("you are logged out")
    return render(request, 'index.html')


# Staff

def staff_reg(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            dob = request.POST['dob']
            gender = request.POST['gender']
            mobile_no = request.POST['mobile_no']
            skills = request.POST['skills']
            wage = request.POST['wage']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            username = request.POST['username']
            profile_pic = request.FILES['image']
            temp_date = datetime.datetime.strptime(dob, '%Y-%m-%d')
            today = date.today()
            age = today.year - temp_date.year - ((today.month, today.day) < (temp_date.month, temp_date.day))

            if password1 == password2:
                if Staff.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists!')
                    return redirect('staff_reg')
                elif Staff.objects.filter(mobile_no=mobile_no).exists():
                    messages.info(request, 'phone no already exists!')
                    return redirect('staff_reg')
                elif len(str(mobile_no)) != 10:
                    messages.info(request, 'Enter a valid mobile no!')
                    return redirect('staff_reg')
                elif age < 18:
                    messages.info(request, 'Age doesn\'t match the Requirements')
                    return redirect('staff_reg')

                else:
                    staff_object = Staff(name=name, dob=dob, gender=gender, mobile_no=mobile_no, skills=skills,
                                         wage=wage, password1=password1, password2=password2, username=username,
                                         profile_pic=profile_pic)
                    staff_object.save()
                    print("user created")

            else:
                messages.info(request, 'password not matching')
                return redirect('staff_reg')

            messages.info(request, "staff added ....")
            return render(request, 'admin.html')
        else:
            return render(request, 'admin.html')

    except Exception as error:
        messages.info(request, error)
        return redirect('staff_reg')


def staff_login(request):
    try:
        if request.method == 'POST':
            username = request.POST['staff_username']
            password = request.POST['staff_password']
            staff_loglist = Staff.objects.get(username=username)
            if password == staff_loglist.password1:
                request.session['user_id'] = staff_loglist.staff_id
                return render(request, 'staff.html', {'user': staff_loglist})
    except:

        return render(request, 'login_staff.html', {'staff_login_error': "please check the password"})


def staff_logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    HttpResponse("you are logged out")
    return render(request, 'index.html')


# Admin

def admin_reg_fn(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists!')
                    return redirect('admin_reg_fn')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists!')
                    return redirect('admin_reg_fn')
                else:
                    user = Admin(username=username, password1=password1, password2=password2, email=email,
                                 name=name)
                    user.save()
                    print("user created")
            else:
                messages.info(request, 'password not matching')
                return redirect('admin_reg_fn')

            return render(request, 'index.html')
        else:
            return render(request, 'admin_register_page.html')

    except Exception as error:
        messages.info(request, error)
        return redirect('admin_reg_fn')


def admin_login_fn(request):
    try:
        if request.method == 'POST':
            username = request.POST['admin_username']
            password = request.POST['admin_password']
            admin_loglist = Admin.objects.get(username=username)
            if password == admin_loglist.password1:
                request.session['user_id'] = admin_loglist.admin_id
                return render(request, 'admin.html', {'users': admin_loglist})
    except:
        return render(request, 'login_staff.html', {'staff_login_error': "please check the password"})


def admin_logout_fn(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    HttpResponse("you are logged out")
    return render(request, 'index.html')


def view_all_staff(request):
    try:
        if request.session['user_id']:
            all_staff = Staff.objects.all()
            return render(request, 'view_all_staff.html', {'user': all_staff})
    except:
        return render(request,'index.html')


def add_course_fn(request):
    all_staff = Staff.objects.all()
    return render(request, 'add_course.html', {'user': all_staff})


def view_courses(request):
    all_course = Core_course.objects.all()
    return render(request, 'view_all_course.html', {'course': all_course})


def view_all_student_fn(request):
    all_student = Student.objects.all()
    return render(request, 'view_all_student.html', {'user': all_student})


def staff_update(request, staff_id):
    staff_id = int(staff_id)
    selected_staff = Staff.objects.get(staff_id=staff_id)
    return render(request, 'staff_update_page.html', {"staff": selected_staff, 'id': staff_id})


def staff_update_submit(request):
    try:
        if request.method == 'POST':
            staff_id = request.POST['staff_id']
            name = request.POST['name']
            mobile_no = request.POST['mobile_no']
            skills = request.POST['skills']
            wage = request.POST['wage']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            username = request.POST['username']
            profile_pic = request.FILES['image']
            staff = Staff.objects.get(staff_id=staff_id)
            staff.name = name
            staff.mobile_no = mobile_no
            staff.skills = skills
            staff.wage = wage
            staff.password1 = password1
            staff.password2 = password2
            staff.profile_pic = profile_pic
            staff.username = username
            staff.save()
            messages.success(request, "Successfully Edited Subject")
            return HttpResponseRedirect(reverse("staff_update", kwargs={"staff_id": staff_id}))
        else:
            return render(request, 'view_all_staff')
    except Exception as error:
        messages.info(request, error)
        return redirect('view_all_staff')


def staff_delete(request, staff_id):
    staff_id = int(staff_id)
    try:
        staff_selected = Staff.objects.get(staff_id=staff_id)
    except Staff.DoesNotExist:
        return redirect('view_all_staff')
    staff_selected.delete()
    return redirect('view_all_staff')


# Course

def add_course_fn(request):
    all_staff = Staff.objects.all()
    return render(request, 'add_course.html', {'user': all_staff})


def add_course_submit_fn(request):
    try:
        if request.method == 'POST':
            course_name = request.POST['course_name']
            description = request.POST['description']
            duration = request.POST['duration']
            thumbnail = request.FILES['thumbnail']
            staff_id = request.POST['staffs']
            fees = request.POST['fees']
            staff_no = int(staff_id)
            admin_obj = Core_course(course_name=course_name, description=description, duration=duration,
                                    thumbnail=thumbnail, staff_id=staff_no, fees=fees)
            admin_obj.save()
            return render(request, 'admin.html')
        else:
            return redirect(add_course_fn)
    except Exception as error:
        messages.info(request, error)
        return redirect(add_course_fn)


def update_course(request, course_id):
    course_id = int(course_id)
    selected_course = Core_course.objects.get(course_id=course_id)
    staff = Staff.objects.all()
    return render(request, 'update_course.html', {"staff": staff, 'course': selected_course})


def update_course_submit_fn(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST['course_id']
        course_name = request.POST['course_name']
        description = request.POST['description']
        duration = request.POST['duration']
        thumbnail = request.POST['thumbnail']
        staff_id = request.POST['staffs']
        fees = request.POST['fees']
        staff_no = int(staff_id)
        course_no = int(course_id)
        try:
            course = Core_course.objects.get(course_id=course_no)
            course.course_name = course_name
            course.description = description
            course.duration = duration
            course.thumbnail = thumbnail
            course.fees = fees
            course.staff_id = staff_no
            course.save()
            messages.success(request, "Successfully Edited Course")
            return HttpResponseRedirect(reverse("update_course", kwargs={"course_id": course_id}))
        except:
            messages.error(request, "Failed to Edit Course")
            return HttpResponseRedirect(reverse("update_course", kwargs={"course_id": course_id}))


def delete_course(request, course_id):
    course_id = int(course_id)
    try:
        course_selected = Core_course.objects.get(course_id=course_id)
    except Staff.DoesNotExist:
        return redirect("view_course.html", kwargs={'course_id': course_id})
    course_selected.delete()
    return redirect("view_course.html", kwargs={'course_id': course_id})

# Fees

def generate_fees(request):
    all_student = Student.objects.all()
    return render(request, 'generate_fees.html', {'user': all_student})


def generate_fees_save(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        extra_fee = request.POST['extra_fee']
        fee_details = request.POST['fee_details']
        payment = request.POST['payment']
        student_id = int(student_id)
        student_selected = Student.objects.get(student_id=student_id)
        selected_student_course = student_selected.course_id
        course_selected = Core_course.objects.get(course_id=selected_student_course)
        course_fee = course_selected.fees
        course_name = course_selected.course_name
        total_fees = course_fee + int(extra_fee)
        fee_object = Calc_fees(student_id=student_id, course_id=selected_student_course, course_name=course_name,
                               extra_fee=extra_fee, fee_details=fee_details, total_fee=total_fees, payment=payment)
        fee_object.save()
        return render(request, 'admin.html')
    else:
        return render(request, 'generate_fees.html')


# Salary

def generate_salary(request):
    all_staff = Staff.objects.all()
    return render(request, 'generate_salary.html', {'staff': all_staff})


def generate_salary_save(request):
    if request.method == 'POST':
        total_hrs = request.POST['total_hrs']
        worked_hrs = request.POST['worked_hrs']
        status = request.POST['status']
        bonus = request.POST['bonus']
        staff_id = request.POST['staff_id']
        if total_hrs < worked_hrs:
            messages.info(request, 'check total hours and worked hours')
            return redirect(generate_salary)
        else:
            staff_id = int(staff_id)
            staff_sel = Staff.objects.get(staff_id=staff_id)
            wage = staff_sel.wage
            total_salary = int(worked_hrs) * wage
            salary_object = Salary(total_hrs=total_hrs, worked_hrs=worked_hrs, total_salary=total_salary, status=status,
                                   bonus=bonus, staff_id=staff_id)
            salary_object.save()
            return render(request, 'admin.html')
    else:
        return render(request, 'generate_salary.html')


# Contact

def contact(request):
    if request.method == "POST":
        name = request.POST.get('contact_name')
        email = request.POST.get('contact_email')
        subject = request.POST.get('contact_subject')
        contact.contact_name = name
        contact.contact_email = email
        contact.contact_subject = subject
        contact.save()
        return HttpResponse("<h1>Thank You For Contacting Us</h1>")
    return render(request, 'contact.html')
