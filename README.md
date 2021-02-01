# Zombie Apocalypse
This is a simple simulation I and some of my fellow students made in High School. It can be improved and is unfinished compared to what our ideas and ambitions was, but it works :). The simulation simulates the last group of humans (represented by red and dark red rectangles), who are trying to survive when zombies (represented by lime rectangles) appear around them. The humans must gather food from the forests aswell as ammo and medicine from the houses nearby. The zombies try to run and kill the humans, and if they do there is a chance that the human turns into a new zombie. If the humans have ammo the human is also able to kill the zombies by a slim chance. The guards (dark red rectangles) have a much greater chance of killing zombies and follow the gatherers around.
##### Menu Variables
* Humans are the amount of humans spawned in the base at start.
* Zombies are the amount of zombies that are added on the start of the simulation.
* Tracking distance is the distance a zombie can see humans and run to them.
* Shooting distance is the range guards can shoot zombies. Guards are faster humans with guns in a draker shade of red. They protect the humans getting supplies.
* Food is the amount of food humans start with. If they run out of food they will begin dying.
* Ammo is the ammonition humans start with, and it is the only thing keeping the humans from dying. If the ammunition is empty there is zero chance that a human can kill a zombie, and also the zombies can always penetrate the wall (Usually it is a 10% chance for them getting through the wall.)
* Medicine is how much medicine the humans start with.

##### Keybinds:
- G - Cycle through graphs (The first shows human/zombie population on the y-axis with time in days on the x-axis. The second shows the amount of human deaths and births every day). PS! Keeping this on decreases fps substantialy every time the graph updates (one time every second)
- B - Shows supply stats (Food, ammo and medicine)
- F - Shows fps.

##### Info:
- Green circles are forests, red structures are buildings, Gray area is the base. Dark red humans are guards.