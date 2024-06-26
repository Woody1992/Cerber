# Generated by Django 5.0.6 on 2024-05-30 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0002_remove_instagramaccount_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParserRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('active', 'Активний'), ('pending', 'Запланований'), ('completed', 'Завершений'), ('failed', 'Помилка')], default='pending', max_length=10)),
                ('errors', models.JSONField()),
                ('parsed_video_amount', models.PositiveIntegerField(default=0)),
                ('worker_id', models.CharField(blank=True, max_length=100, null=True)),
                ('accounts', models.ManyToManyField(related_name='parser_runs', to='parser.instagramaccount')),
            ],
        ),
    ]
