import datetime
import random

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
# from Mod import *
# Create your views here.
from daya_clinic.models import Services, Tips, Employee, Login, Schedule, Feedback, About, Attandance, Contact_details, \
    Patient, book_fee, Slot, Booking, Chat, Medicine, Prescription, Reminder, Leave, Batch, Stock, Sales_master, \
    Sales_sub, Late_message, Symptoms


def homepage(request):
    return render(request,"ADMIN/homepage.html")
def homepage_doc(request):
    return render(request,"DOCTOR/homepage_doc.html")
def homepage_ph(request):
    return render(request,"PHARMACIST/homepage_pharmacist.html")
def login(request):

    if request.method=="POST":
        username=request.POST['name']
        password=request.POST['surname']

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
            elif log.logintype=="Pharmacist":
                request.session['lid']=log.id

                ph_obj=Employee.objects.get(LOGIN_id=Login.objects.get(id=log.id))
                request.session['ph_id']=ph_obj.id
                return homepage_ph(request)
            else:

                return  HttpResponse("no")
        else:
            text = "<script>alert('Invalid username or password');window.location='/myapp/login/';</script>"
            return HttpResponse(text)
            # return HttpResponse("Invalid username or password")
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

        sch_obj=Schedule.objects.filter(EMPPLOYEE=did,from_time=from_time,to_time=to_time,day=day)
        if sch_obj.exists():

            text = "<script>alert('Schedule Already Added');window.location='/myapp/adm_add_schedule/';</script>"
            return HttpResponse(text)
            return (request)
            return render(request, "ADMIN/Add schedule.html")

        else:
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
        sch_obj = Schedule.objects.filter(EMPPLOYEE=did,from_time=from_time, to_time=to_time, day=day)
        if sch_obj.exists():

            text = "<script>alert('Schedule Already Added');window.location='/myapp/adm_add_schedule/';</script>"
            return HttpResponse(text)
            return (request)
            return render(request, "ADMIN/Add schedule.html")

        else:
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
        print("abcd")
        # # return HttpResponse("ok")
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
        print("ssssss")
        emp_image= request.FILES['fileField']
        print("ppppppp")
        # return HttpResponse("ok")

        password=random.randint(10,99)


          # SAVE IMAGE
        fs=FileSystemStorage()
        filename=fs.save(emp_image.name,emp_image)

        login_obj=Login()
        login_obj.uname=emp_email
        login_obj.password=password
        login_obj.logintype=emp_type
        login_obj.save()
        print("login")
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
        print("final")

        text = "<script>alert('Employee Registered');window.location='/myapp/adm_employee_registration/';</script>"
        return HttpResponse(text)

    return render(request,"ADMIN/EMPLOYEE REGISTRATION.html")
def adm_offline_patients(request):
    if request.method == 'POST':
        pa_name = request.POST['txt_name']

        age = request.POST['age']

        gender = request.POST['radio_gender']
        place = request.POST['txt_place']
        housename = request.POST['txt_hname']
        district = request.POST['txt_district']
        pincode = request.POST['txt_pincode']
        phno = request.POST['txt_phno']
        employee = request.POST['select']

        state = request.POST['txt_state']

        email = request.POST['txt_email']
        time = request.POST['time']
        password = "ANNN"
        login_obj = Login()
        login_obj.uname = email
        login_obj.password = password
        login_obj.logintype ="offline_patients"

        login_obj.save()
        print(login_obj)





        #   SAVE IMAGE



        employee_obj = Patient()
        employee_obj.patient_name= pa_name

        employee_obj.age= age
        employee_obj.gender=gender
        employee_obj.place=place
        employee_obj.housename=housename
        employee_obj.district= district
        employee_obj.pincode= pincode
        employee_obj.state=state

        employee_obj.emial_Id=email
        employee_obj.phone_number= phno
        employee_obj.LOGIN= login_obj



        employee_obj.save()
        e_obj=Employee.objects.get(id=employee)

        book_obj = Booking()
        book_obj.PATIENT =employee_obj
        book_obj.EMPLOYEE = e_obj
        book_obj.slot =time
        book_obj.date = datetime.date.today()
        book_obj.save()
        print(book_obj)





        text = "<script>alert('Patient  Registered');window.location='/myapp/adm_view_booking_info/';</script>"
        return HttpResponse(text)
    emp_obj = Employee.objects.filter(emp_type="Doctor")

    return render(request,"ADMIN/ADD OFFLINE PATIENTS.html",{'data':emp_obj})


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
        emp_fee = request.POST['fee']
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
        employee_obj.fee = emp_fee
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
def adm_leave_approval(request,id):
    print("fffff")


    leave_obj = Leave.objects.get(id=id)
    print(leave_obj)
    leave_obj.leave_status = 'Accepted'
    leave_obj.save()
    print("lllll")

    return render(request,"ADMIN/homepage.html")
def adm_accept_leave(request,id):
    if request.method == 'POST':
        print(id)
        res=Leave.objects.get(EMPLOYEE=id)
        print(res)
        res.leave_status='Accepted'
        res.save()
        text = """"<script>alert('Request accepted');window.location='/myapp/adm_leave_approval/';</script>"""
        return HttpResponse(text)
        return redirect("/myapp/adm_leave_approval/")

def adm_leave_approval_post(request):



    leave_obj = Leave.objects.filter(leave_status='pending')
    print(leave_obj)
    return render(request,"ADMIN/Leave Approval.html",{'data':leave_obj})
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
    if request.method=='POST':
        print("hi")
        date1=request.POST['date1']
        date2=request.POST['date2']
        print(date1)
        print(date2)
        # at_obj=Attandance.objects.filter(date__lte=date1,date__gte=date2)
        # at_obj=Attandance.objects.filter(date__range=[date1,date1])
        at_obj=Attandance.objects.filter(date__range=[date1, date2])
        print(at_obj)
        return render(request, "ADMIN/view attandance1.html", {'data': at_obj})
    else:
        print("hello")
        at_obj = Attandance.objects.filter(date=datetime.datetime.now().date())
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



    if request.method == 'POST':
        salem_obj = Sales_master.objects.all()
        sales_sub_obj = Sales_sub.objects.all()

        print("hi")
        date1 = request.POST['date1']
        date2 = request.POST['date2']
        print(date1)
        print(date2)
        # at_obj=Attandance.objects.filter(date__lte=date1,date__gte=date2)
        # at_obj=Attandance.objects.filter(date__range=[date1,date1])
        at_obj =Sales_master.objects.filter(date__range=[date1, date2])
        s=0
        for i in at_obj:
            print(i.total_amount)
            s=s+int(i.total_amount)



        print(at_obj)
        return render(request, "ADMIN/Sales Repor.html", {'data': at_obj,'tot':str(s)})


    else:
        import datetime
        salem_obj = Sales_master.objects.filter(date=datetime.date.today())
        sales_sub_obj = Sales_sub.objects.all()
        s = 0
        for i in salem_obj:
            print(i.total_amount)
            s = s + int(i.total_amount)

        return render(request,"ADMIN/Sales Repor.html",{'data':salem_obj,'data2':sales_sub_obj,'tot':str(s)})

def adm_view_medicine_sale(request,id):
    salem_obj=Sales_master.objects.get(id=id)

    sales_sub_obj = Sales_sub.objects.filter(SALE_MASTER=salem_obj)

    res=[]

    for i in sales_sub_obj:
        print("hhhh")
        bid=i.BATCH_id



        print("biddd")
        print(bid)
        bat_obj=Batch.objects.get(id=bid)

        ss=bat_obj.MEDICINE.name
        res.append(ss)













    return render(request,"ADMIN/View sales report 2.html",{'data':sales_sub_obj})
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

    docid = request.session['doc_id']
    bok_obj = Booking.objects.filter(date=datetime.datetime.now().date())
    if request.method == "POST":
        pat = request.POST['pat']
        bok_obj = Booking.objects.filter(PATIENT__patient_name__contains=pat)

    return render(request,"ADMIN/View booking info.html",{'data':bok_obj})
def adm_view_patients(request):
    if request.method=='POST':
        print("hi")
        date1=request.POST['date1']
        date2=request.POST['date2']
        print(date1)
        print(date2)
        # at_obj=Attandance.objects.filter(date__lte=date1,date__gte=date2)
        # at_obj=Attandance.objects.filter(date__range=[date1,date1])
        at_obj=Booking.objects.filter(date__range=[date1, date2])
        print(at_obj)
        ar = []
        res = []
        for i in at_obj:
            if i.PATIENT.id not in ar:
                s = {'id': i.PATIENT.id, 'name': i.PATIENT.patient_name, 'age': i.PATIENT.age,
                     'gender': i.PATIENT.gender, 'place': i.PATIENT.place, 'housename': i.PATIENT.housename,
                     'district': i.PATIENT.district, 'state': i.PATIENT.state, 'phone_number': i.PATIENT.phone_number,
                     'email': i.PATIENT.emial_Id, 'date': i.date, 'slot': i.slot}
                res.append(s)
                ar.append(i.PATIENT.id)

        print(res)
        return render(request, "ADMIN/View patients.html", {'data': res})
        # return render(request, "ADMIN/View patients.html", {'data': at_obj})
    else:
        ar=[]
        res=[]
        import datetime
        today = datetime.date.today()
        book_obj = Booking.objects.filter(date__year=today.year,
                               date__month=today.month)
        if request.method=="POST":
            pat=request.POST['pat']
            book_obj = Booking.objects.filter(PATIENT__patient_name__contains=pat)
        print(len(book_obj))
        for i in book_obj:
            if i.PATIENT.id not in ar:

                s={'id':i.PATIENT.id, 'name':i.PATIENT.patient_name,'age':i.PATIENT.age,'gender':i.PATIENT.gender,'place':i.PATIENT.place,'housename':i.PATIENT.housename,'district':i.PATIENT.district,'state':i.PATIENT.state,'phone_number':i.PATIENT.phone_number,'email':i.PATIENT.emial_Id,'date':i.date,'slot':i.slot}
                res.append(s)
                ar.append(i.PATIENT.id)

        print(res)
        return render(request,"ADMIN/View patients.html",{'data':res})

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
def doc_view_messages(request):
    docid=request.session['doc_id']
    chat_obj = Chat.objects.filter(DOCTOR=docid)
    return render(request,"DOCTOR/view messages.html",{'data':chat_obj})




def doc_view_schedule(request):
    docid=request.session['doc_id']
    schedule_obj = Schedule.objects.filter(EMPPLOYEE_id=docid)
    return render(request,"DOCTOR/View schedule.html",{'data':schedule_obj})
def doc_view_leave_status(request):
    docid=request.session['doc_id']
    leave_obj = Leave.objects.filter(EMPLOYEE=docid)
    return render(request,"DOCTOR/Leave Status doctor.html",{'data':leave_obj})
def ph_view_leave_status(request):
    docid=request.session['ph_id']
    leave_obj = Leave.objects.filter(EMPLOYEE=docid)
    return render(request,"PHARMACIST/Leave Status status.html",{'data':leave_obj})
def doc_view_booking(request):
    docid=request.session['doc_id']
    bok_obj = Booking.objects.filter(EMPLOYEE=docid,date=datetime.datetime.now().date())
    if request.method=="POST":
        pat=request.POST['pat']
        bok_obj = Booking.objects.filter(EMPLOYEE_id=docid,PATIENT__patient_name__contains=pat)
    return render(request,"DOCTOR/View booking doctor.html",{'data':bok_obj})
def ph_view_booking(request):
    docid=request.session['doc_id']
    bok_obj=Prescription.objects.filter(BOOKING__date=datetime.datetime.now().date())
    # bok_obj = Booking.objects.filter(date=datetime.datetime.now().date(),)
    if request.method=="POST":
        pat=request.POST['pat']
        bok_obj = Booking.objects.filter(PATIENT__patient_name__contains=pat)
    return render(request,"PHARMACIST/View booking pharmacist.html",{'data':bok_obj})
def ph_view_prescription(request,bookid):

    request.session["uid"]=bookid



    print("hi")
    uid=bookid
    use_obj=Patient.objects.get(id=uid)
    print(use_obj)
    # bok_obj=Booking.objects.get(id=bookid)
    import datetime

    showtime = datetime.date.today()
    print(showtime)
    print("asss")
    bok_obj=Booking.objects.filter(PATIENT=uid,date=showtime)
    print(bok_obj)
    res=[]
    for i in bok_obj:
        print("zz")
        print(i.id)
        print(i.date)
        pre_obj=Prescription.objects.filter(BOOKING_id=i.id)
        print(pre_obj)

        for j in pre_obj:
            print(j.prescription)

            ss={'id':id,'pre_name':j.prescription,'mname':j.MEDICINE.name,'qty':j.qty,'unit':j.unit,'date':i.date}
            print(ss)
            res.append(ss)
            print(pre_obj)

        print("fini")





    print("hi")
    print(res)
    res2=[]
    for i in bok_obj:
        print("zz")
        print(i.id)
        print(i.date)
        pre_obj = Prescription.objects.filter(BOOKING_id=i.id)
        print(pre_obj)
        for j in pre_obj:
            print(j.prescription)
            ss = {'id': i.id, 'mname': j.MEDICINE.name,
                  }
            print(ss)
            res2.append(ss)
            print(pre_obj)

        print("fini")

    print("hi")
    print(res)
    return render(request, "PHARMACIST/View prescription pharmacist.html", {'pat_name': use_obj.patient_name, 'data2': res,'data3':res2})

# def ph_view_prescription(request):
#     print("hll")
#     bookid=request.session["uid"]
#     print(bookid)
#
#     if request.method=='POST':
#         print("hi")
#
#         d1 = request.POST["dd1"]
#         print(d1)
#         d2 = request.POST['dd2']
#
#         print(d2)
#         # return HttpResponse("ok")
#         #
#         # # at_obj=Attandance.objects.filter(date__lte=date1,date__gte=date2)
#         # # at_obj=Attandance.objects.filter(date__range=[date1,date1])
#         # # at_obj=Attandance.objects.filter(date__range=[date1, date2])
#         #
#         #
#         #
#         print("hi")
#         uid = bookid
#         use_obj = Patient.objects.get(id=uid)
#         print(use_obj)
#         # bok_obj=Booking.objects.get(id=bookid)
#         bok_obj = Booking.objects.filter(PATIENT=uid,date__range=[d1, d2])
#         print(bok_obj)
#         res = []
#         for i in bok_obj:
#             print("zz")
#             print(i.id)
#             pre_obj = Prescription.objects.filter(BOOKING_id=i.id)
#             print(pre_obj)
#             for j in pre_obj:
#                 print(j.prescription)
#                 ss = {'id': i.id, 'pre_name': j.prescription, 'mname': j.MEDICINE.name, 'qty': j.qty, 'unit': j.unit,
#                       'date': i.date}
#                 print(ss)
#                 res.append(ss)
#                 print(pre_obj)
#
#             print("fini")
#
#         print("hi")
#         print(res)

#         return render(request, "PHARMACIST/View prescription pharmacist.html",{'pat_name': use_obj.patient_name, 'data2': res})

def add_sale(request):
    a=request.POST['btn']
    if request.method == 'POST':
        if a=='Add':

            print("ss")
            sale_id = request.session["mid"]
            print(sale_id)


            bat_name = request.POST['select']
            print(bat_name)


            batch_obj = Batch.objects.get(pk=bat_name)

            print(batch_obj)
            st_obj=Stock.objects.get(BATCH=batch_obj)
            st_count=int(st_obj.quantity)
            print(st_count)

            # batch_obj=Batch.objects.get(MEDICINE=med_obj)


            qty = request.POST['qty']
            ac_count=int(qty)
            print(ac_count)
            print("hlo")
            if st_count>=ac_count:
                print("qqqq")
                salem_obj=Sales_master.objects.get(pk=sale_id)




                sale_obj = Sales_sub(SALE_MASTER=salem_obj, quantity=qty, BATCH=batch_obj)
                sale_obj.save()
            else:
                book_id=request.session["uid"]
                print("out of stock")
                text = "<script>alert('OUT OF STOCK');</script>"
                print(text)
                return HttpResponse(text)
            #####test#######
            batch22 = Batch.objects.all()
            print(batch22)

            bookid = request.session["uid"]

            print("hi")
            uid = bookid
            use_obj = Patient.objects.get(id=uid)
            print(use_obj)
            # bok_obj=Booking.objects.get(id=bookid)
            import datetime

            showtime = datetime.date.today()
            print(showtime)
            print("asss")
            bok_obj = Booking.objects.filter(PATIENT=uid, date=showtime)
            print(bok_obj)
            res = []
            for i in bok_obj:
                print("zz")
                print(i.id)
                print(i.date)
                pre_obj = Prescription.objects.filter(BOOKING_id=i.id)
                print(pre_obj)
                for j in pre_obj:
                    print(j.prescription)


                    ss = {'id': i.id, 'pre_name': j.prescription, 'mname': j.MEDICINE.name, 'qty': j.qty, 'unit': j.unit,
                          'date': i.date}
                    print(ss)
                    res.append(ss)
                    print(pre_obj)

                print("fini")

            print("hi")
            print(res)
            print(sale_id)
            salenew_obj=Sales_sub.objects.filter(SALE_MASTER=sale_id)
            print(salenew_obj)
            print(batch22)
            t=[]

            m=0


            for i in salenew_obj:
                q=i.quantity
                p=i.BATCH.unit_amount
                c=int(q)*int(p)
                t.append({'medname':i.BATCH.MEDICINE.name,'qnty':i.quantity,'unit':i.BATCH.MEDICINE.unit,'cmpy':i.BATCH.MEDICINE.campany,'tax':i.BATCH.MEDICINE.tax,'untamt':i.BATCH.unit_amount,'tamt':c})
                m=m+c
            doc_id = request.session['doc_id']
            doc_obj = Employee.objects.get(id=doc_id)
            fee_obj = book_fee.objects.get(EMPLOYEE=doc_obj)
            kk = fee_obj.fee
            m=m+int(kk)

            request.session['tamt']=m

            return render(request,"PHARMACIST/saLe entry.html",{'pat_name': use_obj.patient_name,'data2': res,'data3': batch22,'data4':salenew_obj,'tt':t,'tm':m,'fee':kk})
        else:
            print("xxx")
            sale_id = request.session["mid"]
            print(sale_id)
            salemaster_obj=Sales_master.objects.get(id=sale_id)
            print(salemaster_obj)
            sini=Sales_sub.objects.filter(SALE_MASTER=salemaster_obj)
            print(sini)
            doc_id=request.session['doc_id']
            doc_obj=Employee.objects.get(id=doc_id)
            fee_obj=book_fee.objects.get(EMPLOYEE=doc_obj)
            kk=fee_obj.fee
            cc=0
            for i in sini:
                print("mm")
                ###########
                bid=i.BATCH.id

                print("bid=",bid)
                bat11_obj=Batch.objects.get(id=bid)
                print(bat11_obj)
                medicine_name=bat11_obj.MEDICINE.name
                stock_obj=Stock.objects.get(BATCH=bat11_obj)
                print(stock_obj)
                stock_no=stock_obj.quantity
                print(stock_no)
                new_stock=int(stock_no)-int(i.quantity)
                print(new_stock)
                if new_stock >0:
                    print("wwwww")










                    qt_obj = Stock.objects.get(pk=stock_obj.id)
                    print(qt_obj)


                    qt_obj.quantity = int(new_stock)
                    qt_obj.save()
                    print("gggggg")
                    cc = cc + int(i.quantity) * int(i.BATCH.unit_amount)

                    print("mm")

                    print()
                    cc = cc + int(kk)

                    s_obj = Sales_master.objects.get(pk=sale_id)
                    print(s_obj)

                    s_obj.total_amount = str(request.session['tamt'])
                    s_obj.save()
                    print("mm")
                else:


                  print("OUT OF STOCK=",medicine_name)

                  # return HttpResponse("OUT OF STOCK",)

            return render(request, "PHARMACIST/homepage_pharmacist.html",)

                ##############





    return render(request,"PHARMACIST/saLe entry.html")

# def add_sale(request):
#     a=request.POST['btn']
#     if request.method == 'POST':
#         if a=='Add':
#
#             print("ss")
#             sale_id = request.session["mid"]
#             print(sale_id)
#
#
#             bat_name = request.POST['select']
#             print(bat_name)
#
#
#             batch_obj = Batch.objects.get(pk=bat_name)
#
#             print(batch_obj)
#             st_obj=Stock.objects.get(BATCH=batch_obj)
#             st_count=int(st_obj.quantity)
#             print(st_count)
#
#             # batch_obj=Batch.objects.get(MEDICINE=med_obj)
#
#
#             qty = request.POST['qty']
#             ac_count=int(qty)
#             print(ac_count)
#             print("hlo")
#             if st_count>=ac_count:
#                 print("qqqq")
#                 salem_obj=Sales_master.objects.get(pk=sale_id)
#                 sale_obj = Sales_sub(SALE_MASTER=salem_obj, quantity=qty, BATCH=batch_obj)
#                 sale_obj.save()
#             else:
#                 book_id=request.session["uid"]
#                 print("out of stock")
#                 text = "<script>alert('OUT OF STOCK');</script>"
#                 print(text)
#                 return HttpResponse(text)
#             #####test#######
#             batch22 = Batch.objects.all()
#             print(batch22)
#
#             bookid = request.session["uid"]
#
#             print("hi")
#             uid = bookid
#             use_obj = Patient.objects.get(id=uid)
#             print(use_obj)
#             # bok_obj=Booking.objects.get(id=bookid)
#             import datetime
#
#             showtime = datetime.date.today()
#             print(showtime)
#             print("asss")
#             bok_obj = Booking.objects.filter(PATIENT=uid, date=showtime)
#             print(bok_obj)
#             res = []
#             for i in bok_obj:
#                 print("zz")
#                 print(i.id)
#                 print(i.date)
#                 pre_obj = Prescription.objects.filter(BOOKING_id=i.id)
#                 print(pre_obj)
#                 for j in pre_obj:
#                     print(j.prescription)
#
#
#                     ss = {'id': i.id, 'pre_name': j.prescription, 'mname': j.MEDICINE.name, 'qty': j.qty, 'unit': j.unit,
#                           'date': i.date}
#                     print(ss)
#                     res.append(ss)
#                     print(pre_obj)
#
#                 print("fini")
#
#             print("hi")
#             print(res)
#             print(sale_id)
#             salenew_obj=Sales_sub.objects.filter(SALE_MASTER=sale_id)
#             print(salenew_obj)
#             print(batch22)
#
#
#
#
#
#             return render(request, "PHARMACIST/saLe entry.html",
#                           {'pat_name': use_obj.patient_name, 'data2': res, 'data3': batch22,'data4':salenew_obj})
#         else:
#             print("xxx")
#             sale_id = request.session["mid"]
#             print(sale_id)
#             salemaster_obj=Sales_master.objects.get(id=sale_id)
#             print(salemaster_obj)
#             sini=Sales_sub.objects.filter(SALE_MASTER=salemaster_obj)
#             print(sini)
#             doc_id=request.session['doc_id']
#             doc_obj=Employee.objects.get(id=doc_id)
#             fee_obj=book_fee.objects.get(EMPLOYEE=doc_obj)
#             kk=fee_obj.fee
#             cc=0
#             for i in sini:
#                 print("mm")
#                 ###########
#                 bid=i.BATCH.id
#
#                 print("bid=",bid)
#                 bat11_obj=Batch.objects.get(id=bid)
#                 print(bat11_obj)
#                 medicine_name=bat11_obj.MEDICINE.name
#                 stock_obj=Stock.objects.get(BATCH=bat11_obj)
#                 print(stock_obj)
#                 stock_no=stock_obj.quantity
#                 print(stock_no)
#                 new_stock=int(stock_no)-int(i.quantity)
#                 print(new_stock)
#                 if new_stock >0:
#                     print("wwwww")
#
#
#
#
#
#
#
#
#
#
#                     qt_obj = Stock.objects.get(pk=stock_obj.id)
#                     print(qt_obj)
#
#
#                     qt_obj.quantity = int(new_stock)
#                     qt_obj.save()
#                     print("gggggg")
#                     cc = cc + int(i.quantity) * int(i.BATCH.unit_amount)
#
#                     print("mm")
#
#                     print()
#                     cc = cc + int(kk)
#
#                     s_obj = Sales_master.objects.get(pk=sale_id)
#                     print(s_obj)
#
#                     s_obj.total_amount = str(cc)
#                     s_obj.save()
#                     print("mm")
#                 else:
#
#
#                   print("OUT OF STOCK=",medicine_name)
#
#                   # return HttpResponse("OUT OF STOCK",)
#
#             return render(request, "PHARMACIST/homepage_pharmacist.html",)
#
#                 ##############
#
#
#
#
#
#     return render(request,"PHARMACIST/saLe entry.html")
def ph_del_salesub(request,id):
    sale_id = request.session["mid"]
    salesub_obj=Sales_sub.objects.get(id=id)
    salesub_obj.delete()
    medicine22 = Medicine.objects.all()

    bookid = request.session["uid"]

    print("hi")
    uid = bookid
    use_obj = Patient.objects.get(id=uid)
    print(use_obj)
    # bok_obj=Booking.objects.get(id=bookid)
    import datetime

    showtime = datetime.date.today()
    print(showtime)
    print("asss")
    bok_obj = Booking.objects.filter(PATIENT=uid, date=showtime)
    print(bok_obj)
    res = []
    for i in bok_obj:
        print("zz")
        print(i.id)
        print(i.date)
        pre_obj = Prescription.objects.filter(BOOKING_id=i.id)
        print(pre_obj)
        for j in pre_obj:
            print(j.prescription)
            ss = {'id': i.id, 'pre_name': j.prescription, 'mname': j.MEDICINE.name, 'qty': j.qty, 'unit': j.unit,
                  'date': i.date}
            print(ss)
            res.append(ss)
            print(pre_obj)

        print("fini")

    print("hi")
    print(res)
    print(sale_id)
    salenew_obj = Sales_sub.objects.filter(SALE_MASTER=sale_id)
    print(salenew_obj)

    return render(request, "PHARMACIST/saLe entry.html",
                  {'pat_name': use_obj.patient_name, 'data2': res, 'data3': medicine22, 'data4': salenew_obj})

    return add_sale(request)

def homepage_doctor(request):
    return render(request,"DOCTOR/homepage_doc.html")

def doc_add_prescription(request,bookid):
    bok_obj=Booking.objects.get(id=bookid)
    pat_name=bok_obj.PATIENT.patient_name
    pat_n=bok_obj.PATIENT.phone_number
    date=bok_obj.date
    med_obj=Medicine.objects.all()
    request.session['bookid']=bookid
    pres_obj=Prescription.objects.filter(BOOKING=bok_obj)
    return render(request,"DOCTOR/ADD PRESCRIPTION.html",{'data':med_obj,'pat_name':pat_name,'date':date,'data2':pres_obj,'pat_n':pat_n})
def doc_add_symptoms(request,bookid):
    bok_obj=Booking.objects.get(id=bookid)
    pat_name=bok_obj.PATIENT.patient_name
    pat_n=bok_obj.PATIENT.phone_number
    date=bok_obj.date
    med_obj=Medicine.objects.all()
    request.session['bookid']=bookid
    pres_obj=Prescription.objects.filter(BOOKING=bok_obj)
    return render(request,"DOCTOR/ADD SYPMPTOMS.html",{'data':med_obj,'pat_name':pat_name,'date':date,'data2':pres_obj,'pat_n':pat_n})

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
def doc_add_symptoms_post(request):
    if request.method == 'POST':
       book_id = request.session['bookid']


       symptoms= request.POST['symptoms']

       res=Symptoms(symptoms=symptoms,BOOKING_id=book_id)
       res.save()
       # bok_obj = Booking.objects.get(id=book_id)
       # pat_name = bok_obj.PATIENT.patient_name
       # date = bok_obj.date
       # pres_obj=Prescription.objects.filter(BOOKING=bok_obj)
       return redirect("/myapp/doc_view_booking/")

       # else:
    #     docid = request.session['doc_id']
    #     bok_obj = Booking.objects.filter(EMPLOYEE=docid, date=datetime.datetime.now().date())
    #     return render(request, "DOCTOR/View booking doctor.html", {'data': bok_obj})

def doc_view_leave_satatus(request):
    return render(request,"DOCTOR/Leave Status doctor.html")
def doc_add_leave(request):
    if request.method == 'POST':
        docid = request.session['doc_id']
        emp_obj = Employee.objects.get(pk=docid)
        print(emp_obj)
        from_date = request.POST['date']
        reason = request.POST['reason']
        to_date = request.POST['todate']
        type = request.POST['type']
        leav_obj = Leave(EMPLOYEE=emp_obj,date=from_date,reason=reason,to_date=to_date,type=type,leave_status='pending')
        leav_obj.save()
        print(leav_obj)
        #sct
        text = "<script>alert('Leave Applied');window.location='/myapp/homepage_doc/';</script>"
        return HttpResponse(text)


    return render(request, "DOCTOR/LEAVE APPLICATION DOCTOR.html")
def ph_add_leave(request):
    if request.method == 'POST':
        docid = request.session['ph_id']
        emp_obj = Employee.objects.get(pk=docid)
        print(emp_obj)
        from_date = request.POST['date']
        reason = request.POST['reason']
        to_date = request.POST['todate']
        type = request.POST['type']
        leav_obj = Leave(EMPLOYEE=emp_obj,date=from_date,reason=reason,to_date=to_date,type=type,leave_status='pending')
        leav_obj.save()
        print(leav_obj)
        #sct
        text = "<script>alert('Leave Applied');window.location='/myapp/homepage_ph/';</script>"
        return HttpResponse(text)


    return render(request, "PHARMACIST/LEAVE APPLICATION PH.html")
def doc_add_late(request):
    if request.method == 'POST':
        docid = request.session['doc_id']
        emp_obj = Employee.objects.get(pk=docid)
        print(emp_obj)
        date = request.POST['date']
        reason = request.POST['reason']
        time = request.POST['time']

        late_obj = Late_message(EMPPLOYEE=emp_obj,date=date,reason=reason,arriving_time=time)
        late_obj.save()
        print(late_obj)
        #sct
        text = "<script>alert('Late Arrival Added');window.location='/myapp/homepage_doc/';</script>"
        return HttpResponse(text)


    return render(request, "DOCTOR/late_arrival.html")


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
    text = "<script>alert('Next visit Added');window.location='/myapp/doc_view_booking/';</script>"
    return HttpResponse(text)
 return render(request,"DOCTOR/NEXT VISIT ENTRY.html")

 # return render(request,"DOCTOR/NEXT VISIT ENTRY.html")

def doc_view_medicine(request):
    book_id=request.session['bookid']
    bok_obj = Booking.objects.get(id=book_id)
    pre_obj = Prescription.objects.filter(BOOKING_id=book_id)
    pat_name = bok_obj.PATIENT.patient_name
    request.session["pid"]=bok_obj.PATIENT.id
    date = bok_obj.date
    return render(request,"DOCTOR/View previous prescription.html",{'data':pre_obj,'pat_name':pat_name,'date':date})
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

            s={'id':i.PATIENT.id, 'name':i.PATIENT.patient_name,'age':i.PATIENT.age,'gender':i.PATIENT.gender,'place':i.PATIENT.place,'housename':i.PATIENT.housename,'district':i.PATIENT.district,'state':i.PATIENT.state,'phone_number':i.PATIENT.phone_number,'email':i.PATIENT.emial_Id,'date':i.date}
            res.append(s)
            ar.append(i.PATIENT.id)

    print(res)
    return render(request,"DOCTOR/View patients doctor.html",{'data':res})

def doc_view_prescription(request,bookid):

    request.session["uid"]=bookid



    print("hi")
    uid=bookid
    use_obj=Patient.objects.get(id=uid)
    print(use_obj)
    # bok_obj=Booking.objects.get(id=bookid)
    bok_obj=Booking.objects.filter(PATIENT=uid)
    res=[]
    for i in bok_obj:
        print("zz")
        print(i.id)
        pre_obj=Prescription.objects.filter(BOOKING_id=i.id)
        print(pre_obj)
        for j in pre_obj:
            print(j.prescription)
            ss={'id':i.id,'pre_name':j.prescription,'mname':j.MEDICINE.name,'qty':j.qty,'unit':j.unit,'date':i.date}
            print(ss)
            res.append(ss)
            print(pre_obj)

        print("fini")




    print("hi")
    print(res)
    return render(request, "DOCTOR/View previous prescription.html", {'pat_name': use_obj.patient_name, 'data2': res})
def doc_view_symptoms(request,bookid):

    request.session["uid"]=bookid



    print("hi")
    uid=bookid
    use_obj=Patient.objects.get(id=uid)
    print(use_obj)
    # bok_obj=Booking.objects.get(id=bookid)
    bok_obj=Booking.objects.filter(PATIENT=uid)
    res=[]
    for i in bok_obj:
        print("zz")
        print(i.id)
        sym_obj=Symptoms.objects.filter(BOOKING_id=i.id)
        print(sym_obj)
        for j in sym_obj:
            print(j.symptoms)
            ss={'id':i.id,'symptoms':j.symptoms,'date':i.date}
            print(ss)
            res.append(ss)
            print(sym_obj)

        print("fini")




    print("hi")
    print(res)
    return render(request, "DOCTOR/View previous symptoms.html", {'pat_name': use_obj.patient_name, 'data2': res})
def doc_view_symptoms_post(request):
    print("hll")
    bookid=request.session["uid"]
    print(bookid)

    if request.method=='POST':
        print("hi")

        d1 = request.POST["dd1"]
        print(d1)
        d2 = request.POST['dd2']

        print(d2)
        # return HttpResponse("ok")
        #
        # # at_obj=Attandance.objects.filter(date__lte=date1,date__gte=date2)
        # # at_obj=Attandance.objects.filter(date__range=[date1,date1])
        # # at_obj=Attandance.objects.filter(date__range=[date1, date2])
        #
        #
        #
        print("hi")
        uid = bookid
        use_obj = Patient.objects.get(id=uid)
        print(use_obj)
        # bok_obj=Booking.objects.get(id=bookid)
        bok_obj = Booking.objects.filter(PATIENT=uid,date__range=[d1, d2])
        print(bok_obj)
        res = []
        for i in bok_obj:
            print("zz")
            print(i.id)
            sym_obj = Symptoms.objects.filter(BOOKING_id=i.id)
            print(sym_obj)
            for j in sym_obj:
                print(j.symptoms)
                ss = {'id': i.id, 'symptoms': j.symptoms,
                      'date': i.date}
                print(ss)
                res.append(ss)
                print(sym_obj)

            print("fini")

        print("hi")
        print(res)
        return render(request, "DOCTOR/View previous prescription.html",{'pat_name': use_obj.patient_name, 'data2': res})

def doc_view_prescription_post(request):
    print("hll")
    bookid=request.session["uid"]
    print(bookid)

    if request.method=='POST':
        print("hi")

        d1 = request.POST["dd1"]
        print(d1)
        d2 = request.POST['dd2']

        print(d2)
        # return HttpResponse("ok")
        #
        # # at_obj=Attandance.objects.filter(date__lte=date1,date__gte=date2)
        # # at_obj=Attandance.objects.filter(date__range=[date1,date1])
        # # at_obj=Attandance.objects.filter(date__range=[date1, date2])
        #
        #
        #
        print("hi")
        uid = bookid
        use_obj = Patient.objects.get(id=uid)
        print(use_obj)
        # bok_obj=Booking.objects.get(id=bookid)
        bok_obj = Booking.objects.filter(PATIENT=uid,date__range=[d1, d2])
        print(bok_obj)
        res = []
        for i in bok_obj:
            print("zz")
            print(i.id)
            pre_obj = Prescription.objects.filter(BOOKING_id=i.id)
            print(pre_obj)
            for j in pre_obj:
                print(j.prescription)
                ss = {'id': i.id, 'pre_name': j.prescription, 'mname': j.MEDICINE.name, 'qty': j.qty, 'unit': j.unit,
                      'date': i.date}
                print(ss)
                res.append(ss)
                print(pre_obj)

            print("fini")

        print("hi")
        print(res)
        return render(request, "DOCTOR/View previous prescription.html",{'pat_name': use_obj.patient_name, 'data2': res})

def view_prescription_post(request):

    if request.method == 'POST':
        bookid = request.session["uid"]
        uid = bookid
        use_obj = Patient.objects.get(id=uid)
        ph_n=request.POST['number']
        import datetime
        date=datetime.date.today()



        sale_obj =Sales_master(PATIENT=use_obj,date=date,phone_number=ph_n,total_amount="0")
        sale_obj.save()
        ab=Sales_master.objects.latest('id')
        mid22=ab.pk
        request.session["mid"]=mid22
     #####test###
        Batch22=Batch.objects.all()

        bookid=request.session["uid"]


        print("hi")
        uid = bookid
        use_obj = Patient.objects.get(id=uid)
        print(use_obj)
        # bok_obj=Booking.objects.get(id=bookid)
        import datetime

        showtime = datetime.date.today()
        print(showtime)
        print("asss")
        bok_obj = Booking.objects.filter(PATIENT=uid, date=showtime)
        print(bok_obj)
        res = []
        for i in bok_obj:
            print("zz")
            print(i.id)
            print(i.date)
            pre_obj = Prescription.objects.filter(BOOKING_id=i.id)
            print(pre_obj)
            for j in pre_obj:
                print(j.prescription)
                ss = {'id': i.id, 'pre_name': j.prescription, 'mname': j.MEDICINE.name, 'qty': j.qty, 'unit': j.unit,
                      'date': i.date}
                print(ss)
                res.append(ss)
                print(pre_obj)

            print("fini")

        print("hi")
        print(res)
        return render(request, "PHARMACIST/saLe entry.html",
                      {'pat_name': use_obj.patient_name, 'data2': res,'data3':Batch22})




    return render(request, "PHARMACIST/saLe entry.html",{'data':sale_obj})








                # pat_name=bok_obj.PATIENT.patient_name
    #
    #
    #
    #
    # request.session['bookid']=bookid
    # pres_obj=Prescription.objects.filter(BOOKING=bok_obj)
    # print(pres_obj)
    # return render(request,"DOCTOR/View previous prescription.html",{'pat_name':pat_name,'data2':pres_obj})



def a(request):
    return render(request,"adminindex.html")

def logout(request):
    return render(request, "login.html")
               #pharmacistdef
def adm_add_medicine(request):
    if request.method=='POST':
        name=request.POST['mname']
        type=request.POST['type']
        company=request.POST['company']
        usage=request.POST['usage']
        unit=request.POST['unit']
        tax=request.POST['tax']

        med_obj=Medicine()
        med_obj.name=name
        med_obj.type=type
        med_obj.usage=usage
        med_obj.campany=company
        med_obj.unit=unit
        med_obj.tax=tax

        med_obj.save()
        text = "<script>alert('Medicine Added');window.location='/myapp/adm_add_medicine/';</script>"
        return HttpResponse(text)
    return render(request,"PHARMACIST/ADD MEDICINE.html")
def adm_delete_medicine(request,id):
    med_obj=Medicine.objects.get(id=id)

    med_obj.delete()
    med_obj = Medicine.objects.all()
    text = "<script>alert('Medicine Deleted');window.location='/myapp/adm_view_medicine/';</script>"
    return HttpResponse(text)
    return render(request, "PHARMACIST/VIEW medicine.html", {'data': med_obj})
def adm_edit_medicine(request,id):
    med_obj=Medicine.objects.get(id=id)
    print(id)
    request.session['uid']=id
    return render(request, "PHARMACIST/UPDATE MEDICINE.html", {'data': med_obj})

def adm_update_medicine(request):
    if request.method == 'POST':
        name = request.POST['mname']
        type = request.POST['type']
        usage = request.POST['usage']
        company = request.POST['company']
        unit = request.POST['unit']
        tax = request.POST['tax']



        hid=request.session['uid']
        print(hid)
        med_obj = Medicine.objects.get(pk=hid)
        print(med_obj)
        med_obj.name=name
        med_obj.type=type
        med_obj.usage=usage

        med_obj.campany=company
        med_obj.unit = unit
        med_obj.tax = tax
        med_obj.save()

        med_obj =Medicine.objects.all()
        text = "<script>alert('Medicine Updated');window.location='/myapp/adm_view_medicine/';</script>"
        return HttpResponse(text)
        return render(request, "PHARMACIST/VIEW medicine.html", {'data': med_obj})



def adm_view_medicine(request):
    if request.method=="POST":
        med_search=request.POST['text']
        # book_obj=book_fee.objects.get(EMPLOYEE__emp_name=emp_search)
        med_obj=Medicine.objects.filter(name__contains=med_search)
        return render(request, "PHARMACIST/VIEW medicine.html", {'data': med_obj})
    med_obj =Medicine.objects.all()
    return render(request,"PHARMACIST/VIEW medicine.html",{'data': med_obj})
# def adm_add_batch(request):
#     med_obj = Medicine.objects.all()
#     if request.method=="POST":
#         bname=request.POST['bname']
#
#         edate=request.POST['edate']
#         mdate=request.POST['mdate']
#         total_amount=request.POST['amount']
#         unit_amount=request.POST['uamount']
#
#         med_id = request.POST['select']
#         med_obj = Medicine.objects.get(pk=med_id)
#         # medc_id = request.POST['select2']
#         # med_obj = Medicine.objects.get(pk=medc_id)
#         # scat_id=request.POST['selectscat']
#         # scat_obj=sub_cat.objects.get(pk=scat_id)
#
#         batch_obj=Batch()
#         batch_obj.b_name=bname
#
#         batch_obj.exp_date=edate
#         batch_obj.man_date=mdate
#         batch_obj.total_amount=total_amount
#         batch_obj.unit_amount=unit_amount
#
#         batch_obj.MEDICINE = med_id
#
#
#         batch_obj.save()
#         text = "<script>alert('Batch added successfully');window.location='/myapp/adm_add_batch/';</script>"
#         return HttpResponse(text)
#
#
#     # medc_obj = Medicine.objects.all()
#
#     return render(request,"PHARMACIST/ADD BATCH.html",{'data1': med_obj})def adm_add_books(request):
def adm_add_batch(request):
    if request.method=="POST":
        bname=request.POST['bname']
        mdate=request.POST['mdate']

        edate=request.POST['edate']
        tamount=request.POST['amount']
        unit_amount=request.POST['uamount']

        med_id = request.POST['select']
        med_obj = Medicine.objects.get(pk=med_id)

        batch_obj = Batch()
        batch_obj.b_name=bname

        batch_obj.exp_date=edate
        batch_obj.man_date=mdate
        batch_obj.total_amount=tamount
        batch_obj.unit_amount=unit_amount
        batch_obj.MEDICINE= med_obj

        batch_obj.save()
        text = "<script>alert('Batch added successfully');window.location='/myapp/adm_add_batch/';</script>"
        return HttpResponse(text)

    med_obj = Medicine.objects.all()


    return render(request, "PHARMACIST/ADD BATCH.html", {'data1': med_obj})
def adm_view_Batch(request):

    batch_obj = Batch.objects.all()

    return render(request,"PHARMACIST/VIEW BATCH.html",{'data':batch_obj})
def adm_edit_batch(request,id):
    print("rrr")
    request.session['id']=id
    bat_obj=Batch.objects.get(id=id)
    print(id)
    med_obj=Medicine.objects.all()
    return render(request, "PHARMACIST/UPDATE BATCH.html", {'data': bat_obj,'data1':med_obj})

def adm_update_batch(request):
    print("hi")
    bname = request.POST['bname']
    medicine_id=request.POST['select']
    mdate = request.POST['mdate']
    edate = request.POST["edate"]
    tamount = request.POST['amount']
    unit_amount = request.POST['uamount']
    id = request.session['id']

    med_obj = Medicine.objects.get(id=medicine_id)
    print(med_obj)

    batch_obj = Batch.objects.get(id=id)
    batch_obj.b_name = bname

    batch_obj.exp_date = edate
    batch_obj.man_date = mdate
    batch_obj.total_amount = tamount
    batch_obj.unit_amount = unit_amount
    batch_obj.MEDICINE = med_obj

    batch_obj.save()

    batch_obj = Batch.objects.all()
    text = "<script>alert('Batch Updated successfully');window.location='/myapp/adm_view_Batch/';</script>"
    return HttpResponse(text)

    return render(request, "PHARMACIST/UPDATE BATCH.html", {'data': batch_obj})

def adm_add_stock(request):
    if request.method == "POST":

        qty = request.POST['qty']

        batch_id = request.POST['select']
        batch_obj = Batch.objects.get(pk=batch_id)

        stock_obj = Stock()
        stock_obj.BATCH =batch_obj

        stock_obj.quantity = qty


        stock_obj.save()
        text = "<script>alert('Stock added successfully');window.location='/myapp/adm_add_stock/';</script>"
        return HttpResponse(text)

    batch_obj = Batch.objects.all()

    return render(request, "PHARMACIST/ADD STOCK.html", {'data1': batch_obj})

def adm_view_stock(request):
    stock_obj = Stock.objects.filter(quantity__gt=0)
    return render(request, "PHARMACIST/VIEW STOCK.html", {'data': stock_obj})

def adm_edit_stock(request, id):
    print("rrr")
    request.session['id'] = id
    st_obj = Stock.objects.get(id=id)
    print(id)
    bat_obj = Batch.objects.all()
    return render(request, "PHARMACIST/UPDATE STOCK.html", {'data': st_obj, 'data1': bat_obj})

def adm_update_stock(request):
    print("hi")
    qty = request.POST['qty']
    batch_id = request.POST['select']

    id = request.session['id']

    bat_obj = Batch.objects.get(id=batch_id)
    print(bat_obj)

    stock_obj = Stock.objects.get(id=id)
    stock_obj.quantity = qty

    stock_obj.BATCH = bat_obj

    stock_obj.save()

    stock_obj = Stock.objects.all()
    text = "<script>alert('Stock Updated successfully');window.location='/myapp/adm_view_stock/';</script>"
    return HttpResponse(text)

    return render(request, "PHARMACIST/VIEW STOCK.html", {'data': stock_obj})

def adm_delete_stock(request, id):
    stock_obj = Stock.objects.get(id=id)
    stock_obj.delete()
    stock_obj = Stock.objects.all()
    text = "<script>alert('Stock deleted successfully');window.location='/myapp/adm_view_stock/';</script>"
    return HttpResponse(text)
    return render(request, "PHARMACIST/VIEW STOCK.html", {'data': stock_obj})

def adm_delete_batch(request, id):
    bat_obj = Batch.objects.get(id=id)
    bat_obj.delete()
    bat_obj = Batch.objects.all()
    text = "<script>alert('Batch deleted successfully');window.location='/myapp/adm_view_Batch/';</script>"
    return HttpResponse(text)
    return render(request, "PHARMACIST/VIEW BATCH.html", {'data': bat_obj})

def doc_out(request):
    out_obj = Stock.objects.filter(quantity=0)
    return render(request, "PHARMACIST/VIEW OUT OF STOCK.html", {'data': out_obj})

def exp_med(request):
    exp_obj = Batch.objects.filter(exp_date__lt=datetime.datetime.now())
    return render(request, "PHARMACIST/view Expiered product.html", {'data': exp_obj})

# def leav_approval(request):
#     leave_obj = Leave.objects.all()
#     print(leave_obj)
#     return render(request, "ADMIN/Leave Approval.html", {'data': leave_obj})




        #ANDROID.......
def patient_view_status(request):
    print("hlw")
    lid = request.POST['lid']
    print(lid)
    login_obj = Login.objects.get(id=lid)
    print(login_obj)
    user_obj = Patient.objects.get(LOGIN=login_obj)
    print(user_obj)
    res2 = []
    ma = Booking.objects.filter(PATIENT=user_obj)
    for i in ma:
        n = i.date
        print("hkk")
        print(n)
        ak = []
        pp = str(n)
        ak = pp.split("-")
        nwdate = ""
        print("aaa")
        nwdate = ak[2] + "-" + ak[1] + "-" + ak[0]
        print(nwdate)
        date = nwdate
        print(date)

        ss = {'id': i.id, 'ename': i.EMPLOYEE.emp_name, 'bookdate': date,  'slot': i.slot
              }
        res2.append(ss)
    print(res2)
    print("************")
    data = {"status": "ok", "res2": res2}
    return JsonResponse(data)


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
    from datetime import date, timedelta
    did=request.POST['did']
    day=request.POST['day']
    dd=request.POST['dd']
    print(dd)

    doc_obj = Employee.objects.get(id=did)
    ######
    leav_obj=Leave.objects.filter(EMPLOYEE=doc_obj)
    list = []
    for zz in leav_obj:
        from_date=zz.date
        to_date=zz.to_date
        print(from_date)
        print(to_date)

        # now_date="17-05-2021"

        ar = []
        ar2 = []

        ar = str(from_date).split("-")
        ar2 = str(to_date).split("-")
        #######date

        d0 = date(int(ar[0]), int(ar[1]), int(ar[2]))
        print("d000",d0)
        d1 = date(int(ar2[0]), int(ar2[1]), int(ar2[2]))
        delta = d1 - d0
        aa = delta.days
        print(delta.days)
        print("days")
        yr = ar[0]
        yr22 = yr[2:]
        date_change = ar[2] + "/" + ar[1] + "/" + yr22

        print(yr[2:])
        import datetime

        for mm in range(0, aa + 1):
            # print(mm)
            #########


            StartDate = date_change
            # print(StartDate)
            date_1 = datetime.datetime.strptime(StartDate, "%d/%m/%y")

            end_date = date_1 + datetime.timedelta(days=mm)

            print(end_date)
            ar3 = []
            ar3 = str(end_date).split(" ")
            # print(ar3)
            ar4 = []
            ar4 = str(ar3[0]).split("-")
            vv = ""
            vv = ar4[2] + "-" + ar4[1] + "-" + ar4[0]
            print("aaaa",vv)
            list.append(vv)
        print("bbb",list)
        if dd in list:
            data = {"status": "no" }
            return JsonResponse(data)


    #########
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
    ######newcode#####
    print("hkk")
    print(date)
    ak=[]
    pp=str(date)
    ak=pp.split("-")
    nwdate=""
    print("aaa")
    nwdate=ak[2]+"-"+ak[1]+"-"+ak[0]
    print(nwdate)
    date=nwdate
    print(date)
    #######newcod######
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
    ######newcode
    print("date")
    print(dt)
    print("hkk")

    ak = []
    pp = str(dt)
    ak = pp.split("-")
    nwdate = ""
    print("aaa")
    nwdate = ak[2] + "-" + ak[1] + "-" + ak[0]
    print(nwdate)
    dt = nwdate
    print(dt)
    ###newcode###
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
def user_update(request):
    if request.method == "POST":
        print("entr")
        name = request.POST['name']
        age = request.POST['age']
        email = request.POST['email']
        gender = request.POST['gender']
        hname = request.POST['house_name']
        city = request.POST['place']
        district = request.POST['district']
        pincode = request.POST['pincode']
        phone = request.POST['phone']
        state = request.POST['state']
        lid = request.POST['lid']
        print(lid)
        print("qqq")

        log_obj = Login.objects.get(id=lid)

        upd_obj = Patient.objects.get(LOGIN=log_obj)
        upd_obj.patient_name = name
        upd_obj.age = age
        upd_obj.emial_Id = email
        upd_obj.gender = gender
        upd_obj.house_name = hname
        upd_obj.place = city
        upd_obj.district = district
        upd_obj.state = state
        upd_obj.pincode = pincode
        upd_obj.phone_number = phone
        upd_obj.save()

        data = {"status": "ok"}
        return JsonResponse(data)


def view_profile(request):
    lid = request.POST['lid']
    log_obj =Login.objects.get(id=lid)
    user_obj =Patient.objects.get(LOGIN=log_obj)

    data = {"status": "ok", 'name': user_obj.patient_name,'email': user_obj.emial_Id, 'age':user_obj.age ,'gender': user_obj.gender,
            'hname': user_obj.housename, 'place': user_obj.place, 'district': user_obj.district,
            'pincode': user_obj.pincode, 'phone': user_obj.phone_number,'state': user_obj.state}
    print(data)
    return JsonResponse(data)
def view_next_visit(request):
    lid = request.POST['lid']
    # lastid22 = request.POST['last_id']
    log_obj =Login.objects.get(id=lid)
    user_obj =Patient.objects.get(LOGIN=log_obj)
    res2 = []
    ma = Booking.objects.filter(PATIENT=user_obj)
    print("maa=",ma)
    for ll in ma:

        na=Reminder.objects.filter(BOOKING=ll,next_date__gte=datetime.date.today())
        print("na",na)
        print(na)
        for ii in na:
            n=ii.next_date
            print("hkk")
            print(n)
            ak = []
            pp = str(n)
            ak = pp.split("-")
            nwdate = ""
            print("aaa")
            nwdate = ak[2] + "-" + ak[1] + "-" + ak[0]
            print(nwdate)
            date = nwdate
            print(date)


            ss = {'id':ii.pk,'next_date':date,'ename': ii.BOOKING.EMPLOYEE.emp_name}
            res2.append(ss)
        print(res2)



    data = {"status": "ok", "res2": res2}
    print(data)

    return JsonResponse(data)
# def view_tips_patient(request):
#     res2 = []
#     ma = Tips.objects.all()
#     for ii in ma:
#         ss = {'id': ii.pk, 'tips': ii.tips}
#         res2.append(ss)
#
#     data = {"status": "ok", "data": res2}
#     return JsonResponse(data)

def chatload(request):
    return render(request,'DOCTOR/fur_chat.html')


def drviewmsg(request,receiverid):

    doclidlid=request.session["lid"]
    print("!!!!!!!!!!",doclidlid,receiverid)
    log_ob=Login.objects.get(id=doclidlid)
    doc=Employee.objects.get(LOGIN=log_ob)
    # print(doc)
    # stud_ob=studentmodel.objects.get(LID=rec)
    xx=Patient.objects.get(id=receiverid)
    print(xx)
    obj=Chat.objects.filter(DOCTOR=doc,PATIENT=xx)
    print(obj)
    user_data=Patient.objects.get(id=receiverid)
    print(user_data)
    print("********************",obj)

    res = []
    for i in obj:
        s = {'id':i.pk, 'date':i.date,'msg':i.message,'type':i.type}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res,'name':user_data.patient_name,'image':"/media/nb.png"})

def chatview(request):
    print("hai")
    cid = request.session["lid"]
    print(cid)
    mmss = Login.objects.get(id=cid)
    print(mmss)
    ms = Employee.objects.get(LOGIN=mmss)
    print(ms)
    docid = request.session['doc_id']
    chat_obj = Chat.objects.filter(DOCTOR=docid)
    lis=[]
    for jj in chat_obj:
        lis.append(jj.PATIENT.id)
    print("patient id here")
    print(lis)
    res = []

    for kk in lis:





        da =Patient.objects.get(id=kk)
        print(da)
        s = {'id':da.pk, 'name': da.patient_name, 'email': da.emial_Id, 'image': "/media/nb.png"}
        res.append(s)



        print(res)
    return JsonResponse({'status': 'ok', 'data': res})


def doctor_insert_chat(request,receiverid,msg):
    print("hai riss")

    dlid= request.session["lid"]
    log_ob=Login.objects.get(id=dlid)
    dobj=Employee.objects.get(LOGIN=log_ob)
    import datetime
    datetime.date.today()  # Returns 2018-01-15
    showtime=datetime.datetime.now()
    print("qqq")

    obj=Chat()
    obj.PATIENT=Patient.objects.get(pk=receiverid)
    obj.DOCTOR=dobj
    obj.message=msg
    obj.type='doctor'
    obj.date=showtime
    obj.save()
    print("yyy")
    return JsonResponse({'status':'ok'})



