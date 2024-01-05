# %%
! pip install 
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
service = roslibpy.Service(client, '/spawn', 'turtlesim/srv/Spawn')
request = roslibpy.ServiceRequest({'x': 3,
                                   'y': 2,
                                   'name': 'john2'})

print('Calling service...')
result = service.call(request)
print(f'Service response: {result}')


# %%
service = roslibpy.Service(client, '/lojza/set_pen', 'turtlesim/srv/SetPen')
request = roslibpy.ServiceRequest({'r': 1,
                                   'g': 250,
                                   'b': 20,
                                   'width': 3})

print('Calling service...')
service.call(request)





# %%
# jaké má moje želva topicy?

# úkol: vypište jen topicy pro vyši želvičku
client.get_topics()

# %%

# pohyb želvy rovně

talker = roslibpy.Topic(client, '/john/cmd_vel', 'geometry_msgs/msg/Twist')
talker.publish(roslibpy.Message(
        {'linear': {'x': 1.0, 'y': 0.0, 'z': 0.0}, 
         'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
         }))
talker.unadvertise()
# %%
listener = roslibpy.Topic(client, '/john/pose', 'turtlesim/msg/Pose')
listener.subscribe(lambda message: print('Heard talking: ' + str(message)))
sleep(1)
listener.unadvertise()
# úkol: nakreslete domeček
# %%

# %%
