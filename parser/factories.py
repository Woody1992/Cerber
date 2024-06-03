from datetime import datetime, timedelta, date
import random
import factory
from faker import Faker

from parser.models import ParserRun, InstagramAccount, AccountStatistics
from zoneinfo import ZoneInfo

faker = Faker()


class InstagramAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "parser.InstagramAccount"

    username = factory.Faker("name")
    password = factory.Faker("password")
    status = "active"
    banned_at = None


class ParserRunFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "parser.ParserRun"

    start_time = date.today() + timedelta(days=random.randint(-3, 3))

    # Generate a random end date from start_date + 1 day to start_date + 2 days
    end_time = start_time + timedelta(days=random.randint(1, 2))

    worker_id = random.choice(['worker_1', 'worker_2', 'worker_3', 'worker_3'])


    @factory.post_generation
    def status(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        if extracted:
            self.status = extracted
        else:
            self.status = self.calc_status()

    @factory.post_generation
    def accounts(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        if extracted:
            for account in extracted:
                self.accounts.add(account)
        else:
            InstagramAccountFactory().create_batch(5, parser_run=self)
            accounts = InstagramAccountFactory().create_batch(5)
            for account in accounts:
                self.accounts.add(account)


class AccountStatisticsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "parser.AccountStatistics"

    parser_videos_amount = factory.Faker("random_int", min=0, max=100)


class AccountWithRunStatisticsFactory:

    @classmethod
    def create(cls, **kwargs):
        accounts = kwargs.pop("accounts", None) or InstagramAccountFactory.create_batch(5)
        parser_run = kwargs.pop("parser_runs", None) or ParserRunFactory.create(accounts=accounts)
        for account in accounts:
            AccountStatisticsFactory.create(account=account, run=parser_run)

    @classmethod
    def create_batch(cls, size, **kwargs):
        for _ in range(size):
            cls.create(**kwargs)

    @classmethod
    def rand(cls, remove=False):
        if remove:
            InstagramAccount.objects.all().delete()
            ParserRun.objects.all().delete()
            AccountStatistics.objects.all().delete()
        accounts = InstagramAccountFactory.create_batch(50)
        accounts = random.sample(accounts, 10)
        runs = [
            {
                "accounts": random.sample(accounts, 10),
                "start_time": datetime(2024, 6, 1, 0, 0, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "end_time": datetime(2024, 6, 1, 11, 59, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "worker_id": "worker_1",
            },
            {
                "accounts": random.sample(accounts, 10),
                "start_time": datetime(2024, 6, 1, 12, 0, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "end_time": datetime(2024, 6, 1, 23, 59, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "worker_id": "worker_2",
                "amount": random.randint(1, 200)
            },
            {
                "accounts": random.sample(accounts, 10),
                "start_time": datetime(2024, 6, 2, 0, 0, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "end_time": datetime(2024, 6, 2, 23, 59, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "worker_id": "worker_2",
                "amount": random.randint(1, 200)
            },
            {
                "accounts": random.sample(accounts, 10),
                "start_time": datetime(2024, 6, 2, 12, 0, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "end_time": datetime(2024, 6, 2, 23, 59, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "worker_id": "worker_3",
                "amount": random.randint(1, 200)
            },
            {
                "accounts": random.sample(accounts, 10),
                "start_time": datetime(2024, 6, 2, 0, 0, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "end_time": datetime(2024, 6, 2, 11, 59, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "worker_id": "worker_3",
                "amount": random.randint(1, 200)
            },
            {
                "accounts": random.sample(accounts, 10),
                "start_time": datetime(2024, 6, 3, 0, 0, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "end_time": datetime(2024, 6, 3, 11, 59, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "worker_id": "worker_4",
                "amount": random.randint(1, 200)
            },
            {
                "accounts": random.sample(accounts, 10),
                "start_time": datetime(2024, 6, 2, 0, 0, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "end_time": datetime(2024, 6, 2, 11, 59, 0, tzinfo=ZoneInfo("Europe/Kiev")),
                "worker_id": "worker_4",
                "amount": random.randint(1, 200)
            }
        ]

        for _run in runs:
            run = ParserRun.objects.create(
                start_time=_run["start_time"]+timedelta(1),
                end_time=_run["end_time"]+timedelta(1),
                worker_id=_run["worker_id"]
            )
            print(run.__dict__)
            run.accounts.add(*_run["accounts"])
            for account in run.accounts.all():
                AccountStatisticsFactory.create(
                    account=account,
                    run=run,
                    parser_videos_amount=_run.get("amount", 0)
                )
