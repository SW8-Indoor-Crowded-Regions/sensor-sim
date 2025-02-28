import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sensorDataSim import initSensors, intervalMovement

sensors, rooms = initSensors()
time = 0

def update(frame):
    global time
    intervalMovement(sensors, time)
    
    ax.clear()
    ax.bar(rooms.keys(), [room.getOccupancy() for room in rooms.values()], color='skyblue')
    ax.set_ylim(0, 15)
    ax.set_ylabel("Occupancy")
    ax.set_title("Room Occupancy")
    time += 1


def main():
    global fig, ax
    fig, ax = plt.subplots(figsize=(6, 4))
    ani = FuncAnimation(fig, update, interval=1000)
    plt.show()
    
if __name__ == "__main__":
    main()