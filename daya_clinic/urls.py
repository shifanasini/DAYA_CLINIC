from django.urls import path
from . import views
urlpatterns = [
    path('adm_add_schedule/', views.adm_add_schedule),
    path('login/', views.login),
    path('adm_add_services/', views.adm_add_services),
    path('adm_view_employee/', views.adm_view_employee),

    path('adm_add_tips/', views.adm_add_tips),
    path('adm_add_about/', views.adm_add_about),
    path('adm_update_about/', views.adm_update_about),
    path('adm_view_about/', views.adm_view_about),
    path('adm_delete_about/<str:id>', views.adm_delete_about),
    path('adm_edit_about/<str:id>', views.adm_edit_about),
    path('adm_edit_about/<str:id>', views.adm_edit_about),
    path('adm_employee_registration/', views.adm_employee_registration),
    path('adm_employee_updation/', views.adm_update_employee),
    path('adm_feedback/', views.adm_feedback),
    path('adm_leave_approval/', views.adm_leave_approval),
    path('admin_view_stock/', views.admin_view_stock),
    path('adm_feedback_replay/', views.adm_feedback_replay),
    path('adm_view_employees/', views.adm_view_employees),
    path('adm_delete_employee/<str:id>', views.adm_delete_employee),
    path('adm_edit_employee/<str:id>', views.adm_edit_employee),
    path('adm_edit_employee/<str:id>', views.adm_edit_employee),
    path('adm_view_patients/', views.adm_view_patients),
    path('adm_view_sales_report_main/', views.adm_view_sales_report_main),
    path('adm_view_schedule/', views.adm_view_schedule),
    path('adm_delete_schedule/<str:id>', views.adm_delete_schedule),
    path('adm_edit_schedule/<str:id>', views.adm_edit_schedule),
    path('adm_update_schedule/', views.adm_update_schedule),
    path('adm_view_services/', views.adm_view_services),
    path('adm_delete_medicine/<str:id>', views.adm_delete_medicine),
    path('adm_view_medicine/<str:id>', views.adm_view_medicine),
    path('adm_update_service/', views.adm_update_service),
    path('adm_edit_service/<str:id>', views.adm_edit_service),

    path('adm_view_tips/', views.adm_view_tips),
    path('adm_delete_tips/<str:id>', views.adm_delete_tips),
    path('adm_edit_tip/<str:id>', views.adm_edit_tip),
    path('adm_edit_medicine/<str:id>', views.adm_edit_medicine),
    path('adm_update_tip/', views.adm_update_tip),
    path('adm_update_medicine/', views.adm_update_medicine),
    path('adm_add_contact/', views.adm_add_contact),

    path('adm_add_attendance/', views.adm_add_attendance),

    path('adm_view_attendance/', views.adm_view_attendance),
    path('adm_checkout/',views.adm_checkout),
    path('adm_checkout_post/',views.adm_checkout_post),
    path('adm_view_booking_info/', views.adm_view_booking_info),
    path('homepage/', views. homepage),
    path('homepage_doctor/', views.homepage_doctor),
    path('doc_add_prescription/<str:bookid>', views.doc_add_prescription),
    path('doc_add_prescription_post/', views.doc_add_prescription_post),
    path('doc_del_presc/<str:id>', views.doc_del_presc),

    path('doc_view_leave_satatus/', views.  doc_view_leave_satatus),
    path('doc_add_leave/', views. doc_add_leave),
    path('doc_next_slot/', views. doc_next_slot),
    path('doc_add_next_visit/', views. doc_add_next_visit),
    path('doc_view_patients/', views. doc_view_patients),
    # path('doc_view_prescription/', views. doc_view_prescription),
    path('doc_view_schedule/', views. doc_view_schedule),



    path('adm_index/', views. adm_temp),

    #doctor
    path('doc_index/', views.doc_temp),
    path('homepage_doctor/', views.homepage_doctor),
    path('doc_view_schedule/', views.doc_view_schedule),
    path('doc_view_patients/', views.doc_view_patients),
    path('doc_view_booking/', views.doc_view_booking),
    path('doc_add_next_visit/<str:bookid>', views.doc_add_next_visit),
    path('doc_add_next_visit_post/', views.doc_add_next_visit_post),
    path('doc_view_prescription/<str:bookid>', views.doc_view_prescription),
    path('doc_view_prescription_post/', views.doc_view_prescription_post),
    path('doc_view_medicine/', views.doc_view_medicine),
    path('a/', views.a),

#####pharmacist
    path('adm_add_medicine/',views.adm_add_medicine),
    path('adm_view_medicine/',views.adm_view_medicine),
    path('adm_add_batch/',views.adm_add_batch),
    path('adm_view_Batch/',views.adm_view_Batch),
    path('adm_update_batch/',views.adm_update_batch),
    path('adm_update_stock/',views.adm_update_stock),
    path('adm_edit_batch/<str:id>',views.adm_edit_batch),
    path('adm_edit_stock/<str:id>',views.adm_edit_stock),
    path('adm_add_stock/',views.adm_add_stock),
    path('adm_view_stock/',views.adm_view_stock),
    path('adm_delete_stock/<str:id>', views.adm_delete_stock),
    path('adm_delete_batch/<str:id>', views.adm_delete_batch),












    path('homepage_ph/', views.homepage_ph),
    path('homepage_doc/', views.homepage_doc),
    #       android
    path("view_contact_info/", views.view_contact_info),
    path("view_about_patient/", views.view_about_patient),
    path("view_tips_patient/", views.view_tips_patient),
    path("view_tips_more/", views.view_tips_more),
    path("view_service_patient/", views.view_service_patient),
    path("view_doctors/", views.view_doctors),
    path("pa_registration/", views.pa_registration),
    path("view_our_doctors/", views.view_our_doctors),
    path("view_schedule/", views.view_schedule),
    path("view_timeslots/", views.view_timeslots),
    path("user_login/", views.user_login),
    path("booking/", views.booking),
    path("inmessage/", views.inmessage),
    path("view_message2/", views.view_message2),




]