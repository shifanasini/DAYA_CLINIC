import datetime
import random

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# from Mod import *
# Create your views here.
from daya_clinic.models import Services, Tips, Employee, Login, Schedule, Feedback, About, Attandance, Contact_details, \
    Patient


def homepage(request):
    return render(request,"ADMIN/homepage.html")
def adm_add_schedule(request):
    if request.method == 'POST':
        did=request.POST['select']
        day=request.POST['select2']
        from_time=request.POST['txt_frm']
        fee=request.POST['fee']
        to_time=request.POST['txt_to']
        doc_obj=Employee.objects.get(id=did)
        schedule_obj =Schedule()
        schedule_obj.day=day
        schedule_obj.from_time=from_time
        schedule_obj.to_time=to_time
        schedule_obj.fee=fee
        schedule_obj.EMPPLOYEE=doc_obj
        schedule_obj.save()
        text = "<script>alert('Schedule Added');window.location='/myapp/adm_add_schedule/';</script>"
        return HttpResponse(text)
    emp_obj = Employee.objects.filter(emp_type="Doctor")
    return render(request,"ADMIN/Add schedule.html",{'data': emp_obj})
def adm_edit_schedule(request,id):
    print("rrr")
    request.session['sch_id']=id
    sch_obj=Schedule.objects.get(id=id)
    print(id)
    employee_obj=Employee.objects.filter(emp_type='Doctor')
    return render(request, "ADMIN/update schedule.html", {'data': sch_obj,'data1':employee_obj})
def adm_update_schedule(request):
    if request.method == 'POST':
        id=request.session['sch_id']
        print("yyy")
        did = request.POST['select']
        day = request.POST['select2']
        from_time = request.POST['txt_frm']
        fee = request.POST['fee']
        to_time = request.POST['txt_to']
        doc_obj = Employee.objects.get(id=did)
        schedule_obj = Schedule.objects.get(id=id)
        schedule_obj.day = day
        schedule_obj.from_time = from_time
        schedule_obj.to_time = to_time
        schedule_obj.fee = fee
        schedule_obj.EMPPLOYEE = doc_obj
        schedule_obj.save()
        text="<script>alert('Schedule Updated');window.location='/myapp/adm_view_schedule/';</script>"
        return HttpResponse(text)

def adm_add_services(request):
    if request.method=='POST':
        serv_name=request.POST['service']

        serv_obj=Services()
        serv_obj.services=serv_name
        serv_obj.date=datetime.datetime.now().date()
        serv_obj.save()
        text = "<script>alert('Service Added');window.location='/myapp/adm_add_services/';</script>"
        return HttpResponse(text)
    return render(request,"ADMIN/ADD_SERVICES.html")

def adm_add_tips(request):
    if request.method == 'POST':
        tips_name = request.POST['tips']

        tips_obj = Tips()
        tips_obj.tips = tips_name
        tips_obj.date = datetime.datetime.now().date()
        tips_obj.save()
        text = "<script>alert('Tips Added');window.location='/myapp/adm_add_tips/';</script>"
        return HttpResponse(text)
    return render(request,"ADMIN/ADD_TIPS.html")

def adm_employee_registration(request):
    if request.method == 'POST':
        emp_name = request.POST['txt_name']

        emp_dob = request.POST['txt_dob']
        emp_type = request.POST['selecttype']
        emp_gender = request.POST['radio_gender']
        emp_place = request.POST['txt_place']
        emp_housename = request.POST['txt_hname']
        emp_district = request.POST['txt_district']
        emp_pincode = request.POST['txt_pincode']
        emp_phno = request.POST['txt_phno']

        emp_state = request.POST['txt_state']
        emp_qualification = request.POST['txt_qualification']
        emp_email = request.POST['txt_email']
        emp_image= request.FILES['fileField']

        password=random.randint(10,99)

        #   SAVE IMAGE
        fs=FileSystemStorage()
        filename=fs.save(emp_image.name,emp_image)

        login_obj=Login()
        login_obj.uname=emp_email
        login_obj.password=password
        login_obj.logintype=emp_type
        login_obj.save()



        employee_obj = Employee()
        employee_obj.emp_name= emp_name

        employee_obj.dob= emp_dob
        employee_obj.gender= emp_gender
        employee_obj.place= emp_place
        employee_obj.housename= emp_housename
        employee_obj.district= emp_district
        employee_obj.pincode= emp_pincode
        employee_obj.state= emp_state
        employee_obj.emial_Id= emp_email
        employee_obj.phone_number= emp_phno
        employee_obj.qualification= emp_qualification
        employee_obj.photo= fs.url(filename)
        employee_obj.LOGIN=login_obj
        employee_obj.emp_type=emp_type
        employee_obj.save()

        text = "<script>alert('Employee Registered');window.location='/myapp/adm_employee_registration/';</script>"
        return HttpResponse(text)

    return render(request,"ADMIN/EMPLOYEE REGISTRATION.html")


def adm_view_employee(request):
    if request.method=="POST":
        emp_search=request.POST['text']
        emp_obj=Employee.objects.filter(emp_name__contains=emp_search)
        return render(request, "ADMIN/VIEW EMPLOYEES.html", {'data': emp_obj})
    emp_obj =Employee.objects.all()
    return render(request,"ADMIN/VIEW EMPLOYEES.html",{'data': emp_obj})

def adm_delete_employee(request,id):
    emp_obj=Employee.objects.get(id=id)
    emp_obj.delete()
    emp_obj = Employee.objects.all()
    text = "<script>alert('Employee Deleted');window.location='/myapp/adm_view_employee/';</script>"
    return HttpResponse(text)
    return render(request, "ADMIN/VIEW EMPLOYEES.html", {'data': emp_obj})

def adm_edit_employee(request,id):
    emp_obj=Employee.objects.get(id=id)

    print(id)
    return render(request, "ADMIN/EMPLOYEE UPDATION.html", {'data': emp_obj})
def adm_update_employee(request):
    if request.method == 'POST':
        emp_name = request.POST['txt_name']

        emp_dob = request.POST['txt_dob']
        emp_type = request.POST['selecttype']
        emp_gender = request.POST['radio_gender']
        emp_place = request.POST['txt_place']
        emp_housename = request.POST['txt_hname']
        emp_district = request.POST['txt_district']
        emp_pincode = request.POST['txt_pincode']
        emp_phno = request.POST['txt_phno']

        emp_state = request.POST['txt_state']
        emp_qualification = request.POST['txt_qualification']
        emp_email = request.POST['txt_email']


        hid_id=request.POST['id']
        print(hid_id)

        employee_obj = Employee.objects.get(pk=hid_id)
        print(employee_obj)
        employee_obj.emp_name = emp_name

        employee_obj.dob = emp_dob
        employee_obj.gender = emp_gender
        employee_obj.place = emp_place
        employee_obj.housename = emp_housename
        employee_obj.district = emp_district
        employee_obj.pincode = emp_pincode
        employee_obj.state = emp_state
        employee_obj.emial_Id = emp_email
        employee_obj.phone_number = emp_phno
        employee_obj.qualification = emp_qualification
        if 'fileField' in request.FILES:
            emp_image = request.FILES['fileField']

            #   SAVE IMAGE
            fs = FileSystemStorage()
            filename = fs.save(emp_image.name, emp_image)
            employee_obj.photo = fs.url(filename)

        employee_obj.emp_type = emp_type
        employee_obj.save()

    text = "<script>alert('Employee Updated');window.location='/myapp/adm_view_employee/';</script>"
    return HttpResponse(text)
    emp_obj = Employee.objects.all()
    return render(request, "ADMIN/VIEW EMPLOYEES.html", {'data': emp_obj})


def adm_employee_updation(request):
    return render(request,"ADMIN/EMPLOYEE UPDATION.html")


def adm_feedback(request):
    feedback_obj =Feedback.objects.all()

    return render(request,"ADMIN/Feedback.html",{'data':feedback_obj})

def adm_add_contact(request):
    if request.method=="POST":
        loc_hint = request.POST['loc_hint']
        contact_number = request.POST['contact_number']
        mail = request.POST['mail']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        cn=Contact_details.objects.all()
        if cn.exists():
            cn=cn[0]
            cn.date = datetime.datetime.now().date()
            cn.loc_hint = loc_hint
            cn.phone_number = contact_number
            cn.latitude = latitude
            cn.longitude = longitude
            cn.email = mail
            cn.save()
        else:
            contact_obj = Contact_details()
            contact_obj.date=datetime.datetime.now().date()
            contact_obj.loc_hint = loc_hint
            contact_obj.phone_number = contact_number
            contact_obj.latitude = latitude
            contact_obj.longitude = longitude
            contact_obj.email = mail
            contact_obj.save()

    cc=Contact_details.objects.all()
    if cc.exists():
        cc=cc[0]

    return render(request,"ADMIN/add contact info.html",{'data':cc})
def adm_leave_approval(request):
    return render(request,"ADMIN/Leave Approval.html")
def admin_view_stock(request):
    return render(request,"ADMIN/LView stock.html")
def adm_feedback_replay(request):
    return render(request,"ADMIN/Send replay to paitents.html")


def adm_add_attendance(request):
    res=Employee.objects.all()
    date = datetime.datetime.now().date()
    if request.method=='POST':
        ids=request.POST.getlist('attendance')
        for id in ids:
            emp=Employee.objects.get(id=id)
            att1=Attandance.objects.filter(EMPLOYEE=emp,date=date)
            tym=datetime.datetime.now().strftime("%H:%M")
            if att1.exists():
                pass
            else:
                att=Attandance()
                att.EMPLOYEE=emp
                att.date=date
                att.from_time=tym
                att.status='checked_in'
                att.save()
        text = "<script>alert('Attendance Added');window.location='/myapp/adm_add_attendance/';</script>"
        return HttpResponse(text)
    arr = []
    att_added = Attandance.objects.filter(date=date)
    for i in att_added:
        arr.append(i.EMPLOYEE.id)
    return render(request,"ADMIN/ADD ATTENDANCE.html",{'data':res, 'arr':arr})
def adm_view_attendance(request):

    at_obj = Attandance.objects.all()
    return render(request,"ADMIN/view attandance1.html",{'data':at_obj})



def adm_checkout(request):
    date = datetime.datetime.now().date()
    ar=[]
    emp=Employee.objects.all()
    for i in emp:
        att1 = Attandance.objects.filter(EMPLOYEE=i, date=date,status='checked_in')
        if att1.exists():
            att=att1[0]
            ar.append(att)
        else:
            pass
    arr = []
    att_added = Attandance.objects.filter(date=date,status='present')
    for i in att_added:
        arr.append(i.EMPLOYEE.id)
    return render(request,"ADMIN/checkout attendance.html",{'data':ar, 'arr':arr})
def adm_checkout_post(request):
    date = datetime.datetime.now().date()
    ids=request.POST.getlist('attendance')
    print(ids)
    for id in ids:
        emp=Employee.objects.get(id=id)
        att1=Attandance.objects.filter(EMPLOYEE=emp,date=date)
        print(att1)
        tym=datetime.datetime.now().strftime("%H:%M")
        if att1.exists():
            att=att1[0]
            att.to_time = tym
            att.status = 'present'
            att.save()
        else:
            pass

    return adm_checkout(request)
    # arr = []
    # att_added = Attandance.objects.filter(date=date)
    # for i in att_added:
    #     arr.append(i.EMPLOYEE.id)
    # return render(request,"ADMIN/ADD ATTENDANCE.html",{'data':res, 'arr':arr})

def adm_view_employees(request):
    return render(request,"ADMIN/VIEW EMPLOYEES.html")
def adm_view_patients(request):
    return render(request,"ADMIN/View patients.html")
def adm_view_sales_report_main(request):
    return render(request,"ADMIN/Sales Repor.html")


def adm_view_schedule(request):

    schedule_obj = Schedule.objects.all()
    return render(request,"ADMIN/View schedule.html",{'data':schedule_obj})
def adm_delete_schedule(request,id):
    schedule_obj=Tips.objects.get(id=id)

    schedule_obj.delete()
    schedule_obj = Schedule.objects.all()
    return render(request, "ADMIN/View schedule.html", {'data': schedule_obj})

def adm_view_services(request):
    service_obj = Services.objects.all()

    return render(request,"ADMIN/View service.html",{'data': service_obj})

def adm_edit_service(request,id):
    serv_obj=Services.objects.get(id=id)
    print(id)
    request.session['uid']=id
    return render(request, "ADMIN/Update service.html", {'data': serv_obj})

def adm_update_service(request):
    if request.method == 'POST':
        service = request.POST['service']


        hid=request.session['uid']
        print(hid)
        service_obj = Services.objects.get(pk=hid)
        print(service_obj)
        service_obj.services=service
        service_obj.save()

        serev_obj = Services.objects.all()

        return render(request, "ADMIN/View service.html", {'data': serev_obj})

def adm_service_updation(request):
    return render(request,"ADMIN/Update service.html")

def adm_delete_services(request,id):
    service_obj=Services.objects.get(id=id)

    service_obj.delete()
    service_obj = Services.objects.all()
    return render(request, "ADMIN/View service.html", {'data': service_obj})


def adm_view_tips(request):
    tips_obj=Tips.objects.all()
    return render(request,"ADMIN/View tips.html",{'data':tips_obj})
def adm_delete_tips(request,id):
    tips_obj=Tips.objects.get(id=id)
    tips_obj.delete()
    tips_obj = Tips.objects.all()
    return render(request, "ADMIN/View tips.html", {'data': tips_obj})
def adm_edit_tip(request,id):
    tip_obj=Tips.objects.get(id=id)
    print(id)
    request.session['uid']=id
    return render(request, "ADMIN/Update tips.html", {'data': tip_obj})

def adm_update_tip(request):
    if request.method == 'POST':
        tip = request.POST['tip']


        hid=request.session['uid']
        print(hid)
        tip_obj = Tips.objects.get(pk=hid)
        print(tip_obj)
        tip_obj.tips=tip
        tip_obj.save()

        tip_obj =Tips.objects.all()
        return render(request, "ADMIN/View tips.html", {'data': tip_obj})



def adm_view_booking_info(request):
    return render(request,"ADMIN/View booking info.html")

def adm_add_about(request):
    if request.method=='POST':
        about_obj=request.POST['about']
        img_obj=request.FILES['fileField']
        fs = FileSystemStorage()
        filename = fs.save(img_obj.name, img_obj)
        image=fs.url(filename)

        date=datetime.datetime.now().date()
        res=About(about=about_obj,photo=image,date=date)
        res.save()

    return render(request,"ADMIN/ABOUT DAYA.html")
def adm_view_about(request):
    about_obj=About.objects.all()
    return render(request,"ADMIN/VIEW ABOUT.html",{'data':about_obj})

def adm_delete_about(request,id):
    ab_obj=About.objects.get(id=id)

    ab_obj.delete()
    ab_obj = About.objects.all()
    return render(request, "ADMIN/VIEW ABOUT.html", {'data': ab_obj})


def adm_edit_about(request,id):
    ab_obj=About.objects.get(id=id)
    print(id)
    request.session['uid']=id
    return render(request, "ADMIN/update about.html", {'data': ab_obj})

def adm_update_about(request):
    if request.method == 'POST':
        about = request.POST['about']


        hid=request.session['uid']
        print(hid)
        ab_obj = About.objects.get(pk=hid)
        print(ab_obj)
        ab_obj.about=about



        if 'fileField' in request.FILES:
            emp_image = request.FILES['fileField']

            #   SAVE IMAGE
            fs = FileSystemStorage()
            filename = fs.save(emp_image.name, emp_image)
            ab_obj.photo = fs.url(filename)


        ab_obj.save()
        ab_obj = About.objects.all()
        return render(request, "ADMIN/VIEW ABOUT.html", {'data': ab_obj})

def adm_temp(request):
    return render(request,"adm_index.html")
# Create your views here.
def homepage_doctor(request):
    return render(request,"DOCTOR/homepagepharmacist.html")
def doc_add_prescription(request):
    return render(request,"DOCTOR/ADD PRESCRIPTION.html")
def doc_view_leave_satatus(request):
    return render(request,"DOCTOR/Leave Status doctor.html")
def doc_add_leave(request):
    return render(request,"DOCTOR/LEAVE APPLICATION DOCTOR.html")
def doc_next_slot(request):
    return render(request,"DOCTOR/Next slot.html")
def doc_add_next_visit(request):
    return render(request,"DOCTOR/NEXT VISIT ENTRY.html")
def doc_view_medicine(request):
    return render(request,"DOCTOR/View medicine.html")
def doc_view_patients(request):
    return render(request,"DOCTOR/View patients doctor.html")

def doc_view_prescription(request):
    return render(request,"DOCTOR/VIew prescription.html")
def doc_view_schedule(request):
    return render(request,"DOCTOR/View schedule.html")








#ANDROID.......



def view_service_patient(request):
    res2 = []
    ma = Services.objects.all()
    for ii in ma:
        ss = {'id': ii.pk, 'services': ii.services}
        res2.append(ss)

    data = {"status": "ok", "res2": res2}
    return JsonResponse(data)

def view_tips_patient(request):
    res2 = []
    ma = Tips.objects.all()
    for ii in ma:
        ss = {'id': ii.pk, 'tips': ii.tips}
        res2.append(ss)

    data = {"status": "ok", "res2": res2}
    return JsonResponse(data)

def view_about_patient(request):
    res2 = []
    ma = About.objects.all()
    for ii in ma:
        ss = {'id': ii.pk, 'about': ii.about,'photo':ii.photo}
        res2.append(ss)

    data = {"status": "ok", "res2": res2}
    return JsonResponse(data)


# def view_contact_info(request):
#     res2 = []
#     ma = Contact_details.objects.all()
#     for ii in ma:
#         ss = {'id': ii.pk, 'phone_number': ii.phone_number,'latitude':ii.latitude,'longitude':ii.longitude,'loc_hint':ii.loc_hint,'email':ii.email}
#         res2.append(ss)
#
#     data = {"status": "ok", "res2": res2}
#     return JsonResponse(data)

def view_contact_info(request):
    ma = Contact_details.objects.all()
    ii=ma[0]
    data = {"status": "ok",  'phone_number': ii.phone_number,'latitude':ii.latitude,'longitude':ii.longitude,'loc_hint':ii.loc_hint,'email':ii.email}
    return JsonResponse(data)

def patients_registration(request):
    if request.method == 'POST':
        pa_name = request.POST['txt_name']

        pa_age = request.POST['txt_age']

        pa_gender = request.POST['radio_gender']
        pa_place = request.POST['txt_place']
        pa_housename = request.POST['txt_hname']
        pa_district = request.POST['txt_district']
        pa_pincode = request.POST['txt_pincode']
        pa_phno = request.POST['txt_phno']

        pa_state = request.POST['txt_state']

        pa_email = request.POST['txt_email']


        password=request.POST['txt_password']




        pa_obj = Patient()
        pa_obj.emp_name= pa_name

        pa_obj.gender= pa_gender
        pa_obj.place= pa_place
        pa_obj.housename= pa_housename
        pa_obj.district= pa_district
        pa_obj.pincode= pa_pincode
        pa_obj.state= pa_state
        pa_obj.emial_Id= pa_email
        pa_obj.phone_number= pa_phno
        pa_obj.password= password



        pa_obj.save()

        data = {"status": "ok"}
        return JsonResponse(data)


