# Automated Docker Image Building with CI/CD Workflow Integration

Summary of the steps that one can take to create a Docker image  and integrate it into an existing CI/CD workflow. This guide will use GitHub Actions as the the continuous integration tool and is placed at [Github Action](https://github.com/arunp77/Job-Market-project/blob/main/.github/workflows/ci.yml).

## Steps

1. **DockerHub account creation:** Create a account at [Docker Hub](https://hub.docker.com/signup). Follow on screen descriptions. Choose Personal version. Verfiy the account creation at the email you registered for. If you have already created our account, login to the DOcker Hub account. 
2. **Generate Docker Access Token:** Navigate to the account settings. Go to the "Security" section and look for the option to generate an access token (Go to `My Profile > [Edit profile] > Security > Access Tokens > New Access Token`). It will ask you Access token description. In our case, I use `Job-Market-access-token` and then gave all the read, write, delete access. Then click generate the access token. 
   <img src="images/docker-access-token.png" alt="snapshot-access-token-Docker" width=50% height=auto>

   you must save the token at some safe place. It will be shown just once. 
3. **Setup GitHub Secrets:** Go to the Github repository. Next click settings tab and then 'Secrets and variables' (`setting > Secrets and variables > Actions`). Click on `New repository secret`. For the secret name, use `DOCKER_USERNAME` and for the secret value, paste your Docker Hub `username`. Repeat the above steps to add another secret named `DOCKER_PASSWORD`, using the Docker Hub access token as the secret value.
   
   <img src="images/Github-action.png" alt="access-token-Github" width=80% height=auto>

   Here the added secrets will be securely stored and accessible to the CI workflows in the `.github/workflows/ci.yml`. 

4. **Add Dockerfile:** Create a `Dockerfile` in the root directory for the project. This file contains instructions for building the Docker image, including setting up the environment and dependencies and it is named as [Dockerfile](Dockerfile) in the root directory. 
   
   |                                             Note                                                  |
|---------------------------------------------------------------------------------------------------|
| Here `.github/workflows/ci.yml` file can access ad use secrets using `{{ secrets.SECRET_NAME }}`  |
| syntax. When secrets are used in a workflow, their values are masked in the logs to prevent       |
| accidental exposure.                                                                              |
5. 
