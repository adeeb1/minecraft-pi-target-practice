# Target Practice
Target Practice is a simple minigame written in Python for Minecraft Pi. In this game, the player must hit a moving target by positioning his Minecraft character in front of the target and pressing a physical button module.

###Requirements

1. A Raspberry Pi 3 with the Raspbian "Jessie" operating system installed. Other versions of the Raspberry Pi may work as well, but Target Practice has only been tested on the Raspberry Pi 3.
2. A connected Button module for shooting at the target and an optional LED sensor.

###Installation

Copy all of the files to a directory on your Raspberry Pi. You can use any directory as long as the files are in the same one.
The Button module is configured to use GPIO pin 17 by default. Change the number in [line 215 in `target_minigame.py`](https://github.com/adeeb1/minecraft-pi-target-practice/blob/master/target_minigame.py#L215) to specify your own GPIO number.

###Starting the Game
1. Launch Minecraft Pi, and enter any world.
2. Open `target_minigame.py` in the Python 2 program on the Raspberry Pi. You should see the source code.
3. Run the file from the Python 2 program.
4. A message should appear on screen with instructions. Since this game requires some space, you will want to go to a flat and empty area in your Minecraft world. Floating in the air is one option.

###Controls
Use your keyboard and mouse as you normally would on Minecraft Pi.
Press the Button module to shoot a block at the target.

###API Reference
Minecraft Pi's API is rather small, but you can find documentation on it at [Stuff about="code"](http://www.stuffaboutcode.com/p/minecraft-api-reference.html).
