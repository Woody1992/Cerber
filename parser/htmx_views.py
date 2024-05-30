import random

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from parser.forms import InstagramAccountForm
from parser.models import InstagramAccount, ParserRun, ParserRunFactory


class HtmxView(View):

    def get_instagram_list(self, target='#instagram_account_list'):
        accounts = InstagramAccount.objects.all().order_by('status', '-created_at')
        context = {
            'accounts': accounts,
        }
        resp = render(self.request, 'htmx_components/instagram_account_list.html', context)
        resp['Hx-Retarget'] = target
        return resp


class HtmxInstagramAccountsCreate(HtmxView):

    def get(self, request, *args, **kwargs):
        return render(request, 'htmx_components/instagram_account_form.html')

    def post(self, request, *args, **kwargs):
        print("In post view: ", request.headers)
        form = InstagramAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "added successfully")
            return self.get_instagram_list()
        messages.error(request, "Something went wrong")

        return HttpResponse(render(request, 'htmx_components/instagram_account_form.html', status=300))


class HtmxInstagramAccounts(HtmxView):
    def get(self, request, *args, **kwargs):
        accounts = InstagramAccount.objects.all().order_by('status', '-created_at')
        context = {
            'accounts': accounts,
        }
        return render(request, 'htmx_components/instagram_account_list.html', context)


class HtmxInstagramAccountsDetail(HtmxView):
    def get(self, request, pk, *args, **kwargs):
        account = InstagramAccount.objects.get(id=pk)
        context = {
            'account': account,
        }
        return render(request, 'htmx_components/edit_from_insta_accaunt.html', context)

    def post(self, request, pk, *args, **kwargs):
        account = InstagramAccount.objects.get(id=pk)
        form = InstagramAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully")
            return self.get_instagram_list()
        messages.error(request, "Something went wrong")
        return HttpResponse()

    def delete(self, request, pk, *args, **kwargs):
        InstagramAccount.objects.get(id=pk).delete()
        messages.success(request, "Deleted Successfully")
        return self.get_instagram_list()


class TimelineView(View):
    def get(self, request, *args, **kwargs):
        runs = ParserRun.objects.all()
        # ParserRunFactory().gen_test_data()
        _groups = set([i.worker_id for i in runs])
        colors = [
            "#e64a94", "#10d9b5", "#d6410e", "#99fa4c", "#a7e97d", "#37232b",
            "#e2a6bc", "#386eee", "#560627", "#1c5928", "#981abe", "#535e3d", "#7ede00", "#642a40", "#3e108b", "#086aea",
            "#cf5da7", "#e85e51", "#942469", "#f519d3", "#acc089", "#4c8001", "#f707d1", "#47141f", "#e9e6af",
            "#2b5ea5", "#1a9a9c", "#95bde2", "#20a61d",
        ]
        random.shuffle(colors)
        group_color_map = {g: colors[i] for i, g in enumerate(_groups)}
        timelines = [{
            **r.timeline, "style": f"background-color: {group_color_map[r.timeline['group']]};"
        } for r in runs]
        groups = [{
            "id": r, "content": r, "style": f"background-color: {group_color_map[r]};"
        } for r in _groups]
        return JsonResponse({
            "data": timelines,
            "groups": groups,
        })
