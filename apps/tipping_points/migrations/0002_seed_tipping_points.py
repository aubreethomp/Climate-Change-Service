"""
0002_seed_tipping_points.py

Data migration: inserts all 19 tipping points, their source references,
and 22 directed relationship edges.
Descriptions updated June 2026 drawing on:
  - Global Tipping Points Report 2023
  - IPCC AR6 WG1
  - Armstrong McKay et al. Science 2022
  - Carbon Brief, Yale E360, NASA, NOAA, ArcticInstitute
"""
from django.db import migrations

DOMAIN_MAP = {
    'Cryosphere':                    'cryosphere',
    'Cryosphere / Carbon cycle':     'cryosphere_carbon_cycle',
    'Biosphere / Ocean':             'biosphere_ocean',
    'Biosphere':                     'biosphere',
    'Ocean-atmosphere circulation':  'ocean_atmosphere_circulation',
    'Cryosphere / Ocean':            'cryosphere_ocean',
    'Cryosphere / Water systems':    'cryosphere_water',
    'Atmosphere / Hydrology':        'atmosphere_hydrology',
    'Biosphere / Hydrology':         'biosphere_hydrology',
    'Biosphere / Freshwater':        'biosphere_freshwater',
    'Biosphere / Food systems':      'biosphere_food',
    'Biosphere / Coastal systems':   'biosphere_coastal',
}

TIPPING_POINTS = [
    {
        'slug': 'gis_collapse',
        'name': 'Greenland Ice Sheet collapse',
        'domain_raw': 'Cryosphere',
        'scale': 'Global core',
        'icon_label': 'ice sheet',
        'severity': 'extreme',
        'near_term_status': 'Possible at current warming; risk locks in additional meters of sea-level rise with each increment of warming',
        'warming_context': (
            'The Greenland Ice Sheet holds enough water to raise global sea levels by approximately 7 meters if it melted entirely. '
            'Greenland is currently melting four times faster than it was in 2003 and accounts for roughly 20% of today\'s sea-level rise. '
            'Scientists estimate that sustaining current warming levels, even without further increases, is likely enough to commit '
            'the ice sheet to several meters of sea-level rise over centuries. A key study found that for every centimeter of global '
            'sea-level rise, an additional 6 million people are exposed to coastal flooding. At current trajectories, Greenland\'s melt '
            'alone could expose 100 million people to annual flooding by 2100. The tipping point is not a single dramatic moment; '
            'it is the point at which self-reinforcing melting becomes impossible to reverse even if we stop all emissions.'
        ),
        'primary_causes': (
            'Surface melting accelerated by Arctic warming (the Arctic warms 3-4 times faster than the global average); '
            'ice-albedo feedback (melting exposes darker ocean and rock that absorbs more heat than white ice); '
            'warm ocean currents eating the ice sheet from below; '
            'black carbon soot from wildfires darkening the ice surface; '
            'meltwater lakes forming on the surface and draining through the ice, lubricating its flow toward the sea.'
        ),
        'effects': (
            'Sea-level rise threatening coastal cities including Miami, Mumbai, Shanghai, Amsterdam, and New York; '
            'increased frequency and severity of coastal flooding for hundreds of millions of people; '
            'freshwater flooding of the North Atlantic slows the ocean circulation system that warms Europe; '
            'loss of traditional Inuit hunting grounds and food sources as sea ice disappears; '
            'navigation hazards from increased iceberg calving into shipping lanes; '
            'salinization of coastal agricultural land and freshwater aquifers worldwide.'
        ),
        'interactions': (
            'Meltwater flowing into the North Atlantic dilutes the salty, dense water that drives the AMOC ocean current, '
            'potentially triggering AMOC slowdown or collapse; '
            'ice loss exposes darker ocean water that absorbs more heat, amplifying warming in a feedback loop; '
            'sea-level rise compounds storm surge impacts during hurricanes and extreme weather events; '
            'loss of ice mass causes land beneath to rebound, creating local sea-level paradoxes and shipping hazards.'
        ),
        'domino_summary': (
            'Warming Arctic -> ice melts faster -> darker surface absorbs more heat -> '
            'more melting locked in -> freshwater floods North Atlantic -> '
            'ocean circulation weakens -> sea levels rise on US East Coast -> '
            'coastal cities face permanent flooding -> mass displacement begins.'
        ),
        'app_card_summary': (
            'Greenland holds enough ice to raise global sea levels by 7 meters. It is already melting four times faster '
            'than 20 years ago, and once enough ice is lost, the melting becomes self-sustaining regardless of what we do next.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "Ice sheets have always changed naturally, so this is nothing new." '
            'What to look for: current Greenland melt rates are unprecedented in at least 350 years of ice-core records, '
            'and the speed, not just the direction, of change is what makes it dangerous. '
            'Natural ice-age cycles operate over tens of thousands of years. Current change is happening in decades. '
            'Attribution science directly links accelerated melt to human-caused warming.'
        ),
        'source_urls': 'https://report-2023.global-tipping-points.org/summary-report/section-1/ | https://sealevel.nasa.gov/news/178/greenlands-rapid-melt-will-mean-more-flooding | https://www.pik-potsdam.de/en/news/latest-news/risk-of-passing-multiple-climate-tipping-points-escalates-above-1-5degc-global-warming',
        'display_order': 1,
    },
    {
        'slug': 'wais_collapse',
        'name': 'West Antarctic Ice Sheet collapse',
        'domain_raw': 'Cryosphere',
        'scale': 'Global core',
        'icon_label': 'glacier cliff',
        'severity': 'extreme',
        'near_term_status': 'Parts of West Antarctica may already be past a point of no return; collapse unfolds over centuries but commitment is now',
        'warming_context': (
            'The West Antarctic Ice Sheet is particularly vulnerable because most of it rests on bedrock that sits below sea level. '
            'Warm ocean water can reach underneath the ice and melt it from below, a process that is invisible from the surface '
            'and extremely difficult to reverse. The Thwaites Glacier alone, sometimes called the "Doomsday Glacier," '
            'holds enough ice to raise global sea levels by 65 centimeters. Under current climate trajectories reaching '
            '3°C of warming, the collapse of the West Antarctic Ice Sheet is considered likely, contributing multiple meters '
            'of sea-level rise over the following centuries.'
        ),
        'primary_causes': (
            'Warm Circumpolar Deep Water intruding beneath ice shelves and melting them from below; '
            'marine ice-sheet instability: once the grounding line (where ice meets bedrock) retreats into deeper water, '
            'the ice sheet can collapse under its own weight in a self-reinforcing process; '
            'loss of buttressing ice shelves that hold back inland glaciers; '
            'atmospheric warming accelerating surface melt.'
        ),
        'effects': (
            'Multi-meter sea-level rise over centuries threatening every coastal city on Earth; '
            'permanent inundation of low-lying nations including Bangladesh, the Maldives, and Pacific island states; '
            'trillions of dollars of coastal infrastructure lost; '
            'forced migration of hundreds of millions of people from coastlines; '
            'compounding impacts with Greenland melt. Together the two ice sheets hold enough ice to raise seas by over 13 meters.'
        ),
        'interactions': (
            'Works in tandem with Greenland collapse to drive sea-level rise beyond what either would cause alone; '
            'meltwater affects Southern Ocean circulation and could release stored carbon from deep ocean; '
            'sea-level rise amplifies the destructive power of hurricanes, storm surges, and king tides; '
            'economic disruption from coastal loss can undermine the political capacity to fund climate adaptation.'
        ),
        'domino_summary': (
            'Warm ocean water reaches under ice -> ice shelf thins from below -> '
            'grounding line retreats into deeper water -> ice collapses under its own weight -> '
            'sea-level rise accelerates -> coastal cities flood -> '
            'mass displacement and economic shock cascade globally.'
        ),
        'app_card_summary': (
            'West Antarctica is melting from underneath. Warm ocean water is invisible until the damage is done. '
            'The Thwaites Glacier alone could raise seas by 65 cm, and parts of it may already be past the point of no return.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "Antarctic ice is growing, which cancels out Arctic losses." '
            'This conflates sea ice extent (which varies seasonally) with ice sheet mass. '
            'Satellite gravity measurements show Antarctica is losing mass overall, with West Antarctica accelerating. '
            'Snowfall gains in some interior regions do not offset ocean-driven melt losses at the margins.'
        ),
        'source_urls': 'https://report-2023.global-tipping-points.org/summary-report/section-1/ | https://www.carbonbrief.org/global-warming-above-1-5c-could-trigger-multiple-tipping-points/ | https://www.pik-potsdam.de/en/news/latest-news/risk-of-passing-multiple-climate-tipping-points-escalates-above-1-5degc-global-warming',
        'display_order': 2,
    },
    {
        'slug': 'east_antarctic_subglacial_basins',
        'name': 'East Antarctic subglacial basin ice loss',
        'domain_raw': 'Cryosphere',
        'scale': 'Global core',
        'icon_label': 'subglacial basin',
        'severity': 'extreme',
        'near_term_status': 'Lower near-term probability than West Antarctica, but the consequences if triggered would dwarf any other tipping point',
        'warming_context': (
            'East Antarctica is the largest ice sheet on Earth, holding enough ice to raise global sea levels by over 50 meters '
            'if it melted entirely. Several marine-based basins within East Antarctica, particularly the Wilkes and Aurora basins, '
            'rest on bedrock below sea level and face the same instability risks as West Antarctica. '
            'These basins become significantly more vulnerable at warming levels of 2-3°C and above, which current emissions '
            'trajectories put well within reach by late century. Even partial destabilization would commit the world to sea-level '
            'rise measured in meters over centuries.'
        ),
        'primary_causes': (
            'Warm ocean water intrusion into marine-based basins as Southern Ocean temperatures rise; '
            'loss of ice shelf buttressing that currently holds back inland ice; '
            'grounding-line retreat into deeper bedrock creating self-reinforcing instability; '
            'sustained high global temperatures over decades to centuries.'
        ),
        'effects': (
            'Potential sea-level rise of several meters to tens of meters over centuries, rendering most current coastal infrastructure obsolete; '
            'permanent reshaping of every coastline on Earth; '
            'forced abandonment of major port cities worldwide; '
            'global economic disruption on a scale that dwarfs any previous human crisis.'
        ),
        'interactions': (
            'Compounds with Greenland and West Antarctic collapse to drive compounding sea-level rise; '
            'meltwater affects deep ocean circulation and carbon uptake; '
            'destabilization risk increases if other tipping points are crossed first, raising global temperatures further.'
        ),
        'domino_summary': (
            'Sustained high warming -> ocean reaches subglacial basins -> '
            'grounding line retreats irreversibly -> slow but unstoppable ice loss -> '
            'meters of sea-level rise over centuries -> '
            'global coastline transformation -> no viable adaptation at scale.'
        ),
        'app_card_summary': (
            'East Antarctica is the sleeping giant of sea-level rise. Less likely to tip in the near term, '
            'but if it does, the consequences would reshape every coastline on Earth over the following centuries.'
        ),
        'misinformation_angle': (
            'Common confusion: "Low probability means we don\'t need to worry about it." '
            'In risk assessment, consequence matters as much as probability. A 10% chance of a catastrophic, '
            'irreversible outcome deserves serious attention, especially when the window to prevent it is closing. '
            'Media-literacy prompt: ask who benefits from framing low-probability, high-consequence risks as "not worth worrying about."'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://www.pik-potsdam.de/en/news/latest-news/risk-of-passing-multiple-climate-tipping-points-escalates-above-1-5degc-global-warming | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 3,
    },
    {
        'slug': 'abrupt_permafrost_thaw',
        'name': 'Abrupt permafrost thaw',
        'domain_raw': 'Cryosphere / Carbon cycle',
        'scale': 'Global core',
        'icon_label': 'thawing ground',
        'severity': 'high',
        'near_term_status': 'Already underway; abrupt thaw features forming 70 years ahead of model projections in some regions',
        'warming_context': (
            'Permafrost, the ground that stays frozen year-round, covers about 24% of the Northern Hemisphere\'s land surface '
            'and contains roughly twice as much carbon as is currently in the atmosphere. '
            'As temperatures rise, this ancient frozen carbon begins decomposing and releasing CO2 and methane. '
            'a greenhouse gas 30 times more potent than CO2 over a 100-year period. '
            'Scientists have documented over 40,000 abrupt thaw features across the Arctic, forming faster than expected. '
            'By end of century, permafrost emissions could be comparable to those of major emitting nations, '
            'consuming 25-40% of the remaining carbon budget to limit warming to 2°C.'
        ),
        'primary_causes': (
            'Arctic temperatures rising 3-4 times faster than the global average; '
            'thermokarst formation, where ground collapses as ice within soil melts, forming lakes and sinkholes; '
            'wildfire burning through peat layers and accelerating thaw; '
            'warming of deeper soil layers that have been frozen for thousands of years; '
            'rain-on-snow events replacing insulating snowpack with water.'
        ),
        'effects': (
            'Release of CO2 and methane that amplifies global warming in a self-reinforcing feedback loop; '
            'in Alaska, more than 144 communities face imminent displacement from thaw, flooding, or erosion; '
            'billions of dollars of infrastructure damage as roads buckle, buildings sink, and pipelines warp; '
            'disruption to Indigenous subsistence hunting and fishing as landscapes transform; '
            'landslides and rockfalls in mountain regions as frozen slopes destabilize; '
            'potential release of long-dormant pathogens frozen in ancient permafrost.'
        ),
        'interactions': (
            'Carbon release accelerates global warming, which thaws more permafrost, a dangerous feedback loop; '
            'wildfire scars remove insulating vegetation, deepening thaw in surrounding areas; '
            'methane released from thermokarst lakes is particularly potent; '
            'infrastructure collapse raises economic and social vulnerability in remote Arctic communities; '
            'interacts with boreal forest dieback; fires release carbon from both trees and the peat beneath them.'
        ),
        'domino_summary': (
            'Arctic warms faster than rest of planet -> frozen ground thaws -> '
            'ancient carbon decomposes and releases CO2 and methane -> '
            'warming accelerates -> more thaw -> '
            'ground collapses under roads, homes, and pipelines -> '
            '144+ communities threatened with displacement -> '
            'global carbon budget shrinks faster than planned.'
        ),
        'app_card_summary': (
            'Permafrost holds nearly twice the carbon currently in the atmosphere. '
            'As it thaws, it releases gases that cause more warming, which causes more thawing.'
            'and in Alaska alone, over 144 communities already face displacement from the collapsing ground beneath them.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "Permafrost carbon release is too small and too slow to matter." '
            'Reality: permafrost emissions alone could consume 25-40% of the remaining global carbon budget '
            'and are occurring 70 years ahead of model projections in some regions. '
            'Prompt users to distinguish between the annual flow of emissions (which seems small) '
            'and the total stock of carbon at risk (which is enormous and cumulative).'
        ),
        'source_urls': 'https://www.esri.com/about/newsroom/arcnews/mapping-permafrost-thaw-is-essential-for-understanding-climate-change | https://www.thearcticinstitute.org/thawing-grounds-rising-stakes-importance-including-permafrost-emissions-climate-policy/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 4,
    },
    {
        'slug': 'permafrost_yedoma_carbon',
        'name': 'Permafrost carbon-rich deposit collapse',
        'domain_raw': 'Cryosphere / Carbon cycle',
        'scale': 'Global core',
        'icon_label': 'carbon release',
        'severity': 'high',
        'near_term_status': 'A serious feedback risk at higher warming levels; not a sudden catastrophe but a slow amplifier with large cumulative impact',
        'warming_context': (
            'Yedoma is a type of permafrost found across vast areas of Siberia and Alaska that is exceptionally rich in '
            'organic carbon. It can contain up to 5% carbon by weight, compared to 1-2% in typical soils. '
            'Formed during the last ice age, Yedoma deposits can be 50 meters deep and store carbon that has been '
            'frozen for tens of thousands of years. When they thaw, microbial activity converts this ancient carbon '
            'into CO2 and methane at high rates. Researchers estimate Yedoma deposits alone could add 0.2-0.4°C '
            'to global warming over time, compounding other warming sources when the world can least afford it.'
        ),
        'primary_causes': (
            'Deep thaw driven by sustained high temperatures; '
            'thermokarst collapse, where ice-rich Yedoma soils are prone to dramatic ground subsidence when they thaw; '
            'wildfire burning through protective surface layers; '
            'erosion of Yedoma deposits by rivers and coastal waves releasing carbon directly into water.'
        ),
        'effects': (
            'Gradual but significant additional warming from CO2 and methane release; '
            'dramatic landscape transformation; ground can collapse by meters as ice-rich soils thaw; '
            'craters forming in Siberia from explosive methane release; '
            'disruption of Arctic ecosystems and the communities that depend on stable ground; '
            'compounding of other climate impacts by adding extra warming at a time when every fraction of a degree matters.'
        ),
        'interactions': (
            'Interacts with and amplifies abrupt permafrost thaw; '
            'additional warming from Yedoma carbon pushes other tipping systems closer to their thresholds; '
            'landscape collapse affects waterways, blocking or rerouting rivers and disrupting communities.'
        ),
        'domino_summary': (
            'Sustained deep warming -> ancient Yedoma ice melts -> '
            'ground collapses into thermokarst craters and lakes -> '
            'microbes decompose 10,000-year-old carbon -> '
            'CO2 and methane enter atmosphere -> '
            'global temperature rises an additional 0.2-0.4°C -> '
            'other tipping points move closer to activation.'
        ),
        'app_card_summary': (
            'Yedoma permafrost deposits in Siberia and Alaska are among the most carbon-rich soils on Earth, '
            'frozen for tens of thousands of years. As they thaw, the carbon they release adds extra warming '
            'on top of everything else, pushing other tipping points closer to their edge.'
        ),
        'misinformation_angle': (
            'Two opposite misleading framings exist: dismissing it as negligible, or exaggerating it as a '
            '"methane bomb" that will cause runaway warming overnight. Both are wrong. '
            'The real risk is serious but gradual: a meaningful amplifier of warming that makes other goals harder to achieve. '
            'Media-literacy prompt: watch for sources that either ignore feedbacks entirely or use apocalyptic framing '
            'that discourages action by making the problem feel hopeless.'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://www.smithsonianmag.com/smart-news/ticking-timebomb-siberia-thawing-permafrost-releases-more-methane-180978381/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 5,
    },
    {
        'slug': 'warm_water_coral_reefs_dieoff',
        'name': 'Warm-water coral reef die-off',
        'domain_raw': 'Biosphere / Ocean',
        'scale': 'Regional impact with global biodiversity importance',
        'icon_label': 'coral reef',
        'severity': 'extreme',
        'near_term_status': 'Earth has already passed its first confirmed climate tipping point: coral reefs. The 2024 event was the worst bleaching on record',
        'warming_context': (
            'Scientists confirmed in 2025 that Earth has officially crossed its first climate tipping point: '
            'the collapse of warm-water coral reefs. Marine heat waves hit 80% of the world\'s warm-water coral reefs in 2024, '
            'causing the fourth and worst global bleaching event on record. '
            'Coral reefs cover less than 1% of the ocean floor but support roughly 25% of all marine species '
            'and provide food, coastal protection, and livelihoods to over 500 million people. '
            'At 1.5°C of warming, scientists estimate a 99% chance that coral reefs will tip past their breaking point. '
            'We are currently at approximately 1.2-1.5°C and breached 1.5°C temporarily in 2024.'
        ),
        'primary_causes': (
            'Marine heatwaves driven by ocean warming; corals bleach when water temperatures exceed their tolerance '
            'by just 1°C for more than a few weeks; '
            'ocean acidification from CO2 absorption making it harder for corals to build their calcium carbonate skeletons; '
            'bleaching events now occurring every 5-6 years, faster than the 10-15 years reefs need to recover; '
            'local stressors including pollution, overfishing, and coastal development reducing resilience; '
            'coral disease outbreaks becoming more frequent in warmer waters.'
        ),
        'effects': (
            'Loss of habitat for 25% of all marine species; '
            'collapse of fisheries that 500 million people depend on for food and income; '
            'loss of natural coastal barriers that currently protect shorelines from storms and erosion,'
            'estimated value of reef storm protection exceeds $9 billion per year; '
            'tourism industry losses of billions of dollars annually in reef-dependent economies; '
            'cascading food insecurity in coastal nations across the Caribbean, Pacific, Southeast Asia, and East Africa.'
        ),
        'interactions': (
            'Reef collapse removes nursery habitat that fisheries across entire ocean regions depend on; '
            'dead reefs no longer buffer coastlines, amplifying sea-level rise and storm damage; '
            'biodiversity loss reduces the ocean\'s capacity to absorb carbon; '
            'reef die-off cascades into mangrove and seagrass loss as connected ecosystems degrade.'
        ),
        'domino_summary': (
            'Ocean absorbs excess heat -> marine heatwave forms -> '
            'corals expel symbiotic algae and turn white (bleaching) -> '
            'if heat persists more than 8-10 weeks, coral dies -> '
            'reef structure crumbles over years -> '
            'fish populations collapse -> '
            '500 million people lose food and income -> '
            'coastal communities lose storm protection -> '
            'flooding and displacement accelerate.'
        ),
        'app_card_summary': (
            'Earth has already crossed this tipping point. The 2024 mass bleaching event hit 80% of the world\'s '
            'warm-water reefs, the worst on record. Reefs support 25% of all marine species and the food security '
            'of 500 million people, and they are running out of time to recover between heatwaves.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "Reefs have bleached before and always bounced back." '
            'Recovery requires 10-15 years of stable, cooler temperatures. Bleaching events are now occurring '
            'every 5-6 years; reefs literally cannot recover fast enough. '
            'Also watch for claims that "some reefs are thriving," cherry-picking healthy patches '
            'ignores the collapse of the broader system.'
        ),
        'source_urls': 'https://www.sciencenews.org/article/coral-collapse-climate-tipping-point | https://global-tipping-points.org/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 6,
    },
    {
        'slug': 'amazon_rainforest_dieback',
        'name': 'Amazon rainforest dieback',
        'domain_raw': 'Biosphere',
        'scale': 'Global core',
        'icon_label': 'rainforest',
        'severity': 'extreme',
        'near_term_status': 'Early warning signals detected; 17-20% of the Amazon already deforested; scientists estimate 20-25% could trigger irreversible collapse',
        'warming_context': (
            'The Amazon rainforest is one of Earth\'s most critical climate regulators, storing 150-200 gigatonnes of carbon '
            'and recycling up to 50% of its own rainfall through transpiration, essentially creating its own weather. '
            'Roughly 17-20% of the Amazon has already been deforested since the 1970s. Scientists estimate that '
            'losing 20-25% of forest cover could trigger a self-reinforcing dieback: less forest means less rainfall, '
            'which means more forest dies, which means even less rainfall. '
            'The five Amazon nations that benefit most from Amazon rainfall generate 70% of their national income '
            'from agribusiness, hydropower, and industry that depends on that water.'
        ),
        'primary_causes': (
            'Deforestation for cattle ranching, soy farming, and logging (up to 20% already lost); '
            'climate change-driven droughts, including the extreme El Nino droughts of 2015-16 and 2023-24; '
            'wildfires deliberately set for land clearing that escape into forest; '
            'disruption of rainfall recycling as forest patches become too small to sustain their own moisture; '
            'edge effects, where fragmented forest edges are hotter and drier, making them more fire-prone.'
        ),
        'effects': (
            'Conversion of the world\'s largest rainforest into a drier savannah-like ecosystem; '
            'release of 150-200 gigatonnes of stored carbon, equivalent to decades of global emissions; '
            'permanent loss of 1 billion tonnes of CO2 absorption capacity per year; '
            'collapse of rainfall across South America affecting agricultural regions in Brazil, Argentina, and beyond; '
            'agricultural income losses of $1 billion or more per year as rainfall patterns change; '
            'extinction of an estimated 10% of all known species on Earth; the Amazon hosts 400 billion trees across 16,000 species; '
            'displacement of Indigenous communities who have lived in the forest for thousands of years.'
        ),
        'interactions': (
            'Reduced Amazon rainfall also affects the West African monsoon via Atlantic moisture patterns; '
            'AMOC weakening can reduce Amazon rainfall further by shifting the tropical rain belt; '
            'carbon release from Amazon dieback pushes other tipping systems closer; '
            'forest loss amplifies regional warming, stressing boreal forests further south.'
        ),
        'domino_summary': (
            'Deforestation removes trees that recycle rainfall -> '
            'rainfall decreases across the region -> '
            'remaining forest stressed by drought -> '
            'fire seasons become more extreme -> '
            'more forest dies -> forest turns to savannah -> '
            'Amazon releases stored carbon -> '
            'South American agriculture collapses -> '
            'global food prices spike -> '
            'millions displaced across the continent.'
        ),
        'app_card_summary': (
            'The Amazon creates its own rainfall; without enough trees, the rain stops. '
            'Up to 20% has already been deforested, and scientists warn that losing just 5% more '
            'could trigger an irreversible conversion of the world\'s largest rainforest into dry savannah, '
            'collapsing rainfall across an entire continent.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "CO2 fertilization will make the Amazon grow back stronger." '
            'CO2 does stimulate some plant growth in controlled conditions, but droughts, heat stress, '
            'wildfires, and deforestation outweigh this benefit in the real Amazon. '
            'Tree mortality rates are already increasing in the eastern Amazon as the region dries out. '
            'Prompt: what does the actual field data from the Amazon show, not greenhouse experiments?'
        ),
        'source_urls': 'https://report-2023.global-tipping-points.org/section2/2-tipping-point-impacts/2-2-assessing-impacts-of-earth-system-tipping-points-on-human-societies/2-2-3-impacts-of-biosphere-tipping-points/2-2-3-1-amazon-dieback/ | https://racetobelem.earth/amazon-forest-dieback-a-tipping-point/ | https://www.germanwatch.org/en/blog/human-security-impacts-crossing-amazon-rainforest-tipping-point',
        'display_order': 7,
    },
    {
        'slug': 'boreal_forest_southern_dieback',
        'name': 'Boreal forest southern dieback',
        'domain_raw': 'Biosphere',
        'scale': 'Global core / regional ecosystem',
        'icon_label': 'boreal forest',
        'severity': 'high',
        'near_term_status': 'Warming, drought, and pest outbreaks already driving accelerating tree mortality across southern boreal zones',
        'warming_context': (
            'The boreal forest, also called the taiga, is the world\'s largest land biome, '
            'stretching across Canada, Russia, Scandinavia, and Alaska. It stores an enormous amount of carbon '
            'in both its trees and the peat soils beneath them. As temperatures rise, the southern edges of the boreal '
            'are experiencing heat stress, drought, and bark beetle outbreaks that are killing trees faster than they can '
            'regrow. Massive wildfires are becoming more frequent. Canada\'s 2023 wildfire season alone burned an area '
            'larger than the UK, releasing more CO2 than the country typically emits in an entire year.'
        ),
        'primary_causes': (
            'Heat stress making southern boreal trees more vulnerable to drought and disease; '
            'bark beetle outbreaks, insects that thrive in warm winters and kill millions of trees; '
            'more frequent and intense wildfires burning through both forest and the deep peat beneath; '
            'drought reducing soil moisture and killing seedlings before they can establish; '
            'permafrost thaw destabilizing the waterlogged soils that some boreal species depend on.'
        ),
        'effects': (
            'Massive carbon release from burning forests and peat; Canada\'s 2023 fires alone released ~1.6 billion tonnes of CO2; '
            'air quality crises affecting millions of people across North America and Europe; '
            'loss of habitat for species including caribou, wolves, migratory birds, and pollinators; '
            'disruption of Indigenous communities whose culture and food systems depend on the forest; '
            'logging and forestry industry losses as tree mortality outpaces regeneration; '
            'peat drainage following fire converting carbon sinks into carbon sources.'
        ),
        'interactions': (
            'Burning peat releases ancient carbon stored for thousands of years, compounding permafrost thaw feedbacks; '
            'darker burnt areas absorb more heat, amplifying regional warming; '
            'tree mortality in southern zones does not simply shift northward; tundra ecosystems '
            'cannot quickly convert to forest, leaving a gap of degraded landscape; '
            'smoke from boreal fires deposits black carbon on Arctic snow and ice, accelerating melt.'
        ),
        'domino_summary': (
            'Warming and drought stress southern boreal trees -> '
            'bark beetles spread unchecked through mild winters -> '
            'millions of dead trees create fuel for fires -> '
            'mega-fires burn forest and peat -> '
            'carbon released equals entire national economies -> '
            'smoke pollutes cities hundreds of miles away -> '
            'surviving forest cannot regenerate in changed climate -> '
            'carbon sink becomes carbon source.'
        ),
        'app_card_summary': (
            'The world\'s largest forest is dying at its southern edges from heat, drought, and beetles. '
            'Canada\'s 2023 wildfire season, already worsening, released more CO2 than the entire country '
            'normally emits in a year, turning a carbon sink into a carbon source.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "Forests are expanding northward, so overall forest cover is increasing." '
            'Northern expansion into tundra takes decades or centuries and stores far less carbon '
            'than mature southern boreal forest. Net carbon loss is what matters, and it is accelerating. '
            'Prompt: look at total carbon stock changes, not just tree cover maps.'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 8,
    },
    {
        'slug': 'boreal_forest_northern_expansion',
        'name': 'Boreal forest northern expansion',
        'domain_raw': 'Biosphere',
        'scale': 'Global core / regional ecosystem',
        'icon_label': 'northward forest line',
        'severity': 'medium',
        'near_term_status': 'Already underway in some regions; expanding treeline is disrupting tundra ecosystems and accelerating warming',
        'warming_context': (
            'As Arctic temperatures rise, shrubs and trees are advancing northward into what was previously open tundra, '
            'a process called "shrubification" or treeline advance. While this might sound like a positive development, '
            'it is actually a significant driver of further warming. Tundra covered in white snow reflects most sunlight '
            'back into space. When dark-colored shrubs and trees replace it, they absorb more heat, warming the local '
            'climate even further. This process also accelerates permafrost thaw beneath the newly established vegetation.'
        ),
        'primary_causes': (
            'Arctic warming opening previously frozen ground to plant colonization; '
            'longer growing seasons allowing shrubs and trees to establish further north; '
            'declining snow cover reducing the competitive advantage of tundra plants adapted to cold; '
            'permafrost thaw creating wet, nutrient-rich conditions that favor certain shrub species.'
        ),
        'effects': (
            'Loss of open tundra habitat for species including caribou, reindeer, polar bears, and Arctic-breeding birds; '
            'disruption of Indigenous herding cultures whose routes and timing depend on stable tundra; '
            'acceleration of permafrost thaw as insulating snow is replaced by heat-absorbing vegetation; '
            'reduced albedo increases regional and global temperatures in a self-reinforcing loop; '
            'alteration of wetland and lake systems that millions of migratory birds depend on.'
        ),
        'interactions': (
            'Darker vegetation surface amplifies Arctic warming, pushing permafrost closer to thaw; '
            'interacts with permafrost carbon release; vegetation change and thaw accelerate together; '
            'loss of tundra habitat reduces biodiversity and disrupts ecosystems across the entire Arctic food web.'
        ),
        'domino_summary': (
            'Arctic warming opens tundra to shrubs and trees -> '
            'dark vegetation replaces reflective white snow -> '
            'surface absorbs more heat -> '
            'local warming accelerates -> '
            'permafrost beneath warms faster -> '
            'more carbon releases -> '
            'tundra animals and Indigenous livelihoods disrupted.'
        ),
        'app_card_summary': (
            'Trees and shrubs spreading into the Arctic tundra sounds positive, but it is not. '
            'They replace bright white snow with dark vegetation that absorbs heat instead of reflecting it, '
            'accelerating Arctic warming in a self-reinforcing loop that also disrupts Indigenous ways of life.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "A greener Arctic means more carbon storage and a better climate." '
            'Shrubification reduces the albedo (reflectivity) of the tundra, warming the climate faster than '
            'any modest carbon storage gain from new vegetation. It also accelerates permafrost thaw, '
            'releasing far more carbon than the new vegetation can store. '
            'Prompt: look at the full energy balance, not just the carbon balance.'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 9,
    },
    {
        'slug': 'amoc_collapse',
        'name': 'Atlantic Meridional Overturning Circulation collapse',
        'domain_raw': 'Ocean-atmosphere circulation',
        'scale': 'Global core',
        'icon_label': 'ocean conveyor',
        'severity': 'extreme',
        'near_term_status': 'Warning signals detected; Iceland designated AMOC collapse a national security threat in 2025; timing uncertain but risk is real',
        'warming_context': (
            'The AMOC is often called the "ocean conveyor belt," a massive system of ocean currents that carries '
            'warm water from the tropics northward and returns cold, dense water southward. '
            'It is what keeps Western Europe\'s climate 5-10°C warmer than it would otherwise be at those latitudes. '
            'Multiple studies now show early warning signals of weakening. A 2024 Science Advances study modeled '
            'a freshwater-forced tipping point and found collapse possible within decades. '
            'In 2025, Iceland\'s government designated AMOC collapse a national security threat. '
            'Models suggest London could cool by 18°F and Bergen, Norway by 27°F under full collapse.'
        ),
        'primary_causes': (
            'Freshwater from melting Greenland ice sheets diluting the salty, dense North Atlantic water that drives the current\'s sinking; '
            'ocean warming reducing the temperature difference that drives circulation; '
            'increased rainfall over the North Atlantic adding more freshwater; '
            'reduced sea ice formation that normally concentrates salt in surface waters.'
        ),
        'effects': (
            'Dramatic cooling of Northwestern Europe; models project average winter temperatures falling 10-30°C in some regions within a century; '
            'sea ice could extend into the waters of the British Isles in winter; '
            'sea levels on the US East Coast rise by up to 1 meter additional to global sea level rise, '
            'because warm water that currently flows northward would instead pile up against the coast; '
            'collapse of the African and Asian monsoons that billions depend on for food and water; '
            'severe disruption to European agriculture as the continent dries and cools simultaneously; '
            'collapse of wheat, maize, and rice growing suitability across most of the Northern Hemisphere; '
            'threat to Atlantic fisheries that underpin food security for hundreds of millions.'
        ),
        'interactions': (
            'AMOC weakening directly threatens Amazon rainfall; a 2024 study found AMOC collapse would flip '
            'the Amazon\'s dry and wet seasons, potentially triggering Amazon dieback; '
            'freshwater input from Greenland melt drives AMOC weakening, creating a compounding cascade; '
            'AMOC collapse stirs the Southern Ocean, releasing more deep-sea carbon; '
            'sea level rise on the US East Coast compounds hurricane damage for cities like New York, Boston, and Miami.'
        ),
        'domino_summary': (
            'Greenland melt floods North Atlantic with freshwater -> '
            'salty, dense water can no longer sink to drive the current -> '
            'ocean conveyor belt slows or stops -> '
            'Europe loses its warming influence and cools dramatically -> '
            'African and Asian monsoons weaken -> '
            'billions face food and water insecurity -> '
            'US East Coast sea levels rise an additional meter -> '
            'Amazon rainfall patterns flip, triggering dieback -> '
            'global food systems destabilize simultaneously.'
        ),
        'app_card_summary': (
            'The AMOC keeps Europe habitable. Without it, London could be as cold as parts of Canada. '
            'A 2024 study confirmed freshwater from melting ice can trigger its collapse, '
            'and Iceland has already declared it a national security threat. '
            'A collapse would simultaneously disrupt monsoons, raise US East Coast sea levels, and threaten the Amazon.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "Regional cooling from AMOC collapse disproves global warming." '
            'These are not contradictory. AMOC collapse would cause severe regional cooling in Europe '
            'while global average temperatures continue rising. It is one of the clearest examples of how '
            'climate change does not mean uniform warming everywhere. '
            'Also watch for claims that AMOC collapse is "just a movie scenario." Real scientific agencies '
            'including Iceland\'s government now treat it as an active security risk.'
        ),
        'source_urls': 'https://e360.yale.edu/features/amoc-climate-change | https://insideclimatenews.org/news/09022024/climate-impacts-from-collapse-of-atlantic-meridional-overturning-current-could-be-worse-than-expected/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 10,
    },
    {
        'slug': 'labrador_irminger_convection',
        'name': 'Labrador-Irminger Sea convection collapse',
        'domain_raw': 'Ocean-atmosphere circulation',
        'scale': 'Regional impact',
        'icon_label': 'subpolar gyre',
        'severity': 'high',
        'near_term_status': 'Possible at current warming; could unfold over about a decade once triggered, faster than the broader AMOC',
        'warming_context': (
            'In the Labrador and Irminger Seas between Canada and Greenland, cold surface water sinks to the deep ocean '
            'in a process called convection, one of the key engines that drives the AMOC. '
            'As Greenland melts, freshwater flooding this region prevents the water from becoming dense enough to sink. '
            'Scientists have already documented declining winter convection in parts of this region. '
            'A collapse of this convective engine could happen faster than the broader AMOC and could be '
            'one of the triggers that pushes the full circulation toward its tipping point.'
        ),
        'primary_causes': (
            'Freshwater input from Greenland melt diluting surface salinity; '
            'ocean warming reducing the temperature difference between surface and deep water; '
            'declining sea ice formation that normally removes freshwater and increases salinity.'
        ),
        'effects': (
            'Disruption of North Atlantic marine ecosystems including the fisheries that feed millions; '
            'changes in storm tracks that affect weather across Western Europe and Eastern North America; '
            'contribution to broader AMOC weakening and potential collapse; '
            'regional sea level changes along the North Atlantic coastline.'
        ),
        'interactions': (
            'Acts as a precursor or trigger for the broader AMOC collapse; '
            'Greenland melt directly drives this process, creating a clear cascade from ice loss to ocean change; '
            'disruption of North Atlantic ecosystems cascades into fisheries and coastal communities.'
        ),
        'domino_summary': (
            'Greenland melt floods Labrador Sea with freshwater -> '
            'surface water cannot sink to drive deep circulation -> '
            'convection collapses -> '
            'AMOC loses one of its key engines -> '
            'North Atlantic circulation weakens further -> '
            'European weather patterns shift -> '
            'fisheries disrupted across the North Atlantic.'
        ),
        'app_card_summary': (
            'Deep beneath the North Atlantic, cold water sinks and drives one of Earth\'s most important '
            'ocean currents. Freshwater from melting Greenland is preventing that sinking,'
            'and if this regional engine stops, it could be the first domino that brings down the entire AMOC.'
        ),
        'misinformation_angle': (
            'Common confusion: "Ocean circulation has always varied naturally, so this is normal." '
            'Natural variability exists, but the driver here is specific: unprecedented freshwater '
            'input from human-caused ice melt. Attribution science can distinguish natural variation '
            'from human-forced change. Prompt: what is driving the change, not just whether change occurs.'
        ),
        'source_urls': 'https://report-2023.global-tipping-points.org/summary-report/section-1/ | https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/',
        'display_order': 11,
    },
    {
        'slug': 'southern_ocean_overturning',
        'name': 'Southern Ocean overturning slowdown',
        'domain_raw': 'Ocean-atmosphere circulation',
        'scale': 'Global core / ocean system',
        'icon_label': 'southern overturning',
        'severity': 'high',
        'near_term_status': 'Already showing signs of slowdown; Antarctic meltwater disrupting deep-water formation',
        'warming_context': (
            'The Southern Ocean around Antarctica drives the deepest part of the global ocean circulation. '
            'Cold, dense water sinks here and flows northward along the ocean floor, driving a return flow '
            'that brings up deep, carbon-rich water from the abyss. This process is responsible for much of '
            'the ocean\'s ability to absorb heat and CO2; the ocean has taken up over 90% of the excess heat '
            'from human-caused warming. A 2023 study found the Southern Ocean overturning had slowed by roughly 30% '
            'since the 1990s, driven by Antarctic meltwater, with potentially enormous consequences for '
            'how much warming the ocean can continue to absorb.'
        ),
        'primary_causes': (
            'Freshwater from Antarctic ice melt reducing the density of surface water that drives deep sinking; '
            'changes in Southern Ocean wind patterns affecting upwelling; '
            'warming of the deep ocean reducing the temperature contrast that drives circulation; '
            'stratification of ocean layers as warm water sits above dense cold water.'
        ),
        'effects': (
            'Reduced ocean carbon uptake, increasing the rate of atmospheric CO2 rise; '
            'reduced ocean heat uptake, accelerating surface warming globally; '
            'changes in Antarctic climate affecting ice sheet stability; '
            'disruption of nutrient upwelling that feeds Antarctic marine ecosystems including krill, '
            'which underpins the entire food chain from fish to penguins to whales.'
        ),
        'interactions': (
            'Reduced carbon uptake amplifies all other tipping points by accelerating atmospheric warming; '
            'interacts with Antarctic ice sheet instability; a slowdown reduces the ocean\'s cooling effect '
            'on ice shelves, accelerating their collapse; '
            'changes in deep ocean circulation affect global heat distribution and regional climates.'
        ),
        'domino_summary': (
            'Antarctic ice melts -> freshwater floods Southern Ocean -> '
            'dense water cannot sink to drive circulation -> '
            'overturning slows by 30%+ -> '
            'ocean absorbs less CO2 and heat -> '
            'atmospheric warming accelerates -> '
            'Antarctic food chain disrupted -> '
            'all other tipping points pushed closer to activation.'
        ),
        'app_card_summary': (
            'The Southern Ocean is Earth\'s most important climate buffer, absorbing over 90% of our excess heat. '
            'It has already slowed by 30% since the 1990s due to Antarctic meltwater. '
            'As it weakens, the ocean absorbs less CO2 and heat, accelerating every other form of climate change.'
        ),
        'misinformation_angle': (
            'Common misconception: "The ocean will always absorb our emissions; it is not a limitless buffer." '
            'Ocean carbon and heat uptake are physically limited and already declining as circulation weakens. '
            'Once the ocean absorbs less, the same emissions cause faster atmospheric warming. '
            'Prompt: the ocean has done us an enormous favor; treating it as a dump with unlimited capacity '
            'is precisely the thinking that leads to tipping points.'
        ),
        'source_urls': 'https://report-2023.global-tipping-points.org/summary-report/section-1/ | https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/',
        'display_order': 12,
    },
    {
        'slug': 'barents_sea_ice_loss',
        'name': 'Barents Sea ice abrupt loss',
        'domain_raw': 'Cryosphere / Ocean',
        'scale': 'Regional impact',
        'icon_label': 'sea ice',
        'severity': 'medium',
        'near_term_status': 'Sea ice in the Barents Sea has declined dramatically in recent decades; abrupt transition to near ice-free state possible',
        'warming_context': (
            'The Barents Sea, located north of Norway and Russia, is one of the fastest-warming regions on Earth. '
            'Its sea ice extent has already declined dramatically, and scientists identify a potential tipping point '
            'where the Barents Sea could transition abruptly from a partially ice-covered to a near-permanently ice-free state. '
            'This matters because sea ice acts like a mirror, reflecting sunlight back into space. '
            'When it disappears, the dark ocean beneath absorbs far more heat,'
            'amplifying Arctic warming in a feedback loop that affects weather patterns far beyond the Arctic.'
        ),
        'primary_causes': (
            'Arctic amplification, where the Arctic is warming 3-4 times faster than the global average; '
            'warm Atlantic ocean currents (Atlantification) pushing further into the Arctic; '
            'ice-albedo feedback: less ice means more heat absorbed, which means less ice; '
            'changing atmospheric circulation patterns bringing warmer air into the Arctic.'
        ),
        'effects': (
            'Amplified Arctic warming through albedo feedback, creating a regional warming hotspot; '
            'disruption of Arctic marine ecosystems; polar bears, walruses, and ice-dependent species lose habitat; '
            'changes in mid-latitude weather patterns, as the jet stream weakens, contributing to more persistent '
            'extreme weather events like cold snaps in Europe and North America; '
            'opening of new shipping routes and resource extraction pressure in the Arctic; '
            'loss of traditional Indigenous sea ice travel routes and hunting grounds.'
        ),
        'interactions': (
            'Loss of sea ice accelerates permafrost thaw on nearby Arctic coasts; '
            'albedo feedback amplifies warming that pushes Greenland melt and permafrost thaw; '
            'jet stream disruption associated with Arctic warming causes more extreme weather events globally; '
            'black carbon from wildfires deposits on remaining sea ice, accelerating its melt.'
        ),
        'domino_summary': (
            'Ocean warms -> Barents Sea ice retreats -> '
            'dark ocean surface exposed -> '
            'more solar heat absorbed -> '
            'Arctic warms faster -> '
            'jet stream weakens -> '
            'extreme weather events increase in frequency across Europe and North America -> '
            'permafrost and Greenland melt accelerate.'
        ),
        'app_card_summary': (
            'Arctic sea ice acts as Earth\'s air conditioner, reflecting sunlight back to space. '
            'The Barents Sea is warming so fast it could lose its ice cover abruptly, exposing dark ocean '
            'that absorbs heat instead. The ripple effects include stronger extreme weather events '
            'across the entire Northern Hemisphere.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "Arctic ice loss is just natural variability." '
            'Attribution science shows current sea ice loss rates are unprecedented in thousands of years '
            'and directly linked to human-caused warming, not natural cycles. '
            'Also watch for claims that new shipping routes or resources are "benefits" of ice loss, '
            'which ignore the broader climate destabilization caused by losing Arctic ice.'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 13,
    },
    {
        'slug': 'mountain_glacier_loss',
        'name': 'Mountain glacier loss',
        'domain_raw': 'Cryosphere / Water systems',
        'scale': 'Regional impact',
        'icon_label': 'mountain glacier',
        'severity': 'high',
        'near_term_status': 'Already underway globally; many glaciers committed to near-complete loss even under current warming',
        'warming_context': (
            'Mountain glaciers are often called the "water towers of the world" because they store winter precipitation as ice '
            'and release it slowly through summer, providing steady freshwater to rivers when rainfall is scarce. '
            'Over 2 billion people depend on glacier-fed rivers for drinking water, irrigation, and hydropower. '
            'Glaciers worldwide have been losing mass at accelerating rates since the 1990s. '
            'Many smaller glaciers are now committed to disappearing entirely even if all emissions stopped today. '
            'The loss pattern is not gradual and manageable; it creates a dangerous transition from '
            'temporary meltwater abundance to permanent water scarcity.'
        ),
        'primary_causes': (
            'Rising temperatures reducing winter snowfall and increasing summer melt; '
            'albedo feedback, where darker exposed rock absorbs more heat than reflective ice; '
            'black carbon from diesel emissions and wildfires depositing on glaciers and accelerating melt; '
            'changes in precipitation patterns reducing the snowfall that replenishes glaciers.'
        ),
        'effects': (
            '"Peak water," an initial increase in meltwater flooding followed by permanent scarcity '
            'as glaciers disappear; '
            'water insecurity for over 2 billion people across South Asia, the Andes, Central Asia, and the Alps; '
            'hydropower failures threatening electricity grids that entire nations depend on; '
            'agricultural collapse in regions where irrigation depends on glacier-fed rivers; '
            'increased glacial lake outburst floods, dangerous surges of water when glacial dams fail; '
            'loss of cultural and tourism economies in mountain communities worldwide.'
        ),
        'interactions': (
            'Glacier retreat contributes to sea-level rise, compounding coastal flooding; '
            'freshwater shortages drive competition for resources and potential conflict; '
            'reduced river flows increase lake eutrophication as nutrient concentrations rise; '
            'loss of hydropower forces reliance on fossil fuels in some regions, adding more emissions.'
        ),
        'domino_summary': (
            'Temperatures rise -> glaciers melt faster than snowfall can replenish them -> '
            'rivers swell temporarily with meltwater (flood phase) -> '
            'glaciers shrink below critical size -> '
            'rivers run dry in summer (scarcity phase) -> '
            '2+ billion people face water insecurity -> '
            'agriculture collapses -> '
            'hydropower fails -> '
            'mass displacement from mountain regions.'
        ),
        'app_card_summary': (
            'Over 2 billion people depend on glacier-fed rivers. '
            'Glaciers first flood, then disappear; the scarcity that follows is permanent. '
            'Many are already committed to vanishing even if we stopped all emissions today, '
            'making adaptation planning for the communities that depend on them urgently necessary.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "More glacier melt just means more water; that is a good thing." '
            'The initial meltwater surge is followed by permanent scarcity when the glacier is gone. '
            'The problem is the loss of natural storage; without the glacier, there is no buffer '
            'between wet seasons and dry seasons. Prompt: what happens downstream when the glacier is completely gone?'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 14,
    },
    {
        'slug': 'west_african_monsoon_shift',
        'name': 'West African monsoon shift',
        'domain_raw': 'Atmosphere / Hydrology',
        'scale': 'Regional impact',
        'icon_label': 'monsoon rain',
        'severity': 'high',
        'near_term_status': 'Possible around 1.5°C; historical evidence shows the Sahara has flipped between wet and dry states abruptly before',
        'warming_context': (
            'The West African monsoon delivers nearly all of the annual rainfall that hundreds of millions of people '
            'in the Sahel and West Africa depend on for food, water, and livelihoods. '
            'Geological evidence shows this monsoon system has shifted abruptly in the past,'
            'most dramatically during the "Green Sahara" period, when the Sahara was a lush, wet landscape '
            'before flipping to desert within centuries. Today, a combination of ocean temperature changes, '
            'AMOC weakening, and deforestation are placing stress on this system. '
            'An abrupt shift in either direction would reshape life across an enormous region.'
        ),
        'primary_causes': (
            'Changes in North Atlantic and tropical ocean temperatures that drive the monsoon; '
            'AMOC weakening shifting the tropical rain belt southward; '
            'land-use change and deforestation reducing moisture recycling; '
            'aerosol emissions from industry and cooking fires affecting atmospheric dynamics; '
            'vegetation feedbacks, where sparse vegetation reduces moisture recycling, weakening the monsoon further.'
        ),
        'effects': (
            'Major shifts in rainfall distribution; some regions flood while others face permanent drought; '
            'food insecurity for hundreds of millions of people across the Sahel and West Africa; '
            'collapse of smallholder agriculture that most of the region depends on; '
            'displacement of populations as formerly productive land becomes uninhabitable; '
            'conflict over water and land resources as scarcity increases; '
            'potential for the Sahel greening trend to reverse catastrophically.'
        ),
        'interactions': (
            'Directly linked to AMOC; an AMOC collapse would shift the tropical rain belt '
            'and could trigger drastic changes in West African rainfall; '
            'Amazon deforestation affects Atlantic moisture patterns and therefore the West African monsoon; '
            'land use change and the monsoon interact bidirectionally: less vegetation weakens the monsoon, '
            'and a weaker monsoon kills more vegetation.'
        ),
        'domino_summary': (
            'AMOC weakens -> tropical rain belt shifts southward -> '
            'Sahel rainfall patterns change abruptly -> '
            'smallholder farming collapses -> '
            'food insecurity spikes across West Africa -> '
            'vegetation dies back -> '
            'less moisture recycling weakens monsoon further -> '
            'displacement of hundreds of millions of people -> '
            'regional conflict over shrinking resources.'
        ),
        'app_card_summary': (
            'The West African monsoon feeds hundreds of millions of people. '
            'Geological history shows it has flipped abruptly before. Within centuries, the Green Sahara '
            'became a desert. The same mechanisms that caused past shifts are being activated again '
            'by AMOC weakening and land-use change.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "The Sahel has been greening recently, so there is no risk." '
            'Recent greening is real but fragile; it is sensitive to the same ocean and atmospheric conditions '
            'that could reverse it rapidly. Cherry-picking a positive recent trend to dismiss long-term risk '
            'is a classic misinformation technique. '
            'Prompt: distinguish a short-term positive trend from the underlying systemic risk.'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 15,
    },
    {
        'slug': 'sahel_greening',
        'name': 'Sahel greening',
        'domain_raw': 'Biosphere / Hydrology',
        'scale': 'Regional impact',
        'icon_label': 'sahel vegetation',
        'severity': 'medium',
        'near_term_status': 'A genuinely positive trend, but fragile, uneven, and reversible if monsoon patterns shift',
        'warming_context': (
            'Since the devastating droughts of the 1970s and 1980s, parts of the Sahel have experienced increased '
            'rainfall and greening, with more vegetation returning to areas that were degraded. '
            'This is one of the few genuinely positive environmental trends in the climate system, '
            'driven partly by increased rainfall, partly by CO2 fertilization of plants, and partly by '
            'improved land management and tree planting programs. '
            'However, scientists identify it as a potential "positive tipping point," a threshold beyond which '
            'vegetation and rainfall reinforce each other upward. Scientists also note that the same '
            'feedback mechanism could rapidly reverse if the monsoon shifts.'
        ),
        'primary_causes': (
            'Increased Sahel rainfall driven by sea surface temperature changes in the Gulf of Guinea; '
            'CO2 fertilization effect helping drought-tolerant plants establish; '
            'improved land management including farmer-managed natural regeneration; '
            'vegetation-rainfall feedback; more plants recycle more moisture into the atmosphere.'
        ),
        'effects': (
            'Recovery of productive agricultural land; '
            'improved food and water security for Sahelian communities; '
            'carbon storage in recovering vegetation and soils; '
            'restoration of biodiversity in recovering areas; '
            'reduction in dust storms that affect air quality across the region and beyond.'
        ),
        'interactions': (
            'Vegetation recovery feeds back positively on rainfall recycling, potentially self-sustaining; '
            'but the same feedback makes it vulnerable to reversal if monsoon weakens; '
            'closely tied to West African monsoon stability; any major shift could reverse the greening rapidly; '
            'shows that positive tipping dynamics are possible, providing a model for restoration efforts.'
        ),
        'domino_summary': (
            'Improved rainfall -> vegetation establishes -> '
            'plants recycle moisture back into atmosphere -> '
            'more rainfall -> more vegetation -> '
            'positive loop strengthens; '
            'BUT if monsoon shifts -> vegetation dies -> '
            'less moisture recycled -> less rainfall -> '
            'rapid reversal to degraded state.'
        ),
        'app_card_summary': (
            'The Sahel is one of the rare places where things are genuinely improving, with more rain, more vegetation, '
            'more food. But this positive trend sits on a knife\'s edge: the same monsoon dynamics that could '
            'amplify the greening could also reverse it catastrophically if ocean temperatures shift.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "The Sahel proves climate change is good for Africa." '
            'Sahel greening is real but geographically uneven; some areas have greened while others have not. '
            'It is also fragile and directly dependent on monsoon stability. Using a partial, regional positive '
            'trend to dismiss broader climate risk is cherry-picking. '
            'Prompt: does citing this positive example acknowledge the conditions it depends on?'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 16,
    },
    {
        'slug': 'lake_eutrophication',
        'name': 'Lake eutrophication',
        'domain_raw': 'Biosphere / Freshwater',
        'scale': 'Regional/local cascading ecosystem',
        'icon_label': 'algal bloom',
        'severity': 'medium',
        'near_term_status': 'Already occurring in lakes worldwide; climate change is accelerating and expanding the problem',
        'warming_context': (
            'Eutrophication, the process by which excess nutrients trigger explosive algae growth, '
            'is one of the most widespread freshwater crises on Earth. It is driven by agricultural runoff '
            'carrying nitrogen and phosphorus into lakes, but warming temperatures are dramatically '
            'accelerating the problem. Warmer water allows algae to grow faster, stratifies into layers '
            'that prevent oxygen from reaching deeper water, and increases the frequency of toxic algal blooms. '
            'Lake Erie, Lake Taihu in China, and hundreds of other lakes worldwide have experienced '
            'severe eutrophication. This is important as a tipping-point example because it can '
            'flip relatively quickly from a clear, healthy lake to a turbid, oxygen-depleted dead zone '
            'that is extremely difficult to reverse.'
        ),
        'primary_causes': (
            'Agricultural nutrient runoff (nitrogen and phosphorus) from fertilizer application; '
            'warming water temperatures that accelerate algae growth rates; '
            'reduced lake mixing as warming creates stronger temperature stratification; '
            'urban wastewater and stormwater adding nutrients; '
            'internal phosphorus loading, where phosphorus already stored in lake sediments releases '
            'when oxygen levels drop, feeding more algae growth even if external inputs stop.'
        ),
        'effects': (
            'Toxic algal blooms that poison drinking water supplies. Toledo, Ohio was cut off from its '
            'water supply for 400,000 people for three days in 2014 due to Lake Erie blooms; '
            'fish kills as oxygen depletion creates dead zones; '
            'loss of recreational value and tourism income for lakeside communities; '
            'ecosystem collapse replacing diverse aquatic species with algae monocultures; '
            'potential health risks from cyanobacteria toxins in drinking water and through fish consumption; '
            'economic losses to commercial and recreational fisheries.'
        ),
        'interactions': (
            'Connects to fisheries collapse; dead lake ecosystems eliminate food sources; '
            'reduces freshwater supply reliability, compounding water stress from glacier loss; '
            'warming amplifies eutrophication, which in turn releases more methane from lake sediments; '
            'affected lakes release CO2 and methane as organic matter decomposes in low-oxygen conditions.'
        ),
        'domino_summary': (
            'Nutrient runoff enters lake -> algae grows rapidly in warmer water -> '
            'dense algae blocks sunlight from reaching lake bottom -> '
            'aquatic plants die -> '
            'algae dies and decomposes consuming all oxygen -> '
            'fish suffocate and die -> '
            'drinking water becomes toxic -> '
            'community loses water supply -> '
            'internal phosphorus feeding further blooms makes recovery take decades.'
        ),
        'app_card_summary': (
            'Lakes can flip from clear and healthy to choked with toxic algae surprisingly fast,'
            'and once they do, recovery takes decades. In 2014, a toxic bloom in Lake Erie cut '
            '400,000 people off from their drinking water for three days. '
            'Climate warming is making these events more frequent and severe worldwide.'
        ),
        'misinformation_angle': (
            'Common misleading framing: "Water pollution is a local development issue, not a climate problem." '
            'Warming temperatures are a direct driver of more severe eutrophication, not a bystander. '
            'The same nutrient levels that produced manageable blooms in a cooler lake '
            'produce catastrophic toxic events in a warmer one. '
            'Prompt: if the nutrient levels haven\'t changed but blooms are getting worse, what has changed?'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 17,
    },
    {
        'slug': 'fisheries_collapse',
        'name': 'Fisheries collapse',
        'domain_raw': 'Biosphere / Food systems',
        'scale': 'Regional impact',
        'icon_label': 'fisheries',
        'severity': 'high',
        'near_term_status': 'Already underway in multiple regions; FAO reports over 35% of global fish stocks are now unsustainably harvested',
        'warming_context': (
            'Fish feed over 3 billion people and provide the primary source of protein for many coastal and island communities. '
            'Fisheries collapse is not a single event but a compound crisis driven by multiple simultaneous stressors. '
            'The FAO reports that over 35% of global fish stocks are harvested at biologically unsustainable levels, '
            'up from 10% in 1974. Climate change compounds overfishing through ocean warming, '
            'acidification, deoxygenation, and the collapse of the reef and coastal habitats '
            'that serve as nurseries for juvenile fish. When multiple stressors hit simultaneously, '
            'stocks can collapse faster than they would from any single cause alone,'
            'and some collapsed stocks have not recovered even after decades of reduced fishing.'
        ),
        'primary_causes': (
            'Overfishing removing fish faster than populations can reproduce; '
            'habitat loss as coral reefs, mangroves, and seagrass meadows, critical nursery environments, degrade; '
            'ocean warming shifting species distributions and disrupting food chains; '
            'ocean acidification weakening the shells and skeletons of shellfish and juvenile fish; '
            'deoxygenation of ocean dead zones where fish cannot survive; '
            'changes in ocean currents altering the upwelling of nutrients that feed marine food chains.'
        ),
        'effects': (
            'Food insecurity for the 3+ billion people who depend on fish as their primary protein source; '
            'economic collapse in fishing-dependent communities and nations; '
            'loss of livelihoods for the estimated 600 million people who depend on fisheries directly or indirectly; '
            'cascading ecosystem effects as removing top predators or key species destabilizes entire marine food webs; '
            'increased pressure on already stressed land-based food systems as marine protein disappears; '
            'geopolitical conflict as nations compete for shrinking fish stocks in international waters.'
        ),
        'interactions': (
            'Coral reef collapse directly reduces nursery habitat for commercial fish species; '
            'mangrove and seagrass loss removes breeding and juvenile habitat; '
            'AMOC weakening disrupts the nutrient upwelling that feeds the North Atlantic fisheries; '
            'lake eutrophication eliminates freshwater fisheries, compounding marine losses; '
            'fisheries collapse hits poorest coastal communities hardest, reducing their capacity to adapt to other climate impacts.'
        ),
        'domino_summary': (
            'Overfishing depletes stocks -> coral reefs collapse removing nursery habitat -> '
            'ocean warms and acidifies -> juvenile fish cannot form shells -> '
            'dead zones expand without oxygen -> '
            'species shift to new ranges leaving fishers behind -> '
            'stock collapses faster than recovery is possible -> '
            '600 million livelihoods threatened -> '
            'coastal food insecurity spreads -> '
            'pressure on land food systems intensifies.'
        ),
        'app_card_summary': (
            'Over 3 billion people depend on fish as their main protein, and 600 million depend on fisheries for income. '
            'The FAO reports 35% of global stocks are already overexploited, and climate change is accelerating '
            'collapse by simultaneously destroying the reefs, heating the water, acidifying the ocean, '
            'and expanding the dead zones where fish cannot survive.'
        ),
        'misinformation_angle': (
            'Common misleading claim: "Fish stocks have always fluctuated; they will recover on their own." '
            'Recovery requires both reduced fishing pressure AND stable ocean conditions. '
            'When multiple stressors hit at once, stocks can collapse to levels too low to rebuild,'
            'a true ecological tipping point. '
            'Some North Atlantic cod stocks have not recovered 30 years after fishing was drastically reduced. '
            'Prompt: what conditions existed when stocks previously recovered that may no longer exist today?'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 18,
    },
    {
        'slug': 'mangrove_seagrass_dieoff',
        'name': 'Mangrove and seagrass meadow die-off',
        'domain_raw': 'Biosphere / Coastal systems',
        'scale': 'Regional impact',
        'icon_label': 'coastal habitat',
        'severity': 'high',
        'near_term_status': 'Ongoing in many regions; accelerating with sea-level rise, warming, and coastal development',
        'warming_context': (
            'Mangrove forests and seagrass meadows are among the most productive and carbon-rich ecosystems on Earth. '
            'Mangroves store up to four times more carbon per acre than tropical rainforests. '
            'They also provide critical storm protection, acting as natural breakwaters that reduce '
            'wave energy during hurricanes and tsunamis, protecting the communities behind them. '
            'Seagrass meadows provide nursery habitat for over 20% of the world\'s major fisheries '
            'and feed endangered species like dugongs and sea turtles. '
            'Both are under compounding pressure from sea-level rise, warming, coastal development, '
            'pollution, and ocean acidification. Their loss creates a cascading crisis '
            'that hits food security, coastal protection, and the climate simultaneously.'
        ),
        'primary_causes': (
            'Sea-level rise drowning mangroves that cannot migrate inland due to coastal development; '
            'warming ocean temperatures stressing seagrass beyond their thermal tolerance; '
            'coastal development directly destroying mangrove areas for shrimp farms, ports, and tourism; '
            'pollution and agricultural runoff reducing water clarity that seagrass needs to photosynthesize; '
            'increased storm frequency damaging coastal habitats; '
            'ocean acidification weakening the carbonate sediments that seagrass ecosystems build on.'
        ),
        'effects': (
            'Release of "blue carbon," the enormous carbon stocks stored in mangrove soils for centuries, '
            'adding to atmospheric CO2 when these ecosystems are destroyed; '
            'loss of storm protection for tens of millions of people living on low-lying coastlines; '
            'collapse of the nursery habitat that supports 20%+ of global fisheries; '
            'coastal erosion accelerating as natural buffers are removed; '
            'loss of habitat for endangered species including dugongs, sea turtles, seahorses, and many fish; '
            'economic losses to communities that depend on reef-adjacent tourism and fishing.'
        ),
        'interactions': (
            'Directly feeds into fisheries collapse by removing nursery grounds; '
            'blue carbon release contributes to atmospheric CO2, accelerating warming and sea-level rise; '
            'coastal protection loss compounds sea-level rise and storm surge impacts; '
            'coral reef die-off and mangrove loss often occur together, creating compounding coastal vulnerability.'
        ),
        'domino_summary': (
            'Sea-level rise and warming stress mangroves and seagrass -> '
            'coastal development blocks landward migration -> '
            'ecosystems die in place -> '
            'centuries of stored blue carbon released -> '
            'fish nurseries disappear -> '
            'coastal storm protection lost -> '
            'fishing communities face simultaneous food and safety crisis -> '
            'coastlines erode as natural barriers vanish -> '
            'adaptation costs soar.'
        ),
        'app_card_summary': (
            'Mangroves store four times more carbon per acre than rainforests and protect coastlines from storms. '
            'Seagrass meadows provide nursery habitat for over 20% of global fisheries. '
            'Both are dying from rising seas, warming water, and coastal development,'
            'and when they go, they take coastal protection, fisheries, and stored carbon with them.'
        ),
        'misinformation_angle': (
            'Common misconception: "Coastal habitat loss is a local development issue, not a climate problem." '
            'Climate change is now the primary accelerator of mangrove and seagrass loss through '
            'sea-level rise, warming, acidification, and increased storms, even where direct development is controlled. '
            'And blue carbon release from these ecosystems feeds back directly into global CO2 levels. '
            'Prompt: follow the carbon; coastal ecosystem destruction is a global climate problem,'
            'not just a local environmental one.'
        ),
        'source_urls': 'https://climatetippingpoints.info/2022/09/09/climate-tipping-points-reassessment-explainer/ | https://report-2023.global-tipping-points.org/summary-report/section-1/',
        'display_order': 19,
    },
]

RELATIONSHIPS = [
    ('gis_collapse',                    'amoc_collapse',                  'freshwater_circulation',     4, False),
    ('wais_collapse',                   'gis_collapse',                   'sea_level',                  3, False),
    ('gis_collapse',                    'wais_collapse',                  'sea_level',                  3, False),
    ('abrupt_permafrost_thaw',          'gis_collapse',                   'temperature_amplification',  4, False),
    ('permafrost_yedoma_carbon',        'abrupt_permafrost_thaw',         'carbon_feedback',            5, False),
    ('abrupt_permafrost_thaw',          'permafrost_yedoma_carbon',       'carbon_feedback',            4, True),
    ('amazon_rainforest_dieback',       'west_african_monsoon_shift',     'rainfall_recycling',         3, False),
    ('amazon_rainforest_dieback',       'fisheries_collapse',             'ecosystem_cascade',          3, False),
    ('warm_water_coral_reefs_dieoff',   'fisheries_collapse',             'habitat_livelihood',         5, False),
    ('warm_water_coral_reefs_dieoff',   'mangrove_seagrass_dieoff',       'ocean_chemistry',            3, False),
    ('mangrove_seagrass_dieoff',        'fisheries_collapse',             'habitat_livelihood',         4, False),
    ('amoc_collapse',                   'west_african_monsoon_shift',     'monsoon_shift',              3, False),
    ('amoc_collapse',                   'amazon_rainforest_dieback',      'rainfall_recycling',         3, False),
    ('barents_sea_ice_loss',            'boreal_forest_northern_expansion', 'temperature_amplification', 3, False),
    ('boreal_forest_southern_dieback',  'amazon_rainforest_dieback',      'carbon_feedback',            2, False),
    ('mountain_glacier_loss',           'lake_eutrophication',            'ecosystem_cascade',          3, False),
    ('lake_eutrophication',             'fisheries_collapse',             'ecosystem_cascade',          4, False),
    ('southern_ocean_overturning',      'amoc_collapse',                  'ocean_chemistry',            3, False),
    ('labrador_irminger_convection',    'amoc_collapse',                  'freshwater_circulation',     4, False),
    ('gis_collapse',                    'labrador_irminger_convection',   'freshwater_circulation',     3, False),
    ('sahel_greening',                  'west_african_monsoon_shift',     'monsoon_shift',              3, True),
    ('east_antarctic_subglacial_basins','wais_collapse',                  'sea_level',                  2, False),
]


def seed_tipping_points(apps, schema_editor):
    TippingPoint             = apps.get_model('tipping_points', 'TippingPoint')
    TippingPointRelationship = apps.get_model('tipping_points', 'TippingPointRelationship')
    SourceReference          = apps.get_model('tipping_points', 'SourceReference')
    tp_cache = {}
    for row in TIPPING_POINTS:
        domain = DOMAIN_MAP.get(row['domain_raw'], 'cryosphere')
        source_urls = row.pop('source_urls')
        tp, _ = TippingPoint.objects.get_or_create(
            slug=row['slug'],
            defaults={**row, 'domain': domain, 'source_urls': source_urls, 'is_active': True},
        )
        tp_cache[tp.slug] = tp
        for url in (u.strip() for u in source_urls.split('|') if u.strip()):
            SourceReference.objects.get_or_create(tipping_point=tp, url=url)
    for src_slug, tgt_slug, rel_type, strength, bidir in RELATIONSHIPS:
        src = tp_cache.get(src_slug)
        tgt = tp_cache.get(tgt_slug)
        if src and tgt:
            TippingPointRelationship.objects.get_or_create(
                source=src, target=tgt, relationship_type=rel_type,
                defaults={'strength': strength, 'is_bidirectional': bidir},
            )


def unseed_tipping_points(apps, schema_editor):
    TippingPoint = apps.get_model('tipping_points', 'TippingPoint')
    TippingPoint.objects.filter(slug__in=[row['slug'] for row in TIPPING_POINTS]).delete()


class Migration(migrations.Migration):
    dependencies = [('tipping_points', '0001_initial')]
    operations = [migrations.RunPython(seed_tipping_points, reverse_code=unseed_tipping_points)]
