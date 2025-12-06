import platform

operating_system = platform.platform()

if 'Windows' in operating_system:
    SLASH = '\\'    
else:
    SLASH = '/'

COMPANIES_MASTERLIST = f'{SLASH}company_lists{SLASH}company_masterlist.csv'
DEFAULT_LOCATION = 'United Kingdom'
ENHANCED_COMPANY_LIST_DIR = f'{SLASH}company_lists{SLASH}enhanced_lists{SLASH}'

PROCESSED_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}processed{SLASH}'
RAW_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}new{SLASH}'
RECRUITER_COMPANIES_LIST_DIR = f'{SLASH}company_lists{SLASH}recruiter_interests{SLASH}'
