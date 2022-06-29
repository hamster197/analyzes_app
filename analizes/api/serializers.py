from django.contrib.auth.models import Group
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from analizes.models import *


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(label='Имя', required=True)
    last_name = serializers.CharField(label='Фамилия', required=True)
    patronymic = serializers.CharField(label='Oтчество', required=True)
    age = serializers.IntegerField(label='Возраст', required=True)
    height = serializers.FloatField(label='Pост', required=True)
    weight = serializers.FloatField(label='Bес', required=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('pk', 'username', 'email', 'first_name', 'patronymic', 'last_name', 'password', 'age', 'height',
                  'weight', 'gender', 'phone', 'sport',)

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)
        group = Group.objects.get(name='patients')
        new_user.groups.add(group)
        return new_user

class DoctorEditSerializer(BaseUserRegistrationSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(label='Имя', required=True)
    last_name = serializers.CharField(label='Фамилия', required=True)
    patronymic = serializers.CharField(label='Oтчество', required=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('pk', 'username', 'email', 'first_name', 'patronymic', 'last_name', 'password', 'photo', 'position',
                  )

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)
        group = Group.objects.get(name='doctors')
        new_user.groups.add(group)
        return new_user

class ChemicalElementsMainQuideSerializer(ModelSerializer):
    class Meta:
        model = ChemicalElementsMainQuide
        fields = ('__all__')

class DoctorsPositionQuideListEditSerializer(ModelSerializer):
    class Meta:
        model = DoctorsPositionQuide
        fields = ('__all__')

class AdminRecomendationsQuideSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = RecomendationsQuide
        exclude = ('type', 'patient',)

class DoctorRecomendationsSerializer(ModelSerializer):
    type = serializers.ChoiceField(['Рекомендация', 'Пишевая рекомендация',])
    class Meta:
        model = RecomendationsQuide
        exclude = ('patient', 'name', 'author',)

    def validate(self, data):
        if data['type'] == 'Рекомендация' and data['attach']:
            raise serializers.ValidationError('У этого типа рекомендации нет Химических элементов')
        return data

class DoctorRecomendationsQuideSerializer(Serializer):
    recomendations_list = []
    for recomendation in RecomendationsQuide.objects.filter(type='Пишевая рекомендация(Справочник)', patient=None):
        recomendations_list.append(recomendation.pk)
    pk = serializers.ChoiceField(recomendations_list)

class PatientAnalizesSerializer(Serializer):

    def get_fields(self):
        for element in ChemicalElementsMainQuide.objects.all():
            if element.required == True:
                self._declared_fields.update({element.name: serializers.FloatField(label=element.name, required=True),})
            else:
                self._declared_fields.update({element.name: serializers.FloatField(label=element.name, required=False,),})

        return self._declared_fields









