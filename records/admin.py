from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

class MyAdminSite(admin.AdminSite):

    def index(self, request, extra_context=None):
        if not request.user.is_authenticated:
            # ログインしていない場合はログインページにリダイレクト
            return HttpResponseRedirect(reverse('admin:login'))
        else:
            # ログインしている場合はホーム画面にリダイレクト
            return HttpResponseRedirect(reverse('admin:upload_pdf'))