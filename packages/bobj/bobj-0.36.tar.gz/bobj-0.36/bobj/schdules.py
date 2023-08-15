import requests
from . import support as sup


class schedule_management:
    
    def __init__(self, R):
        self.url = R.url
        self.header = sup.create_header(self.R.logon_token)
        
        

    def job_count(self, **kwargs):
        
        #url and param defination
        url = f"{self.url}/bionbi/job"
        params = sup.schedules_params(**kwargs)
        
        # Make the GET request
        response = requests.get(url, headers=self.header, params=params)
        if response.status_code != 200:
            sup.inform_bobj_error(response)

        # Parsing the response to return job count details
        entries = response.json().get('feed', {}).get('entry', [])
        job_count_details = [{'count': entry['content']['attrs']['count'], 'status_type': entry['content']['attrs']['status_type']} for entry in entries]

        return job_count_details
    
    
    
    def list_jobs(self, **kwargs):
        
        #url and param defination
        url = f'{self.url}/bionbi/job/list'
        params = sup.schedules_params(**kwargs)
        
        response = requests.get(url, headers=self.headers, params=params)
        # Check for successful response
        if response.status_code != 200:
            sup.inform_bobj_error(response)

        # Parsing the response and creating a dictionary of jobs
        jobs = []
        feed = response.json().get('feed', {})
        entries = feed.get('entry', [])
        for entry in entries:
            attrs = entry.get('content', {}).get('attrs', {})
            job = {key: value for key, value in attrs.items()}
            jobs.append(job)


        return jobs
    
    
    
