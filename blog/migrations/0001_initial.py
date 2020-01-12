# Generated by Django 2.1.1 on 2019-12-10 14:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.City')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('crimetype1', models.CharField(choices=[('White-Collar Crime', 'White-Collar Crime'), ('Robbery', 'Robbery'), ('Rape', 'Rape'), ('Assualt', 'Assault'), ('Arson', 'Arson'), ('Homicide', 'Homicide'), ('Crimes Against Morality', 'Crimes Against Morality'), ('Illegal goods', 'Illegal goods'), ('Poaching and Illegal Felling', 'Poaching and Illegal Felling'), ('Adultery in Food Sector', 'Adultery in Food Sector'), ('Ill-treatment of Workers', 'Ill-treatment of Workers'), ('Tax Evasion', 'Tax Evasion'), ('Sexual Harrassment', 'Sexual Harrassment'), ('Communal Crimes', 'Communal Crimes')], default='not provided', max_length=100, null=True)),
                ('crimetype2', models.CharField(choices=[('None', 'None'), ('White-Collar Crime', 'White-Collar Crime'), ('Robbery', 'Robbery'), ('Rape', 'Rape'), ('Assualt', 'Assault'), ('Arson', 'Arson'), ('Homicide', 'Homicide'), ('Crimes Against Morality', 'Crimes Against Morality'), ('Illegal goods', 'Illegal goods'), ('Poaching and Illegal Felling', 'Poaching and Illegal Felling'), ('Adultery in Food Sector', 'Adultery in Food Sector'), ('Ill-treatment of Workers', 'Ill-treatment of Workers'), ('Tax Evasion', 'Tax Evasion'), ('Sexual Harrassment', 'Sexual Harrassment'), ('Communal Crimes', 'Communal Crimes')], default=None, max_length=100, null=True)),
                ('crimetype3', models.CharField(choices=[('None', 'None'), ('White-Collar Crime', 'White-Collar Crime'), ('Robbery', 'Robbery'), ('Rape', 'Rape'), ('Assualt', 'Assault'), ('Arson', 'Arson'), ('Homicide', 'Homicide'), ('Crimes Against Morality', 'Crimes Against Morality'), ('Illegal goods', 'Illegal goods'), ('Poaching and Illegal Felling', 'Poaching and Illegal Felling'), ('Adultery in Food Sector', 'Adultery in Food Sector'), ('Ill-treatment of Workers', 'Ill-treatment of Workers'), ('Tax Evasion', 'Tax Evasion'), ('Sexual Harrassment', 'Sexual Harrassment'), ('Communal Crimes', 'Communal Crimes')], default=None, max_length=100, null=True)),
                ('crimetype4', models.CharField(choices=[('None', 'None'), ('White-Collar Crime', 'White-Collar Crime'), ('Robbery', 'Robbery'), ('Rape', 'Rape'), ('Assualt', 'Assault'), ('Arson', 'Arson'), ('Homicide', 'Homicide'), ('Crimes Against Morality', 'Crimes Against Morality'), ('Illegal goods', 'Illegal goods'), ('Poaching and Illegal Felling', 'Poaching and Illegal Felling'), ('Adultery in Food Sector', 'Adultery in Food Sector'), ('Ill-treatment of Workers', 'Ill-treatment of Workers'), ('Tax Evasion', 'Tax Evasion'), ('Sexual Harrassment', 'Sexual Harrassment'), ('Communal Crimes', 'Communal Crimes')], default=None, max_length=100, null=True)),
                ('authority', models.CharField(default='Incometax Department', max_length=10000)),
                ('location', models.TextField(max_length=60)),
                ('content', models.TextField(max_length=300)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('country', models.CharField(default='India', max_length=20)),
                ('tags', models.CharField(default='None', max_length=1000)),
                ('pincode', models.CharField(default='000000', max_length=6, validators=[django.core.validators.MinLengthValidator(6)], verbose_name='Pincode')),
                ('photo1', models.ImageField(blank='True', upload_to='post_pics')),
                ('photo2', models.ImageField(blank='True', upload_to='post_pics')),
                ('photo3', models.ImageField(blank='True', upload_to='post_pics')),
                ('photo4', models.ImageField(blank='True', upload_to='post_pics')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.City')),
                ('downvotes', models.ManyToManyField(blank=True, related_name='downvotes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='registerCamera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=60)),
                ('pincode', models.CharField(max_length=6, validators=[django.core.validators.MinLengthValidator(6)], verbose_name='Pincode')),
                ('state', models.CharField(choices=[('Select State', 'Select State'), ('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh ', 'Arunachal Pradesh '), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jammu and Kashmir ', 'Jammu and Kashmir '), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal'), ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'), ('Chandigarh', 'Chandigarh'), ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'), ('Daman and Diu', 'Daman and Diu'), ('Lakshadweep', 'Lakshadweep'), ('National Capital Territory of Delhi', 'National Capital Territory of Delhi'), ('Puducherry', 'Puducherry')], default='not provided', max_length=100)),
                ('city', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.State'),
        ),
        migrations.AddField(
            model_name='post',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='upvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.State'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Post'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.State'),
        ),
    ]
