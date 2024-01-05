# %%
! pip install 


# %%
import roslibpy
from time import sleep


# %%
client = roslibpy.Ros(host='KFKL-18.karlov.mff.cuni.cz', port=9090)
client.run()

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

client.get_topics()

# %%

# pohyb želvy rovně

talker = roslibpy.Topic(client, '/???/cmd_vel', 'geometry_msgs/msg/Twist')
talker.publish(roslibpy.Message(
        {'linear': {'x': 1.0, 'y': 0.0, 'z': 0.0}, 
         'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
         }))
talker.unadvertise()
# %%
listener = roslibpy.Topic(client, '/john/pose', 'turtlesim/msg/Pose')
listener.subscribe(lambda message: print('Rychlost: ' + str(message["linear_velocity"])))
sleep(0.1)
listener.unsubscribe()


# úkol: nakreslete domeček