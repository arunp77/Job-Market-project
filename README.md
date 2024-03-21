# InsightfulRecruit: Unveiling the Job Market Landscape through Data Engineering

[![GitHub repo size](https://img.shields.io/github/repo-size/arunp77/Job-Market-project)](https://github.com/arunp77/Job-Market-project) [![Top Language](https://img.shields.io/github/languages/top/arunp77/Job-Market-project)](https://github.com/arunp77/Job-Market-project)

 
## Overview

This project aims to showcase skills in data engineering by gathering and analyzing job market data from various sources. By the end of the project, we aim to have a clearer understanding of the job market, including sectors with the highest demand, required skills, active cities, and more.

## Prerequisite
- **WebScrapping:** BeautifulSoup, Selenium
- **Python:** -3.10.x
- **NoSQL:** ElasticSearch 
- **Docker Compose:** Docker v2.15.1
- **API:** fastAPI

## Project Stages

The project is divided into the following stages and sub-stages

### 1. Collecting Data

- **Objective**: Gather job offers and company information from multiple sources.
- **Sources**:
  - [The Muse API](https://www.themuse.com/developers/api/v2)
  - [Adzuna API](https://developer.adzuna.com/)
  - Web Scraping from stepstone using selenium and beautifulsoup.
- **Tools**:
  - Requests library for API interaction.
  - Postman tool (for testing)
  - Web scraping techniques.

### 2. Data Modeling

- **Objective**: Create a data lake or database to store collected data.
- **Approaches**: 
  - NoSQL Database (Elastic search)
- **Tools**:
  - Elasticsearch
  - UML Diagram for data model visualization.

### 3. Data Consumption

<details>
<summary>Click to expand</summary>
  In our present scenario, we get data from 3 sources, MUSE API, Adjurna API, and Stepstone.
</details>

- **Objective**: Analyze the collected data to derive insights about the job market.
- **Analysis Tasks**:
  - Number of offers per company.
  - Sectors with the highest recruitment.
  - Ideal job criteria (location, technologies, sector, level).
- **Tools**:
  - Dash for visualization.
  - Elasticsearch for statistics.
  - Queries fed by the database(s).

### 4. Going into Production

- **Objective**: Deploy project components and create APIs for data retrieval.
- **Components**:
  - API using FastAPI or Flask.
  - Docker containers for each component. Steps for the dockerization are available in [Docker-image file](Docker-image-integration.md).
- **Tools**:
  - FastAPI or Flask for API development.
  - Docker for containerization.
  - Docker Compose for container orchestration.

### 5. Automation of Flow (future work)

- **Objective**: Automate data retrieval from sources.
- **Tools**:
  - Apache Airflow for workflow automation.
  - Python file defining the DAG.

## Project structure:

```
Job-Market-project/
│
├── .env                                        # Environment variables file
├── .github/
│   └── workflows/                              # GitHub Actions workflow directory
│       └── ci.yml                              # CI/CD workflow file
├── images/                                     # Directory for image files
├── scripts/                                    # Directory for scripts
│   ├── web_scraping/                          # Directory for web scraping scripts
│   │   ├── adjurna.py                          # Script for Adjurna data extraction
│   │   ├── muse.py                             # Script for Muse data extraction
│   │   └── ss.py                               # Script for Stepstone data extraction
│   ├── etl/                                    # Directory for ETL scripts
│   │   └── etlscript.py                        # ETL script
│   ├── database/                               # Directory for database scripts
│   │   └── db_connection.py                    # Database connection script
│   └── plot_analysis/                         # Directory for plot analysis scripts
│        └── uscase.py                          # Use case plot analysis script
├── data/                                      # Directory for data
│   ├── scraped_data/                          # Directory for scraped data
│   │   ├── adjurna/                           # Directory for Adjurna data
│   │   │   └── csv/                           # Directory for CSV files
│   │   │       └── adzuna_scrapped_data.csv   # Adjurna scraped data file
│   │   ├── muse/                              # Directory for Muse data
│   │   │   └── csv/                           # Directory for CSV files
│   │   │       └── muse_scrapped_data.csv     # Muse scraped data file
│   │   └── ss/                                # Directory for Stepstone data
│   │       └── ss_datascience_germany_20240221.csv # Stepstone data file
│   └── processed_data/                        # Directory for processed data
│       ├── adjurna_processed_data/            # Directory for processed Adjurna data
│       │   └── adzuna_scrapped_data.csv       # Processed Adjurna data file
│       ├── muse_processed_data/               # Directory for processed Muse data
│       │   └── muse_scrapped_data.csv         # Processed Muse data file
│       └── ss_processed_data/                 # Directory for processed Stepstone data
│           └── ss_datascience_germany_20240221.csv # Processed Stepstone data file
├── README.md                                  # Readme file
├── ProjectPlan.md                             # Project plan file
├── LICENSE.md                                 # License file
├── Contribution-guidelines.md                 # Contribution guidelines file
└── UserStories.md                             # User stories file

```

## Docker Images

We also maintain a Docker image for our project, available on Docker Hub at [arunp77/job_market](https://hub.docker.com/r/arunp77/job_market), ensuring accessibility and easy deployment.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/arunp77/Job-Market-Project.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Job-Market-Project
   ```
3. Follow the instructions in each stage's folder to execute the corresponding tasks.

## Launch on Binder
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/arunp77/Job-Market-project/main)

## Contributors
This project is a group effort and would not have been possible without the help of these contributors:

- [Arun Kumar Pandey](https://github.com/arunp77): [Email to Arun](arunp77@gmail.com)
- [Brindha Sadayappan](https://github.com/brindha311): [Email to Brindha](brindha311@gmail.com)
- [Khushboo Goyal](https://github.com/khushboo026): [Email to Khusboo](khushboo026@gmail.com)
- **Cohort Leader:** [Vincent](https://github.com/AtoutPillard)

## Feedback and Contributions

Feedback and contributions are welcome! Please open an issue or create a pull request if you have any suggestions or improvements. [Contribution guidelines](Contribution-guidelines.md)

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Resource

> [Link to the docs for project](https://docs.google.com/document/d/1glRF8HtyNqcHnZud8KqeJYLdC07_MqjuFGJVOuw7gBc/edit)

<!--------reference: https://github.com/kevAnto/fast-API/tree/main>
