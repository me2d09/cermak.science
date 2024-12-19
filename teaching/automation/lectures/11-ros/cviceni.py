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
# Ukončení spojení
client.terminate()


# %%
# Jaké máme services?
client.get_services()


# %%
# Jaké má command parametry?

service_type = client.get_service_type("/spawn")
print(service_type)
# %%
client.get_service_request_details(service_type)


#%%
# Jaké mám topicy
client.get_topics()
#%%
client.get_topic_type('/connected_clients')
#%%
listener = roslibpy.Topic(client, '/connected_clients', 'rosbridge_msgs/msg/ConnectedClients')
listener.subscribe(print)  ## print je callback! bude tisknout výstup

#%%
# odpojím se
listener.unsubscribe()







# %%
# Vytvořte si vlastní želvu
service = roslibpy.Service(client, '/spawn', 'turtlesim/srv/Spawn')
request = roslibpy.ServiceRequest({'x': ??,
                                   'y': ??,
                                   'name': ??})
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



# %%

# pohyb želvy rovně

talker = roslibpy.Topic(client, '/nejakazelva/cmd_vel', 'geometry_msgs/msg/Twist')
# jeď rovně
talker.publish(roslibpy.Message(
        {'linear': {'x': 10.0, 'y': 0.0, 'z': 0.0}, 
         'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
         }))
sleep(1)
# zatoč
talker.publish(roslibpy.Message(
        {'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 
         'angular': {'x': 0.0, 'y': 0.0, 'z': 1.0}
         }))
talker.unadvertise()
# %%
# pozorování rychlosti kamarádovy želvy 
v = 0

def update_vel(m):
    global v
    if v != m["linear_velocity"]:
        print(f'Rychlost: {v} -> {m["linear_velocity"]}')
        v = m["linear_velocity"]
          
listener = roslibpy.Topic(client, '/nejakacizizelva/pose', 'turtlesim/msg/Pose')
listener.subscribe(update_vel)

while v == 0:
    sleep(0.1)
print("už jede")
while v > 0:
    sleep(0.1)
print("už stojí")

listener.unsubscribe()


# úkol: nakreslete domeček/vánoční stromek/hvězdu
# %%






# %%
#úkol: napište želvu, co bude pronásledovat vybranou spolužákovu želvu

