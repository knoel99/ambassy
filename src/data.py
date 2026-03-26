"""
G20 Embassy and Power Center Data Module.

Contains coordinates for:
- Power centers (government seats) of each G20 country
- Embassy locations of G20 countries in each G20 capital
"""

from math import radians, sin, cos, sqrt, atan2

# G20 member countries with their capitals and power centers
POWER_CENTERS = {
    "Argentina": {
        "capital": "Buenos Aires",
        "name": "Casa Rosada",
        "lat": -34.6083,
        "lon": -58.3712,
        "country_code": "AR",
    },
    "Australia": {
        "capital": "Canberra",
        "name": "Parliament House",
        "lat": -35.3082,
        "lon": 149.1245,
        "country_code": "AU",
    },
    "Brazil": {
        "capital": "Brasília",
        "name": "Palácio do Planalto",
        "lat": -15.7999,
        "lon": -47.8603,
        "country_code": "BR",
    },
    "Canada": {
        "capital": "Ottawa",
        "name": "Parliament Hill",
        "lat": 45.4236,
        "lon": -75.7009,
        "country_code": "CA",
    },
    "China": {
        "capital": "Beijing",
        "name": "Zhongnanhai",
        "lat": 39.9130,
        "lon": 116.3815,
        "country_code": "CN",
    },
    "France": {
        "capital": "Paris",
        "name": "Palais de l'Élysée",
        "lat": 48.8704,
        "lon": 2.3167,
        "country_code": "FR",
    },
    "Germany": {
        "capital": "Berlin",
        "name": "Bundeskanzleramt",
        "lat": 52.5200,
        "lon": 13.3693,
        "country_code": "DE",
    },
    "India": {
        "capital": "New Delhi",
        "name": "Rashtrapati Bhavan",
        "lat": 28.6143,
        "lon": 77.1994,
        "country_code": "IN",
    },
    "Indonesia": {
        "capital": "Jakarta",
        "name": "Istana Merdeka",
        "lat": -6.1701,
        "lon": 106.8272,
        "country_code": "ID",
    },
    "Italy": {
        "capital": "Rome",
        "name": "Palazzo Chigi",
        "lat": 41.9009,
        "lon": 12.4803,
        "country_code": "IT",
    },
    "Japan": {
        "capital": "Tokyo",
        "name": "Kantei",
        "lat": 35.6735,
        "lon": 139.7525,
        "country_code": "JP",
    },
    "Mexico": {
        "capital": "Mexico City",
        "name": "Palacio Nacional",
        "lat": 19.4326,
        "lon": -99.1312,
        "country_code": "MX",
    },
    "Russia": {
        "capital": "Moscow",
        "name": "Kremlin",
        "lat": 55.7520,
        "lon": 37.6175,
        "country_code": "RU",
    },
    "Saudi Arabia": {
        "capital": "Riyadh",
        "name": "Al-Yamamah Palace",
        "lat": 24.6500,
        "lon": 46.7100,
        "country_code": "SA",
    },
    "South Africa": {
        "capital": "Pretoria",
        "name": "Union Buildings",
        "lat": -25.7411,
        "lon": 28.2120,
        "country_code": "ZA",
    },
    "South Korea": {
        "capital": "Seoul",
        "name": "Yongsan Presidential Office",
        "lat": 37.5320,
        "lon": 126.9800,
        "country_code": "KR",
    },
    "Turkey": {
        "capital": "Ankara",
        "name": "Presidential Complex",
        "lat": 39.9310,
        "lon": 32.7990,
        "country_code": "TR",
    },
    "United Kingdom": {
        "capital": "London",
        "name": "10 Downing Street",
        "lat": 51.5034,
        "lon": -0.1276,
        "country_code": "GB",
    },
    "United States": {
        "capital": "Washington, D.C.",
        "name": "White House",
        "lat": 38.8977,
        "lon": -77.0365,
        "country_code": "US",
    },
    "European Union": {
        "capital": "Brussels",
        "name": "European Commission (Berlaymont)",
        "lat": 50.8438,
        "lon": 4.3828,
        "country_code": "EU",
    },
}

# Embassy locations organized by host country
# Each entry: { "country_of_origin": (lat, lon) }
# Coordinates sourced from OpenStreetMap/Nominatim geocoding of official addresses
EMBASSIES = {
    "United States": {
        # Washington, D.C. — Embassies of G20 countries
        "Argentina": (38.9114, -77.0424),      # 1600 New Hampshire Ave NW
        "Australia": (38.9080, -77.0370),       # 1601 Massachusetts Ave NW
        "Brazil": (38.9189, -77.0610),          # 3006 Massachusetts Ave NW
        "Canada": (38.8930, -77.0186),          # 501 Pennsylvania Ave NW
        "China": (38.9426, -77.0670),           # 3505 International Place NW
        "France": (38.9140, -77.0786),          # 4101 Reservoir Road NW
        "Germany": (38.9146, -77.0888),         # 4645 Reservoir Road NW
        "India": (38.9113, -77.0471),           # 2107 Massachusetts Ave NW
        "Indonesia": (38.9103, -77.0461),       # 2020 Massachusetts Ave NW
        "Italy": (38.9178, -77.0605),           # 3000 Whitehaven St NW
        "Japan": (38.9156, -77.0564),           # 2520 Massachusetts Ave NW
        "Mexico": (38.9007, -77.0440),          # 1911 Pennsylvania Ave NW
        "Russia": (38.9243, -77.0745),          # 2650 Wisconsin Ave NW
        "Saudi Arabia": (38.8978, -77.0540),    # 601 New Hampshire Ave NW
        "South Africa": (38.9200, -77.0606),    # 3051 Massachusetts Ave NW
        "South Korea": (38.9147, -77.0547),     # 2450 Massachusetts Ave NW
        "Turkey": (38.9165, -77.0560),          # 2525 Massachusetts Ave NW
        "United Kingdom": (38.9199, -77.0627),  # 3100 Massachusetts Ave NW
        "European Union": (38.9029, -77.0486),  # 2175 K Street NW
    },
    "United Kingdom": {
        # London — Embassies of G20 countries
        "Argentina": (51.5123, -0.1487),        # 65 Brook Street
        "Australia": (51.5129, -0.1156),        # Australia House, Strand
        "Brazil": (51.5075, -0.1308),           # 14 Cockspur Street
        "Canada": (51.5079, -0.1296),           # Canada House, Trafalgar Square
        "China": (51.5210, -0.1460),            # 49 Portland Place
        "France": (51.5025, -0.1581),           # 58 Knightsbridge
        "Germany": (51.4980, -0.1545),          # 23 Belgrave Square
        "India": (51.5126, -0.1182),            # India House, Aldwych
        "Indonesia": (51.4969, -0.1275),        # 30 Great Peter Street
        "Italy": (51.5119, -0.1493),            # 14 Three Kings Yard
        "Japan": (51.5053, -0.1461),            # 101 Piccadilly
        "Mexico": (51.5130, -0.1437),           # 16 St George Street
        "Russia": (51.5095, -0.1919),           # 6 Kensington Palace Gardens
        "Saudi Arabia": (51.5073, -0.1479),     # 30 Charles Street
        "South Africa": (51.5083, -0.1268),     # South Africa House, Trafalgar Sq
        "South Korea": (51.4975, -0.1356),      # 60 Buckingham Gate
        "Turkey": (51.4999, -0.1522),           # 43 Belgrave Square
        "United States": (51.4826, -0.1322),    # 33 Nine Elms Lane
        "European Union": (51.4955, -0.1279),   # 32 Smith Square
    },
    "France": {
        # Paris — Embassies of G20 countries
        "Argentina": (48.8682, 2.2900),         # 6 rue Cimarosa
        "Australia": (48.8552, 2.2904),         # 4 rue Jean Rey
        "Brazil": (48.8645, 2.3102),            # 34 cours Albert Ier
        "Canada": (48.8724, 2.3124),            # 130 rue du Faubourg Saint-Honoré
        "China": (48.8501, 2.3165),             # 20 rue Monsieur
        "Germany": (48.8661, 2.3100),           # 13 avenue Franklin Roosevelt
        "India": (48.8601, 2.2705),             # 15 rue Alfred Dehodencq
        "Indonesia": (48.8602, 2.2784),         # 47 rue Cortambert
        "Italy": (48.8545, 2.3218),             # 51 rue de Varenne
        "Japan": (48.8774, 2.3041),             # 7 avenue Hoche
        "Mexico": (48.8648, 2.2923),            # 9 rue de Longchamp
        "Russia": (48.8633, 2.2685),            # 40 boulevard Lannes
        "Saudi Arabia": (48.8788, 2.3039),      # 92 rue de Courcelles
        "South Africa": (48.8623, 2.3078),      # 59 quai d'Orsay
        "South Korea": (48.8578, 2.3163),       # 125 rue de Grenelle
        "Turkey": (48.8546, 2.2805),            # 16 avenue de Lamballe
        "United Kingdom": (48.8693, 2.3196),    # 35 rue du Faubourg Saint-Honoré
        "United States": (48.8674, 2.3204),     # 2 avenue Gabriel
        "European Union": (48.8642, 2.2854),    # 12 avenue Eylau
    },
    "Germany": {
        # Berlin — Embassies of G20 countries
        "Argentina": (52.5070, 13.3544),        # Von-der-Heydt-Strasse 2
        "Australia": (52.5123, 13.4095),        # Wallstrasse 76
        "Brazil": (52.5136, 13.4136),           # Wallstrasse 57
        "Canada": (52.5103, 13.3775),           # Leipziger Platz 17
        "China": (52.5136, 13.4168),            # Märkisches Ufer 54
        "France": (52.5172, 13.3795),           # Pariser Platz 5
        "India": (52.5094, 13.3621),            # Tiergartenstrasse 17
        "Indonesia": (52.5086, 13.3559),        # Clara-Wieck-Strasse 1
        "Italy": (52.5093, 13.3597),            # Hiroshimastrasse 1
        "Japan": (52.5092, 13.3581),            # Hiroshimastrasse 6
        "Mexico": (52.5081, 13.3513),           # Klingelhöferstrasse 3
        "Russia": (52.5161, 13.3837),           # Unter den Linden 63
        "Saudi Arabia": (52.5092, 13.3533),     # Tiergartenstrasse 33
        "South Africa": (52.5094, 13.3616),     # Tiergartenstrasse 18
        "South Korea": (52.5096, 13.3507),      # Stülerstrasse 8
        "Turkey": (52.4741, 13.5621),           # Tiergartenstrasse 19
        "United Kingdom": (52.5157, 13.3810),   # Wilhelmstrasse 70
        "United States": (52.4523, 13.2726),    # Clayallee 170
        "European Union": (52.5170, 13.3804),   # Unter den Linden 78
    },
    "Japan": {
        # Tokyo — Embassies of G20 countries
        "Argentina": (35.6556, 139.7296),       # 2-14-14 Motoazabu, Minato
        "Australia": (35.6468, 139.7414),       # 2-1-14 Mita, Minato
        "Brazil": (35.6709, 139.7145),          # 2-11-12 Kita-Aoyama, Minato
        "Canada": (35.6732, 139.7284),          # 7-3-38 Akasaka, Minato
        "China": (35.6563, 139.7272),           # 3-4-33 Moto-Azabu, Minato
        "France": (35.6489, 139.7260),          # 4-11-44 Minami-Azabu, Minato
        "Germany": (35.6489, 139.7260),         # 4-5-10 Minami-Azabu, Minato
        "India": (35.6940, 139.7472),           # 2-2-11 Kudan-Minami, Chiyoda
        "Indonesia": (35.6273, 139.7265),       # 5-2-9 Higashi-Gotanda, Shinagawa
        "Italy": (35.6468, 139.7414),           # 2-5-4 Mita, Minato
        "Mexico": (35.6769, 139.7432),          # 2-15-1 Nagatacho, Chiyoda
        "Russia": (35.6597, 139.7412),          # 2-1-1 Azabudai, Minato
        "Saudi Arabia": (35.6625, 139.7335),    # 1-8-4 Roppongi, Minato
        "South Africa": (35.6838, 139.7379),    # 1-4 Kojimachi, Chiyoda
        "South Korea": (35.6515, 139.7287),     # 1-2-5 Minami-Azabu, Minato
        "Turkey": (35.6732, 139.7084),          # 2-33-6 Jingumae, Shibuya
        "United Kingdom": (35.6889, 139.7415),  # 1 Ichibancho, Chiyoda
        "United States": (35.6717, 139.7356),   # 1-10-5 Akasaka, Minato
        "European Union": (35.6503, 139.7303),  # 4-6-28 Minami-Azabu, Minato
    },
    "China": {
        # Beijing — Embassies (Jianguomenwai / Sanlitun / Liangmaqiao)
        "Argentina": (39.9428, 116.4500),
        "Australia": (39.9406, 116.4415),       # 21 Dongzhimenwai Dajie
        "Brazil": (39.9124, 116.4310),          # 27 Guanghua Lu
        "Canada": (39.9406, 116.4432),          # 19 Dongzhimenwai Dajie
        "France": (39.9516, 116.4630),          # 60 Tianze Road
        "Germany": (39.9406, 116.4454),         # 17 Dongzhimenwai Dajie
        "India": (39.9521, 116.4610),           # 5 Liangmaqiao Bei Jie
        "Indonesia": (39.9394, 116.4537),
        "Italy": (39.9349, 116.4542),
        "Japan": (39.9210, 116.4380),           # 7 Ritan Lu
        "Mexico": (39.9429, 116.4525),
        "Russia": (39.9380, 116.4240),          # 4 Dongzhimennei Beizhongjie
        "Saudi Arabia": (39.9434, 116.4458),
        "South Africa": (39.9405, 116.4518),
        "South Korea": (39.9519, 116.4594),
        "Turkey": (39.9425, 116.4509),
        "United Kingdom": (39.9125, 116.4541),
        "United States": (39.9532, 116.4602),
        "European Union": (39.9431, 116.4425),  # 15 Dongzhimenwai Dajie
    },
    "Russia": {
        # Moscow — Embassies
        "Argentina": (55.7310, 37.6237),
        "Australia": (55.7526, 37.6425),
        "Brazil": (55.7584, 37.5879),
        "Canada": (55.7468, 37.5950),
        "China": (55.7108, 37.5162),
        "France": (55.7325, 37.6133),
        "Germany": (55.6714, 37.5274),
        "India": (55.7528, 37.6499),
        "Indonesia": (55.7380, 37.6301),
        "Italy": (55.7432, 37.5875),
        "Japan": (55.7779, 37.6419),
        "Mexico": (55.7432, 37.5898),
        "Saudi Arabia": (55.7393, 37.5833),
        "South Africa": (55.7590, 37.5944),
        "South Korea": (55.7379, 37.5752),
        "Turkey": (55.7410, 37.5743),
        "United Kingdom": (55.7506, 37.5774),   # Smolenskaya
        "United States": (55.7560, 37.5794),
        "European Union": (55.7460, 37.5900),
    },
    "Canada": {
        # Ottawa — Embassies / High Commissions
        "Argentina": (45.4214, -75.6958),
        "Australia": (45.4210, -75.6989),
        "Brazil": (45.4292, -75.6759),
        "China": (45.4363, -75.6850),
        "France": (45.4434, -75.6944),
        "Germany": (45.4185, -75.6817),
        "India": (45.4445, -75.6839),           # 10 Springfield Rd
        "Indonesia": (45.4103, -75.7340),
        "Italy": (45.4188, -75.7015),
        "Japan": (45.4333, -75.6987),
        "Mexico": (45.4217, -75.6978),
        "Russia": (45.4299, -75.6731),
        "Saudi Arabia": (45.4344, -75.6982),
        "South Africa": (45.4441, -75.6925),
        "South Korea": (45.4349, -75.6948),
        "Turkey": (45.4348, -75.6754),
        "United Kingdom": (45.4222, -75.6949),  # 80 Elgin St
        "United States": (45.4280, -75.6959),
        "European Union": (45.4198, -75.6951),
    },
    "Australia": {
        # Canberra — Embassies / High Commissions in Yarralumla
        "Argentina": (-35.3076, 149.1332),
        "Brazil": (-35.3033, 149.1174),
        "Canada": (-35.3095, 149.1290),
        "China": (-35.3022, 149.1210),
        "France": (-35.3041, 149.1178),
        "Germany": (-35.3077, 149.1127),
        "India": (-35.3060, 149.1200),
        "Indonesia": (-35.3039, 149.1166),
        "Italy": (-35.3112, 149.1142),
        "Japan": (-35.3100, 149.1114),
        "Mexico": (-35.3038, 149.1145),
        "Russia": (-35.3208, 149.1381),
        "Saudi Arabia": (-35.3114, 149.1061),
        "South Africa": (-35.3030, 149.1150),
        "South Korea": (-35.3050, 149.1170),
        "Turkey": (-35.3078, 149.1184),
        "United Kingdom": (-35.3013, 149.1246),
        "United States": (-35.3064, 149.1167),
        "European Union": (-35.3040, 149.1180),
    },
    "Brazil": {
        # Brasília — Embassies in Setor de Embaixadas
        "Argentina": (-15.8118, -47.8784),
        "Australia": (-15.8084, -47.8741),
        "Canada": (-15.8152, -47.8796),
        "China": (-15.8365, -47.9067),
        "France": (-15.8058, -47.8733),
        "Germany": (-15.8213, -47.8863),
        "India": (-15.8189, -47.8879),
        "Indonesia": (-15.8164, -47.8852),
        "Italy": (-15.8247, -47.8899),
        "Japan": (-15.8303, -47.8960),
        "Mexico": (-15.8151, -47.8839),
        "Russia": (-15.8048, -47.8755),
        "Saudi Arabia": (-15.8377, -47.8773),
        "South Africa": (-15.8075, -47.8738),
        "South Korea": (-15.7842, -47.8642),
        "Turkey": (-15.8182, -47.8872),
        "United Kingdom": (-15.8094, -47.8745),
        "United States": (-15.8043, -47.8728),
        "European Union": (-15.8436, -47.8952),
    },
    "Argentina": {
        # Buenos Aires — Embassies
        "Australia": (-34.5647, -58.4439),
        "Brazil": (-34.5922, -58.3830),
        "Canada": (-34.5798, -58.3977),
        "China": (-34.5628, -58.4961),
        "France": (-34.5918, -58.3825),
        "Germany": (-34.5668, -58.4394),
        "India": (-34.5966, -58.3706),
        "Indonesia": (-34.5792, -58.3997),
        "Italy": (-34.5824, -58.4026),
        "Japan": (-34.6016, -58.3688),
        "Mexico": (-34.5649, -58.4505),
        "Russia": (-34.5907, -58.3883),
        "Saudi Arabia": (-34.5794, -58.4020),
        "South Africa": (-34.5964, -58.3752),
        "South Korea": (-34.5793, -58.4052),
        "Turkey": (-34.5657, -58.4456),
        "United Kingdom": (-34.5852, -58.3952),
        "United States": (-34.5767, -58.4188),
        "European Union": (-34.5830, -58.4020),
    },
    "India": {
        # New Delhi — Embassies in Chanakyapuri
        "Argentina": (28.5700, 77.1580),
        "Australia": (28.5920, 77.1750),
        "Brazil": (28.6020, 77.2195),
        "Canada": (28.5950, 77.1830),
        "China": (28.6000, 77.1900),
        "France": (28.5956, 77.1877),
        "Germany": (28.5889, 77.1884),
        "Indonesia": (28.6022, 77.1947),
        "Italy": (28.5912, 77.1823),
        "Japan": (28.5903, 77.1891),
        "Mexico": (28.5801, 77.1640),
        "Russia": (28.5935, 77.1866),
        "Saudi Arabia": (28.5922, 77.1807),
        "South Africa": (28.5661, 77.1602),
        "South Korea": (28.5870, 77.1860),
        "Turkey": (28.5853, 77.1833),
        "United Kingdom": (28.5988, 77.1936),
        "United States": (28.5971, 77.1884),
        "European Union": (28.5950, 77.2300),   # 65 Golf Links
    },
    "Indonesia": {
        # Jakarta — Embassies in Menteng / Kuningan
        "Argentina": (-6.1857, 106.8222),
        "Australia": (-6.2329, 106.8337),
        "Brazil": (-6.2150, 106.8250),
        "Canada": (-6.2153, 106.8204),
        "China": (-6.2256, 106.8254),
        "France": (-6.1888, 106.8235),
        "Germany": (-6.1968, 106.8237),
        "India": (-6.2242, 106.8336),
        "Italy": (-6.2009, 106.8401),
        "Japan": (-6.1918, 106.8225),
        "Mexico": (-6.2292, 106.8252),
        "Russia": (-6.2204, 106.8311),
        "Saudi Arabia": (-6.2119, 106.8299),
        "South Africa": (-6.2174, 106.8128),
        "South Korea": (-6.2394, 106.8329),
        "Turkey": (-6.2362, 106.8286),
        "United Kingdom": (-6.2309, 106.8345),
        "United States": (-6.1811, 106.8309),
        "European Union": (-6.2250, 106.8300),
    },
    "Italy": {
        # Rome — Embassies
        "Argentina": (41.8988, 12.4971),
        "Australia": (41.9168, 12.5139),
        "Brazil": (41.8981, 12.4728),
        "Canada": (41.9223, 12.5012),
        "China": (41.9228, 12.4995),
        "France": (41.8948, 12.4708),
        "Germany": (41.9051, 12.5034),
        "India": (41.9028, 12.4916),
        "Indonesia": (41.9104, 12.4935),
        "Japan": (41.9081, 12.4948),
        "Mexico": (41.9131, 12.5094),
        "Russia": (41.9026, 12.4626),
        "Saudi Arabia": (41.9169, 12.4924),
        "South Africa": (41.9183, 12.5020),
        "South Korea": (41.9135, 12.4968),
        "Turkey": (41.9065, 12.5028),
        "United Kingdom": (41.9082, 12.5012),
        "United States": (41.9069, 12.4916),
        "European Union": (41.9010, 12.4830),
    },
    "Mexico": {
        # Mexico City — Embassies in Polanco / Lomas
        "Argentina": (19.4163, -99.2292),
        "Australia": (19.4298, -99.1832),
        "Brazil": (19.4153, -99.2138),
        "Canada": (19.4290, -99.1861),
        "China": (19.3360, -99.1972),
        "France": (19.4282, -99.1995),
        "Germany": (19.4347, -99.2052),
        "India": (19.4367, -99.1962),
        "Indonesia": (19.4280, -99.1970),
        "Italy": (19.4265, -99.1933),
        "Japan": (19.4263, -99.1708),
        "Russia": (19.4098, -99.1826),
        "Saudi Arabia": (19.4074, -99.2289),
        "South Africa": (19.4269, -99.1959),
        "South Korea": (19.4157, -99.2137),
        "Turkey": (19.4161, -99.2243),
        "United Kingdom": (19.4303, -99.1657),
        "United States": (19.4251, -99.2094),
        "European Union": (19.4122, -99.2211),
    },
    "Saudi Arabia": {
        # Riyadh — Embassies in Diplomatic Quarter
        "Argentina": (24.6834, 46.6796),
        "Australia": (24.6755, 46.6217),
        "Brazil": (24.6843, 46.6293),
        "Canada": (24.6818, 46.6273),
        "China": (24.6733, 46.6263),
        "France": (24.6846, 46.6281),
        "Germany": (24.6862, 46.6235),
        "India": (24.6859, 46.6309),
        "Indonesia": (24.6814, 46.6250),
        "Italy": (24.6849, 46.6290),
        "Japan": (24.6866, 46.6246),
        "Mexico": (24.6858, 46.6253),
        "Russia": (24.6830, 46.6270),
        "South Africa": (24.7021, 46.6184),
        "South Korea": (24.6840, 46.6260),
        "Turkey": (24.6803, 46.6210),
        "United Kingdom": (24.6880, 46.6274),
        "United States": (24.6725, 46.6191),
        "European Union": (24.6850, 46.6290),
    },
    "South Africa": {
        # Pretoria — Embassies / High Commissions
        "Argentina": (-25.7492, 28.2354),
        "Australia": (-25.7650, 28.2280),
        "Brazil": (-25.7874, 28.2790),
        "Canada": (-25.7620, 28.2300),
        "China": (-25.7447, 28.2289),
        "France": (-25.7724, 28.2268),
        "Germany": (-25.7706, 28.2225),
        "India": (-25.7580, 28.2350),
        "Indonesia": (-25.7471, 28.2270),
        "Italy": (-25.7412, 28.2190),
        "Japan": (-25.7723, 28.2139),
        "Mexico": (-25.7708, 28.2366),
        "Russia": (-25.7615, 28.2476),
        "Saudi Arabia": (-25.7572, 28.2385),
        "South Korea": (-25.7700, 28.2400),
        "Turkey": (-25.7738, 28.2367),
        "United Kingdom": (-25.7457, 28.2268),
        "United States": (-25.7462, 28.2236),
        "European Union": (-25.7550, 28.2300),
    },
    "South Korea": {
        # Seoul — Embassies
        "Argentina": (37.5361, 126.9874),
        "Australia": (37.5712, 126.9778),
        "Brazil": (37.5816, 126.9804),
        "Canada": (37.5669, 126.9709),
        "China": (37.5630, 126.9830),
        "France": (37.5614, 126.9655),
        "Germany": (37.5559, 126.9735),
        "India": (37.5355, 127.0111),
        "Indonesia": (37.5185, 126.9316),
        "Italy": (37.5372, 127.0055),
        "Japan": (37.5752, 126.9801),
        "Mexico": (37.5755, 126.9805),
        "Russia": (37.5649, 126.9718),
        "Saudi Arabia": (37.5317, 126.9917),
        "South Africa": (37.5359, 127.0117),
        "Turkey": (37.5530, 126.9750),
        "United Kingdom": (37.5673, 126.9747),
        "United States": (37.5732, 126.9778),
        "European Union": (37.5600, 126.9780),
    },
    "Turkey": {
        # Ankara — Embassies in Çankaya district
        "Argentina": (39.8881, 32.8722),
        "Australia": (39.8957, 32.8797),
        "Brazil": (39.8962, 32.8700),
        "Canada": (39.8925, 32.8559),
        "China": (39.8517, 32.8323),
        "France": (39.9026, 32.8558),
        "Germany": (39.9054, 32.8564),
        "India": (39.8896, 32.8559),
        "Indonesia": (39.8702, 32.8559),
        "Italy": (39.9041, 32.8576),
        "Japan": (39.8942, 32.8700),
        "Mexico": (39.8881, 32.8496),
        "Russia": (39.8936, 32.8529),
        "Saudi Arabia": (39.8960, 32.8645),
        "South Africa": (39.8914, 32.8815),
        "South Korea": (39.8958, 32.8565),
        "United Kingdom": (39.8897, 32.8583),
        "United States": (39.9085, 32.8033),
        "European Union": (39.8959, 32.8794),
    },
    "European Union": {
        # Brussels — Missions/Embassies to the EU
        "Argentina": (50.8258, 4.3649),
        "Australia": (50.8411, 4.3669),
        "Brazil": (50.8357, 4.4061),
        "Canada": (50.8407, 4.3666),
        "China": (50.8403, 4.3705),
        "France": (50.8468, 4.3680),
        "Germany": (50.8439, 4.3738),
        "India": (50.8201, 4.3660),
        "Indonesia": (50.8384, 4.4347),
        "Italy": (50.8463, 4.3709),
        "Japan": (50.8408, 4.3780),
        "Mexico": (50.8083, 4.3850),
        "Russia": (50.8056, 4.3538),
        "Saudi Arabia": (50.8101, 4.3820),
        "South Africa": (50.8413, 4.3688),
        "South Korea": (50.7957, 4.4026),
        "Turkey": (50.8419, 4.3677),
        "United Kingdom": (50.8417, 4.3845),
        "United States": (50.8445, 4.3670),
    },
}

# Country flag emoji mapping
FLAGS = {
    "Argentina": "\U0001F1E6\U0001F1F7",
    "Australia": "\U0001F1E6\U0001F1FA",
    "Brazil": "\U0001F1E7\U0001F1F7",
    "Canada": "\U0001F1E8\U0001F1E6",
    "China": "\U0001F1E8\U0001F1F3",
    "France": "\U0001F1EB\U0001F1F7",
    "Germany": "\U0001F1E9\U0001F1EA",
    "India": "\U0001F1EE\U0001F1F3",
    "Indonesia": "\U0001F1EE\U0001F1E9",
    "Italy": "\U0001F1EE\U0001F1F9",
    "Japan": "\U0001F1EF\U0001F1F5",
    "Mexico": "\U0001F1F2\U0001F1FD",
    "Russia": "\U0001F1F7\U0001F1FA",
    "Saudi Arabia": "\U0001F1F8\U0001F1E6",
    "South Africa": "\U0001F1FF\U0001F1E6",
    "South Korea": "\U0001F1F0\U0001F1F7",
    "Turkey": "\U0001F1F9\U0001F1F7",
    "United Kingdom": "\U0001F1EC\U0001F1E7",
    "United States": "\U0001F1FA\U0001F1F8",
    "European Union": "\U0001F1EA\U0001F1FA",
}

# Color mapping for each country (for map markers)
COUNTRY_COLORS = {
    "Argentina": "#75AADB",
    "Australia": "#003399",
    "Brazil": "#009739",
    "Canada": "#FF0000",
    "China": "#DE2910",
    "France": "#002395",
    "Germany": "#000000",
    "India": "#FF9933",
    "Indonesia": "#FF0000",
    "Italy": "#009246",
    "Japan": "#BC002D",
    "Mexico": "#006847",
    "Russia": "#0039A6",
    "Saudi Arabia": "#006C35",
    "South Africa": "#007A4D",
    "South Korea": "#003478",
    "Turkey": "#E30A17",
    "United Kingdom": "#00247D",
    "United States": "#3C3B6E",
    "European Union": "#003399",
}


def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on Earth (in km)."""
    R = 6371.0  # Earth's radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def compute_distances():
    """
    Compute distances from each embassy to the host country's power center.

    Returns a dict: {host_country: {origin_country: distance_km, ...}, ...}
    """
    distances = {}
    for host_country, embassies in EMBASSIES.items():
        pc = POWER_CENTERS[host_country]
        distances[host_country] = {}
        for origin_country, (e_lat, e_lon) in embassies.items():
            dist = haversine_km(pc["lat"], pc["lon"], e_lat, e_lon)
            distances[host_country][origin_country] = round(dist, 2)
    return distances


def get_statistics():
    """Compute summary statistics for embassy distances."""
    distances = compute_distances()
    stats = {}

    for host_country, embassy_distances in distances.items():
        values = list(embassy_distances.values())
        sorted_embassies = sorted(embassy_distances.items(), key=lambda x: x[1])
        stats[host_country] = {
            "closest": sorted_embassies[0],
            "farthest": sorted_embassies[-1],
            "average": round(sum(values) / len(values), 2),
            "all_sorted": sorted_embassies,
        }

    return stats
