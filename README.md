##How to get the ros-morrf-project up and running on your machine:

Before anything, make sure that you're running Ubuntu 14.04 or a variant that runs it.
We will discuss small changes that you need to make if you're running Elementary OS,
but if your variant is not Elementary then you will be on your own if you run into issues.

####1. Install ROS
You can follow the tutorial here: <http://wiki.ros.org/indigo/Installation/Ubuntu>

If what you're doing requires use of the turtlebot, it's better to install Indigo.

If you install Jade you will not be able to run any of the turtlebot sims or anything like that.

Elementary OS Only:

    Run the following command before you install: echo "export ROS_OS_OVERRIDE=elementary" >> ~/.bashrc

    On the part where you set up your sources.list in the ROS tutorial,
    you need to replace "$(lsb_release-sc)" with the word "trusty" in order to get it to work correctly.

####2. Follow the tutorial link at the bottom of the ROS installation page.

Look where it says "Please proceed to the ROS Tutorials," to set up your ROS Environment.

Section 3 of "Installing and Configuring your ROS Environment" is the only one you need to follow.
It will allow you to set up your catkin workspace.
This is where you will put the ros-morrf-project in order to run it.


####3. Clone the the following repositories into your ~/catkin_ws/src/ directory

the links are found here respectively:

ros-morrf-project: <https://github.com/wfearn/ros-morrf-project>

mm_apriltags_tracker: <https://github.com/darin-costello/mm_apriltags_tracker>

multi_apriltags_tracker: <https://github.com/dqyi11/multi_apriltags_tracker>

####4. Install dependencies.

Go to somewhere that isn't your catkin_ws folder.
I personally like to use the Documents folder in the home directory for this,
but it doesn't really matter where you go.

Clone the following two repositories into the folder of your choice:

<https://github.com/dqyi11/MORRF>

<https://github.com/dqyi11/TopologyPathPlanning>

The third repository you will need to use svn. Run the following command:
    svn co https://svn.csail.mit.edu/apriltags

At this point you will need to install other packages if you don't have them installed already.

Run the following command:

    sudo apt-get install qt-sdk python-xlib gengetopt libcgal-dev ros-indigo-usb-cam

*Note:* You might have some of these installed already, if you don't when you try and install the libraries we have cloned the console output will let you know.

a. Go to the MORRF folder that you have cloned

b. type: mkdir build

c. type: cd build

d. type: cmake ..

e. Once it finishes, type: sudo make install

f. At this point a bunch of lines should come up showing you that the program is compiling, if it is successful and has no error messages then you've installed the library correctly.

Repeat steps a through f for the TopologyPathPlanning and apriltags folders.

The only errors I've run into with these are dependency errors, but I have covered most of them, if not all, with the four package installations above.

At this point you should be ready to run catin_make

####5. cd to ~/catkin_ws and run the catkin_make command

This may fail at first and you might have to run it a couple times. Check the progress and the error messages.
Frequently catkin will mark error messages as saying that you just need to run the command again to get it to work.

If you keep running into the same error at the same place during the compilation, then check and make sure that you have all of the dependencies that we've discussed.

Try running "source ~/catkin_ws/devel/setup.bash" (It's even a good idea to put this into your ~/.bashrc) and running catkin_make again.

If this doesn't work then you're on your own.

####6. Run the ros-morrf-project.

The base command is "roslaunch commander ..." where the "..." can be one of several options:

#####a. morrf_launch.launch:

This will run the basic GUI. You'll need to load an image to run morrf on by clicking "file" and "load image"
if you don't have images to run there are 3 that you can choose from in ~/catkin_ws/src/ros-morrf-project/commander/data/

#####b. simple_launch.launch:

This will run an even simpler version of morrf_launch. Here you just need to select an image and decide what objectives you want.

If you don't have a full setup and are just running the program for testing, you can use:

    roslaunch multi_apriltags_tracker launch_multi_april_tags_tracker.launch

If you have a room set up, then you'll want to use more than one camera, in that case run:

    roslaunch mm_apriltags_tracker launchAll.launch

*Note:* Read down about how to properly configure your environment if you're using this option with multiple cameras.

*Additional Note:* These use an apriltag tracking system, so you will just get a white window unless you have a usb camera hooked up to your computer and pointed at the apriltags.

Read below to find out how to set up your environment correctly.

#####c. turtlebot_config.launch:

This will run a window specifically made for the turtlebot. You can find more advanced options to mess with things such as the number of iterations MORRF will go through under file->advanced options

You will not see obstacles here unless the apriltags are specific numbers. If you open commander/scripts/commander_gui/turtlebot_config.py you will see the variable OBS_DICT which has the numbers of the apriltags that correspond to obstacles, and the width and height of the obstacles they represent.

#####d. topology.launch:

This runs a variant of morrf where you select the path that you want morrf to build other paths around. You may only select one objective.

Once you have your obstacles, and start and end positions, you may click on the white window and create a path for MORRF to base its planning around. All subsequent clicks after the first click will draw paths from where you previously clicked to where you last clicked.

If the path is undesirable, you can right click and select "reset" to clear the path you have created.

#####e. camera_config.launch:

This runs something similar to turtlebot_config.launch except it uses a different costmap generator meant for the sphero robot. The paths generated with this will be farther from the obstacles than what you'll see with the other config files.

Also the obstacles will be smaller, they're scaled up in the turtlebot window to compensate for the turtlebot's radius.

##How to set up the apriltag camera environment

####1. Apriltags

You can find all of the apriltags you need at the following link:
<http://www.dotproduct3d.com/assets/pdf/apriltags.pdf>

If that link has been deprecated, the tag family we used was 36h11. You should be able to search that in Google and find apriltags you can print off.

If you want to modify what values are associated with what icons,
you will need to modify the image window python file that corresponds to the type of GUI you're running.

As it stands, the numbers correspond to the following values:

Apriltag 51 is the robot goal position.

Apriltag 50 is the robot start position.

Apriltag 97 is the robot itself.

Apriltags 40 - 49 are considered enemies.

Within each python image file there is an OBS_DICT variable that has the values associated with each obstacle.
Some of the image files will just convert any apriltag from 30 - 39 into a generically sized obstacle.

*Note:* We used color coded apriltags to help differentiate between them, the same may help you.

####2. Camera Setup

The apriltags are picked up by USB Webcams.
We used four of them hooked up to two computers (two cameras for each computer).

In our case, we hung the cameras from the ceiling with PVC pipe, however you choose to do it is your perogative.

The important part is that you create a viable coordinate field for the cameras.

We used large white apriltags to mark off the coordinate field. Each camera must be able to see at least one, but if you don't have some overlap (meaning apriltags that more than one camera can see) you're going to get a lot of dead zones (where the robot just stops because a camera loses track of it).

You can find what apriltag numbers correspond to what values in the mm_apriltags_tracker/launch/param/pos.yaml file. You can modify these numbers as you wish, and you do not need to use all of them.

In our case we used the following setup:

![Alt text](/readme_images/ApriltagDiagram.jpg?raw=true "Apriltag Setup")

The blue squares represent the large apriltags we used, the red squares represent what the camera is able to see.

If you notice, there is an area of overlap in the shape of a cross, with the middle apriltag having overlap from all four cameras.

If the cameras do not overlap at all, an object can get lost, and when more than one camera can see an object it will often jump around in the GUI. However, the more cameras that can see it the less it will jump.

In this case, the top left corner of the top left red square would be 0,0 according to the camera, and the bottom right corner of the bottom right square would be 600, 600.

*Note: If you're going to modify the size of the world, you will need to adjust the numbers in the pos.yaml file (whether changing their values or adding more) and adjust the window size in the python image file of the GUI you're wanting to use, otherwise it won't function how you want.*

*For example, if I wanted to modify the window for turtlebot_config.launch to be 800 by 800 instead of 600 by 600, I would open the pos.yaml and add 7 more numbers that corresponded to the outer right edge values of an 800 by 800 grid, basically adding 200 where necessary to the already existing values.*

*Then I would open the /ros-morrf-project/commander/scripts/commander_gui/turtlebot_window.py file and modify the HEIGHT and WIDTH values to somewhere between 750 and 800.*

Basically you just need to think of the apriltags as marking off a grid, and each one corresponds to a point on that grid, the camera picks them up and then infers where an object is based on its relative position to those apriltags.

After you've run the file, if you see the word "Calibrated" in each output window, then it is successful.

If you're not seeing "Calibrated" you could need to modify your exposure values in the cameras.

Open a terminal and type in "qv4l2", a window should pop up. Go to the second tab over from General, then click the dropdown menu next to "Exposure, Auto" and change it to "Manual Mode."

After this, if the "Exposure (Absolute)" is somewhere around 300+, you can just knock off the last number. You need it sub 50 or around there.

At this point check the cameras again, and they should work.
