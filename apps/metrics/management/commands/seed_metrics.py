"""
python manage.py seed_metrics

Seeds:
  - StatisticCard   : headline dashboard numbers
  - ClimateMetric   : named time-series (placeholder data; swap in real API data later)
  - SimulationScenario : preset slider configurations
"""

from django.core.management.base import BaseCommand
from apps.metrics.models import StatisticCard, ClimateMetric, MetricDataPoint
from apps.simulator.models import SimulationScenario


STAT_CARDS = [
    {
        'title': 'Atmospheric CO₂',
        'value': '~424 ppm',
        'context': 'As of 2024, atmospheric CO₂ is the highest in at least 800,000 years of ice-core records.',
        'source_name': 'NOAA Global Monitoring Laboratory',
        'source_url':  'https://gml.noaa.gov/ccgg/trends/',
        'display_order': 1,
    },
    {
        'title': 'Global Temperature Anomaly',
        'value': '+1.2 – 1.5 °C',
        'context': 'Global average surface temperature has risen roughly 1.2–1.5 °C above pre-industrial levels.',
        'source_name': 'NASA GISS / Berkeley Earth',
        'source_url':  'https://climate.nasa.gov/vital-signs/global-temperature/',
        'display_order': 2,
    },
    {
        'title': 'Sea Level Rise (since 1993)',
        'value': '+100 mm',
        'context': 'Global mean sea level has risen approximately 100 mm since satellite altimetry began in 1993.',
        'source_name': 'NASA Sea Level Change',
        'source_url':  'https://sealevel.nasa.gov/',
        'display_order': 3,
    },
    {
        'title': 'Arctic Sea Ice Decline',
        'value': '−13% / decade',
        'context': 'September Arctic sea ice extent is declining at roughly 13% per decade relative to the 1981–2010 average.',
        'source_name': 'NSIDC',
        'source_url':  'https://nsidc.org/arcticseaicenews/',
        'display_order': 4,
    },
    {
        'title': 'Ocean Heat Content',
        'value': 'Record highs (2023–2024)',
        'context': 'The ocean has absorbed over 90% of excess heat from human-caused warming. Ocean heat content set consecutive records in 2023 and 2024.',
        'source_name': 'NOAA / Cheng et al.',
        'source_url':  'https://www.ncei.noaa.gov/access/global-ocean-heat-content/',
        'display_order': 5,
    },
    {
        'title': 'Coral Reef Bleaching (2023–2024)',
        'value': '4th global event',
        'context': 'NOAA confirmed the 4th global coral bleaching event in 2024, affecting reefs across all ocean basins.',
        'source_name': 'NOAA Coral Reef Watch',
        'source_url':  'https://coralreefwatch.noaa.gov/',
        'display_order': 6,
    },
]


# Placeholder CO₂ time series (replace with Our World in Data / NOAA API import)
CO2_DATA = [
    (1960, 316.9), (1970, 325.7), (1980, 338.7),
    (1990, 354.4), (2000, 369.5), (2010, 389.9),
    (2015, 400.8), (2020, 412.5), (2023, 419.3), (2024, 424.0),
]

# Placeholder temperature anomaly (replace with NASA GISS import)
TEMP_DATA = [
    (1960, -0.01), (1970, 0.03), (1980, 0.26),
    (1990, 0.44),  (2000, 0.41), (2010, 0.72),
    (2015, 0.87),  (2020, 1.02), (2023, 1.17), (2024, 1.29),
]

METRICS = [
    {
        'slug': 'global_co2_concentration',
        'name': 'Global Atmospheric CO₂ Concentration',
        'metric_type': 'co2_emissions',
        'unit': 'ppm',
        'description': 'Annual mean atmospheric CO₂ concentration at Mauna Loa Observatory.',
        'source_name': 'NOAA / Scripps Institution of Oceanography',
        'source_url': 'https://gml.noaa.gov/ccgg/trends/',
        'data': CO2_DATA,
    },
    {
        'slug': 'global_temperature_anomaly',
        'name': 'Global Surface Temperature Anomaly',
        'metric_type': 'temperature_anomaly',
        'unit': '°C',
        'description': 'Global mean surface temperature anomaly relative to 1951–1980 baseline.',
        'source_name': 'NASA GISS',
        'source_url': 'https://climate.nasa.gov/vital-signs/global-temperature/',
        'data': TEMP_DATA,
    },
]

SCENARIOS = [
    {
        'slug': 'business_as_usual',
        'name': 'Business as Usual',
        'description': 'High emissions, slow policy, moderate misinformation. Represents a trajectory without meaningful climate action.',
        'is_featured': True,
        'defaults': {'misinformation': 70, 'media_literacy': 30, 'public_trust': 35, 'policy_speed': 20, 'emissions': 80, 'resilience': 30},
    },
    {
        'slug': 'accelerated_action',
        'name': 'Accelerated Action',
        'description': 'Strong policy, high media literacy, low misinformation. Represents a society mobilising effectively.',
        'is_featured': True,
        'defaults': {'misinformation': 20, 'media_literacy': 80, 'public_trust': 75, 'policy_speed': 85, 'emissions': 25, 'resilience': 70},
    },
    {
        'slug': 'misinformation_crisis',
        'name': 'Misinformation Crisis',
        'description': 'Rampant misinformation collapses public trust and stalls policy even as emissions stay moderate.',
        'is_featured': True,
        'defaults': {'misinformation': 95, 'media_literacy': 15, 'public_trust': 20, 'policy_speed': 25, 'emissions': 55, 'resilience': 40},
    },
    {
        'slug': 'resilient_communities',
        'name': 'Resilient Communities',
        'description': 'Moderate emissions and trust but very high ecosystem and social resilience — explores buffer capacity.',
        'is_featured': False,
        'defaults': {'misinformation': 40, 'media_literacy': 60, 'public_trust': 55, 'policy_speed': 50, 'emissions': 50, 'resilience': 90},
    },
]


class Command(BaseCommand):
    help = 'Seed StatisticCards, ClimateMetrics, and SimulationScenarios'

    def handle(self, *args, **options):
        # Stat cards
        for card in STAT_CARDS:
            StatisticCard.objects.update_or_create(
                title=card['title'], defaults=card
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(STAT_CARDS)} stat cards.'))

        # Metrics + data points
        for m in METRICS:
            data = m.pop('data')
            metric, _ = ClimateMetric.objects.update_or_create(slug=m['slug'], defaults=m)
            for year, value in data:
                MetricDataPoint.objects.update_or_create(
                    metric=metric, year=year, defaults={'value': value}
                )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(METRICS)} metrics.'))

        # Simulation scenarios
        for s in SCENARIOS:
            defaults_inner = s.pop('defaults')
            s.update({
                'default_misinformation': defaults_inner['misinformation'],
                'default_media_literacy': defaults_inner['media_literacy'],
                'default_public_trust':   defaults_inner['public_trust'],
                'default_policy_speed':   defaults_inner['policy_speed'],
                'default_emissions':      defaults_inner['emissions'],
                'default_resilience':     defaults_inner['resilience'],
            })
            SimulationScenario.objects.update_or_create(slug=s['slug'], defaults=s)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(SCENARIOS)} simulation scenarios.'))
