from django.shortcuts import redirect, get_object_or_404
from functools import wraps

from analizes.models import User


def doctor_check(user):
    return user.groups.get().name == 'doctors'

def admin_check(user):
    return user.groups.get().name == 'admins'

def patients_check(user):
    return user.groups.get().name == 'patients'

def is_anonymous(user):
    return user.is_anonymous

def is_autor_or_doctor(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
      if not User.objects.filter(pk=kwargs['pk']).exists() or not request.user.is_authenticated:
          return redirect('analizes_urls:main_page_url')
      else:
          if get_object_or_404(User, pk=kwargs['pk']).groups.get().name != 'patients':
              return redirect('analizes_urls:main_page_url')
          if request.user.groups.get().name != 'doctors':
              if kwargs['pk'] != str(request.user.pk):
                  return redirect('analizes_urls:main_page_url')
          return function(request, *args, **kwargs)

  return wrap

