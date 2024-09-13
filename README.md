# OpenShift Space Challenge

## Requirements

Currently tested to work on OCP 4.16 as deployed by "Red Hat OpenShift
Container Platform Cluster (AWS)" from demo.redhat.com.

The game requires a control cluster, and one or more player clusters.
The control cluster can also be a game cluster, however, to ensure a
good experience, especially for large groups, we recommend deploying a
control cluster and one or more player clusters.

Make sure to have the `oc` and `jq` command-line tools installed on your laptop.

## Getting started

Request "Red Hat OpenShift Container Platform Cluster (AWS)" from
demo.redhat.com. Provisioning time is usually around 60 mins.

On your laptop, create a python environment and install all python
modules dependencies.
`pip install -r requirements.txt`

Create a file called game-clusters.yaml that identifies the domains
for both the control and player clusters.  It should look something
like this.
```
---
control_cluster: cluster-abcd5.acd5.sandbox1337.opentlc.com

player_clusters:
 - cluster-vnb47.vnb47.sandbox3000.opentlc.com
 - cluster-n5mmk.n5mmk.sandbox290.opentlc.com
 - cluster-94bh6.94bh6.sandbox1488.opentlc.com
```

Log on to your control cluster using `oc login` as admin and run
the deployment playbook like so:
`ansible-playbook deploy-control-cluster.yaml`.

For each player cluster, log into the cluster using `oc login` as
admin and run the player cluster deployment playbook like so:
`ansible-playbook deploy-player-cluster.yaml`.

In addition to deploying CTFd, and Gitea, the playbook creates player
accounts on OCP, CTFd and Gitea. Credentials for CTFd, gitea and OCP
are found in `credentials.txt`. PDF handouts are
`credential-handouts.pdf`.

## CTFd configuration

This is the tool we are using to define all the challenges and track
user points as those challenges are solved.  More information about
this tool here: https://ctfd.io/

The `deploy-control-cluster.yaml` playbook installs and configures
CTFd automatically.

Get CTFd URL: `oc get route -n ctfd`

Admin access: username = `admin`, password = `redhat123`.
User access: see `credentials.csv`` file.

## Validate that Gitea is running fine

This Git repo will be required to solve some challenges. All users
have access to their own git repo using their credentials.

Get Gitea URL: `oc get route -n gitea`
User access: see `credentials.csv`` file.

## Optional scripts and tools

### Make new user credentials

Run `make-user-creds.sh` if you ever wish to generate new batch credentials.

### Add more challenges

Using the admin access in CTFd, you can create new challenges. Under Config/Backup, you can export all your configuration including your new challenges. `challenges.json` is the file you need. That said, this file must be cleaned up as a template before pushing it to your git repo. You can use this script to generate this file: `cat challenges.json | update-challenges.sh > ./ctfd-config/db/challenges.json.in`

# Authors

The OpenShift Space Challenge was created by Anthony Green, Marco Berube and Nikhil Malvankar.
