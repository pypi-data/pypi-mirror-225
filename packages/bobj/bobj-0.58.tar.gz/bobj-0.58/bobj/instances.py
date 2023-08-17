import requests
from . import support as sup


class _instancesmanagement:
    
    def __init__(self, R):
        self.url = R.url
        self.header = sup.create_header(R.logon_token)
        
        
    def _job_count(self, **kwargs):
        
        #url and param defination
        url = f"{self.url}/bionbi/job"
        
        param = sup.instance_params(self, **kwargs)
        response = requests.get(url, headers=self.header, params=param)
        
        full_url = response.url
        print("Full URL:", full_url)
        
        if response.status_code != 200:
            sup.inform_bobj_error(response)

        # Parsing the response to return job count details
        entries = response.json().get('feed', {}).get('entry', [])
        job_count_details = [{'count': entry['content']['attrs']['count'], 'status_type': entry['content']['attrs']['status_type']} for entry in entries]

        return job_count_details
    
    
    
    def _list_jobs(self, **kwargs):
        
        #url and param defination
        url = f'{self.url}/bionbi/job/list'
        param = sup.instance_params(self, **kwargs)
        print (url)     
        print (param)
        
        response = requests.get(url, headers=self.header, params=param)
        full_url = response.url
        print("Full URL:", full_url)
        
        # Check for successful response
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
    
    
    
