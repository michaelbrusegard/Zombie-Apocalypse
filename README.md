# Zombie Apocalypse

#### Requirements:
* Python3 (Used versions 3.8.1, 3.8.2 and 3.8.3) *when installing, remember to check 'td/tk and IDLE' if not checked matplotlib will not work*
* Pygame (Used version 2.0.0dev6) *Install using 'pip3 install pygame==2.0.0dev6' in terminal*

##### Menu Variables
* Humans is the amount of humans spawned in the base at start.
* Zombies is the amount of zombies that are added on the start of the simulation.
* Tracking distance is the distance a zombie can see humans and run to them.
* Shooting distance is the range guards can shoot zombies. Guards are faster humans with guns in a draker shade of red. They protect the humans getting supplies.
* Food is the amount of food humans start with. If they run out of food they will begin dying.
* Ammo is the ammonition humans start with, and it is the only thing keeping the humans from dying. If the ammunition is empty there is zero chance that a human can kill a zombie, and also the zombies can always penetrate the wall (Usually it is a 10% chance for them getting through the wall.)
* Medicine is how much medicine the humans start with.

##### Keybinds:
G - Cycle through graphs (The first shows human/zombie population on the y-axis with time in days on the x-axis. The second shows the amount of human deaths and births every day). PS! Keeping this on decreases fps substantialy every time the graph updates (one time every second)
B - Shows supply stats (Food, ammo and medicine)
F - Shows fps.
