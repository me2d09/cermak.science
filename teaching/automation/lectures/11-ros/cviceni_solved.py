# %%
!pip install roslibpy


# %%
import roslibpy
from time import sleep


# %%
client = roslibpy.Ros(host='KFKL-18.karlov.mff.cuni.cz', port=9090)
client.run()
# %%
print('Is ROS connected?', client.is_connected)



# %%
# Jaké máme services?
client.get_services()


# %%
# Jaké má command parametry?

service_type = client.get_service_type("/spawn")
print(service_type)
#
# %%
# Vytvořte si vlastní želvu
service = roslibpy.Service(client, '/spawn', 'turtlesim/srv/Spawn')
request = roslibpy.ServiceRequest({'x': [0-10],
                                   'y': [0-10],
                                   'name': '??'})
service.call(request)


# %%
# nastavte si barvu

service = roslibpy.Service(client, '/???/set_pen', 'turtlesim/srv/SetPen')
request = roslibpy.ServiceRequest({'r': 1,
                                   'g': 250,
                                   'b': 20,
                                   'width': 3})
service.call(request)





# %%
# jaké má moje želva topicy?

# úkol: vypište jen topicy pro vyši želvičku

for t in client.get_topics():
    if "turtle1" in t:
        print(t)

# %%

# pohyb želvy rovně

talker = roslibpy.Topic(client, '/turtle1/cmd_vel', 'geometry_msgs/msg/Twist')
talker.publish(roslibpy.Message(
        {'linear': {'x': 1.0, 'y': 0.0, 'z': 0.0}, 
         'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
         }))
sleep(1)
talker.publish(roslibpy.Message(
        {'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 
         'angular': {'x': 0.0, 'y': 0.0, 'z': 1.0}
         }))
talker.unadvertise()
# %%

v = None

def update_vel(m):
    global v
    if v != m["linear_velocity"]:
        print(f'Rychlost: {v} -> {m["linear_velocity"]}')
        v = m["linear_velocity"]
          
listener = roslibpy.Topic(client, '/turtle1/pose', 'turtlesim/msg/Pose')
listener.subscribe(update_vel)

print("čekám")
sleep(1)
print("jedu")
talker = roslibpy.Topic(client, '/turtle1/cmd_vel', 'geometry_msgs/msg/Twist')
talker.publish(roslibpy.Message(
        {'linear': {'x': 1.0, 'y': 0.0, 'z': 0.0}, 
         'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
         }))
sleep(0.1)
while v > 0:
    sleep(0.1)
print("hotovo")
talker.unadvertise()

listener.unsubscribe()


# úkol: nakreslete domeček
# %%
from math import sqrt, atan2
# %%



class Zelvak:

    def __init__(self, client, name):
        #self._c = client
        self.n = name

        self.velocity_publisher = roslibpy.Topic(client, f'/{self.n}/cmd_vel', 'geometry_msgs/msg/Twist')

        self.pose_subscriber = roslibpy.Topic(client, f'/{self.n}/pose', 'turtlesim/msg/Pose')
        self.pose_subscriber.subscribe(self.update_pose)
        self.pose = None

    def update_pose(self, data):
        self.pose = data
        self.pose["x"] = round(self.pose["x"], 4)
        self.pose["y"] = round(self.pose["y"], 4)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose["x"] - self.pose["x"]), 2) +
                    pow((goal_pose["y"] - self.pose["y"]), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose["y"] - self.pose["y"], goal_pose["x"] - self.pose["x"])

    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose["theta"])

    def move2goal(self, x, y):
        """Moves the turtle to the goal."""
        goal_pose = {}

        # Get the input from the user.
        goal_pose["x"] = x
        goal_pose["y"] = y

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = 0.01

        vel_msg = {}

        while self.euclidean_distance(goal_pose) >= distance_tolerance:

            vel_msg = {
                'linear': {'x': self.linear_vel(goal_pose), 'y': 0.0, 'z': 0.0}, 
                'angular': {'x': 0.0, 'y': 0.0, 'z': self.angular_vel(goal_pose)}
                }
            

            # Publishing our vel_msg
            self.velocity_publisher.publish(
                roslibpy.Message(vel_msg)
            )

            # Publish at the desired rate.
            sleep(0.1)

        # Stop zelvak
        self.velocity_publisher.publish(roslibpy.Message(
        {'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 
         'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
         }))
# %%
moje = Zelvak(client, "turtle1")
# %%
moje.move2goal(9,3)
# %%
# zelvicky
zelvy = []
for t in client.get_topics():
    if "cmd_vel" in t:
        n = t[1:-8]
        if n != "turtle1":
            zelvy.append(n)
zelvy
# %%

x,y = 0,0

def get_pose(m):
    global x,y
    x = m["x"]
    y = m["y"]

for z in zelvy:          
    listener = roslibpy.Topic(client, f'/{z}/pose', 'turtlesim/msg/Pose')
    listener.subscribe(get_pose)
    sleep(0.1)
    listener.unsubscribe()
    print(f"Jdu na {x},{y}")
    moje.move2goal(x,y)
# %%
