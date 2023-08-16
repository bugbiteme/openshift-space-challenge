# catalyst

Make sure to have the ``oc`` command-line tool installed.

Create a python environment and install all python modules dependancies.
``pip install -r requirements.txt``

Log on your OpenShift cluster using the ``oc login`` as admin.

Run ``ansible-playbook deploy.yaml``.

In addition to deploying CTFd, the playbook creates player accounts on OCP.
Credentials are in ``credentials.txt``.

Run ``make-user-creds.sh`` to generate a new batch credentials.
