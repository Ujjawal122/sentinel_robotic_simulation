# Published by perception when a checkpoint looks different from its baseline.

# Constants for change_type
uint8 CHANGE_NONE=0
uint8 CHANGE_OBJECT_ADDED=1
uint8 CHANGE_OBJECT_REMOVED=2
uint8 CHANGE_OBJECT_MOVED=3
uint8 CHANGE_DOOR_STATE=4
uint8 CHANGE_UNKNOWN=255

std_msgs/Header header                 # timestamp + frame_id
string checkpoint_name                 # which checkpoint was inspected
uint8 change_type                      # one of the CHANGE_* constants
float32 confidence                     # 0.0 to 1.0
string description                     # human-readable summary
geometry_msgs/Pose robot_pose          # where the robot stood (in the map frame)
sensor_msgs/Image baseline_snippet     # what it looked like before
sensor_msgs/Image current_snippet      # what it looks like now