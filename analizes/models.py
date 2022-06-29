from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class SportQuide(models.Model):
    sport_name = models.CharField(verbose_name='Вид спорта', max_length=80)
    class Meta:
        verbose_name = 'Справочник видов спорта'
        verbose_name_plural = 'Справочник видов спорта'
    def __str__(self):
        return self.sport_name


class DoctorsPositionQuide(models.Model):
    name = models.CharField(verbose_name='Должность', max_length=75, unique=True)

    class Meta:
        verbose_name = 'Справочник должностей докторов'
        verbose_name_plural = 'Справочник должностей докторов'

    def __str__(self):
        return self.name

class User(AbstractUser):
    patronymic = models.CharField(verbose_name='Oтчество', max_length=45, blank=False,)
    age = models.IntegerField(verbose_name='Возраст', null=True,)
    height = models.FloatField(verbose_name='Pост', null=True,)
    weight = models.FloatField(verbose_name='Bес', null=True,)
    gender_choises = (('Мужской','Мужской'),('Женский ','Женский'))
    gender = models.CharField(verbose_name='Пол', choices=gender_choises, max_length=15, default='Мужской', )
    phone = models.CharField(verbose_name='Телефон', null=True, max_length=13)
    sport = models.ForeignKey(SportQuide, related_name='user_sport_id', verbose_name='Вид спорта',
                              on_delete=models.CASCADE, default=SportQuide.objects.first().pk)
    photo = models.ImageField(verbose_name='Фото', upload_to='image/usr/%Y%m%d/', blank=True)
    position = models.ForeignKey(DoctorsPositionQuide, verbose_name='Должность', related_name='user_position_id',
                                on_delete=models.CASCADE, default=DoctorsPositionQuide.objects.first().pk)

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class ChemicalElementsMainQuide(models.Model):
    name = models.CharField(verbose_name='Название элемента', max_length=25, unique=True)
    data_min = models.FloatField(verbose_name='Недостаток',)
    data_max = models.FloatField(verbose_name='Избыток', )
    discription = models.CharField(verbose_name='Описание элемента', max_length=50, )
    must_not_contain = models.CharField(verbose_name='Не должен содержаться', max_length=50, blank=True)
    url1 = models.URLField(verbose_name='Сслылка на производителя товаров 1', blank=True)
    url2 = models.URLField(verbose_name='Сслылка на производителя товаров 2', blank=True)
    required = models.BooleanField(verbose_name='Обязательное?', default=True,)
    size_choises = (('мг', 'мг'),('мкг/г','мкг/г'),('мкг/г','мкг/г'),('мкг','мкг'),)
    size = models.CharField(verbose_name='Мера измерения', choices=size_choises, max_length=10, blank=True)

    class Meta:
        verbose_name = 'Справочник химических элементов в биологическом материал'
        verbose_name_plural = 'Справочник химических элементов в биологическом материал'

    def __str__(self):
        return self.name


class RecomendationsQuide(models.Model):
    name = models.CharField(verbose_name='Название', max_length=25, blank=False, )
    discription = models.TextField(verbose_name='Описание', )
    patient = models.ForeignKey(User, verbose_name='Пациент', related_name='recomendation_pathient_id',
                                on_delete=models.CASCADE, null=True, )
    author = models.ForeignKey(User, verbose_name='Автор', related_name='recomendation_author_id',
                               on_delete=models.CASCADE, null=True, )
    creation_date = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    attach = models.ManyToManyField(ChemicalElementsMainQuide, verbose_name='Химические элементы',
                                    related_name='recomendation_attach_id', blank=True)
    type_choises = (('Рекомендация', 'Рекомендация'), ('Пишевая рекомендация', 'Пишевая рекомендация'),
                    ('Пишевая рекомендация(Справочник)', 'Пишевая рекомендация(Справочник)'),)
    type = models.CharField(verbose_name='', max_length=40, choices=type_choises, )

    class Meta:
        verbose_name = 'Рекомендации'
        verbose_name_plural = 'Рекомендации'

    def __str__(self):
        return self.name


class PatirntAnalizler(models.Model):
    creation_date = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    patient = models.ForeignKey(User, verbose_name='Пациент', related_name='analizer_pathient_id',
                                on_delete=models.CASCADE, null=True, )
    eliment = models.ForeignKey(ChemicalElementsMainQuide, verbose_name='Химический элемент',
                                related_name='analizer_element_id', on_delete=models.CASCADE, )
    rezult = models.FloatField(verbose_name='Результат анализа')

    class Meta:
        verbose_name = 'Результаты анализа'
        verbose_name_plural = 'Результаты анализа'

    def __str__(self):
        return str(self.eliment)
