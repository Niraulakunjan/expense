from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_loan_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'Cash'), ('ESEWA', 'eSewa'), ('KHALTI', 'Khalti'), ('SIDDHARTH_QR', 'Siddharth Bank (QR)'), ('GLOBAL_IME_QR', 'Global IME Bank (QR)'), ('CONNECT_IPS', 'Connect IPS'), ('OTHER', 'Other')], default='CASH', max_length=20),
        ),
        migrations.AddField(
            model_name='income',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'Cash'), ('ESEWA', 'eSewa'), ('KHALTI', 'Khalti'), ('SIDDHARTH_QR', 'Siddharth Bank (QR)'), ('GLOBAL_IME_QR', 'Global IME Bank (QR)'), ('CONNECT_IPS', 'Connect IPS'), ('OTHER', 'Other')], default='CASH', max_length=20),
        ),
    ]
