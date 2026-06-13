from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '__first__'),
        ('groups', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание задания')),
                ('due_date', models.DateField(verbose_name='Срок сдачи')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='courses.course', verbose_name='Курс')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='groups.group', verbose_name='Группа')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Создал')),
            ],
            options={'verbose_name': 'Домашнее задание', 'verbose_name_plural': 'Домашние задания', 'ordering': ['-due_date']},
        ),
        migrations.CreateModel(
            name='AIExplanation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('question', models.TextField(verbose_name='Вопрос студента')),
                ('answer', models.TextField(verbose_name='Ответ AI')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='explanations', to='homework.homework')),
            ],
            options={'verbose_name': 'Объяснение AI', 'verbose_name_plural': 'Объяснения AI', 'ordering': ['-created_at']},
        ),
    ]
