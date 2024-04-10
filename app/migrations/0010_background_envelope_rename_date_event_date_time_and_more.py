# Generated by Django 4.2.11 on 2024-03-17 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_guest_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_bg', models.CharField(max_length=50)),
                ('pattern_bg', models.FilePathField(path='backgrounds')),
            ],
        ),
        migrations.CreateModel(
            name='Envelope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_env', models.CharField(max_length=50)),
                ('pattern_env', models.FilePathField(path='envelopes')),
            ],
        ),
        migrations.RenameField(
            model_name='event',
            old_name='date',
            new_name='date_time',
        ),
        migrations.RenameField(
            model_name='invitation',
            old_name='image',
            new_name='card',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='confirmation_date',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='confirmed',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='name',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='sent_at',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='invitation',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='invitation',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guest',
            name='first_name',
            field=models.CharField(default='jacob', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guest',
            name='history',
            field=models.JSONField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guest',
            name='last_name',
            field=models.CharField(default='Khalili', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guest',
            name='rsvp',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='background',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.background'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invitation',
            name='envelope',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.envelope'),
            preserve_default=False,
        ),
    ]