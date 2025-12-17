import platform

operating_system = platform.platform()

if 'Windows' in operating_system:
    SLASH = '\\'    
else:
    SLASH = '/'

COMPANIES_MASTERLIST = f'{SLASH}company_lists{SLASH}company_masterlist.csv'
COOLDOWN_DAYS = 7
DEFAULT_LOCATION = 'United Kingdom'
ENHANCED_COMPANY_LIST_DIR = f'{SLASH}company_lists{SLASH}enhanced_lists{SLASH}'
FAILED_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}failed{SLASH}'

JOBS_LAST_CHECK_DATES = f'{SLASH}job_lists{SLASH}CHECK_DATES.csv'
JOB_KEYWORDS = [
    'Python',
    'Quantitative',
]
JOB_LIST_DIR = f'{SLASH}job_lists{SLASH}'

MAX_SIMILAR_COMPANIES = 50

PROCESSED_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}processed{SLASH}'
RAW_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}new{SLASH}'
RECRUITER_COMPANIES_LIST_DIR = f'{SLASH}company_lists{SLASH}recruiter_interests{SLASH}'

SIMILAR_COMPANIES_LIST_DIR = f'{SLASH}company_lists{SLASH}similar_companies{SLASH}'
SKIP_COMPANIES_NAMES = ['hackajob', 'Aurora Energy Research', 'Bending Spoons', 'Tech Returners', 'Man Group', 'Man AHL', 'Man GLG', 'Man Numeric', 'Man FRM','Kraken']
SKIP_COMPANIES_IDS = [5396873, 3354218, 3175130, 28657301, 6903]
SKIP_INDUSTRIES = [
    'Construction',
]
SKIP_JOBS_LIST = f'{SLASH}job_lists{SLASH}CHECKED_JOBS.csv'
SKIP_KEYWORDS = [
    'Java',
    'Manager',
    'Head',
    'Support',
    'Cloud',
    '365',
    'DevOps',
    'People',
    'HR',
    ' AI ',
    'Salesforce',
    'Mechanical',
    'Nuclear',
    'Electrical',
    'Graduate',
    'Internship',
    'Intern',
    'LLM',
    'Sales',
    'Marketing',
    'Scala',
    'Prompt'
]
SKIP_LOCATIONS = []
START_COMPANY_URL = 'https://uk.linkedin.com/company/tesla-motors'

TARGET_INDUSTRIES = [
    #'Financial Services',
    'Banking',
    # 'Insurance',
]

