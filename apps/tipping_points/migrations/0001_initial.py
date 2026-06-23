from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TippingPoint',
            fields=[
                ('id',                   models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug',                 models.SlugField(unique=True, max_length=100, help_text='URL-safe identifier')),
                ('name',                 models.CharField(max_length=200)),
                ('domain',               models.CharField(max_length=100)),
                ('domain_raw',           models.CharField(max_length=150, blank=True)),
                ('scale',                models.CharField(max_length=100)),
                ('icon_label',           models.CharField(max_length=100, blank=True)),
                ('severity',             models.CharField(max_length=50)),
                ('near_term_status',     models.TextField()),
                ('warming_context',      models.TextField()),
                ('primary_causes',       models.TextField()),
                ('effects',              models.TextField()),
                ('interactions',         models.TextField()),
                ('domino_summary',       models.TextField()),
                ('app_card_summary',     models.TextField()),
                ('misinformation_angle', models.TextField()),
                ('suggested_ui',         models.TextField(blank=True)),
                ('source_urls',          models.TextField(blank=True)),
                ('display_order',        models.PositiveIntegerField(default=0)),
                ('is_active',            models.BooleanField(default=True)),
                ('created_at',           models.DateTimeField(auto_now_add=True)),
                ('updated_at',           models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['display_order', 'name'], 'verbose_name': 'Tipping Point', 'verbose_name_plural': 'Tipping Points'},
        ),
        migrations.CreateModel(
            name='TippingPointRelationship',
            fields=[
                ('id',                models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_type', models.CharField(max_length=100)),
                ('description',       models.TextField(blank=True)),
                ('strength',          models.IntegerField(default=1)),
                ('is_bidirectional',  models.BooleanField(default=False)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_relationships', to='tipping_points.tippingpoint')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_relationships', to='tipping_points.tippingpoint')),
            ],
            options={'verbose_name': 'Tipping Point Relationship', 'verbose_name_plural': 'Tipping Point Relationships'},
        ),
        migrations.AddConstraint(
            model_name='tippingpointrelationship',
            constraint=models.UniqueConstraint(fields=['source', 'target', 'relationship_type'], name='unique_tp_relationship'),
        ),
        migrations.CreateModel(
            name='SourceReference',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url',          models.URLField(max_length=500)),
                ('title',        models.CharField(max_length=300, blank=True)),
                ('notes',        models.TextField(blank=True)),
                ('tipping_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_references', to='tipping_points.tippingpoint')),
            ],
            options={'ordering': ['id'], 'verbose_name': 'Source Reference', 'verbose_name_plural': 'Source References'},
        ),
    ]
