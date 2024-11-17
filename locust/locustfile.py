from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    pass
    # wait_time = between(1, 5)

    # @task
    # def load_homepage(self):
    #     self.client.get("/")
    
    # @task
    # def create_short_link(self):
    #     self.client.post("/api/v1/short-links/", json={
    #         "original_url": "https://example.com"
    #     })
