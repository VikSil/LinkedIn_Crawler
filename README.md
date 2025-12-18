# LinkedIn Crawler

This repo contains a set of scripts for scraping company and job advertisement data from LinkedIn website.

## How to use the scripts

In order to gather job advertisements you will first need to gather companies whose ads you want to check. There are two pathways to gathering companies.

1. Check companies that other people are interested in

    * Configure the following:

        * `FAILED_RECRUITER_INTERESTS_DIR` - where the HTML file will be moved to if parsing fails
        * `PROCESSED_RECRUITER_INTERESTS_DIR` - where the HTML file will be moved to if parsing is successful
        * `RAW_RECRUITER_INTERESTS_DIR` - put your starting HTML files here (see next point)
        * `RECRUITER_COMPANIES_LIST_DIR` - where companies list will be stored
    
    * Go to the profile page of your favourite person on LinkedIn. Perhaps, a recruiter who <s>works</s> gatekeeps in your industry, or a particularly connected peer. Scroll down to the bottom of the page and click on "Show all companies" in the "Interests" section. Scroll to the bottom of the page repeatedly until all companies have been loaded. Save the page to `RAW_RECRUITER_INTERESTS_DIR`. Inspecting the page and copying the top element is recommended, since only HTML is needed for the next steps, and saving all of the elements is much slower.

    * Run `parse_recruiter_interests` function. This will output the list of companies for further parsing.

<p style='color:red'> N.B. The first step is the only one you need to be logged into LinkedIn account for. All of the following steps <b>MUST</b> be done while logged out of LinkedIn website. Clearing your cookies is recommended.</p>

2. Check companies that are similar to another company

    * Configure the following:

        * `MAX_SIMILAR_COMPANIES` - once this number is reached the processing will stop
        * `SIMILAR_COMPANIES_LIST_DIR` - where companies list will be stored
        * `SKIP_INDUSTRIES` - industries that you are not interested in 
        * `SKIP_LOCATIONS` - locations that you are not interested in
        * `START_COMPANY_URL` - company that you want find similar companies to

    * Run `gather_companies` function. This will output the list of companies for further parsing.

Once you have gathered companies, you will need to enhance the data before you can use it for gathering the job advertisements.

3. * First configure the following:

        * `COMPANIES_MASTERLIST` - the file where all gathered companies will be listed
        * `ENHANCED_COMPANY_LIST_DIR` - intermediary directory for storing enhanced company lists

    * Run `enhance_company_list` function.
    * If you did not pass `add_to_masterlist = True` to the `enhance_company_list`, then run `refresh_masterlist`

4. To gather the jobs that you may be interested in:

    * Configure the following:

        * `COOLDOWN_DAYS` - the number of days to pass before checking for jobs at the same company again
        * `DEFAULT_LOCATION` - location where you are looking for jobs at
        * `JOBS_LAST_CHECK_DATES` - a file that will track when were jobs at each company last checked
        * `JOB_KEYWORDS` - keywords that you are looking for in jobs. The more of these you configure the longer it will take to run the script
        * `JOB_LIST_DIR` - where the list of job ads will be output
        * `SKIP_COMPANIES_NAMES` - names of companies that you are not interested in working at (used independently of `SKIP_COMPANIES_IDS`)
        * `SKIP_COMPANIES_IDS` - ids of companies that you are not interested in working at (used independently of `SKIP_COMPANIES_NAMES`)
        * `SKIP_JOBS_LIST` - job ads that have been encountered before
        * `SKIP_KEYWORDS` - keywords that you do not want in jobs, overrides `JOB_KEYWORDS`
        * `TARGET_INDUSTRIES` - industries that you are interested in

    * Run `gather_jobs` function. 

A list of job ads will be output to `JOB_LIST_DIR`.




# Is this legal?

Web-scraping is generally viewed as ***not illegal*** when it is publicly available data that is being scraped. Which it is in this case, since the scripts are designed to be used without signing into LinkedIn. 

At the same time, LinkedIn's `robots.txt` file states:

        # Notice: The use of robots or other automated means to access LinkedIn without
        # the express permission of LinkedIn is strictly prohibited.
        # See https://www.linkedin.com/legal/user-agreement.

However, it can be argued that since the scripts is designed to run **without** a LinkedIn account (and it may not work correctly if you are logged in!), this use falls outside of the user agreement. If it so happens that you don't have a LinkedIn account at all, then you definitely did not enter into a user agreement with them. However, LinkedIn can argue that the mere act of accessing the data hosted on LinkedIn, signed in or not, is equivalent to entering a legally biding contract with them. To which you can argue that:

* A. LinkedIn did not create any of the company or ad data, their users did. LinkedIn's own User Agreement states that the users remain the owners of the content, and LinkedIn has the license to: *"use, copy, modify, distribute, publicly perform and display, host, and process"* said content. So, you copying somebody else's content that LinkedIn distributed does not infringe on any of LinkedIn's rights as a licensee. And LinkedIn is not the owner of the content, so they cannot claim that *their* content was taken without their permission. They are also not a guardian of the content owners, and cannot act on the owners' behalf, or decide on their behalf who else accesses the content and by what means.

* B. LinkedIn distributes the content to the public without requiring authorisation. Why? They could have walled everything off. And yet they allow three job advertisements per page to be viewed by unauthorised users. They could have shown all of the advertisements, but they made the effort to limit the number of visible ads - why? Likely because there is no profit potential in showing all ads. LinkedIn make part of their profits from coaxing users into paying for Premium memberships that is *supposed to* grant better access to job advertisements. Without Premium membership, the algorithm feeds users with rotating ads from recruitment agencies who pay to LinkedIn to promote their ads. So displaying all of the ads to the public is not in LinkedIn's economic interests. And that's understandable. But LinkedIn could have also chosen to show none of the ads to the unauthorised public. And yet they do show some - why? Likely because it is the first step in the pipeline to profit. If you are not a user, they want to make you a user. So, LinkedIn shows you a little bit of what you *could* (allegedly) get access to if you were a user. Just enough to incentivise you to sign up. And that's how they convert you into a non-Premium user. Then they can start employing the tactics for converting you from a regular user to a paying Premium user... So, essentially, by looking at LinkedIn data while unauthorised you are accessing their advertisement data. And LinkedIn would have to argue that you are allowed to see their advertisement, but not allowed to record it. Which is a (morally) shaky argument, since it implies that they want a relationship where from the get-go you are allowed to benefit them, but not allowed to have a relationship that benefits you. 

Anyway. None of this is legal advice. For all practical purposes, it only becomes relevant if LinkedIn and/or content owners decide to take legal action. In which case - the courts will decide. Please consult legal professionals before using the scripts, if in doubt. And don't use any data you obtain for nefarious or commercial purposes, because that definitely can be illegal. 
