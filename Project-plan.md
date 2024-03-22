# Various steps to work on the project

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


These are the instructions given to us from the Course cohost and is available at [Datascientist.com project doc](https://docs.google.com/document/d/1glRF8HtyNqcHnZud8KqeJYLdC07_MqjuFGJVOuw7gBc/edit) 

# Contributions
## Step 0 
### Framing (first meeting):
| Task | Description and links|
|-------------------|--------------------|
| Introduction of each team member | All ready done in the [Readme.md file](README.md) |
| Explanation of the project framework (the different stages) | Each step is discussed below |

## Step 1
### Discovery of available data sources & Data organization: Deadline 10 February
| Task | Description and links| Responsibilities to whom |
|-------------------|--------------------|---------------|
| Define the context and scope of the project (don't underestimate this step) | This project aims to showcase skills in data engineering by gathering and analyzing job market data from various sources. By the end of the project, we aim to have a clearer understanding of the job market, including sectors with the highest demand, required skills, active cities, and more.| |
| Get to grips with the different data sources (explore the APIs provided but available to you, the web pages for which you will apply webs-scraping) | [The Muse API](https://www.themuse.com/developers/api/v2) and [Adzuna API](https://developer.adzuna.com/)|  Arun + Brindha |
| You will be asked to organize the data via different databases: Relational or NoSQL | | |
| You will have to think about the data architecture, including how to link the different data together. | We need to do some data cleaning before creating bases and datalake. | Khushboo  |

- Deliverable:
    - Report explaining the different data sources with examples of collected data
    - Any document explaining the chosen architecture (UML diagram)
    - File implementing the databases
    - Query file

## Step 2 
### Data consumption: Deadline Feb 17th 2024
| Task | Description and links| Responsibilities to whom |
|-------------------|--------------------|---------------|
| Once your data is organized, it needs to be consumed, this is not the initial role of a Data Engineer, but for the data pipeline to be complete, you need to have this part. | | | 
| It will be expected to make a notebook where you do Machine Learning on it or a dashboard with Dash | | |

## Step 3
### Deployment: Deadline  Feb 24th 2024
| Task | Description and links| Responsibilities to whom |
|-------------------|--------------------|---------------|
| Create an API of the Machine Learning model or Dash application | | |
| Perform unit tests on your API | | |
| Contain this API via Docker and databases | | |

## Step 4 
### Automate the flows: Optional step (Mar 10th 2024)
| Task | Description and links| Responsibilities to whom |
|-------------------|--------------------|---------------|
| Automate the various previous steps so that the application is continuously functional | | |
| Set up a CI/CD pipeline to efficiently update your application | | |

## Step 5
### Demonstration of the application + Support (30 minutes): Mar 18th 2024
- Explain the progress of your project
- Explain the architecture chosen when organizing the data
- Show that the application is functional
