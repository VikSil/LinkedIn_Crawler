import platform

operating_system = platform.platform()

if 'Windows' in operating_system:
    SLASH = '\\'
else:
    SLASH = '/'


RAW_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}new{SLASH}'
PROCESSED_RECRUITER_INTERESTS_DIR = f'{SLASH}recruiter_interests_html{SLASH}processed{SLASH}'
RECRUITER_COMPANIES_LIST_DIR = f'{SLASH}company_lists{SLASH}recruiter_interests{SLASH}'
