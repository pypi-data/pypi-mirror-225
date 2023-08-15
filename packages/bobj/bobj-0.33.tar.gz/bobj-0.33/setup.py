from setuptools import setup, find_packages


long_description = """
This library provides a solution for automating SAP Business Objects (BOBJ) tasks. It has been designed to accelerate processes and empower practitioners with the following capabilities:

1. **User Management**
   <div style="display: flex; justify-content: space-between;">
     <div style="width: 48%;">Listing: View all users</div>
     <div style="width: 48%;">Creating: Add new users</div>
   </div>
   <div style="display: flex; justify-content: space-between;">
     <div style="width: 48%;">Modifying/Updating: Edit existing user details</div>
     <div style="width: 48%;">Deleting: Remove users</div>
   </div>

2. **Folder Management**
   <div style="display: flex; justify-content: space-between;">
     <div style="width: 48%;">Listing: View all folders</div>
     <div style="width: 48%;">Creating: Create new folders</div>
   </div>
   <div style="display: flex; justify-content: space-between;">
     <div style="width: 48%;">Modifying/Updating: Edit existing folder details</div>
     <div style="width: 48%;">Deleting: Remove folders</div>
   </div>

3. **Server Management**
   <div style="display: flex; justify-content: space-between;">
     <div style="width: 48%;">Utilization: Monitor server usage</div>
     <div style="width: 48%;">Hung-up Notification: Receive notifications for hung-up issues</div>
   </div>
   <div style="display: flex; justify-content: space-between;">
     <div style="width: 48%;">Event Server Health: Check the health status of event servers</div>
     <div style="width: 48%;">... (Additional features)</div>
   </div>

4. **Instance Management**
   <div style="display: flex; justify-content: space-between;">
     <div style="width: 48%;">
       Running Instances: View details including
       <ul>
         <li>Historical Running Time</li>
         <li>Database Details</li>
         <li>History of Failures and Totals</li>
       </ul>
     </div>
     <div style="width: 48%;">
       Failed Instances: Examine details including
       <ul>
         <li>Historical Running Time</li>
         <li>Database Details</li>
         <li>History of Failures and Totals</li>
       </ul>
     </div>
   </div>
   <div style="display: flex; justify-content: space-between;">
     <div style="width: 48%;">
       Upcoming Instances: Preview details including
       <ul>
         <li>Historical Running Time</li>
         <li>Database Details</li>
         <li>History of Failures and Totals</li>
       </ul>
     </div>
     <div style="width: 48%;"></div>
   </div>

This library serves as an essential tool for managing and maintaining SAP Business Objects efficiently and effectively.
"""

setup(
    name='bobj', # You can replace this with your chosen name
    version='0.33', # Indicating beta version
    packages=find_packages(),
    install_requires=[
        'requests>=2.25', # Required dependency
    ],
    author='Rajat Gupta',
    author_email='rajatgupta.1988@gmail.com',
    description='A comprehensive toolkit designed to streamline tasks for SAP Business Objects administrators',
    long_description=long_description,
    long_description_content_type="text/markdown", 
)
    
