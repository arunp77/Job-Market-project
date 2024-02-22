# InsightfulRecruit: Unveiling the Job Market Landscape through Data Engineering

## Overview

This project aims to showcase skills in data engineering by gathering and analyzing job market data from various sources. By the end of the project, we aim to have a clearer understanding of the job market, including sectors with the highest demand, required skills, active cities, and more.

## Prerequisite
- **WebScrapping:** BeautifulSoup
- Python -3.10.x
- **SQL/NoSQL:** MySQL DBMS, MongoDB DBMS
- Dash, ElasticSearch
- Docker Compose: v2.15.1
- Docker
- Airflow

## Project Stages

The project is divided into the following stages and sub-stages

### 1. Collecting Data

- **Objective**: Gather job offers and company information from multiple sources.
- **Sources**:
  - [The Muse API](https://www.themuse.com/developers/api/v2)
  - [Adzuna API](https://developer.adzuna.com/)
  - Web Scraping from platforms like Welcome To The Jungle, LinkedIn, etc.
- **Tools**:
  - Requests library for API interaction.
  - Postman tool (for testing)
  - Web scraping techniques.

### 2. Data Modeling

- **Objective**: Create a data lake or databases to store collected data.
- **Approaches**: Either of the databases
  - SQL Database
  - NoSQL Database (e.g., MongoDB)
- **Tools**:
  - SQL (e.g., Hbase)
  - NoSQL (e.g., MongoDB)
  - Elasticsearch
  - UML Diagram for data model visualization (Justification for choice of DBMS(es)).

### 3. Data Consumption

<details>
<summary>Click to expand</summary>
  We need to fix the following question: "Find the job of your dreams: location; technologies; sector; level (senior etc...)"
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
  - Docker containers for each component.
- **Tools**:
  - FastAPI or Flask for API development.
  - Docker for containerization.
  - Docker Compose for container orchestration.

### 5. Automation of Flow (Optional)

- **Objective**: Automate data retrieval from sources.
- **Tools**:
  - Apache Airflow for workflow automation.
  - Python file defining the DAG.

## Project structure:

```
Job-Market-project/
│
├── .env                                         # to save the APIs secret keys and are ignored before pushing the files to GitHub via .gitignore
├── .github/
│   └── workflows/                               # Contains all the ci-cd yml and the Issue/bug files 
│       └── ci.yml                               # GitHub Actions workflow file
|── images /
│       └── (all image files in the directory)
├── scripts/
│   ├── web_scraping/
│   │   ├── adjurna.py                           # Adjurna python file to extract data using API
│   │   ├── muse.py                              # Muse python file to extract data using API
│   │   ├── ss.py                                # Stepstone python file to extract 
│   │   └── requirements.txt                     # Dependent files
│   └── etl/
│       └── etl_script.py                        # The etl python file
│
├── data/
│   ├── scraped_data/
│   │   └── ajurna                               # Adjurna data
│   │          └── ajurna_Json/ajurna_data.Json
│   │          └── ajurna_csv/ajurna_data.csv
│   │   └── muse/                                # Muse data
│   │          └── muse_Json/muse_data.Json
│   │          └── muse_csv/muse_data.csv
│   │   └── ss/                                  # Stepstone data
│   │          └── ss_Json/muse_data.Json
│   │          └── ss_csv/muse_data.csv
│   └── processed_data/
│       └── (empty folder for storing processed data)
│
└── documentation/
    └── README.md
    └──  ProjectPlan.md
    └──  LICENSE.md
    └──  Contribution-guidelines.md
    └──  UserStories.md
```

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
4. For the contributions, go to [COntribution guidelines](Contribution-guidelines.md)

## Contributors

- [Arun Kumar Pandey](https://github.com/arunp77)
  - [Email to Arun](arunp77@gmail.com)
- [Brindha Sadayappan](https://github.com/brindha311)
  - [Email to Brindha](brindha311@gmail.com)
- [Khushboo Goyal](https://github.com/khushboo026)
  - [Email to Khusboo](khushboo026@gmail.com)
- [Vincent](https://github.com/AtoutPillard)

## Feedback and Contributions

Feedback and contributions are welcome! If you have any suggestions or improvements, please open an issue or create a pull request.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Resource

> [Link to the docs for project](https://docs.google.com/document/d/1glRF8HtyNqcHnZud8KqeJYLdC07_MqjuFGJVOuw7gBc/edit)
