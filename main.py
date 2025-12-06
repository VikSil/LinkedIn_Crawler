# Global imports
from bs4 import BeautifulSoup as bs
from os.path import isfile
from pathlib import Path
from selenium.webdriver.common.by import By
from typing import Dict, List

import pandas as pd
import os

# Local imports
from browser import Browser
from config import *


BASE_DIR = Path(__file__).resolve().parent


def main():

    refresh_masterlist()


def check_if_jobs_page_empty(browser: Browser) -> bool:
    empty_text = browser.get_element(By.XPATH, f'//h1[contains(text(), "find a match for")]')
    if empty_text is not None:
        return True
    return False


def enhance_company_list(filepath: str = None, filedir: str = None, check_against_masterlist: bool = True) -> None:

    if filepath is None and filedir is None:
        print('Please provide either file or directory for processing')
        return

    company_files = []
    if filepath is not None:
        company_files.append(filepath)
    else:
        dir_path = filedir
        company_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if isfile(os.path.join(dir_path, f))]

    if os.path.isfile(f'{BASE_DIR}{COMPANIES_MASTERLIST}'):
        masterfile_df = pd.read_csv(f'{BASE_DIR}{COMPANIES_MASTERLIST}')
        skip_company_ids = masterfile_df['COMPANY_ID'].to_list()

    try:
        for file in company_files:
            print(f'Processing file {file}')
            companies_df_in = pd.read_csv(file)
            companies_list_out = []

            for index, row in companies_df_in.iterrows():
                if 'COMPANY_NAME' in row:
                    print(f'Processing company record - {row['COMPANY_NAME']}')

                if check_against_masterlist and is_in_masterlist(company_row=row):
                    print(f'Company already in masterlist. Will skip.')
                    continue

                if 'URL' not in row:
                    company_url = get_company_named_link(row['COMPANY_ID'])
                else:
                    company_url = row['URL']

                company_details = {}
                if company_url is not None:
                    company_details = get_company_details(url=company_url)

                company_id = None
                if 'COMPANY_ID' in row:
                    company_id = row['COMPANY_ID']
                elif 'COMPANY_ID' in company_details:
                    company_id = company_details['COMPANY_ID']

                company_name = None
                if 'COMPANY_NAME' in row:
                    company_name = row['COMPANY_NAME']
                elif 'COMPANY_NAME' in company_details:
                    company_name = company_details['COMPANY_NAME']

                company_sector = None
                if 'INDUSTRY' in row:
                    company_sector = row['INDUSTRY']
                elif 'INDUSTRY' in company_details:
                    company_sector = company_details['INDUSTRY']

                company_hq = None
                if 'LOCATION' in row:
                    company_hq = row['LOCATION']
                elif 'LOCATION' in company_details:
                    company_hq = company_details['LOCATION']

                company_description = None
                if 'DESCRIPTION' in row:
                    company_description = row['DESCRIPTION']
                elif 'DESCRIPTION' in company_details:
                    company_description = company_details['DESCRIPTION']

                company_dict = {
                    'COMPANY_ID': company_id,
                    'COMPANY_NAME': company_name,
                    'URL': company_url,
                    'INDUSTRY': company_sector,
                    'LOCATION': company_hq,
                    'DESCRIPTION': company_description,
                }
                companies_list_out.append(company_dict)

    except Exception as e:
        print('Something went wrong')
        print(e)

    finally:
        new_file_name = Path(file).stem
        companies_df_out = pd.DataFrame(companies_list_out)
        companies_df_out.to_csv(
            f'{BASE_DIR}{ENHANCED_COMPANY_LIST_DIR}{new_file_name}.csv',
            index=False,
        )


def get_company_details(name: str = None, url: str = None) -> Dict[str, str]:
    browser = Browser()

    company_url = url
    if name is not None:
        company_url = f'https://uk.linkedin.com/company/{name}'

    browser.open_page(company_url)
    browser.sleep(2)
    reject_login(browser)
    reject_cookies(browser)
    reject_popup(browser)

    company_id = browser.get_element(By.XPATH, f'//a[contains(@href, "org-employees_cta_face-pile-cta")]')
    if company_id is not None:
        company_id = company_id.get_attribute('href').split('%255D')[0].split('%3D%255B')[-1].split('%252C%2B')[-1]

    company_name = browser.get_element(By.CLASS_NAME, 'top-card-layout__title')
    if company_name is not None:
        company_name = company_name.text.strip()

    company_industry = browser.get_element(By.CLASS_NAME, 'top-card-layout__headline')
    if company_industry is not None:
        company_industry = company_industry.text.strip()

    company_hq = browser.get_element(By.CLASS_NAME, 'top-card-layout__first-subline')
    if company_hq is not None:
        company_hq = company_hq.get_attribute('innerHTML').split('<')[0].strip()

    company_description = browser.get_element(By.CLASS_NAME, 'top-card-layout__second-subline')
    if company_description is not None:
        company_description = company_description.text.strip()

    company_dict = {
        'COMPANY_ID': company_id,
        'COMPANY_NAME': company_name,
        'INDUSTRY': company_industry,
        'LOCATION': company_hq,
        'DESCRIPTION': company_description,
    }
    return company_dict


def get_company_named_link(company_id: int, browser: Browser = None) -> str:
    if browser is None:
        browser = Browser()
        open_jobs_page(browser, company_id, 'worldwide')

    named_link = None

    try:
        if not check_if_jobs_page_empty(browser):
            job_list = get_job_cards(browser)
            named_link = job_list[0].find('a', {'class': 'hidden-nested-link'})['href'].split('?')[0]
    except Exception as e:
        print(e)
        print('Something went wrong. Is the job list open?')
    return named_link


def get_job_cards(browser: Browser) -> List[bs]:
    html = browser.get_element(By.TAG_NAME, 'html').get_attribute('innerHTML')
    soup = bs(html, 'html.parser')

    jobs_ul = soup.find('ul', {'class': 'jobs-search__results-list'})
    job_li_list = jobs_ul.findChildren('li', recursive=False)

    return job_li_list


def is_in_masterlist(company_id: str = None, company_name: str = None, company_row: pd.Series = None) -> bool:
    if os.path.isfile(f'{BASE_DIR}{COMPANIES_MASTERLIST}'):
        masterfile_df = pd.read_csv(f'{BASE_DIR}{COMPANIES_MASTERLIST}')

        if company_id is not None and company_id in masterfile_df['COMPANY_ID'].to_list():
            return True

        elif company_name is not None and company_name in masterfile_df['COMPANY_NAME'].to_list():
            return True

        elif isinstance(company_row, pd.Series):
            if 'COMPANY_ID' in company_row:
                if company_row['COMPANY_ID'] in masterfile_df['COMPANY_ID'].to_list():
                    return True

            elif 'COMPANY_NAME' in company_row:
                if company_row['COMPANY_NAME'] in masterfile_df['COMPANY_NAME'].to_list():
                    return True

            elif 'URL' in company_row:
                if company_row['URL'] in masterfile_df['URL'].to_list():
                    return True

    return False


def open_jobs_page(browser: Browser, company_id: int, location: str = DEFAULT_LOCATION) -> None:
    if location is None:
        location = 'worldwide'

    url = f'https://www.linkedin.com/jobs/search?f_C={company_id}&location={location.replace(' ', '%20')}&position=1&pageNum=0'
    browser.open_page(url)
    browser.sleep(2)

    reject_login(browser)
    reject_cookies(browser)
    reject_popup(browser)


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


def refresh_masterlist(filedir: str = None) -> None:
    if filedir is None:
        filedir = f'{BASE_DIR}{ENHANCED_COMPANY_LIST_DIR}'
    else:
        filedir = f'{BASE_DIR}{filedir}'

    if os.path.isfile(f'{BASE_DIR}{COMPANIES_MASTERLIST}'):
        masterfile_df = pd.read_csv(f'{BASE_DIR}{COMPANIES_MASTERLIST}')
    else:
        masterfile_df = pd.DataFrame(
            {
                'COMPANY_ID': pd.Series(dtype='int'),
                'COMPANY_NAME': pd.Series(dtype='str'),
                'URL': pd.Series(dtype='str'),
                'INDUSTRY': pd.Series(dtype='str'),
                'LOCATION': pd.Series(dtype='str'),
                'DESCRIPTION': pd.Series(dtype='str'),
            }
        )

    masterfile_company_ids = masterfile_df['COMPANY_ID'].to_list()

    company_files = [os.path.join(filedir, f) for f in os.listdir(filedir) if isfile(os.path.join(filedir, f))]

    for company_file in company_files:
        print(f'Consolidating records from {company_file}')
        company_df = pd.read_csv(company_file)
        filtered_company_df = company_df[~company_df['COMPANY_ID'].isin(masterfile_company_ids)]
        masterfile_df = pd.concat([masterfile_df, filtered_company_df], ignore_index=True, sort=False)
        masterfile_company_ids += filtered_company_df['COMPANY_ID'].to_list()

    masterfile_df.to_csv(f'{BASE_DIR}{COMPANIES_MASTERLIST}', index=False)


def reject_cookies(browser: Browser) -> None:
    reject_btn = browser.get_element(By.XPATH, f"//button[contains(text(), 'Reject')]")
    if reject_btn is not None:
        browser.click_button(By.XPATH, f"//button[contains(text(), 'Reject')]")


def reject_login(browser: Browser) -> None:
    login_overlay = browser.get_element(By.CLASS_NAME, 'contextual-sign-in-modal__modal-dismiss')
    if login_overlay is not None:
        browser.click_button(By.CLASS_NAME, 'contextual-sign-in-modal__modal-dismiss')
    else:
        login_overlay = browser.get_element(By.ID, 'base-contextual-sign-in-modal')
        if login_overlay is not None:
            result = browser.delete_element(By.ID, 'base-contextual-sign-in-modal')


def reject_popup(browser: Browser) -> None:
    login_overlay = browser.get_element(By.CLASS_NAME, 'cta-modal__dismiss-btn')
    if login_overlay is not None:
        browser.click_button(By.CLASS_NAME, 'cta-modal__dismiss-btn')


if __name__ == '__main__':
    main()
