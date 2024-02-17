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
        # self.client.delete("cart")
        self.client.post("cart", json={"id": item_id, "quantity": 1})
        self.client.get("basket.html")
        self.client.post("orders")

    @task 
    def main(self): 
        self.client.get(url='')
    @task 
    def catalogue(self): 
        self.client.get(url="catalogue").json()

