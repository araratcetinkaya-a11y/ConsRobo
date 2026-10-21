import rosbag
from geometry_msgs.msg import Point
import pandas as pd

# The bag file should be in the same directory as your terminal
bag = rosbag.Bag('./subseto.bag')
topic = '/distance_to_camera' #   /gazebo/model_states
# column_names = ['x', 'y']
column_names = ['distance_to_camera']
df = pd.DataFrame(columns=column_names)

for topic, msg, t in bag.read_messages(topics=topic):
    # x = msg.pose[-1].position.x
    # y = msg.pose[-1].position.y
    data = msg.data
    df = df.append(
        {'distance_to_camera': data},
        ignore_index=True
    )
    # print(msg.pose[-1].position)
df.to_csv('distance_to_camera.csv')