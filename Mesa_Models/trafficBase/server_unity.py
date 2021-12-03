from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
from agent import Car, Traffic_Light, Destination, Obstacle, Road
import atexit
import os
import json


number_agents = 4
width = 10
height = 10
TrafficModel = None
density = 0
currentStep = 0

app = Flask(__name__, static_url_path='')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


@app.route('/init', methods=['Post', 'GET'])
def initModel():
    global currentStep, TrafficModel, number_agents

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        currentStep = 0

        TrafficModel = RandomModel(number_agents)

        return jsonify({'message': 'INIT.'})


@app.route('/getCars', methods=['GET'])
def getAgents():
    global TrafficModel
    cars = []
    carsPositions = []

    for (a, x, z) in TrafficModel.grid.coord_iter():
        for b in a:
            if isinstance(b, Car):
                cars.append(b)
    cars.sort()
    for car in cars:
        carsPositions.append({"x": car.pos[0], "y": 0, "z": car.pos[1]})

    print(carsPositions)

    return jsonify({'positions': carsPositions})


@app.route('/getTL', methods=['GET'])
def getTL():
    global TrafficModel

    TLPositions = []
    TLStates = []
    TL = []

    for (a, x, z) in TrafficModel.grid.coord_iter():
        for b in a:
            if isinstance(b, Traffic_Light):
                TL.append(b)

    TL.sort()
    for L in TL:
        TLPositions.append({"x": L.pos[0], "y": 0, "z": L.pos[1]})
        TLStates.append(L.state)

    return jsonify({'positions': TLPositions, 'states': TLStates})


@app.route('/getDestination', methods=['GET'])
def getDestination():
    global TrafficModel

    destPositions = []
    dest = []

    for (a, x, z) in TrafficModel.grid.coord_iter():
        for b in a:
            if isinstance(b, Destination):
                dest.append(b)

    dest.sort()
    for des in dest:
        destPositions.append({"x": des.pos[0], "y": 0, "z": des.pos[1]})

    return jsonify({'positions': destPositions})


@app.route('/getObstacle', methods=['GET'])
def getObstacle():
    global TrafficModel

    obstPositions = []
    obst = []

    for (a, x, z) in TrafficModel.grid.coord_iter():
        for b in a:
            if isinstance(b, Obstacle):
                obst.append(b)

    obst.sort()
    for ob in obst:
        obstPositions.append({"x": ob.pos[0], "y": 0, "z": ob.pos[1]})

    return jsonify({'positions': obstPositions})


@app.route('/getRoad', methods=['GET'])
def getRoad():
    global TrafficModel

    roadsPositions = []
    roads = []

    for (a, x, z) in TrafficModel.grid.coord_iter():
        for b in a:
            if isinstance(b, Road):
                roads.append(b)

    roads.sort()
    for road in roads:
        roadsPositions.append({"x": road.pos[0], "y": 0, "z": road.pos[1]})

    return jsonify({'positions': roadsPositions})


@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, TrafficModel
    if request.method == 'GET':
        TrafficModel.step()
        currentStep += 1
        return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep': currentStep})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
