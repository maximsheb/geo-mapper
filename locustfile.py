from locust import HttpUser, task, between
# from prometheus_client import start_http_server
# import threading


# def start_prometheus_server():
#     start_http_server(9101)
#
#
# threading.Thread(target=start_prometheus_server, daemon=True).start()


class GeoMapperUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def calculate_distance(self):
        with open("/mnt/locust/test_file.csv", "rb") as file:
            self.client.post("/calculateDistance", files={"file": file})
