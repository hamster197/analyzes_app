from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from extra_views import ModelFormSetView
from analizes.decorators import *
from django.views.generic import TemplateView, CreateView, FormView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from analizes.forms import *
from django.contrib.auth.models import Group

admin_decorators = [login_required, user_passes_test(admin_check)]
doctor_decorators = [login_required, user_passes_test(doctor_check)]
patients_decorators = [login_required, user_passes_test(patients_check)]

# Create your views here.

class MainPage(TemplateView):
    template_name = 'analizes/main_page.html'

@method_decorator(user_passes_test(is_anonymous), name='dispatch')
class RegisterPage(CreateView):
    template_name = 'analizes/patient_register.html'
    form_class = PathientRegisterForm
    success_url = reverse_lazy('analizes_urls:main_page_url')

    def form_valid(self, form):
        self.object = form.save()
        self.object.groups.add(Group.objects.get(name='patients'))
        self.object.is_active = True
        return super().form_valid(form)

@method_decorator(user_passes_test(is_anonymous), name='dispatch')
class LoginPage(LoginView):
    template_name = 'analizes/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        if self.request.user.groups.get().name == 'admins':
            return reverse_lazy('analizes_urls:admin_chemical_elements_edit_url')
        if self.request.user.groups.get().name == 'doctors':
            return reverse_lazy('analizes_urls:doctor_patinets_list_url')
        if self.request.user.groups.get().name == 'patients':
            return reverse_lazy('analizes_urls:patinet_account_url', kwargs={'pk': self.request.user.pk})

@method_decorator(admin_decorators, name='dispatch')
class AdminChemicalElementsMainQuideEdit(ModelFormSetView):
    template_name = 'analizes/admin_chemical_elements_edit.html'
    model = ChemicalElementsMainQuide
    exclude = ['rezult', ]
    success_url = reverse_lazy('analizes_urls:admin_chemical_elements_edit_url')

@method_decorator(admin_decorators, name='dispatch')
class AdminPatientsList(ListView):
    queryset = User.objects.filter(groups__name='patients', )
    template_name = 'analizes/admin_patient_list.html'
    context_object_name = 'patients'

@method_decorator(admin_decorators, name='dispatch')
class AdminPatientEdit(UpdateView):
    template_name = 'analizes/admin_patient_edit.html'
    form_class = PathientEditForm
    queryset = User.objects.filter(groups__name='patients')

    def get_success_url(self,):
        return reverse_lazy('analizes_urls:admin_patient_edit_url', kwargs = {'pk': self.kwargs['pk']})

@method_decorator(admin_decorators, name='dispatch')
class DoctorsList(ListView):
    queryset = User.objects.filter(groups__name='doctors', )
    template_name = 'analizes/admin_doctors_list.html'
    context_object_name = 'doctors'

@method_decorator(admin_decorators, name='dispatch')
class DoctorNew(CreateView):
    form_class = DoctorNewForm
    template_name = 'analizes/admin_patient_edit.html'
    success_url = reverse_lazy('analizes_urls:admin_doctors_list_url')

    def form_valid(self, form):
        self.object = form.save()
        self.object.groups.add(Group.objects.get(name='doctors'))
        self.object.is_active = True
        return super().form_valid(form)

@method_decorator(admin_decorators, name='dispatch')
class DoctorEdit(TemplateView):
    template_name = 'analizes/admin_doctor_edit.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorEdit, self).get_context_data(**kwargs)
        user = get_object_or_404(User, id=int(self.kwargs['pk']), groups__name='doctors',)
        context['profile_form'] = DoctorEditForm(instance=user)
        context['password_form'] = PswChangeForm(get_object_or_404(User, id=int(self.kwargs['pk'])))
        return context

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=int(self.kwargs['pk']), groups__name='doctors',)
        if '_save_profile' in request.POST:
            profile_form = DoctorEditForm(request.POST, instance=user)
            password_form = PswChangeForm(user,)
            if profile_form.is_valid():
                profile_form.save()
        if '_save_new_password' in request.POST:
            password_form = PswChangeForm(user, self.request.POST)
            profile_form = DoctorEditForm(instance=user)
            if password_form.is_valid():
                password_form.save()

        return self.render_to_response({'profile_form':profile_form, 'password_form':password_form})

@method_decorator(admin_decorators, name='dispatch')
class DoctorDelete(DeleteView):
    queryset = User.objects.filter(groups__name='doctors',)
    template_name = 'analizes/admin_doctor_delete.html'
    success_url = reverse_lazy('analizes_urls:admin_doctors_list_url')
    context_object_name = 'doctor'

@method_decorator(admin_decorators, name='dispatch')
class RecomendationsQuideList(ListView):
    template_name = 'analizes/admin_recomendations_list.html'
    context_object_name = 'recomendations'
    queryset = RecomendationsQuide.objects.filter(type='Пишевая рекомендация(Справочник)')

@method_decorator(admin_decorators, name='dispatch')
class RecomendationNew(CreateView):
    template_name = 'analizes/admin_recomendations_new.html'
    model = RecomendationsQuide
    form_class = RecmendationEdit
    success_url = reverse_lazy('analizes_urls:admin_recomendations_list_url')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.type = 'Пишевая рекомендация(Справочник)'
        return super().form_valid(form)

@method_decorator(admin_decorators, name='dispatch')
class RecomendationEdit(UpdateView):
    template_name = 'analizes/admin_recomendations_new.html'
    queryset = RecomendationsQuide.objects.filter(author__groups__name='admins')
    form_class = RecmendationEdit
    success_url = reverse_lazy('analizes_urls:admin_recomendations_list_url')

@method_decorator(admin_decorators, name='dispatch')
class RecomendetionDelete(DeleteView):
    queryset = RecomendationsQuide.objects.filter(author__groups__name='admins')
    template_name = 'analizes/admin_doctor_delete.html'
    success_url = reverse_lazy('analizes_urls:admin_recomendations_list_url')
    context_object_name = 'recomendation'

@method_decorator(doctor_decorators, name='dispatch')
class DoctorPatientsList(ListView):
    queryset = User.objects.filter(groups__name='patients')
    template_name = 'analizes/admin_patient_list.html'
    context_object_name = 'patients'

@method_decorator(is_autor_or_doctor, name='dispatch')
class PatientAccount(TemplateView):
    template_name = 'analizes/pathient_account.html'

    def get_context_data(self, **kwargs):
        context = super(PatientAccount, self).get_context_data()
        context['patient'] = get_object_or_404(User, pk=self.kwargs['pk'])
        context['recomendations'] = RecomendationsQuide.objects.filter(patient=context['patient']).order_by(
            '-creation_date')
        return context

@method_decorator(doctor_decorators, name='post')
class PatientAccountForm(FormView, PatientAccount):
    template_name = 'analizes/pathient_account.html'

    def get_form(self, form_class=None):
        if str(self.kwargs['idd']) == '1':
            form_class = RecomendationForm
        elif str(self.kwargs['idd']) == '2':
            form_class = RecomendationFoodForm
        elif str(self.kwargs['idd']) == '3':
            form_class = RecomendationFoodQuideForm
        else:
            return reverse_lazy('analizes_urls:patinet_account_form_index_url', kwargs={'pk': self.kwargs['pk']})

        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        patient = get_object_or_404(User, pk=self.kwargs['pk'])
        request = self.request
        if str(self.kwargs['idd']) != '3':
            new_recomendation = form.save(commit=True)
            new_recomendation.patient = patient
            new_recomendation.author = request.user
            if str(self.kwargs['idd']) == '1':
                new_recomendation.type = 'Рекомендация'
            else:
                new_recomendation.type = 'Пишевая рекомендация'
            new_recomendation.save()
        else:
            new_recomendation = get_object_or_404(RecomendationsQuide, name=form.cleaned_data['name'])
            recomendation = RecomendationsQuide.objects.create(discription=new_recomendation.discription,
                                                               patient=patient, author=request.user,
                                                               type='Пишевая рекомендация(Справочник)',
                                                               )
            recomendation.attach.set(new_recomendation.attach.all())

        return super(PatientAccountForm, self).form_valid(form)

    def get_success_url(self,):
            return reverse_lazy('analizes_urls:patinet_account_form_index_url', kwargs={'pk': self.kwargs['pk']})


@method_decorator(is_autor_or_doctor, name='dispatch')
@method_decorator(doctor_decorators, name='post')
class PatientAnalizesFormsetExample(ModelFormSetView, ):
    template_name = 'analizes/pathient_analizes.html'
    model = ChemicalElementsMainQuide
    form_class = ChemicalElementsForm
    factory_kwargs = {'extra': 0, 'max_num': None,
                      'can_order': False, 'can_delete': False}


    def get_context_data(self, **kwargs):
        context = super(PatientAnalizesFormsetExample, self).get_context_data(formset=self.get_formset())
        context['analizes'] = PatirntAnalizler.objects.filter(patient__pk=self.kwargs['pk']).order_by('-pk')
        return context

    def formset_valid(self, formset):
        new_analize_instances = []
        for form in formset:
            rezult = form.cleaned_data['rezult']
            if rezult is not None:
                element = get_object_or_404(ChemicalElementsMainQuide, name=form.cleaned_data['name'])
                new_analize = PatirntAnalizler(patient_id=self.kwargs['pk'], eliment=element,
                                           rezult=rezult)

                new_analize_instances.append(new_analize)
        PatirntAnalizler.objects.bulk_create(new_analize_instances)

        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_success_url(self,):
            return reverse('analizes_urls:patinet_analize_formset_example_url', kwargs={'pk': self.kwargs['pk']})