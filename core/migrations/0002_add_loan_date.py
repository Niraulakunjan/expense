from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='loan',
            name='loan_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
