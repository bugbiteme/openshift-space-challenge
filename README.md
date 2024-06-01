# OpenShift Space Challenge

## Requirements

Currently tested to work on "Red Hat OpenShift Container Platform 4.13 Workshop" from demo.redhat.com
Make sure to have the `oc` and `jq` command-line tools installed on your laptop.

## Getting started

Request "Red Hat OpenShift Container Platform 4.13 Workshop" from demo.redhat.com. Provisioning time is usually around 60 mins.

On your laptop, create a python environment and install all python modules dependancies.
`pip install -r requirements.txt`

Log on your OpenShift cluster using the `oc login` as admin.

Run `ansible-playbook deploy.yaml`.

In addition to deploying CTFd, and gitea, the playbook creates player
accounts on OCP, ctfd and gitea. Gitea credentials are
playerX/openshift. Credentials for CTFd and OCP are found in
`credentials.txt`. PDF handouts are `credential-handouts.pdf`.

## CTFd configuration

This is the tool we are using to define all the challenges and track user points as those challenges are solved.
More information about this tool here: https://ctfd.io/

Get CTFd URL: `oc get route -n ctfd`

Go through the setup wizard (your answers don't matter as they will be overwritten by our zipped conf files later).
Once completed,

- click on "Admin Panel" in top menu.
- click on "Config" in top menu.
- click on "Backup" in side menu.
- click on "Import" tab, "Choose File" and upload `ctfd-upload-me.zip` created by the `deploy.yaml` playbook.

This will take a few seconds and will send you back to the Login page.
Admin access: username = `admin`, password = `redhat123`.
User access: see `credentials.csv`` file.

## Validate that Gitea is running fine

This Git repo will be required to solve some challenges. All users have access to their own git repo using their credentials.

Get Gitea URL: `oc get route -n gitea`
User access: see `credentials.csv`` file.


## Running Judges required by some challenges.

Some challenges need a juge to get points or to receive some info on your app API endpoint.   You start all judges this way:
`ansible-playbook judge/deployments/deploy-judges.yaml`

This script will deploy all judges in the judge namespace.  Each judge will run in one pod, but you can scale those pods manually if needed.   

It's also possible to run any judge locally on your laptop.  Export your cluster domain before running your judge script:
`export CLUSTERDOMAIN=cluster-dgdbx.dgdbx.sandboxXXXX.opentlc.com`
`python judge/{judge_name}/app.py`



## Optional scripts and tools

### Make new user credentials

Run `make-user-creds.sh` if you ever wish to generate a new batch
credentials.

### Add more challenges

Using the admin access in CTFd, you can create new challenges. Under Config/Backup, you can export all your configuration including your new challenges. `challenges.json` is the file you need. That said, this file must be cleaned up as a template before pushing it to your git repo. You can use this script to generate this file: `cat challenges.json | update-challenges.sh > ./ctfd-config/db/challenges.json.in`

# Authors

The OpenShift Space Challenge was created by Anthony Green, Marco Berube and Nikhil Malvankar.
