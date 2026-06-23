from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tipping_points', '0002_seed_tipping_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimTopic',
            fields=[
                ('id',          models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',        models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='MisinformationTechnique',
            fields=[
                ('id',                  models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug',                models.SlugField(unique=True)),
                ('name',                models.CharField(max_length=100)),
                ('technique',           models.CharField(max_length=60, blank=True)),
                ('description',         models.TextField()),
                ('example',             models.TextField()),
                ('media_literacy_tip',  models.TextField()),
                ('flicc_category',      models.CharField(max_length=100, blank=True)),
            ],
            options={'ordering': ['name'], 'verbose_name': 'Misinformation Technique', 'verbose_name_plural': 'Misinformation Techniques'},
        ),
        migrations.CreateModel(
            name='ClimateClaim',
            fields=[
                ('id',             models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_text',     models.TextField()),
                ('label',          models.CharField(max_length=20)),
                ('explanation',    models.TextField(blank=True)),
                ('difficulty',     models.CharField(max_length=20, default='medium')),
                ('source_dataset', models.CharField(max_length=100, blank=True)),
                ('source_id',      models.CharField(max_length=100, blank=True)),
                ('is_active',      models.BooleanField(default=True)),
                ('created_at',     models.DateTimeField(auto_now_add=True)),
                ('topic', models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='claims', to='claims.claimtopic')),
                ('related_tipping_points', models.ManyToManyField(blank=True, related_name='related_claims', to='tipping_points.tippingpoint')),
            ],
            options={'ordering': ['id'], 'verbose_name': 'Climate Claim', 'verbose_name_plural': 'Climate Claims'},
        ),
        migrations.CreateModel(
            name='ClaimTechniqueLink',
            fields=[
                ('id',        models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes',     models.TextField(blank=True)),
                ('claim',     models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='claims.climateclaim')),
                ('technique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='claims.misinformationtechnique')),
            ],
        ),
        migrations.AddConstraint(
            model_name='claimtechniquelink',
            constraint=models.UniqueConstraint(fields=['claim', 'technique'], name='unique_claim_technique'),
        ),
        migrations.CreateModel(
            name='EvidenceSentence',
            fields=[
                ('id',          models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text',        models.TextField()),
                ('stance',      models.CharField(max_length=20)),
                ('source_name', models.CharField(max_length=255, blank=True)),
                ('source_url',  models.URLField(max_length=500, blank=True)),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidence', to='claims.climateclaim')),
            ],
            options={'ordering': ['id'], 'verbose_name': 'Evidence Sentence', 'verbose_name_plural': 'Evidence Sentences'},
        ),
    ]
