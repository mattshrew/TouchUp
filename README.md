![touchUp Banner.png](https://cdn.dorahacks.io/static/files/18ffd4b567518ac591c1ae54675bd050.png)

TouchUp is a product that **revolutionises the way people interact with their devices**. We allow our users to **control their computers, monitors, and TVs using just hand gestures**.

## Holo-Touch:
Control your device from a distance, with Holo-Touch! Using AI models, our Holo-Touch technology allows you to control your cursor with your body, whether you’re a few centimetres, or a few metres away from your device. With Holo-Touch, you can do so much: present to others seamlessly, game in an immersive environment, or control computers and TVs from anywhere with just your hands.

## Any-Touch:
Any-Touch is a modular computer add-on that enables any device to become touch-screen. Our state-of-the-art software detects your hand movements, calculates your precise location in respect to the screen, and tracks your clicks as well. Any-Touch is compatible with any device: computers, monitors, TVs … **if it’s not yet a touch screen, Any-Touch will turn it into one**.

| **Tool** | **Description** |
| ----------- | ----------- |
| MediaPipe | Hand-tracking |
| OpenCV | Camera recording, Gaussian blur, Canny edge detection, and Contouring |
| Pystray | Tray application |
| Pynput | Mouse input |
| Python Imaging Library | Application visuals |
| Threading | Running tray application & Holo/Any-Touch in parallel |
| PyInstaller | Create one single executable file |
| Time, numpy, math | Controlling program flow, calculating coordinates, and finding depth |
| VSCode, GitHub, liveshare | Coding, workflow, and collaboration |

# Challenges we ran into
 - Object detection and framing for computer screens (esp. at angles)
 - Relating objects in three dimensions with a single camera (lack of depth)
 - Instability with MediaPipe hand-tracking (variance)
 - Bugs with installing modules on the Raspberry Pi
 - Inability to use WiFi or Bluetooth to send camera data on the Raspberry Pi

# What we learned & accomplished
 - Learning many new skills, such as using Raspberry Pis, MediaPipe, OpenCV, etc.
 - Persevering through struggles, particularly with these new technologies
 - We learned that we can accomplish so much more in 36 hours than in 24 hours

# What’s next for TouchUp
We hope to reduce the physical footprint of our product by switching the phone out for 2 Raspberry Pis, or just two cameras and a chip. We would also love some more time to train our own model to better detect the distance between our fingers and the computer screen.

**Try it out!**
To use TouchUp,
1. Clone the GitHub repository : ```git clone https://github.com/mattshrew/TouchUp.git```
2. Install the required dependencies: OpenCV, Mediapipe, Pynput, Pyautogui, Time, Math, Numpy, Pystray, PIL, Threading, Platform
3. Run main.py.
4. Click the app on the tray and select Holo-Touch or Any-Touch!
Holo-Touch Gestures:
 - Primary Hand:
   - Left Click: thumb to index finger
   - Right Click: thumb to middle finger
 - Secondary Hand:
   - Scroll Down: thumb to index finger
   - Scroll Up: thumb to middle finger
