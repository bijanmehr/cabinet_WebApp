# Generated by Django 2.0.3 on 2019-09-04 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('control_start_manual', models.CharField(max_length=4096)),
            ],
        ),
        migrations.RenameModel(
            old_name='command',
            new_name='ParrotCommand',
        ),
        migrations.AlterField(
            model_name='stage',
            name='name',
            field=models.CharField(choices=[('GAME_STAGE', 'game'), ('WHEEL_STAGE', 'Wheel'), ('PARROT_STAGE', 'parrot'), ('DONE', 'done')], default='GAME_STAGE', max_length=2),
        ),
    ]
