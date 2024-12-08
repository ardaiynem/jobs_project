import json
import scrapy
import os
from jobs_project.items import JobsProjectItem
from dateutil import parser

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'jobs_project.pipelines.JobsProjectPipeline': 300,
        },
    }

    def __init__(self):
        super(JobSpider, self).__init__()

    def start_requests(self):
        """
        Reads the JSON files and yields a request object for each file.
        """
        root_dir = os.path.abspath(os.path.join('/', 'usr', 'src', 'app'))

        # Add your local JSON file paths here
        files = ['s01.json', 's02.json']
        for file_path in files:
            yield scrapy.Request(
                url='file://' + os.path.join(root_dir, file_path),
                callback=self.parse_page)


    def parse_page(self, response):
        """
        Parses the JSON data from the response object and extracts the job data.
        
        Args:
            response (scrapy.http.Response): The response object containing the JSON data.
        
        Yields:
            item: A JobsProjectItem object containing the extracted job data.
        """
        # Load the JSON data
        data = json.loads(response.text)
        jobs = data.get('jobs')

        # Extract the job data into JobsProjectItem objects
        for job in jobs:
            job_data = job.get('data', {})
            item = JobsProjectItem()
            item['slug'] = job_data.get('slug', '')
            item['language'] = job_data.get('language', '')
            item['languages'] = job_data.get('languages', [])
            item['req_id'] = job_data.get('req_id', '')
            item['title'] = job_data.get('title', '')
            item['description'] = job_data.get('description', '')
            item['street_address'] = job_data.get('street_address', '')
            item['city'] = job_data.get('city', '')
            item['state'] = job_data.get('state', '')
            item['country_code'] = job_data.get('country_code', '')
            item['postal_code'] = job_data.get('postal_code', '')
            item['location_type'] = job_data.get('location_type', '')
            item['latitude'] = job_data.get('latitude', 0)
            item['longitude'] = job_data.get('longitude', 0)
            item['categories'] = job_data.get('categories', [])
            item['tags'] = job_data.get('tags', [])
            item['tags5'] = job_data.get('tags5', [])
            item['tags6'] = job_data.get('tags6', [])
            item['brand'] = job_data.get('brand', '')
            item['promotion_value'] = job_data.get('promotion_value', 0)
            item['salary_currency'] = job_data.get('salary_currency', '')
            item['salary_value'] = job_data.get('salary_value', 0)
            item['salary_min_value'] = job_data.get('salary_min_value', 0)
            item['salary_max_value'] = job_data.get('salary_max_value', 0)
            item['benefits'] = job_data.get('benefits', [])
            item['employment_type'] = job_data.get('employment_type', '')
            item['hiring_organization'] = job_data.get('hiring_organization', '')
            item['source'] = job_data.get('source', '')
            item['apply_url'] = job_data.get('apply_url', '')
            item['internal'] = job_data.get('internal', False)
            item['searchable'] = job_data.get('searchable', False)
            item['applyable'] = job_data.get('applyable', False)
            item['li_easy_applyable'] = job_data.get('li_easy_applyable', False)
            item['ats_code'] = job_data.get('ats_code', '')
            item['meta_data'] = job_data.get('meta_data', {})
            item['update_date'] = parser.parse(job_data.get('update_date', '')) if job_data.get('update_date') else None
            item['create_date'] = parser.parse(job_data.get('create_date', '')) if job_data.get('create_date') else None
            item['category'] = job_data.get('category', [])
            item['full_location'] = job_data.get('full_location', '')
            item['short_location'] = job_data.get('short_location', '')
            yield item