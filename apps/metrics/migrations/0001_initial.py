from django.db import migrations, models

STAT_CARDS = [
    {
        'title':        'Atmospheric CO2',
        'value':        '~424 ppm',
        'context':      'As of 2024, atmospheric CO2 is the highest in at least 800,000 years of ice-core records.',
        'source_name':  'NOAA Global Monitoring Laboratory',
        'source_url':   'https://gml.noaa.gov/ccgg/trends/',
        'display_order': 1,
    },
    {
        'title':        'Global Temperature Anomaly',
        'value':        '+1.2 - 1.5 C',
        'context':      'Global average surface temperature has risen roughly 1.2-1.5 C above pre-industrial levels.',
        'source_name':  'NASA GISS / Berkeley Earth',
        'source_url':   'https://climate.nasa.gov/vital-signs/global-temperature/',
        'display_order': 2,
    },
    {
        'title':        'Sea Level Rise (since 1993)',
        'value':        '+100 mm',
        'context':      'Global mean sea level has risen approximately 100 mm since satellite altimetry began in 1993.',
        'source_name':  'NASA Sea Level Change',
        'source_url':   'https://sealevel.nasa.gov/',
        'display_order': 3,
    },
    {
        'title':        'Arctic Sea Ice Decline',
        'value':        '-13% / decade',
        'context':      'September Arctic sea ice extent is declining at roughly 13% per decade relative to the 1981-2010 average.',
        'source_name':  'NSIDC',
        'source_url':   'https://nsidc.org/arcticseaicenews/',
        'display_order': 4,
    },
    {
        'title':        'Ocean Heat Content',
        'value':        'Record highs (2023-2024)',
        'context':      'The ocean has absorbed over 90% of excess heat from human-caused warming. Ocean heat content set consecutive records in 2023 and 2024.',
        'source_name':  'NOAA / Cheng et al.',
        'source_url':   'https://www.ncei.noaa.gov/access/global-ocean-heat-content/',
        'display_order': 5,
    },
    {
        'title':        'Coral Reef Bleaching (2023-2024)',
        'value':        '4th global event',
        'context':      'NOAA confirmed the 4th global coral bleaching event in 2024, affecting reefs across all ocean basins.',
        'source_name':  'NOAA Coral Reef Watch',
        'source_url':   'https://coralreefwatch.noaa.gov/',
        'display_order': 6,
    },
]

METRICS = [
    {
        'slug':        'global_co2_concentration',
        'name':        'Global Atmospheric CO2 Concentration',
        'metric_type': 'co2_emissions',
        'unit':        'ppm',
        'description': 'Annual mean atmospheric CO2 concentration at Mauna Loa Observatory.',
        'source_name': 'NOAA / Scripps Institution of Oceanography',
        'source_url':  'https://gml.noaa.gov/ccgg/trends/',
        'data': [
            (1960, 316.9), (1970, 325.7), (1980, 338.7),
            (1990, 354.4), (2000, 369.5), (2010, 389.9),
            (2015, 400.8), (2020, 412.5), (2023, 419.3), (2024, 424.0),
        ],
    },
    {
        'slug':        'global_temperature_anomaly',
        'name':        'Global Surface Temperature Anomaly',
        'metric_type': 'temperature_anomaly',
        'unit':        'C',
        'description': 'Global mean surface temperature anomaly relative to 1951-1980 baseline.',
        'source_name': 'NASA GISS',
        'source_url':  'https://climate.nasa.gov/vital-signs/global-temperature/',
        'data': [
            (1960, -0.01), (1970, 0.03), (1980, 0.26),
            (1990, 0.44),  (2000, 0.41), (2010, 0.72),
            (2015, 0.87),  (2020, 1.02), (2023, 1.17), (2024, 1.29),
        ],
    },
]


def seed_metrics(apps, schema_editor):
    StatisticCard    = apps.get_model('metrics', 'StatisticCard')
    ClimateMetric    = apps.get_model('metrics', 'ClimateMetric')
    MetricDataPoint  = apps.get_model('metrics', 'MetricDataPoint')

    for card in STAT_CARDS:
        StatisticCard.objects.get_or_create(title=card['title'], defaults={**card, 'is_active': True})

    for m in METRICS:
        data = m.pop('data')
        metric, _ = ClimateMetric.objects.get_or_create(slug=m['slug'], defaults=m)
        for year, value in data:
            MetricDataPoint.objects.get_or_create(metric=metric, year=year, defaults={'value': value})


def unseed_metrics(apps, schema_editor):
    StatisticCard = apps.get_model('metrics', 'StatisticCard')
    ClimateMetric = apps.get_model('metrics', 'ClimateMetric')
    StatisticCard.objects.filter(title__in=[c['title'] for c in STAT_CARDS]).delete()
    ClimateMetric.objects.filter(slug__in=[m['slug'] for m in METRICS]).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        # Schema 
        migrations.CreateModel(
            name='ClimateMetric',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug',         models.SlugField(unique=True)),
                ('name',         models.CharField(max_length=150)),
                ('metric_type',  models.CharField(max_length=50)),
                ('unit',         models.CharField(max_length=50)),
                ('description',  models.TextField(blank=True)),
                ('source_name',  models.CharField(max_length=200, blank=True)),
                ('source_url',   models.URLField(max_length=500, blank=True)),
                ('last_updated', models.DateField(null=True, blank=True)),
            ],
            options={'ordering': ['metric_type', 'name']},
        ),
        migrations.CreateModel(
            name='MetricDataPoint',
            fields=[
                ('id',    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year',  models.IntegerField()),
                ('value', models.FloatField()),
                ('note',  models.CharField(max_length=200, blank=True)),
                ('metric', models.ForeignKey(on_delete=models.CASCADE, related_name='data_points', to='metrics.climatemetric')),
            ],
            options={'ordering': ['year']},
        ),
        migrations.AddConstraint(
            model_name='metricdatapoint',
            constraint=models.UniqueConstraint(fields=['metric', 'year'], name='unique_metric_year'),
        ),
        migrations.CreateModel(
            name='StatisticCard',
            fields=[
                ('id',            models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title',         models.CharField(max_length=150)),
                ('value',         models.CharField(max_length=100)),
                ('context',       models.TextField()),
                ('source_name',   models.CharField(max_length=200, blank=True)),
                ('source_url',    models.URLField(max_length=500, blank=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('is_active',     models.BooleanField(default=True)),
            ],
            options={'ordering': ['display_order']},
        ),
        #  Seed data 
        migrations.RunPython(seed_metrics, reverse_code=unseed_metrics),
    ]
