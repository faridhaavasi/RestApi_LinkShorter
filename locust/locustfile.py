from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)  
    token = None 

    def on_start(self):
        response = self.client.post('authentication/authentication_v1_api_login_token_create', data={
            'email': 'admin@gmail.com',
            'password': '1'
         }).json()
        if response.status_code == 200:
            self.token = response.json().get('access')
            print(f"Token received: {self.token}")
        else:
            print(f"Failed to log in: {response.status_code} - {response.text}")

    @task
    def get_profile(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.client.get('accounts/accounts_api_v1_profile_retrieve', headers=headers)
            if response.status_code == 200:
                print("Profile data fetched successfully!")
            else:
                print(f"Failed to fetch profile: {response.status_code} - {response.text}")
        else:
            print("No token available. Cannot fetch profile.")

