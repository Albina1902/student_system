from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '__first__'),
        ('courses', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')], verbose_name='День недели')),
                ('time_start', models.TimeField(verbose_name='Начало')),
                ('time_end', models.TimeField(verbose_name='Конец')),
                ('room', models.CharField(max_length=50, verbose_name='Аудитория')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='courses.course', verbose_name='Курс')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='groups.group', verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Расписание',
                'ordering': ['day_of_week', 'time_start'],
            },
        ),
    ]
