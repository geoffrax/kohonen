import numpy as np
from PIL import Image
from flask import Flask, send_file, request
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io

app = Flask(__name__)

# calculation of influence decay
def influence( x,  y,  x2,  y2,radius):
    inf = np.sqrt((x-x2)**2+(y-y2)**2)
    inf_decayed = np.exp(-(inf**2)/(2*(radius**2)))
    return inf_decayed

# Calcuation to determine if square is in radius
def in_radius(x, y, x2, y2, radius):
    if np.sqrt((x-x2)**2+(y-y2)**2) <= radius-1:
        return True
    return False

# Map of radius influence decay for current iteration (to reduce sqrt calls)
def inf_map_maker(radius):
    int_radius = int(radius)
    inf_map = np.zeros((int_radius,int_radius))
    for x in range(int_radius):
        for y in range(int_radius):
            if in_radius(x, y, 0, 0, radius):
                inf_map[x,y] = influence( x, y, 0, 0, radius)
    return inf_map

# Only accessible function on app
# Performs and creates kohonen network, and returns PNG image of map
@app.route('/draw_map')
def draw_map():

    input_num = int(request.args.get('inputs', 20))
    sizeX = int(request.args.get('sizex', 10))
    sizeY = int(request.args.get('sizey', 10))    
    iterations = int(request.args.get('iterations', 100)) 
    initial_learning_rate = float(request.args.get('learningrate', 0.1)) 
    input_vect = 3

    initial_radius=np.maximum(sizeX,sizeY)/2
    time_const = iterations/np.log(initial_radius)

    input_data = np.random.random((input_num,input_vect))
    weights = np.random.random((sizeX, sizeY,input_vect))

    for c in range(iterations):
        BMU_array = np.zeros((iterations,2))
        cur_radius = initial_radius*np.exp(-c/time_const)
        cur_radius_int = int(cur_radius)-1
        cur_learning_rate = initial_learning_rate*np.exp(-c/time_const) 

        inf_map = inf_map_maker(cur_radius)

        # Find BMU locations
        for i in range(input_num):
            BMU = 100
            BMUx = 0
            BMUy = 0
            
            for x in range(sizeX):
                for y in range(sizeY):
                        temp_BMU = sum((input_data[i]-weights[x,y])**2) #np.linalg.norm(input_data[i] -weights[x,y])
                        if temp_BMU < BMU:
                            BMU, BMUx, BMUy = temp_BMU, x, y
            BMU_array[i,:] = [BMUx, BMUy]

        # Update the BMU weights    
        for i in range(input_num):
            [BMUx, BMUy] = int(BMU_array[i,0]),int(BMU_array[i,1])
            for x in range(np.max([BMUx-cur_radius_int,0]), np.min([BMUx+cur_radius_int,sizeX])):
                for y in range(np.max([BMUy-cur_radius_int,0]), np.min([BMUy+cur_radius_int,sizeY])):
                        inf_weight = inf_map[abs(x-BMUx), abs(y-BMUy)]
                        if inf_weight:
                            weights[x,y] = weights[x,y] + inf_weight * cur_learning_rate * (input_data[i]-weights[x,y])

    # Draw and export graphs
    # To match the spirit of the exercise I'll be creating matplotlib pngs directly, with axes in the image.
    # Outputs of the array itself could similarly be exported in a text format or BMP.

    plt.imshow(weights)
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight', pad_inches=.1)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)