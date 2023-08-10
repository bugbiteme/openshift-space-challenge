# catalyst

This playbook requires the ``oc`` command.
After logging into the OCP cluster as admin, run ``ansible-playbook deploy.yaml``.

In addition to deploying CTFd, the playbook creates player accounts on OCP.
Credentials are in ``credentials.txt``.
Run ``make-user-creds.sh`` to generate a new batch credentials.
