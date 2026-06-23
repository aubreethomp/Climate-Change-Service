from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tipping_points', '0002_seed_tipping_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tippingpoint',
            name='icon_emoji',
        ),
    ]