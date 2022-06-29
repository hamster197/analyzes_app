
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from analizes.api.permissions import *
from analizes.api.serializers import *
from analizes.models import *

class ChemicalElementsMainQuideEdit(ModelViewSet):
    """
           Перечисляет все химические элементы или создает и редактирует элемент.
           permission_classes = (IsAdminOrDoctorsReadOnly,)
    """
    queryset = ChemicalElementsMainQuide.objects.all()
    serializer_class = ChemicalElementsMainQuideSerializer
    permission_classes = (IsAuthenticated, IsAdminOrDoctorsReadOnly,)

class AdminPatientsListEdit(ModelViewSet):
    """
           Перечисляет всех пациентов, добавляеет и редактирует пациента.
           permission_classes = (IsAuthenticated, IsAdminOrDoctorsReadOnly,)
    """
    queryset = User.objects.filter(groups__name='patients', )
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsAuthenticated, IsAdminOrDoctorsReadOnly,)

class DoctorsPositionQuideListEdit(ModelViewSet):
    """
           Перечисляет всех должности докторов, создает, удаляет, редактирует их.
           permission_classes = (IsAuthenticated, IsAdminOnly,)
    """
    queryset = DoctorsPositionQuide.objects.all()
    serializer_class = DoctorsPositionQuideListEditSerializer
    permission_classes = (IsAuthenticated, IsAdminOnly,)

class AdminDoctorsListEdit(ModelViewSet):
    """
           Перечисляет всех Докторов, создает, удаляет, редактирует доктора.
           permission_classes = (IsAuthenticated, IsAdminOnly,)
    """
    queryset = User.objects.filter(groups__name='doctors',)
    serializer_class = DoctorEditSerializer
    permission_classes = (IsAuthenticated, IsAdminOnly,)

class RecomendationsQuideListEdit(ModelViewSet):
    """
           Перечисляет все Пишевая рекомендация(Справочник), создает, удаляет, редактирует.
           permission_classes = (IsAuthenticated, IsAdminOrDoctorsReadOnly,)
    """
    queryset = RecomendationsQuide.objects.filter(author__groups__name='admins')
    serializer_class = AdminRecomendationsQuideSerializer
    permission_classes = (IsAuthenticated, IsAdminOrDoctorsReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, type='Пишевая рекомендация(Справочник)')

class PatientsDetail(RetrieveAPIView):
    """
           Отображает учетные данные пациента
           permission_classes = (IsAuthenticated, AuthorOrDoctorsReadOnly,)
    """
    queryset = User.objects.filter(groups__name='patients')
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsAuthenticated, AuthorOrDoctorsReadOnly,)

class DoctorPatientsRecomendationsList(ListCreateAPIView):
    """
           Отображает все рекомендации пациента,
           добавляет 'Рекомендация', 'Пишевая рекомендация'
           permission_classes = (IsAuthenticated, IsDoctorOrPatientReadOnly),
    """

    serializer_class = DoctorRecomendationsSerializer
    http_method_names = ['get', 'post',]
    permission_classes = (IsAuthenticated, IsDoctorOrPatientReadOnly,)

    def get_queryset(self, ):
        return RecomendationsQuide.objects.filter(patient=get_object_or_404(User, pk=self.kwargs['pk'])) \
            .order_by('-creation_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, patient=get_object_or_404(User, pk=self.kwargs['pk']))

class QuideDoctorPatientsRecomendationsList(APIView):
    """
           добавляет Пишевые рекомендации(Справочник) пациенту
           permission_classes = (IsAuthenticated, IsDoctorOrPatientReadOnly),
    """
    serializer_class = DoctorRecomendationsQuideSerializer
    permission_classes = (IsAuthenticated, IsDoctorOrPatientReadOnly,)

    def post(self, request, **kwargs):
        serializer = DoctorRecomendationsQuideSerializer(data=request.data)
        if serializer.is_valid():
            recomendation = get_object_or_404(RecomendationsQuide, pk=serializer.data['pk'])
            patient = get_object_or_404(User, pk=kwargs['pk'])
            new_recomendation = RecomendationsQuide.objects.create(patient=patient, author=request.user,
                                                                   type='Пишевая рекомендация(Справочник)',
                                                                   discription=recomendation.discription)

            new_recomendation.attach.set(recomendation.attach.all())
        return Response(serializer.data)

class PatientAnalizesEdits(APIView):
    """
           добавляет Результаты анализы пациенту
           permission_classes = (IsAuthenticated, IsDoctorOrPatientReadOnly,),
    """
    serializer_class = PatientAnalizesSerializer
    permission_classes = (IsAuthenticated, IsDoctorOrPatientReadOnly,)

    def post(self, request, **kwargs):
        serializer = PatientAnalizesSerializer(data=request.data)
        if serializer.is_valid():
            new_analize_instances = []
            for element in ChemicalElementsMainQuide.objects.all():
                if request.data[element.name]:
                    new_analize = PatirntAnalizler(patient_id=self.kwargs['pk'], eliment=element,
                                                   rezult=request.data[element.name])

                    new_analize_instances.append(new_analize)
            PatirntAnalizler.objects.bulk_create(new_analize_instances)
            
        return Response(serializer.data)









