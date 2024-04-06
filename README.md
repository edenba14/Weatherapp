# GitLab Pipeline with AWS GitLab Server, GitLab Runner, and Vault

This project implements a GitLab pipeline using GitLab Server hosted on an AWS instance, GitLab Runner instance, and Vault instance. The pipeline is configured to build, test, and push Docker images.


## Prerequisites
* AWS account with access to EC2 instances.
* GitLab Server instance running on an EC2 instance.
* GitLab Runner instance running on a separate EC2 instance.
* Vault instance for managing secrets.
## Setting Gitlab server
To set up the GitLab Server, Docker Compose was used.   
Below is a summary of the Docker Compose setup:
``` yaml
services:
  gitlab:
    image: 'gitlab/gitlab-ce:latest'
    restart: always
    hostname: '34.193.158.247'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://34.193.158.247'
        gitlab_rails['gitlab_shell_ssh_port'] = 2424
        registry_external_url 'http://34.193.158.247:5050/'
        registry['enable'] = true
        registry['insecure_skip_verify'] = true
        registry['env'] = {
                  "REGISTRY_HTTP_RELATIVEURLS" => true
                }
        gitlab_rails['registry_enabled'] = true
    ports:
      - '80:80'
      - '2424:2424'
      - '5050:5050'
    volumes:
      - '/srv/gitlab/config:/etc/gitlab'
      - '/srv/gitlab/logs:/var/log/gitlab'
      - '/srv/gitlab/data:/var/opt/gitlab'
```

## Setting up a gitlab-runner instance
First on an Ec2-instance we will install gitlab runner using this commands:
```bash
sudo apt update
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
sudo apt install gitlab-runner
```
## Setting Hashicorp Vault server
Install the vaule by this commands: 
```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt install vault
```
Since we are using http make sure the etc/vault.d/vault.hcl file is configures this way: 
```conf
# HTTP listener
listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 1
}
```
```bash
sudo systemctl start vault.service

export VAULT_ADDR="https://your_server:8200"

vault operator init -key-shares=3 -key-threshold=2

vault operator unseal
```
and then enter the unseal keys you got after the init command.

## Configuration
### gitlab-runner

Follow these steps to set up the GitLab Runner:

1. install Docker and Vault CLI on the gitlab-runner instance.
2. register the gitlab runner to the gitlab project using this guide: https://docs.gitlab.com/ee/tutorials/create_register_first_runner/

### gitlab server
The GitLab Server instance should have the following configurations:

* Set up a project/repository on the GitLab Server to trigger the pipeline.
* Set a runner on the project and connect it to your runner instance using the register command on the gitlab-runner and the token that was given to you on the server

### Hashicorp vault instance
* Create a K/V secert engine
* Create the secrets key you will need for your project.
* Create for the secerts a policy of permissions (Read,update..etc)
* Create an AppRole authentication to authenticate in the pipeline using vault_role_id and vault_secret_id
 
### Gitlab server variables
The following GitLab CI/CD variables need to be set:

* VAULT_ROLE_ID: Role ID for authenticating with Vault.
* VAULT_SECRET_ID: Secret ID for authenticating with Vault.
* ACCESS_TOKEN: Personal access token for Docker registry authentication.
## Pipeline stages
* Build: Build the Docker image using Environment variables saved in Hashicorp vault.
* Test: Perform test of accessability on the Docker image.
* Push: Push the Docker image to the GitLab Container Registry.
* Clean: Cleans my workspace.
