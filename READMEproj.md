# README for EE267 project - Hand Shadow Game

### 0. Authors
Yixin Wang (wyixin@stanford.edu)
Chenyue Meng (chenyue@stanford.edu)

### 1. Hardware setup
##### 1.1 Laptop
The laptop we used to run this project is an early 2015 MacBook Pro 13 model (macOS Sierra 10.12.5). This laptop has two USB ports (one on the left and one on the right) and one HDMI port. 

##### 1.2 Intel RealSense RGB-D camera
Provide by the lab.

##### 1.3 Vrduino
Provide by the lab.

##### 1.4 Viewmaster HMD
Provide by the lab.

### 2. Environment setup
##### 2.1 RealSense
To have an Intel RealSense camera work on a MacBook Pro, we need to install `librealsense` package as camera driver, and then install its Python wrapper `pyrealsense`. Details are as follows. 
###### 2.1.1 librealsense (official)
Please see the official github link [https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_osx.md](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_osx.md) and install via Homebrew
```
$ brew install librealsense
```
###### 2.1.2 pyrealsense (third-party)
This is a package for python to call functions to use RealSense. Please see the link to the repo
[https://github.com/toinsson/pyrealsense](https://github.com/toinsson/pyrealsense)
and install via pip
```
$ pip install pyrealsense
```
###### 2.1.3 sanity check
After having the above two packages installed, please plug in the usb cable from Intel RealSense to the **left** usb port (strongly encouraged. weird bugs may happen otherwise) and try `import pyrealsense as pyrs` in python. If it works, then the RealSense packages are installed successfully. 

##### 2.2 opencv
We need opencv to process images and extract hands. Therefore, Python `cv2` package is needed and can be installed via
```
$ pip install opencv-python
```
This could be tested by `import cv2` in python. If there is a bug complaining upon `cv2`, then it might be inevitable to build from source. 

### 3. Start the game
##### 3.1 Vrduino
The first thing to do is to start the vrdruino by reset. The code to realize head tracking is the same as TAs provided, which can be found under `./HandShadowGame/vrdruino`. Please plug the usb cable to the **right** side of the laptop (because the **left** usb port is reserved for RealSense). 

##### 3.2 RealSense camera
The second thing to do is to start the server end where RealSense takes images and extract hands, and wait for calls from client (C# code in Unity). Please plug the usb cable of RealSense to the **left** side of the laptop. And `cd ./EE267_hand_shadow_game` to switch to the server code directory and run
```
$ python stream_colour_and_depth.py
```
This sould start a server successfully. As a sign of success, you should be able to see some RealSense camera info printing in the terminal and red beaming light coming out of the camera. 

##### 3.3 Unity
The last thing to do is open the Unity project, which is `./HandShadowGame/EE267/`. You should see a castle like scene by now. Here are two places are hard-coded which need human touch. 

1. Vrduino port number - this is the same as the Unity starter project. The port name in `ReadUSB.cs` needs to be changed to whatever port runs VRduino in the Arduino program. 
`const string portName = "/dev/cu.usbmodem2815121";`

~~2. Images load path - We've hard coded the path to three textures (which is actually the 3,2,1 counting down after game starts) as absolute path. Please see line 21, 27, 33 and look for `string filePath_1 = "/Users/chenyue/Documents/EE267/project/number-solid-1.jpg";`. Please kindly change the path of `number-solid-1.jpg` and 2 and 3 as well. You could find them under `./`. This hotfix is actually optional if you only want to test the game scenes. If not fixed, those counting down images would be shown as question marks.~~

Please start from `Assets/Handpainted Forest Environment Free Sample/scenes/start_scene.unity` by double-clicking the `start_scene` unity file. Then you could hit the play button at the very top to start rendering (it would be better to reset the vrduino again before start).

##### 3.4 Control
The only key to control is `space` key. At the beginning, you can hit `space` to avoid unnecessarily long wait time to start the game. Whenever getting stuck at a round (there are 5 rounds of game in total, in which you may use one/both hand(s) to make shadows of animals/objects like scissors, spock, dog, stag and crab), please hit `space` to pass this round and go to the next level. At the last round (crab), hitting `space` will restart the game from beginning. 

### 4. Troubleshooting
##### 1. Scene not moving along with vrduino
If the scene does not change accordingly with the rotation of vrduino. Then it is most likely that the connection is broken, which requires unplugging and plugging the usb cable of vrduino again. (This happens very often)

##### 2. Snoopy in game scene
If in the game scene, you see a snoopy on the right hand side rather than a black-background, red hand shadow contour. Then with high probability that the server is not working as expected. Please kill the server in terminal and restart it. Again you sould see some RealSense info printing once the server has started. Then restart the `start_scene` in Unity. 

##### 3. Not enough usb ports
Realsense will take one usb, vrduino will take one usb, HMD will take one usb (for power supply) and one HDMI. If there are not enough usb ports (like in my case, I only have two but need three). One hotfix is to plug the usb cable of HMD to any other usb because it is just for power supply and don't require any data comming in. 
