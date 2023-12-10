from locust import HttpUser, task

class WebsiteUser(HttpUser): 
    
    @task 
    def hello_world(self): 
        self.client.get(url='/')

    @task 
    def square_numbers(self): 
        self.client.get(url='/square-root') 
    
    @task 
    def cube_numbers(self): 
        self.client.get(url='/cube-root')