from locust import HttpUser, task
from random import randint, choice

class WebsiteUser(HttpUser): 

    @task
    def load(self):

        catalogue = self.client.get("catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("")
        self.client.get("login", headers={"Authorization":"Basic dXNlcjpwYXNzd29yZA=="})
        self.client.get("category.html")
        self.client.get("detail.html?id={}".format(item_id))
        self.client.delete("cart")
        self.client.post("cart", json={"id": item_id, "quantity": 1})
        self.client.get("basket.html")
        self.client.post("orders")

    @task 
    def main(self): 
        self.client.get(url='')
    @task 
    def catalogue(self): 
        self.client.get(url="catalogue").json()

# import base64

# from locust import HttpUser, TaskSet, task
# from random import randint, choice


# class WebTasks(TaskSet):

#     @task
#     def load(self):
#         base64string = base64.encodestring('%s:%s' % ('user', 'password')).replace('\n', '')

#         catalogue = self.client.get("/catalogue").json()
#         category_item = choice(catalogue)
#         item_id = category_item["id"]

#         self.client.get("/")
#         self.client.get("/login", headers={"Authorization":"Basic %s" % base64string})
#         self.client.get("/category.html")
#         self.client.get("/detail.html?id={}".format(item_id))
#         self.client.delete("/cart")
#         self.client.post("/cart", json={"id": item_id, "quantity": 1})
#         self.client.get("/basket.html")
#         self.client.post("/orders")


# class Web(HttpUser):
#     task_set = WebTasks
#     min_wait = 0
#     max_wait = 0
