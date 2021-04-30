import datetime
import random

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
# from Mod import *
# Create your views here.
from daya_clinic.models import Services, Tips, Employee, Login, Schedule, Feedback, About, Attandance, Contact_details, \
    Patient, book_fee, Slot, Booking, Chat, Medicine, Prescription, Reminder


def homepage(request):
    return render(request,"ADMIN/homepage.html")
def login(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        login_obj=Login.objects.filter(uname=username,password=password)
        if login_obj.exists():
            log=login_obj[0]
            if log.logintype=="admin":
                return homepage(request)
            elif log.logintype=="Doctor":
                request.session['lid']=log.id

                doc_obj=Employee.objects.get(LOGIN_id=Login.objects.get(id=log.id))
                request.session['doc_id']=doc_obj.id
                return homepage_doctor(request)
            else:
                return  HttpResponse("no")
        else:
            return HttpResponse("Invalid username or password")
    else:
        return render(request,"login.html")

def ahome(request):
    return render(request,'admin/adminhome.html')


def adm_add_schedule(request):
    if request.method == 'POST':
        did=request.POST['select']
        day=request.POST['select2']
        from_time=request.POST['txt_frm']
        # fee=request.POST['fee']
        to_time=request.POST['txt_to']
        doc_obj=Employee.objects.get(id=did)
        schedule_obj =Schedule()
        schedule_obj.day=day
        schedule_obj.from_time=from_time
        schedule_obj.to_time=to_time
        # schedule_obj.fee=fee
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
        print(did)
        day = request.POST['select2']
        from_time = request.POST['txt_frm']
       # fee = request.POST['fee']
        to_time = request.POST['txt_to']
        doc_obj = Employee.objects.get(id=did)
        schedule_obj = Schedule.objects.get(id=id)
        schedule_obj.day = day
        schedule_obj.from_time = from_time
        schedule_obj.to_time = to_time
        #schedule_obj.fee = fee
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
        emp_fee = request.POST['fee']

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
        print(login_obj)


        employee_obj = Employee()
        employee_obj.emp_name= emp_name

        employee_obj.dob= emp_dob
        employee_obj.gender= emp_gender
        employee_obj.place= emp_place
        employee_obj.housename= emp_housename
        employee_obj.district= emp_district
        employee_obj.pincode= emp_pincode
        employee_obj.state= emp_state
        employee_obj.fee= emp_fee
        employee_obj.emial_Id= emp_email
        employee_obj.phone_number= emp_phno
        employee_obj.qualification= emp_qualification
        employee_obj.photo= fs.url(filename)
        employee_obj.LOGIN=login_obj
        employee_obj.emp_type=emp_type
        employee_obj.save()
        emp=Employee.objects.get(pk=employee_obj.id)
        book_obj = book_fee()
        book_obj.fee = emp_fee
        book_obj.EMPLOYEE =emp
        book_obj.save()

        text = "<script>alert('Employee Registered');window.location='/myapp/adm_employee_registration/';</script>"
        return HttpResponse(text)

    return render(request,"ADMIN/EMPLOYEE REGISTRATION.html")


def adm_view_employee(request):
    if request.method=="POST":
        emp_search=request.POST['text']
        # book_obj=book_fee.objects.get(EMPLOYEE__emp_name=emp_search)
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
    fee_obj=book_fee.objects.filter(EMPLOYEE=emp_obj)
    if fee_obj.exists():
        fee_obj = book_fee.objects.get(EMPLOYEE=emp_obj)
        # fee_obj=fee_obj[0]
        fee=fee_obj.fee
        fee_obj.save()
    else:
        fee="0"
    return render(request, "ADMIN/EMPLOYEE UPDATION.html", {'data': emp_obj,'fee':fee})
def adm_update_employee(request):
    if request.method == 'POST':
        emp_name = request.POST['txt_name']
       # emp_fee = request.POST['fee']
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
        #employee_obj.fee = emp_fee
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
    emp = Employee.objects.get(pk=employee_obj.id)
    # book_obj = book_fee()
    # book_obj.fee = emp_fee
    # book_obj.EMPLOYEE = emp
    # book_obj.save()
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
    schedule_obj=Schedule.objects.get(id=id)

    schedule_obj.delete()
    schedule_obj = Schedule.objects.all()
    text = "<script>alert('Schedule Deleted');window.location='/myapp/adm_view_schedule/';</script>"
    return HttpResponse(text)
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
        text = "<script>alert('Service Updated');window.location='/myapp/adm_view_services/';</script>"
        return HttpResponse(text)
        return render(request, "ADMIN/View service.html", {'data': serev_obj})

def adm_service_updation(request):
    return render(request,"ADMIN/Update service.html")

def adm_delete_services(request,id):
    service_obj=Services.objects.get(id=id)

    service_obj.delete()
    service_obj = Services.objects.all()
    text = "<script>alert('Service Deleted');window.location='/myapp/adm_view_services/';</script>"
    return HttpResponse(text)
    return render(request, "ADMIN/View service.html", {'data': service_obj})


def adm_view_tips(request):
    tips_obj=Tips.objects.all()
    return render(request,"ADMIN/View tips.html",{'data':tips_obj})
def adm_delete_tips(request,id):
    tips_obj=Tips.objects.get(id=id)
    tips_obj.delete()
    tips_obj = Tips.objects.all()
    text = "<script>alert('Tips Deleted');window.location='/myapp/adm_view_tips/';</script>"
    return HttpResponse(text)
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
        text = "<script>alert('Tips Updated');window.location='/myapp/adm_view_tips/';</script>"
        return HttpResponse(text)
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
        text = "<script>alert('About Added');window.location='/myapp/adm_add_about/';</script>"
        return HttpResponse(text)
    return render(request,"ADMIN/ABOUT DAYA.html")
def adm_view_about(request):
    about_obj=About.objects.all()
    return render(request,"ADMIN/VIEW ABOUT.html",{'data':about_obj})

def adm_delete_about(request,id):
    ab_obj=About.objects.get(id=id)

    ab_obj.delete()
    ab_obj = About.objects.all()
    # text = "<script>alert('About deleted);window.location='/myapp/adm_view_about/';</script>"
    # return HttpResponse(text)
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
        if 'fileField' in request.FILES:
            emp_image = request.FILES['fileField']
            #   SAVE IMAGE
            fs = FileSystemStorage()
            filename = fs.save(emp_image.name, emp_image)
            ab_obj.photo = fs.url(filename)
            ab_obj.about = about
            ab_obj.save()
        else:
            ab_obj.about = about
            ab_obj.save()



        # ab_obj = About.objects.all()
        # text = "<script>alert('About deleted);window.location='/myapp/adm_view_about/';</script>"
        # return HttpResponse(text)
        # return render(request, "ADMIN/VIEW ABOUT.html", {'data': ab_obj})
        return redirect("/myapp/adm_view_about/")

def adm_temp(request):
    return render(request,"adm_index.html")
# Create your views here.


def doc_temp(request):
    return render(request,"doc_index.html")
def doc_view_schedule(request):
    docid=request.session['doc_id']
    schedule_obj = Schedule.objects.filter(EMPPLOYEE_id=docid)
    return render(request,"DOCTOR/View schedule.html",{'data':schedule_obj})
def doc_view_booking(request):
    docid=request.session['doc_id']
    bok_obj = Booking.objects.filter(EMPLOYEE=docid,date=datetime.datetime.now().date())
    if request.method=="POST":
        pat=request.POST['pat']
        bok_obj = Booking.objects.filter(EMPLOYEE_id=docid,PATIENT__patient_name__contains=pat)
    return render(request,"DOCTOR/View booking doctor.html",{'data':bok_obj})

def homepage_doctor(request):
    return render(request,"DOCTOR/homepage_doc.html")

def doc_add_prescription(request,bookid):
    bok_obj=Booking.objects.get(id=bookid)
    pat_name=bok_obj.PATIENT.patient_name
    date=bok_obj.date
    med_obj=Medicine.objects.all()
    request.session['bookid']=bookid
    pres_obj=Prescription.objects.filter(BOOKING=bok_obj)
    return render(request,"DOCTOR/ADD PRESCRIPTION.html",{'data':med_obj,'pat_name':pat_name,'date':date,'data2':pres_obj})

def doc_del_presc(request,id):
    pr=Prescription.objects.get(id=id)
    pr.delete()
    book_id = request.session['bookid']
    return doc_add_prescription(request,book_id)
def doc_add_prescription_post(request):
    btn=request.POST['button']
    med_obj = Medicine.objects.all()
    if btn=="Add":
       pre= request.POST['pres']
       quantity= request.POST['qty']
       unit= request.POST['unit']
       med= request.POST['select']
       book_id=request.session['bookid']
       res=Prescription(prescription=pre,qty=quantity,unit=unit,MEDICINE_id=med,BOOKING_id=book_id)
       res.save()
       bok_obj = Booking.objects.get(id=book_id)
       pat_name = bok_obj.PATIENT.patient_name
       date = bok_obj.date
       pres_obj=Prescription.objects.filter(BOOKING=bok_obj)
       return render(request, "DOCTOR/ADD PRESCRIPTION.html", {'data': med_obj, 'pat_name': pat_name, 'date': date,'data2':pres_obj})
    else:
        docid = request.session['doc_id']
        bok_obj = Booking.objects.filter(EMPLOYEE=docid, date=datetime.datetime.now().date())
        return render(request, "DOCTOR/View booking doctor.html", {'data': bok_obj})


def doc_view_leave_satatus(request):
    return render(request,"DOCTOR/Leave Status doctor.html")
def doc_add_leave(request):
    return render(request,"DOCTOR/LEAVE APPLICATION DOCTOR.html")
def doc_next_slot(request):
    return render(request,"DOCTOR/Next slot.html")
def doc_add_next_visit(request,bookid):
    bok_obj = Booking.objects.get(id=bookid)
    pat_name = bok_obj.PATIENT.patient_name

    return render(request,"DOCTOR/NEXT VISIT ENTRY.html",{'data':bok_obj,'pat_name':pat_name})

def doc_add_next_visit_post(request):
 if request.method == 'POST':
    # date = request.POST['date']
    # book_id = request.session['bookid']
    # res = Reminder(date=date, BOOKING_id=book_id)
    # res.save()
    next_date = request.POST['date']
    book_id = request.session['bookid']
    next_obj = Reminder()
    next_obj.next_date = next_date

    next_obj.BOOKING_id = book_id
    next_obj.save()
    # text = "<script>alert('Next visit Added');window.location='/myapp/doc_add_next_visit/';</script>"
    # return HttpResponse(text)
 return render(request,"DOCTOR/NEXT VISIT ENTRY.html")

 # return render(request,"DOCTOR/NEXT VISIT ENTRY.html")

def doc_view_medicine(request):
    book_id=request.session['bookid']
    pre_obj = Prescription.objects.filter(BOOKING_id=book_id)
    return render(request,"DOCTOR/View previous prescription.html",{'data':pre_obj})
def doc_view_patients(request):
    docid = request.session['doc_id']
    ar=[]
    res=[]
    book_obj = Booking.objects.filter(EMPLOYEE_id=docid)
    if request.method=="POST":
        pat=request.POST['pat']
        book_obj = Booking.objects.filter(EMPLOYEE_id=docid,PATIENT__patient_name__contains=pat)
    print(len(book_obj))
    for i in book_obj:
        if i.PATIENT.id not in ar:
            s={'id':i.PATIENT.id, 'name':i.PATIENT.patient_name,'age':i.PATIENT.age,'gender':i.PATIENT.gender,'place':i.PATIENT.place,'housename':i.PATIENT.housename,'district':i.PATIENT.district,'state':i.PATIENT.state,'phone_number':i.PATIENT.phone_number,'email':i.PATIENT.emial_Id}
            res.append(s)
            ar.append(i.PATIENT.id)
    print(res)
    return render(request,"DOCTOR/View patients doctor.html",{'data':res})

def doc_view_prescription(request,bookid):
    bok_obj=Booking.objects.get(id=bookid)
    pat_name=bok_obj.PATIENT.patient_name
    date=bok_obj.date

    request.session['bookid']=bookid
    pres_obj=Prescription.objects.filter(BOOKING=bok_obj)
    return render(request,"DOCTOR/View previous prescription.html",{'pat_name':pat_name,'date':date,'data2':pres_obj})







                          #ANDROID.......



def view_service_patient(request):
    res2 = []
    ma = Services.objects.all()
    for ii in ma:
        ss = {'id': ii.pk, 'service': ii.services}
        res2.append(ss)

    data = {"status": "ok", "res2": res2}
    return JsonResponse(data)

def view_tips_patient(request):
    res2 = []
    ma = Tips.objects.all()
    for ii in ma:
        ss = {'id': ii.pk, 'tips': ii.tips}
        res2.append(ss)

    data = {"status": "ok", "data": res2}
    return JsonResponse(data)

def view_tips_more(request):

    if request.method == 'POST':
        tipid = request.POST['tipid']
        ma = Tips.objects.get(id=tipid)

        data = {"status": "ok", "tips": ma.tips}
        return JsonResponse(data)


def view_about_patient(request):
    res2 = []
    ma = About.objects.all()
    for ii in ma:
        ss = {'id': ii.pk, 'about': ii.about,'photo':ii.photo}
        res2.append(ss)

    data = {"status": "ok", "data": res2}
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
    print(data)
    return JsonResponse(data)

# def patients_registration(request):
#     if request.method == 'POST':
#         pa_name = request.POST['name']
#
#         # pa_age = request.POST['age']
#
#         pa_gender = request.POST['gender']
#         pa_place = request.POST['place']
#         pa_housename = request.POST['house_name']
#         pa_district = request.POST['district']
#         # pa_pincode = request.POST['pincode']
#         pa_phno = request.POST['phone']
#
#         pa_state = request.POST['state']
#
#         pa_email = request.POST['email']
#
#
#         password=request.POST['password']
#
#         log_obj = Login()
#         log_obj.username = pa_email
#         log_obj.password = password
#         log_obj.type = 'user'
#         log_obj.save()
#
#
#         pa_obj = Patient()
#         pa_obj.patient_name= pa_name
#
#         pa_obj.gender= pa_gender
#         pa_obj.housename= pa_housename
#         pa_obj.district= pa_district
#         pa_obj.state= pa_state
#         pa_obj.emial_Id= pa_email
#         pa_obj.phone_number= pa_phno
#
#         pa_obj.LOGIN_id = log_obj.id
#         pa_obj.save()
#
#         data = {"status": "ok"}
#         return JsonResponse(data)
def user_login(request):
    print("ooooo")
    username=request.POST['username']
    password=request.POST['password']

    login_obj = Login.objects.filter(uname=username, password=password, logintype="user")
    if login_obj.exists():
        lg=login_obj[0]
        return JsonResponse({'status': 'ok','lid':lg.id})
    else:
        return JsonResponse({'status': 'Invalid username or password'})
def pa_registration(request):
    print("hhhh")
    name=request.POST['name']
    housename=request.POST['hname']
    place=request.POST['place']
    pincode=request.POST['pincode']
    age=request.POST['age']
    phone=request.POST['phone']
    email=request.POST['email']
    password=request.POST['password']

    gender=request.POST['gender']
    district=request.POST['district']
    state=request.POST['state']
    print("yyy")


    # import time
    # import base64
    #
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    # a = base64.b64decode(image)
    # fh = open("C:\\Users\\DELL\\PycharmProjects\\myproject\\media\\" + timestr + ".jpg", "wb")
    # path = "/media/" + timestr + ".jpg"
    # fh.write(a)
    # fh.close()

    login_obj=Login()
    login_obj.uname=email
    login_obj.password=password
    login_obj.logintype='user'
    login_obj.save()
    print("pppp")


    user_obj=Patient()
    user_obj.patient_name=name
    user_obj.housename=housename
    user_obj.place=place
    user_obj.pincode=pincode
    user_obj.age=age
    user_obj.phone_number=phone
    user_obj.emial_Id=email

    user_obj.gender=gender
    user_obj.district=district
    user_obj.state=state
    user_obj.LOGIN_id=login_obj.id

    user_obj.save()
    return JsonResponse({'status':'ok'})
def view_doctors(request):
    doc_obj=Employee.objects.filter(emp_type='Doctor')
    res2=[]
    for ii in doc_obj:
        ss = {'id': ii.pk, 'doc_name': ii.emp_name, 'photo': ii.photo, }
        res2.append(ss)
    data = {"status": "ok", "data": res2}
    return JsonResponse(data)
def view_our_doctors(request):
    doc_obj=Employee.objects.filter(emp_type='Doctor')
    res2=[]
    for ii in doc_obj:
        ss = {'id': ii.pk, 'doc_name': ii.emp_name, 'photo': ii.photo,'qua':ii.qualification }
        res2.append(ss)
    data = {"status": "ok", "data": res2}
    return JsonResponse(data)
def view_schedule(request):
    did=request.POST['did']
    day=request.POST['day']
    doc_obj = Employee.objects.get(id=did)
    print("hhh")
    res2 = []
    ma = Schedule.objects.filter(EMPPLOYEE=doc_obj,day=day)

    print("qqq")
    for ii in ma:
        print("wwww")

        ss = {'id': ii.pk, 'day': ii.day,'from_time':ii.from_time,'to_time':ii.to_time}
        res2.append(ss)

    data = {"status": "ok", "data": res2}
    return JsonResponse(data)

def view_timeslots(request):
    start_time=request.POST['stime']
    end_time=request.POST['etime']
    print(start_time)
    print(end_time)
    date=request.POST['date']
    sch_id=request.POST['sch_id']

    # chk
    import datetime as dt

    start_dt = dt.datetime.strptime(str(start_time), '%H:%M:%S')
    end_dt = dt.datetime.strptime(str(end_time), '%H:%M:%S')
    diff = (end_dt - start_dt)
    aa = diff.seconds / 60
    print("time=", diff)
    print("time2=", aa)
    # ovr
    dd = aa / 15
    print("dd=", dd)
    msk = int(dd)

    lst22 = []
    lst22.append(start_time)
    for jj in range(0, msk-1):
        print(jj)

        t1 = dt.datetime.strptime(str(start_time), '%H:%M:%S')
        t2 = dt.datetime.strptime('00:15:00', '%H:%M:%S')
        time_zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
        print((t1 - time_zero + t2).time())
        qq = (t1 - time_zero + t2).time()
        ms22 = str(qq)
        start_time = ms22
        lst22.append(start_time)

        # sch_obj = Schedule.objects.filter(id=sch_id)
        # if sch_obj.exists():
        #     sch_obj = Schedule.objects.get(id=sch_id)
        #     slot_obj=Slot.objects.filter(SCHEDULE_id=sch_obj.id,slot_time=start_time)
        #     if slot_obj.exists():
        #         print("hi")
        #     else:
        #         res =Slot(slot_time=start_time, slot_status='pending', SCHEDULE_id=sch_id )
        #         res.save()

    avl_slots=[]
    for slot in lst22:
        print("sss=",slot)
        print("ddd=",date)

        book_obj=Booking.objects.filter(slot=slot,date=date)
        if book_obj.exists():
            print("entr")
            pass
        else:
            s={'slot':slot}


            avl_slots.append(s)


    print("final")
    print(lst22)
    # ovr
    data = {"status": "ok", "data": avl_slots}
    return JsonResponse(data)

def booking(request):

    emp_id = request.POST['doc_id']
    dt=request.POST['dt']
    emp_obj = Employee.objects.get(id=emp_id)
    pa_id = request.POST['pa_id']
    print("hi5")
    pa_obj=Patient.objects.get(LOGIN_id=pa_id)


    slot_id = request.POST['slot_id']
    print("mm=",slot_id)
    # slot_obj =Slot.objects.get(slot_time=slot_id)
    # print("hhhhh")
    # print(slot_obj)
    res=Booking(PATIENT=pa_obj,EMPLOYEE=emp_obj,slot=slot_id,date=dt)
    res.save()
    data = {"status": "ok"}
    return JsonResponse(data)
#
# ef chatload(request):
#     return render(request,'featuremember/fur_chat.html')

def drviewmsg(request,receiverid):

    doclidlid=request.session["lid"]
    print("!!!!!!!!!!",doclidlid,receiverid)
    doc=featuremember.objects.get(LOGIN=doclidlid)
    obj=chat.objects.filter(FID=doc,NID=normalmember.objects.get(id=receiverid))
    user_data=normalmember.objects.get(id=receiverid)
    print("********************",obj)

    res = []
    for i in obj:
        s = {'id':i.pk, 'date':i.date,'msg':i.message,'type':i.type}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res,'name':user_data.name,'image':user_data.image})

def chatview(request):
    print("hai")
    da = Patient.objects.all()
    res = []
    for i in da:
        s = {'id': i.pk, 'name': i.name, 'email': i.email}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res})
def in_message2(request,receiverid,msg):

    dlid= request.session["lid"]
    dobj=Patient.objects.get(LOGIN=dlid)
    import datetime
    datetime.date.today()  # Returns 2018-01-15
    showtime=datetime.datetime.now()

    obj=Chat()
    obj.NID=normalmember.objects.get(pk=receiverid)
    obj.FID=dobj
    obj.message=msg
    obj.type='fuser'
    obj.date=showtime
    obj.save()
    return JsonResponse({'status':'ok'})




def inmessage(request):
    fid=request.POST['fid']
    log_obj = Login.objects.get(id=fid)
    pat_obj = Patient.objects.get(LOGIN=log_obj)
    toid=request.POST['toid']
    msg=request.POST['msg']
    rtype=request.POST['type']
    ch=Chat()
    ch.date=datetime.datetime.now().date()
    ch.PATIENT_id=pat_obj.id
    ch.DOCTOR_id=toid
    ch.message=msg
    ch.type=rtype
    ch.save()
    return JsonResponse({'status':'ok'})

def view_message2(request):
    fid=request.POST['fid']
    log_obj=Login.objects.get(id=fid)
    pat_obj=Patient.objects.get(LOGIN=log_obj)
    toid=request.POST['toid']
    lmid=request.POST['lastmsgid']


    cha = Chat.objects.filter(PATIENT_id=pat_obj.id, DOCTOR_id=toid, pk__gte=lmid)

    if cha.exists():
        a = []
        for i in cha:
            if i.pk > int(lmid):
                a.append({'id': i.pk, 'msg': i.message, 'date': i.date, 'type': i.type})
        return JsonResponse({'status': 'ok', 'data': a})
    else:
        return JsonResponse({'status': 'no'})


