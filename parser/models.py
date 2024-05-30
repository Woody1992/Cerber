import time
import random
from datetime import date, datetime

from django.db import models


ACCOUNT_STATUS = (
    ('active', 'Активний'),
    ('inactive', 'Неактивний'),
    ('banned', 'Заблокований'),
)

class InstagramAccount(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=ACCOUNT_STATUS, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    in_use = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Інстаграм Аккаунт"
        verbose_name_plural = "Інстаграм Аккаунты"


PARSER_RUN_STATES = (
    ('active', 'Активний'),
    ('pending', 'Запланований'),
    ('completed', 'Завершений'),
    ('failed', 'Помилка'),
)


class ParserRun(models.Model):
    accounts = models.ManyToManyField(InstagramAccount, related_name='parser_runs')
    created_at = models.DateTimeField(auto_now_add=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=PARSER_RUN_STATES, default='pending')
    errors = models.JSONField(null=True, blank=True)
    parsed_video_amount = models.PositiveIntegerField(default=0)
    worker_id = models.CharField(max_length=100, null=True, blank=True)

    def get_date_timeline(self) -> tuple[date, date]:
        """
        Get the date timeline of the parser run (without time)
        :return: tuple of start and end date
        """
        start_date = self.start_time.date() if self.start_time else None
        end_date = self.end_time.date() if self.end_time else None
        return start_date, end_date

    @property
    def timeline(self):
        """
        Get the timeline dict for vis.js
        structure:
            start: new Date(2010, 7, 15),
            end: new Date(2010, 8, 2),  // end is optional
            content: 'Trajectory A'
        Optional fields:
            id
            type
            group
            className
            style
        :return: dict with start and end time
        """
        start_date, end_date = self.get_date_timeline()
        return {
            "start":  start_date,
            "end": end_date,
            "content": f"Run {self.id}",
            "id": self.id,
            "group": self.worker_id,
        }


class ParserRunFactory:

    def gen_test_data(self):
        ParserRun.objects.all().delete()
        data = [
            {
                "accounts": [self.gen_account() for _ in range(5)],
                "start_time": datetime(2024, 5, 29, 0, 0, 0),
                "end_time": datetime(2024, 5, 30, 0, 0, 0),
                "worker_id": "worker_1",
            },
            {
                "accounts": [self.gen_account() for _ in range(5)],
                "start_time": datetime(2024, 5, 30, 0, 0, 0),
                "end_time": datetime(2024, 5, 31, 0, 0, 0),
                "worker_id": "worker_1",
            },
            {
                "accounts": [self.gen_account() for _ in range(5)],
                "start_time": datetime(2024, 5, 28, 0, 0, 0),
                "end_time": datetime(2024, 5, 30, 0, 0, 0),
                "worker_id": "worker_2",
            },
            {
                "accounts": [self.gen_account() for _ in range(5)],
                "start_time": datetime(2024, 5, 31, 0, 0, 0),
                "end_time": datetime(2024, 6, 1, 0, 0, 0),
                "worker_id": "worker_2",
            },
            {
                "accounts": [self.gen_account() for _ in range(5)],
                "start_time": datetime(2024, 5, 29, 0, 0, 0),
                "end_time": datetime(2024, 5, 30, 0, 0, 0),
                "worker_id": "worker_3",
            },
            {
                "accounts": [self.gen_account() for _ in range(5)],
                "start_time": datetime(2024, 5, 30, 0, 0, 0),
                "end_time": datetime(2024, 5, 31, 0, 0, 0),
                "worker_id": "worker_3",
            },
            {
                "accounts": [self.gen_account() for _ in range(5)],
                "start_time": datetime(2024, 5, 30, 0, 0, 0),
                "end_time": datetime(2024, 5, 31, 0, 0, 0),
                "worker_id": "worker_4",
            },
            {
                "accounts": [self.gen_account() for _ in range(5)],
                "start_time": datetime(2024, 6, 1, 0, 0, 0),
                "end_time": datetime(2024, 6, 2, 0, 0, 0),
                "worker_id": "worker_4",
            },
        ]
        for d in data:
            run = ParserRun.objects.create(
                start_time=d["start_time"],
                end_time=d["end_time"],
                worker_id=d["worker_id"],
            )
            run.accounts.add(*d["accounts"])
        return data


    def gen_account(self):
        return InstagramAccount.objects.create(
            username=f"test_user_{random.randint(1, 100)}",
            password="test_password",
            status="active",
        )

    def str_time_prop(self, start, end, time_format, prop):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formatted in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """

        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(time_format, time.localtime(ptime))

    def random_date(self, start, end, prop=random.random()):
        return self.str_time_prop(start, end, "%Y-%m-%d%H:%M:%S", prop)
