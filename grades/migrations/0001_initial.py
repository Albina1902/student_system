from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '__first__'),
        ('courses', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('value', models.IntegerField(
                    choices=[(5, '5 — Отлично'), (4, '4 — Хорошо'), (3, '3 — Удовл.'), (2, '2 — Неудовл.')],
                    validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(5)],
                    verbose_name='Оценка'
                )),
                ('date', models.DateField(verbose_name='Дата')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='courses.course', verbose_name='Курс')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='students.student', verbose_name='Студент')),
            ],
            options={'verbose_name': 'Оценка', 'verbose_name_plural': 'Оценки', 'ordering': ['-date']},
        ),
    ]
