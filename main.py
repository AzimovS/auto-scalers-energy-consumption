from flask import Flask

app = Flask(__name__) 

@app.route('/') 
def hello_world(): 
    return 'Hello World' 

@app.route('/cube-root/') 
def get_cube_root(): 
    new_list = [x**3 for x in range(0, 1001)] 
    return f'{new_list}' 

@app.route('/square-root/') 
def get_square_root(): 
    new_list = [x**2 for x in range(0, 1001)] 
    return f'{new_list}' 

if __name__ == '__main__':
    app.run()