from locust import HttpUser, task, between


class BookaUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_books(self):
        self.client.get("/api/books/")
