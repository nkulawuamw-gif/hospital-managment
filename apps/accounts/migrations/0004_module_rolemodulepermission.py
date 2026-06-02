from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_historicaluser_department_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('codename', models.CharField(max_length=50, unique=True)),
                ('icon', models.CharField(default='bi bi-circle', max_length=50)),
                ('url_name', models.CharField(blank=True, max_length=200)),
                ('section', models.CharField(max_length=50)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'modules',
                'ordering': ['section', 'order'],
            },
        ),
        migrations.CreateModel(
            name='RoleModulePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('super_admin', 'Super Admin'), ('hospital_admin', 'Hospital Administrator'), ('doctor', 'Doctor'), ('nurse', 'Nurse'), ('receptionist', 'Receptionist'), ('pharmacist', 'Pharmacist'), ('lab_technician', 'Laboratory Technician'), ('cashier', 'Cashier'), ('accountant', 'Accountant'), ('patient', 'Patient')], max_length=20, unique=True)),
                ('modules', models.ManyToManyField(to='accounts.module')),
            ],
            options={
                'db_table': 'role_module_permissions',
                'verbose_name': 'Role Module Permission',
            },
        ),
    ]
