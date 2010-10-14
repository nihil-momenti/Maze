Focuses:
========
`model.py`, `material.py`
-------------------------
The first code written for this project was for generating models, the Wavefront OBJ format was chosen after a quick glance at the wikipedia page for it and the code in the above two files was developed to load and generate models from these files.  This allowed be to create models in Blender and export them, I decided my model making skills weren't up to the task though so the torch and lamp post were found from a repository of free models[4] and modified slightly to suit.
  
`player.py`, `robot.py`
-----------------------
The player code was split over two main files, `player.py` determines the position of the camera and takes all the input from the user.  `robot.py` defines the players model, this is only displayed in third person or disconnected view.

`perlin.py`, `fractal_map.py`, `fractal_map.c`
----------------------------------------------
This is where I probably spent the most time, even though none of it directly contributes to the marking.  Initially I utilised the Diamond-Square algorithm for generating the fractal map, but I wasn't satisfied with that method and decided to implement Perlin noise instead following the outline at [3].  This had a large performance detriment so I had to re-implement it as a C extension.  This was used for generating a 3d texture for the maze walls, roof and floor; 2d bump mapping for the walls, roof and floor and for the flickering of the light sources.

`controller.py`, `world.py`, `view.py`
--------------------------------------
These are the main Model-View-Controller classes; the controller connects the users input to the player object, the world loads and defines the layout of the objects in the world and the view is responsible for the OpenGL configuration and display.

`world.config`
--------------
Early on I decided to use a JSON based configuration file to allow easily changing most of the world parameters from one place.  This was very useful for getting the texture and bump mapping of the maze looking good while not having too bad a performance penalty.

`maze.py`
---------
The maze is procedurally generated using a method similar to the one detailed at [2], _runners_ carve there way through the unspecified terrain creating tunnels and walls as they go, with chances to split off and chances to die, until no runner can proceed further.  The cells that have been specified as floor are then turned into cell objects.  These cells calculate their bump mapping and texture offsets and apply them when they're being displayed.  The maze then calculates a 3d texture using the fractal map and loads that into memory.

`special.py`
------------
This encompasses the random object found in the maze; the torch, lamp post and bouncing ball.  The torch and lamp post are simply Blender models loaded and displayed at their position with a flickering light source.  The bouncing ball is its own class that simply creates a sphere that moves up and down on the spot.


Controls
========
  Hold the left mouse button down on the window and use the mouse to look around.
  
  WASD are used for movement.

  E switches between first and third person view.
  
  Q disconnects the view from the character and allows free movement within the scene.  Use WASD to move the camera and IJKL to move the character.  The view can also be moved up and down by using the spacebar and Z.

References
==========
1. Alot of procedural content generation found at http://pcg.wikidot.com/

2. Basic maze/cavern creation found at http://properundead.com/2009/03/cave-generator.html

3. Fractal perlin noise generator from http://freespace.virgin.net/hugo.elias/models/m_perlin.htm

4. Models taken from http://e2-productions.com/repository/
    1. Torch by worker11811 from http://e2-productions.com/repository/modules/PDdownloads/singlefile.php?cid=10&lid=270
    2. Lamp post by Obsurus from http://e2-productions.com/repository/modules/PDdownloads/singlefile.php?cid=24&lid=276

TODO
====
+ Fix torch's rotation so it's actually against a wall.
+ Animate fire in torch
+ Add third animated textured special object