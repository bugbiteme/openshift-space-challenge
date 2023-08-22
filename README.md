# catalyst

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

## Optional scripts and tools

### Make new user credentials

Run `make-user-creds.sh` if you ever wish to generate a new batch
credentials.

### Add more challenges

Using the admin access in CTFd, you can create new challenges. Under Config/Backup, you can export all your configuration including your new challenges. `challenges.json` is the file you need. That said, this file must be cleaned up as a template before pushing it to your git repo. You can use this script to generate this file: `cat challenges.json | update-challenges.sh > ./ctfd-config/db/challenges.json.in`
