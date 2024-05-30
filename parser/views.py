from django.shortcuts import render
from django.views import View
from parser.models import InstagramAccount, ACCOUNT_STATUS

class HomePageView(View):
    def get(self, request, *args, **kwargs):

        accounts = InstagramAccount.objects.all().order_by('status', '-created_at')

        available_accounts = accounts.filter(in_use=False, status="active")
        context = {
            'accounts': accounts,
            'available_accounts': available_accounts,
        }
        return render(request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        return render(request, 'home.html')

