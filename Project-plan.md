# Various steps to work on the project

These are the instructions given to us from the Course cohost and is available at [Datascientist.com project doc](https://docs.google.com/document/d/1glRF8HtyNqcHnZud8KqeJYLdC07_MqjuFGJVOuw7gBc/edit) 

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

- Deliverable :
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
