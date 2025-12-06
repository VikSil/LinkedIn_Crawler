# Global imports
from bs4 import BeautifulSoup as bs
from os.path import isfile

import pandas as pd
import os

# # Local imports
from config import *

# Imports from root dir
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def main():

    parse_recruiter_interests()


def parse_recruiter_interests(filepath: str = None) -> None:

    company_files = []
    if filepath is not None:
        company_files.append(filepath)
    else:
        dir_path = f'{BASE_DIR}{RAW_RECRUITER_INTERESTS_DIR}'
        company_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if isfile(os.path.join(dir_path, f))]

    for file in company_files:
        with open(file, encoding='utf8') as f:
            soup = bs(f, 'html.parser')

        recruiter = (
            soup.find('div', {'class': 'artdeco-entity-lockup__title ember-view'}).text.strip().replace(' ', '_')
        )
        print(f'Processing interests of {recruiter}')

        companies = soup.find_all('div', {'data-view-name': 'profile-component-entity'})

        companies_data = []
        for company in companies:

            url = company.find('a', {'data-field': 'active_tab_companies_interests'})
            if url is not None:
                url = url['href']
                company_id = url.split('/')[-2]
                company_name = company.find('span', {'class': 'visually-hidden'}).text.strip()
                companies_data.append({'COMPANY_ID': company_id, 'COMPANY_NAME': company_name})

        companies_df = pd.DataFrame(companies_data)
        companies_df.to_csv(
            f'{BASE_DIR}{RECRUITER_COMPANIES_LIST_DIR}{recruiter}.csv',
            index=False,
        )

        moved_file_name = Path(file).name
        os.rename(file, f'{BASE_DIR}{PROCESSED_RECRUITER_INTERESTS_DIR}{moved_file_name}')


if __name__ == '__main__':
    main()
