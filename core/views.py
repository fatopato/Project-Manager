from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView, DeleteView
from .forms import UserProfileForm
from django.core.exceptions import PermissionDenied

from .forms import SignUpForm

DEVELOPER = "Developer"
ANALYST = "Analyst"
PM = "ProjectManager"


class StaffAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return is_project_manager(self.request.user) or is_admin(self.request.user)


class AnalystRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return is_project_manager(self.request.user) or is_admin(self.request.user) or is_analyst(self.request.user)


class DeveloperRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return is_project_manager(self.request.user) or is_admin(self.request.user) or is_developer(self.request.user)


class MemberRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return (is_project_manager(self.request.user) or is_admin(self.request.user) or is_developer(self.request.user)
                or is_analyst(self.request.user))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    pass
    # if created:
    #     instance.groups.add(Group.objects.get(name=ANALYST))


@user_passes_test(lambda u: u.is_superuser or is_project_manager(u))
def create_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('core:users')
    else:
        form = SignUpForm()
    return render(request, 'user_edit.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'logout.html')


def is_project_manager(user):
    return user.groups.filter(name=PM).exists()


def is_analyst(user):
    return user.groups.filter(name=ANALYST).exists()


def is_developer(user):
    return user.groups.filter(name=DEVELOPER).exists()


def is_admin(user):
    return user.is_superuser


@method_decorator(login_required, name='dispatch')
class UserListView(StaffAdminRequiredMixin, ListView):
    model = User
    paginate_by = 10
    template_name = "user_list.html"

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context["users"] = User.objects.filter(is_superuser=False)
        return context

class UserProfileUpdateView(StaffAdminRequiredMixin, UpdateView):
    model = User
    template_name = "user_edit.html"

    def get_initial(self):
        initial = super(UserProfileUpdateView, self).get_initial()
        try:
            current_group = self.object.groups.get()
        except:
            # exception can occur if the edited user has no groups
            # or has more than one group
            pass
        else:
            initial['group'] = current_group.pk
        return initial

    def get_form_class(self):
        return UserProfileForm

    def form_valid(self, form):
        if self.object.is_superuser:
            raise PermissionDenied
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data['group'])
        return super(UserProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('core:users')


class UserProfileCreateView(StaffAdminRequiredMixin, CreateView):
    model = User
    template_name = "user_edit.html"

    def get_form_class(self):
        return UserProfileForm

    def form_valid(self, form):
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data['group'])
        return super(UserProfileCreateView, self).form_valid(form)
