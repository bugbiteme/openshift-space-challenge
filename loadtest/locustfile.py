from locust import HttpUser, task
import json, random

# Get the token below from the Settings section of the ctfd application.
# Run this like so:
# $ locust --host https://space-ctfd.apps.cluster-mcrhz.mcrhz.sandbox742.opentlc.com/
# Then point your browser at http://localhost:8089.
# Set the number of users to 350 and start testing.

class ChangeName(HttpUser):
    @task(1)
    def change_name(self):
        payload = { 'name': f'name{random.randint(1, 3000000)}' }
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token ctfd_d0d12a5a1b5401b9961b8138fed9bb5cdce0ec633af82e07f1caaf32d10cde81' }
        response = self.client.patch(f"api/v1/users/{random.randint(1, 400)}", data=json.dumps(payload), headers=headers)
        
