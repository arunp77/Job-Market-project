Elastic search offers several advantages in job market analysis:

1. **Fast Search Performance**: Elastic search is renowned for its speed and efficiency in searching and retrieving data. In the context of job market analysis, this means users can quickly search through large volumes of job listings and related data to extract valuable insights.

2. **Scalability**: Elastic search is highly scalable, allowing users to easily scale up or down based on their needs. This is crucial for job market analysis, where data volumes can vary significantly over time, especially during peak hiring seasons or in rapidly changing job markets.

3. **Full-text Search**: Elastic search supports full-text search capabilities, enabling users to search for keywords or phrases within job descriptions, titles, skills, and other relevant fields. This allows for more comprehensive and accurate analysis of job market trends and patterns.

4. **Open Source**: Elastic search is an open-source tool, which means it is freely available and supported by a vast community of developers and users. This open-source nature fosters innovation, flexibility, and collaboration in job market analysis initiatives, as users can leverage community-contributed plugins, extensions, and enhancements to tailor Elastic search to their specific needs.

By leveraging these advantages, organizations and researchers can gain valuable insights into the job market landscape, including emerging trends, skill requirements, salary benchmarks, and competitive dynamics, to inform strategic decisions related to talent acquisition, workforce planning, and career development.

Steps to launch the Elastic search and load data,

1. Run the docker-compose.yml as below where the repo present
docker-compose up -d. 
2. open kibana in any browser using :: http://localhost:5601/
3. To access it, open pane like,
![alt text](image.png)
4. Then run the python script in scripts/database/db_connection.py to load the dataset.
5. This script will establish connection to Elastic search and create job_list table and schema as below
+---------------------------------------+
|                JobListing             |
+---------------------------------------+
| - id: String                          |
| - title: String                       |
| - company: String                     |
| - location: String                    |
| - job_posted: Date                    |
| - categories: String                  |
| - experience_level: String            |
| - full_part_time: String              |
| - description: String                 |
| - link: String                        |
| - source: String                      |
+---------------------------------------+
6. The above schema will accomodate all 3 dataset. 
