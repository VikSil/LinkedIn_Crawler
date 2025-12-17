import platform

operating_system = platform.platform()

if 'Windows' in operating_system:
    SLASH = '\\'    
else:
    SLASH = '/'

COMPANIES_MASTERLIST = f'{SLASH}company_lists{SLASH}company_masterlist.csv'
DEFAULT_LOCATION = 'United Kingdom'
ENHANCED_COMPANY_LIST_DIR = f'{SLASH}company_lists{SLASH}enhanced_lists{SLASH}'
FAILED_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}failed{SLASH}'


MAX_SIMILAR_COMPANIES = 50

PROCESSED_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}processed{SLASH}'
RAW_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}new{SLASH}'
RECRUITER_COMPANIES_LIST_DIR = f'{SLASH}company_lists{SLASH}recruiter_interests{SLASH}'

SIMILAR_COMPANIES_LIST_DIR = f'{SLASH}company_lists{SLASH}similar_companies{SLASH}'
SKIP_INDUSTRIES = ['Construction','Retail',
'Administrative and Support Services',
'Advertising Services',
'Agriculture, Construction, Mining Machinery Manufacturing',
'Air, Water, and Waste Program Management',
'Apparel & Fashion',
'Apparel Manufacturing',
'Beverage Manufacturing',
'Boilers, Tanks, and Shipping Container Manufacturing',
'Building Materials',
'Business Consulting and Services',
'Business Content',
'Business Supplies & Equipment',
'Community Services',
'Dairy',
'Dairy Product Manufacturing',
'Distilleries',
'Events Services',
'Executive Search Services',
'Facilities Services',
'Farming',
'Fire Protection',
'Fisheries',
'Food & Beverages',
'Food and Beverage Manufacturing',
'Food and Beverage Retail',
'Food and Beverage Services',
'Food Production',
'Gambling Facilities and Casinos',
'Hospitality',
'Hospitals and Health Care',
'Human Resources',
'Human Resources Services',
'HVAC and Refrigeration Equipment Manufacturing',
'Individual and Family Services',
'Internet Marketplace Platforms',
'Law Enforcement',
'Medical Practices',
'Mental Health Care',
'Nursing Homes and Residential Care Facilities',
'Outsourcing and Offshoring Consulting',
'Outsourcing/Offshoring',
'Plastics Manufacturing',
'Primary and Secondary Education',
'Retail',
'Retail Apparel and Fashion',
'Seafood Product Manufacturing',
'Staffing and Recruiting',
'Textile Manufacturing',
                   ]
SKIP_LOCATIONS = []
START_COMPANY_URL = 'https://uk.linkedin.com/company/tesla-motors'

