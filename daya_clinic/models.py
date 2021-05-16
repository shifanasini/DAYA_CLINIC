from django.db import models

# Create your models h
class Login(models.Model):
    uname=models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    logintype= models.CharField(max_length=50)
    class Meta:
        db_table="login"


class Employee(models.Model):

    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    emp_name = models.CharField(max_length=50)
    emp_type = models.CharField(max_length=50)

    dob=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    housename=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    #fee=models.CharField(max_length=50)
    emial_Id = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    photo = models.CharField(max_length=300)
    # fee = models.CharField(max_length=300,default="100")

    class Meta:
        db_table="employee"
class Tips(models.Model):
    tips= models.CharField(max_length=400)
    date = models.DateField(max_length=50)


    class Meta:
        db_table = "tips"
class book_fee(models.Model):
    EMPLOYEE = models.ForeignKey(Employee, on_delete=models.CASCADE)
    fee = models.CharField(max_length=50)

    class Meta:
        db_table="book_fee"
class About(models.Model):
  about = models.CharField(max_length=400)
  date = models.DateField(max_length=50)
  photo = models.CharField(max_length=300)

  class Meta:
    db_table = "about"

class Services(models.Model):
    services= models.CharField(max_length=400)
    date = models.DateField(max_length=50)

    class Meta:
        db_table = "services"


class Schedule(models.Model):
    EMPPLOYEE = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day= models.CharField(max_length=50)
    from_time = models.TimeField(max_length=50)
    to_time = models.TimeField(max_length=50)
    # fee = models.CharField(max_length=50,default="100")

    class Meta:
        db_table = "schedule"
class Slot(models.Model):
     SCHEDULE= models.ForeignKey(Schedule, on_delete=models.CASCADE)
     slot_time = models.TimeField(max_length=50)
     slot_status = models.CharField(max_length=50)
     class Meta:
      db_table = "slot"
class Leave(models.Model):
    EMPLOYEE = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date= models.DateField(max_length=50)
    to_date= models.DateField(max_length=50 )

    reason = models.CharField(max_length=100)
    leave_status = models.CharField(max_length=100)
    type= models.CharField(max_length=100)


    class Meta:
        db_table = "leave"


class Late_message(models.Model):
    EMPPLOYEE = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date= models.DateField(max_length=50)
    arriving_time = models.TimeField(max_length=50)


    class Meta:
        db_table = "late_message"
class Patient(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)

    patient_name = models.CharField(max_length=50)
    age = models.CharField(max_length=50)

    gender = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    housename = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    emial_Id = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    class Meta:
        db_table = "patient"


class Feedback(models.Model):
    PATIENT = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(max_length=50)
    feedback = models.CharField(max_length=200)

    class Meta:
        db_table = "feedback"
class Contact_details(models.Model):

    date = models.DateField(max_length=50)
    phone_number = models.CharField(max_length=50)
    latitude = models.CharField(max_length=300)
    longitude = models.CharField(max_length=300)
    loc_hint = models.CharField(max_length=300)
    email = models.CharField(max_length=30, default="aaa")
    class Meta:
        db_table = "contact_details"
class Attandance(models.Model):
    EMPLOYEE = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(max_length=400)
    from_time=models.CharField(max_length=200,default="00:00")
    to_time=models.CharField(max_length=200,default="00:00")
    status=models.CharField(max_length=200,default="absent")


    class Meta:
        db_table = "attendance"

class Booking(models.Model):
    PATIENT = models.ForeignKey(Patient, on_delete=models.CASCADE)
    EMPLOYEE = models.ForeignKey(Employee, on_delete=models.CASCADE)

    slot= models.CharField(max_length=200)
    date = models.DateField(max_length=300)

    class Meta:
        db_table = "booking"



    class Meta:
        db_table = "booking"


class Medicine(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    usage = models.CharField(max_length=50)
    unit = models.CharField(max_length=100, default="0")

    campany = models.CharField(max_length=50)


    class Meta:
        db_table = "medicine"

class Prescription(models.Model):
    BOOKING = models.ForeignKey(Booking, on_delete=models.CASCADE)
    MEDICINE= models.ForeignKey(Medicine, on_delete=models.CASCADE)
    prescription = models.CharField(max_length=50)
    qty = models.CharField(max_length=50,default="0")
    unit = models.CharField(max_length=50)

    class Meta:
        db_table = "prescription"
class Batch(models.Model):

    MEDICINE= models.ForeignKey(Medicine, on_delete=models.CASCADE)
    b_name = models.CharField(max_length=100)
    man_date = models.DateField(max_length=100)
    exp_date = models.DateField(max_length=100)
    total_amount = models.CharField(max_length=50,default="0")
    unit_amount = models.CharField(max_length=50)

    class Meta:
        db_table = "batch"

class Reminder(models.Model):
    BOOKING = models.ForeignKey(Booking, on_delete=models.CASCADE)
    next_date = models.DateField(max_length=300)

    class Meta:
        db_table = "reminder"



class Stock(models.Model):
    BATCH = models.ForeignKey(Batch, on_delete=models.CASCADE,default="2")
    quantity = models.CharField(max_length=100)



    class Meta:
        db_table = "stock"

class Sales_master(models.Model):
    date = models.DateField(max_length=100)
    PATIENT = models.ForeignKey(Patient, on_delete=models.CASCADE)
    total_amount = models.FloatField(max_length=50)
    phone_number = models.CharField(max_length=50)

    class Meta:
        db_table = "sales_master"


class Sales_sub(models.Model):
    SALE_MASTER = models.ForeignKey(Sales_master, on_delete=models.CASCADE)
    BATCH= models.ForeignKey(Batch, on_delete=models.CASCADE)

    quantity = models.CharField(max_length=100)




    class Meta:
        db_table = "sales_sub"


class Current_slot(models.Model):
    EMPLOYEE = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(max_length=50)
    current_slot = models.CharField(max_length=50)


    class Meta:
        db_table = "current_slot"


class Chat(models.Model):
    PATIENT=models.ForeignKey(Patient,on_delete=models.CASCADE)
    DOCTOR=models.ForeignKey(Employee,on_delete=models.CASCADE)

    date = models.DateField(max_length=50)
    message = models.CharField(max_length=200)
    type = models.CharField(max_length=50)


    class Meta:
        db_table = "chat"


