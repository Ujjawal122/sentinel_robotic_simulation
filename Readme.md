# Build Sentinel: An Autonomous Patrol and Change Detection Robot

Sentinel is a simulated security robot built with ROS 2 and Gazebo. Think of it as an automated night-shift guard for a warehouse. The robot drives along a set route, stops at checkpoints to take pictures, and checks if anything in the room has changed since its last visit.

## Understand How the Robot Works

Imagine a robot playing a real-life game of "Spot the Difference":

1. **Record the Baseline (First Patrol):** On its very first trip, the robot doesn't know what a "normal" room looks like yet. It drives to each checkpoint, takes a photo and a 3D depth scan, and saves them to a database. This becomes the baseline.
2. **Compare the View (Later Patrols):** On future trips, the robot visits the exact same spots and takes new photos. It compares the new photo with the original baseline photo.
3. **Report Changes:** If everything looks the same, the robot quietly moves to the next spot. If something is different—like a new box on the floor or an open door—it sends an alert (`ChangeEvent`) to your dashboard. When the route finishes, the robot returns to its charging dock.

## Explore the System Architecture

The software splits into three main parts: the 3D simulation, the standard ROS 2 navigation tools, and Sentinel's custom brain.

```
+-------------------------------------------------------+
|                   Gazebo Simulation                   |
|                 (World, Robot, Sensors)               |
+-------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------+
|                   Bridge & Control                    |
|             (ros_gz_bridge, ros2_control)             |
+-------------------------------------------------------+
       /                    |                    \
      v                     v                     v
+------------+      +---------------+     +-------------+
|Localization| ---> |  Navigation   |     | Perception  |
| EKF, SLAM, |      | Nav2, Behavior|     |   Change    |
|    AMCL    |      |     Tree      |     |  Detection  |
+------------+      +---------------+     +-------------+
                            |                    /
                            v                   v
                    +-----------------------+
                    |    Mission Manager    |
                    | Patrol, Detect, Report|
                    +-----------------------+
                                |
                                v
                    +-----------------------+
                    |   Dashboard and Log   |
                    |   Foxglove, SQLite    |
                    +-----------------------+
```

* **Simulate the World (Gazebo):** Provides the virtual warehouse, the robot body, wheels, and cameras.
* **Connect the Robot (Bridge and Control):** Translates signals between the Gazebo simulator and ROS 2 so the robot can move and read sensors.
* **Find the Position (Localization):** Acts like indoor GPS so the robot always knows where it is on the map.
* **Drive Safely (Navigation):** Plans a path from point A to point B without hitting walls or obstacles.
* **Spot the Differences (Perception):** Compares old photos with new photos to see if objects moved.
* **Run the Mission (Mission Manager):** Acts as the boss. It tells the robot where to drive, when to take a photo, and when to send an alert.
* **Watch the Dashboard (Foxglove and SQLite):** Lets you watch the robot live on your screen and saves a history of all patrols.

## Follow the Patrol Loop

```
                  [ Start Patrol ]
            (PatrolRoute Action Goal)
                         |
                         v
             [ Navigate to Checkpoint ]
               (Nav2 NavigateToPose)
                         |
                         v
             [ Capture Observation ]
               (Image, Depth, Pose)
                /                \
   (First Patrol Only)      (Later Patrols)
              /                    \
             v                      v
   [ Save as Baseline ]   [ Compare with Baseline ]
             |                      |
             v                      v
  [ Store in Database ]    [ Publish ChangeEvent ]
 (SQLite + Image Files)    (Only if change found)
              \                    /
               \                  /
                v                v
               [ Next Checkpoint ]
               (Or Return to Dock)
```

## Learn Core ROS 2 Concepts

By building this project, you practice specific ROS 2 tools at each step of the robot's patrol:

| Action Step | ROS 2 Concept You Learn | Plain English Explanation |
| :--- | :--- | :--- |
| **Start Patrol** | Action Server and Client (`PatrolRoute`) | Start a long task, get live progress updates ("At checkpoint 2 of 3"), or cancel the patrol early. |
| **Navigate to Checkpoint** | Nav2 Action Client, TF2, and Map | Send map coordinates to the self-driving stack and track where the camera sits relative to the wheels. |
| **Capture Observation** | Topic Subscriptions, `message_filters`, QoS | Grab the color photo, 3D depth scan, and robot position at the exact same split-second so nothing is blurry. |
| **Compare with Baseline** | Lifecycle Node, OpenCV, `cv_bridge` | Turn the image checker on only when parked to save CPU power, and use OpenCV to spot visual changes. |
| **Publish ChangeEvent** | Custom Message (`ChangeEvent.msg`) | Create your own custom alert format that bundles the checkpoint name, time, and before/after photos. |
| **Store in Database** | Services (`/save_checkpoint`) and Parameters | Send a quick request to save the baseline photo to the hard drive and log the details in SQLite. |
| **Monitor on Dashboard** | Foxglove Bridge or `rosbridge` | Stream the robot's camera feed, map, and security alerts to a visual control panel. |

## Set Up the Project

### Install Prerequisites

* Ubuntu 22.04 or 24.04 LTS
* ROS 2 (Humble or Jazzy)
* Gazebo and Nav2 packages
* Python 3 and standard ROS build tools (`colcon`, `rosdep`)

### Build the Workspace

```bash
# 1. Create a workspace folder
mkdir -p ~/sentinel_ws/src
cd ~/sentinel_ws/src

# 2. Clone this repository
git clone https://github.com/<your-username>/sentinel.git

# 3. Install required packages
cd ~/sentinel_ws
rosdep install --from-paths src --ignore-src -r -y

# 4. Build and source the code
colcon build --symlink-install
source install/setup.bash
```

## Track the Build Progress

* [x] Design system architecture and patrol loop
* [ ] Define custom messages, services, and actions (`ChangeEvent`, `PatrolRoute`, `SaveCheckpoint`)
* [ ] Build the Gazebo warehouse world and robot model
* [ ] Configure mapping (SLAM) and self-driving (Nav2)
* [ ] Write the camera and depth synchronization node
* [ ] Create the SQLite database service to save baselines
* [ ] Build the OpenCV change detection node
* [ ] Connect the Mission Manager and Foxglove dashboard

## Read the License

This project uses the MIT License. See the `LICENSE` file for details.