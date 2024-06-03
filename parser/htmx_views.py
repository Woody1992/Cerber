import json

from django.contrib import messages
from django.contrib.messages import get_messages
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import action

from parser.forms import InstagramAccountForm
from parser.models import InstagramAccount, ParserRun, AccountStatistics


class HtmxView(View):

    def get_instagram_list(self, target='#instagram_account_list'):
        accounts = InstagramAccount.objects.all().order_by(
            'status', '-created_at'
        ).annotate(videos_parsed=Sum('statistics__parser_videos_amount'))
        context = {
            'accounts': accounts,
        }
        for acc in accounts:
            print("-->", acc.videos_parsed)
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
        accounts = InstagramAccount.objects.all().order_by('status', '-created_at').order_by(
            'status', '-created_at'
        ).annotate(videos_parsed=Coalesce(Sum('statistics__parser_videos_amount'), 0))
        context = {
            'accounts': accounts,
        }
        for acc in accounts:
            print("-->", acc.videos_parsed)
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
        _groups = set([i.worker_id for i in runs])
        timelines = [{**r.timeline} for r in runs]
        groups = [{"id": r, "content": r} for r in _groups]
        return JsonResponse(
            {
                "items": timelines,
                "groups": groups,
            }
        )


class AccountStatisticViewSet(viewsets.GenericViewSet):

    @action(detail=True, methods=['get'], url_path='account', url_name='account-stats')
    def account_stats(self, request, pk, *args, **kwargs):
        stats = AccountStatistics.objects.filter(
            account_id=pk
        ).select_related("run", "account").order_by("run__start_time")
        if not stats:
            messages.warning(request, "No data found")

            resp = JsonResponse(None, safe=False)
            msg = [{"message": m.message, "tags": m.tags} for m in get_messages(request)]
            hx_trigger = {"messages": msg}
            resp.headers["HX-Trigger"] = json.dumps(hx_trigger)

            return resp

        stats_dict = {
            "username": stats[0].account.username,
            "chartData": [
                {
                    "label": f"{i.run.end_time.strftime('%d %b %y')}",
                    "data": i.parser_videos_amount,
                    "run_id": i.run_id,
                } for i in stats
            ]
        }
        return JsonResponse(stats_dict, safe=False)

