REGISTRATION_CATEGORIES = [
    ('district', 'District'),
    ('state', 'State'),
    ('national', 'National'),
]

GENDERS = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

TSHIRT_SIZES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
]

LEVELS = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]

ROLE = [
    ("Right Hand Batsman", "Right Hand Batsman"),
    ("Left Hand Batsman", "Left Hand Batsman"),
    ("Opener", "Opener"),
    ("Middle-Order Batsman", "Middle-Order Batsman"),
    ("Lower-Order Batsman", "Lower-Order Batsman"),
    ("Wicketkeeper Batsman", "Wicketkeeper"),
    ("Right Hand Bowler", "Right Hand Bowler"),
    ("Left Hand Bowler", "Left Hand Bowler"),
    ("Fast Bowler", "Fast Bowler"),
    ("Medium-Pace Bowler", "Medium-Pace Bowler"),
    ("Spin Bowler", "Spin Bowler"),
    ("All-Rounder", "All-Rounder"),
    ("Opening Bowler", "Opening Bowler"),
    ("Death Bowler", "Death Bowler"),
    ("Part-Time Bowler", "Part-Time Bowler"),
    ("Fielding Specialist", "Fielding Specialist"),
    ("Power-Hitter", "Power-Hitter"),
]


BOWLING_ARMS = [
    ('left', 'Left'),
    ('right', 'Right'),
]

BOWLING_PACES = [
    ('fast', 'Fast'),
    ('medium', 'Medium'),
    ('spin', 'Spin'),
]

FIRST_PREFERENCES = [
    ('batting', 'Batting'),
    ('bowling', 'Bowling'),
]

CAPTAIN_EXPERIENCES = [
    ('yes', 'Yes'),
    ('no', 'No'),
]

STATES = [
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CT', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OD', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
    ('AN', 'Andaman and Nicobar Islands'),
    ('CH', 'Chandigarh'),
    ('DH', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DL', 'Delhi'),
    ('JK', 'Jammu and Kashmir'),
    ('LA', 'Ladakh'),
    ('LD', 'Lakshadweep'),
    ('PY', 'Puducherry'),
]


DISTRICT_ZONE_MAP = {
    'Kanyakumari': 'ZONE A',
    'Tirunelveli': 'ZONE A',
    'Thoothukudi': 'ZONE A',
    'Tenkasi': 'ZONE A',
    'Virudhunagar': 'ZONE A',
    'Ramanathapuram': 'ZONE A',
    'Theni': 'ZONE A',
    'Madurai': 'ZONE A',
    'Sivagangai': 'ZONE A',
    'Dindigul': 'ZONE A',
    'Pudukkottai': 'ZONE B',
    'Thanjavur': 'ZONE B',
    'Thiruvarur': 'ZONE B',
    'Nagapattinam': 'ZONE B',
    'Tiruchi': 'ZONE B',
    'Ariyalur': 'ZONE B',
    'Mayiladuthurai': 'ZONE B',
    'Perambalur': 'ZONE B',
    'Cuddalore': 'ZONE B',
    'Chennai': 'ZONE C',
    'Tiruvallur': 'ZONE C',
    'Kanchipuram': 'ZONE C',
    'Chengalpattu': 'ZONE C',
    'Tiruvannamalai': 'ZONE C',
    'Tirupattur': 'ZONE C',
    'Vellore': 'ZONE C',
    'Ranipet': 'ZONE C',
    'Kallakkurichi': 'ZONE C',
    'Villuppuram': 'ZONE C',
    'Krishnagiri': 'ZONE D',
    'Dharmapuri': 'ZONE D',
    'Nilgiris': 'ZONE D',
    'Erode': 'ZONE D',
    'Salem': 'ZONE D',
    'Coimbatore': 'ZONE D',
    'Tiruppur': 'ZONE D',
    'Namakkal': 'ZONE D',
    'Karur': 'ZONE D',
}

DISTRICT_CHOICES = [(district, district) for district in DISTRICT_ZONE_MAP.keys()]
