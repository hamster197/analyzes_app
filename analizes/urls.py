from django.urls import path, reverse_lazy, include
from analizes import views
from django.contrib.auth.views import LogoutView

app_name = 'analizes_urls'

urlpatterns = [
    path('', views.MainPage.as_view(), name = 'main_page_url'),

    path('register/', views.RegisterPage.as_view(), name = 'patient_register_url', ),
    path('login/', views.LoginPage.as_view(), name = 'login_url', ),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('analizes_urls:main_page_url')), name='logout'),

    path('admin_chemical_elements_edit/', views.AdminChemicalElementsMainQuideEdit.as_view(),
         name = 'admin_chemical_elements_edit_url', ),
    path('admin_patient_list/', views.AdminPatientsList.as_view(),
         name='admin_patient_list_url', ),
    path('admin_patient_list/edit/<int:pk>/', views.AdminPatientEdit.as_view(),
         name='admin_patient_edit_url', ),
    path('admin_doctors_list/', views.DoctorsList.as_view(),
         name='admin_doctors_list_url', ),
    path('admin_doctors_list/new/', views.DoctorNew.as_view(),
         name='admin_doctors_new_url', ),
    path('admin_doctors_list/edit/<int:pk>/', views.DoctorEdit.as_view(),
         name='admin_doctors_edit_url', ),
    path('admin_doctors_list/delete/<int:pk>/', views.DoctorDelete.as_view(),
         name='admin_doctors_delete_url', ),
    path('admin_recomendations_list/', views.RecomendationsQuideList.as_view(),
         name='admin_recomendations_list_url', ),
    path('admin_recomendations_list/new/', views.RecomendationNew.as_view(),
         name='admin_recomendations_new_url', ),
    path('admin_recomendations_list/edit/<int:pk>/', views.RecomendationEdit.as_view(),
         name='admin_recomendations_edit_url', ),
    path('admin_recomendations_list/delete/<int:pk>/', views.RecomendetionDelete.as_view(),
         name='admin_recomendations_delete_url', ),

    path('patinet_account_form/<int:pk>/', views.PatientAccount.as_view(),
         name='patinet_account_form_index_url', ),
    path('patinet_account_form/<int:pk>/<int:idd>/', views.PatientAccountForm.as_view(),
         name='patinet_account_form_url', ),
    path('patinet_analizes_formset/<int:pk>/', views.PatientAnalizesFormsetExample.as_view(),
         name='patinet_analize_formset_example_url', ),

    path('doctor_patinets_list/', views.DoctorPatientsList.as_view(),
         name='doctor_patinets_list_url', ),

    path('api/', include('analizes.api.urls'),)
]