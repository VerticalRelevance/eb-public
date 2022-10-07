## Experiment Broker

Repository for core Resiliency code

### Clone the Repo
First, clone this repository:
```shell
git clone https://github.com/VerticalRelevance/resiliency-framework-code
```
The master branch of this tool is the AWS Branch. All development is done via a personalized branch, *i.e.* ` user_aws `. Once code has been tested and finalized, a Pull Request can be made to the AWS branch to merge the code with the main framework.

 Next, navigate to the checkout the appropriate branch.
```shell
cd resiliency-framework-code
git checkout <branch>
```
This repository holds the actions and probes used in the [Resiliency Testing Experiments](https://github.com/VerticalRelevance/resiliency-framework-experiments.git) repository. 

### Installation
Before installing the code dependencies, we recommend installing and preparing a virtual environment

#### MacOS
First, install pyenv and pyenv virtual-env to allow the creation of new environments. You must then configure your shell to use it. Note: this installation requires [Homebrew](https://brew.sh/) to be installed as well. If it is not, follow the instructions on the linked page to install.
```sh
brew install pyenv pyenv-virtualenv
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
eval "$(pyenv virtualenv-init -)"  >> ~/.zshrc
```
Then, you will need install the version of python which is used by the lambda. You can then create a virtual environment and name it as you please.

```
pyenv install 3.8.11
pyenv virtualenv 3.8.11 <env_name>
```

Then, use the `requirements.txt` file to install the dependencies necessary for development.
```
cd resiliencyvr
pip install -r requirements.txt
```
You are now set to begin creating actions and probes.
## Creating Actions and Probes

Actions and probes are the way that an experiment is able to both induce failure in the environment and get information from the environment. 
* **Actions**:  Python functions referenced by experiments which either induce failure or have some sort of effect on the environment. 
* **Probes**: Python functions which retrieve information from the environment.
