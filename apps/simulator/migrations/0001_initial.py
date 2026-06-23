from django.db import migrations, models
import django.db.models.deletion

SCENARIOS = [
    {
        'slug': 'business_as_usual',
        'name': 'Business as Usual',
        'description': 'High emissions, slow policy, moderate misinformation. Represents a trajectory without meaningful climate action.',
        'is_featured': True,
        'default_misinformation': 70,
        'default_media_literacy': 30,
        'default_public_trust':   35,
        'default_policy_speed':   20,
        'default_emissions':      80,
        'default_resilience':     30,
    },
    {
        'slug': 'accelerated_action',
        'name': 'Accelerated Action',
        'description': 'Strong policy, high media literacy, low misinformation. Represents a society mobilising effectively.',
        'is_featured': True,
        'default_misinformation': 20,
        'default_media_literacy': 80,
        'default_public_trust':   75,
        'default_policy_speed':   85,
        'default_emissions':      25,
        'default_resilience':     70,
    },
    {
        'slug': 'misinformation_crisis',
        'name': 'Misinformation Crisis',
        'description': 'Rampant misinformation collapses public trust and stalls policy even as emissions stay moderate.',
        'is_featured': True,
        'default_misinformation': 95,
        'default_media_literacy': 15,
        'default_public_trust':   20,
        'default_policy_speed':   25,
        'default_emissions':      55,
        'default_resilience':     40,
    },
    {
        'slug': 'resilient_communities',
        'name': 'Resilient Communities',
        'description': 'Moderate emissions and trust but very high ecosystem and social resilience - explores buffer capacity.',
        'is_featured': False,
        'default_misinformation': 40,
        'default_media_literacy': 60,
        'default_public_trust':   55,
        'default_policy_speed':   50,
        'default_emissions':      50,
        'default_resilience':     90,
    },
]


def seed_scenarios(apps, schema_editor):
    SimulationScenario = apps.get_model('simulator', 'SimulationScenario')
    for s in SCENARIOS:
        SimulationScenario.objects.get_or_create(slug=s['slug'], defaults=s)


def unseed_scenarios(apps, schema_editor):
    SimulationScenario = apps.get_model('simulator', 'SimulationScenario')
    SimulationScenario.objects.filter(slug__in=[s['slug'] for s in SCENARIOS]).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tipping_points', '0002_seed_tipping_points'),
    ]

    operations = [
        # --- Schema ---
        migrations.CreateModel(
            name='SimulationScenario',
            fields=[
                ('id',                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',                  models.CharField(max_length=150, unique=True)),
                ('slug',                  models.SlugField(unique=True)),
                ('description',           models.TextField()),
                ('is_featured',           models.BooleanField(default=False)),
                ('default_misinformation',models.IntegerField(default=50)),
                ('default_media_literacy',models.IntegerField(default=50)),
                ('default_public_trust',  models.IntegerField(default=50)),
                ('default_policy_speed',  models.IntegerField(default=50)),
                ('default_emissions',     models.IntegerField(default=50)),
                ('default_resilience',    models.IntegerField(default=50)),
                ('created_at',            models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-is_featured', 'name']},
        ),
        migrations.CreateModel(
            name='SimulationRun',
            fields=[
                ('id',              models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key',     models.CharField(max_length=40, blank=True)),
                ('misinformation',  models.IntegerField()),
                ('media_literacy',  models.IntegerField()),
                ('public_trust',    models.IntegerField()),
                ('policy_speed',    models.IntegerField()),
                ('emissions',       models.IntegerField()),
                ('resilience',      models.IntegerField()),
                ('trust_score',     models.FloatField()),
                ('delay_risk',      models.FloatField()),
                ('climate_pressure',models.FloatField()),
                ('narrative',       models.TextField(blank=True)),
                ('created_at',      models.DateTimeField(auto_now_add=True)),
                ('scenario', models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='runs', to='simulator.simulationscenario')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ActivatedNode',
            fields=[
                ('id',               models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_score', models.FloatField()),
                ('triggered_by',     models.CharField(max_length=200, blank=True)),
                ('run',           models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activated_nodes', to='simulator.simulationrun')),
                ('tipping_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tipping_points.tippingpoint')),
            ],
            options={'ordering': ['-activation_score']},
        ),
        # --- Seed data ---
        migrations.RunPython(seed_scenarios, reverse_code=unseed_scenarios),
    ]
