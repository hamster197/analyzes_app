from django.urls import path, include, re_path
from rest_framework import routers

from analizes.api.views import *

admin_chemical_elements_router = routers.SimpleRouter()
admin_chemical_elements_router.register('admin_chemical_elements_edit', ChemicalElementsMainQuideEdit,
                                        basename='admin_chemical_elements_edit')

patient_edit_router = routers.SimpleRouter()
patient_edit_router.register('patients_edit', AdminPatientsListEdit, basename='patient_edit_router')

doctor_edit_router = routers.SimpleRouter()
doctor_edit_router.register('doctor_edit', AdminDoctorsListEdit, basename='doctor_edit_router')

doctor_position_router = routers.SimpleRouter()
doctor_position_router.register('doctor_position', DoctorsPositionQuideListEdit, basename='doctor_position_router')

admin_recomendation_router = routers.SimpleRouter()
admin_recomendation_router.register('admin_recomendation', RecomendationsQuideListEdit,
                                    basename='admin_recomendation_router')

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    re_path('v1/auth/', include('djoser.urls.authtoken')),

    path('v1/', include(admin_chemical_elements_router.urls)),
    path('v1/', include(patient_edit_router.urls)),
    path('v1/', include(doctor_edit_router.urls)),
    path('v1/', include(doctor_position_router.urls)),
    path('v1/', include(admin_recomendation_router.urls)),
    path('v1/patient_detail/<int:pk>/', PatientsDetail.as_view(),),
    path('v1/patient_detail/recomendations/<int:pk>/', DoctorPatientsRecomendationsList.as_view(),),
    path('v1/patient_detail/recomendations_quide/<int:pk>/', QuideDoctorPatientsRecomendationsList.as_view(),),
    path('v1/patinet_analizes/add/<int:pk>/', PatientAnalizesEdits.as_view(),),
]