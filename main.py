#Basic modules
import pygame
import random
import math

#User files
import classes
import config

#Initializes pygame 
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('music.ogg')
pygame.mixer.music.play(-1)

#Menu values
menu = True
humantext = classes.textInput(config.line_spacing, config.line_spacing, 140, config.font_size, '  humans', config.amount_humans)
zombietext = classes.textInput(config.line_spacing, 2 * config.line_spacing + config.font_size, 140, config.font_size, '  zombies', config.amount_zombies)
tracking_distance = classes.textInput(config.line_spacing, 3 * config.line_spacing + 2 * config.font_size, 140, config.font_size, '  tracking', config.zombie_tracking_distance)
foodtext = classes.textInput(config.line_spacing, 5 * config.line_spacing + 4 * config.font_size, 140, config.font_size, '  food', config.base_food)
ammotext = classes.textInput(config.line_spacing, 6 * config.line_spacing + 5 * config.font_size, 140, config.font_size, '  ammo', config.base_ammo)
medicinetext = classes.textInput(config.line_spacing, 7 * config.line_spacing + 6 * config.font_size, 140, config.font_size, '  medicine', config.base_medicine)
guntext = classes.textInput(config.line_spacing, 4 * config.line_spacing + 3 * config.font_size, 140, config.font_size, '  shooting', config.gunning_distance)
start = classes.startBox(config.width - config.line_spacing - 5 * config.font_size, config.height - config.font_size - config.line_spacing, 140, config.font_size)
inputs = [humantext, zombietext, tracking_distance, guntext, foodtext, ammotext, medicinetext]

#Menu
while menu:
    for event in pygame.event.get():

        #If quit
        if event.type == pygame.QUIT:
            menu = False
            pygame.quit(); quit()

        elif event.type == pygame.KEYDOWN:
            #Starts the main simulation
            if event.key == pygame.K_RETURN:
                humancount = int(humantext.text)
                zombiecount = int(zombietext.text)
                tracking_distance = int(tracking_distance.text)
                config.base_food = int(foodtext.text)
                config.base_ammo = int(ammotext.text)
                config.base_medicine = int(medicinetext.text)
                config.gunning_distance = int(guntext.text)
                menu = False

        #Checks if user uses the text inputs, and updates them
        for x in inputs:
            x.text_function(event)

        #Starts the simulation if user clicks on 'start'
        if start.start(event):
            humancount = int(humantext.text)
            zombiecount = int(zombietext.text)
            tracking_distance = int(tracking_distance.text)
            config.base_food = int(foodtext.text)
            config.base_ammo = int(ammotext.text)
            config.base_medicine = int(medicinetext.text)
            config.gunning_distance = int(guntext.text)
            menu = False
   
   #Fills the background
    config.window.fill(config.white)
    #Updates text inputs
    for x in inputs:
        x.update()
        x.draw(config.window)
    #Draws start button
    start.draw(config.window)
    
    #Draws the screen, and updates clock
    pygame.display.flip()
    pygame.time.Clock().tick(config.fps)

#Creates humans
for i in range(humancount):
    base_sector = config.base_triangles[random.randint(0, 7)]
    spawn_point = classes.point_on_triangle(base_sector[0], base_sector[1], base_sector[2])
    config.humans.append(classes.human(int(spawn_point[0]), int(spawn_point[1])))

#Creates zombies
for i in range(zombiecount):   
    spawn_area = random.choice((config.zombie_spawn_south, config.zombie_spawn_north))
    config.zombies.append(classes.zombie(spawn_area[0] + random.randint(-100, 100), spawn_area[1]+random.randint(-100, 100)))

#Mainly draws the classes, but also updates existing objects
def draw():
    classes.background_draw()

    #Checks if new humans should be added to human_group (active group of humans), and adds new humans if true
    if len(config.human_group) < config.amount_humans//5 and config.forest_food + config.house_ammo + config.house_medicine + config.house_food > 10:
        config.human_group += list(filter(lambda h: (h not in config.human_guards) and (h not in config.human_group), config.humans))[0 : int(config.amount_humans // 5)]
        #config.human_group = list(filter(lambda h: h not in config.human_guards, config.humans))[0 : int(config.amount_humans // 5)]

    elif config.forest_food + config.house_ammo + config.house_medicine + config.house_food > 10:
        for human in config.human_group:
            human.delete = True
    
    #Checks if new humans should be added to human_guards (attacking humans), and adds new humans if truee
    if len(config.human_guards) < config.amount_humans // 20:
        config.human_guards += random.sample(list(filter(lambda h: (h not in config.human_group) and (h not in config.human_guards), config.humans)), min(5, config.amount_humans//10))

    #Updates every zombie
    for zombie in config.zombies:
        #Draws the zombies
        zombie.draw()

        #Checks if zombie doesn't have a target
        if not zombie.target:
            #Tries to find a target
            for human in config.humans:
                if zombie.x - tracking_distance < human.x < zombie.x + config.zombie_width + tracking_distance and zombie.y - tracking_distance < human.y < zombie.y + config.zombie_height + tracking_distance:
                    zombie.target = human
                    human.targeted = True
                
        #Checks if target is still in human list (incase other zombie killed human)
        if zombie.target in config.humans:

            #Tries to attack human
            try :
                zombie.attack(zombie.target)

            #Runs if zombie is on human, tries to kill human
            except ZeroDivisionError:
            
                human.targeted = False
                chance = random.randint(0, 20)

                #Chance of zombie getting killed 
                if (chance < 6) and (config.base_ammo > 0):
                    config.zombies.remove(zombie)
                    config.base_ammo -= 1

                #Chance of human getting killed
                if chance > 2:
                        config.humans.remove(zombie.target)
                        config.deaths += 1
                        if zombie.target in config.human_group:
                            config.human_group.remove(zombie.target)

                #Chance of human becoming zombie
                if chance > 7:
                    config.zombies.append(classes.zombie(zombie.target.x, zombie.target.y))

        #Runs if target is already dead or zombie has no target
        else:
            #Resets target
            zombie.target = False
            #If zombie hasn't set steps, sets new amount of steps and random direction
            if not zombie.set_steps:
                zombie.set_steps = random.randint(40, 200)
                zombie.direction = (random.randint(-1, 1), random.randint(-1, 1))

            #If zombie hasn't walked enough steps, zombie continues walking
            if zombie.steps < zombie.set_steps:

                if zombie.steps % int(config.zombie_wandering_speed) == 0:
                    zombie.move(zombie.direction[0], zombie.direction[1])
                zombie.steps += 1

            #If zombie is done walking set steps, resets steps (stops walking)
            if zombie.steps >= zombie.set_steps:
                zombie.set_steps = 0
                zombie.steps = 0
    
    #Runs for every guard
    for human in config.human_guards:
        #Gives guards new colour to diffferentiate from other humans
        if human.colour == config.human_colour:
            human.colour = config.guard_colour
        #Runs if guard doesn't have a target at the moment
        if not human.guard_target:
            try:
                #Most likely to guard a human from human_group
                if random.randint(0, 100) > 15:
                    human.guard_target = random.choice(config.human_group)
                #If guard doesn't choose a human to guard, guard chooses place in base instead
                else:
                    base_sector = config.base_triangles[random.randint(0, 7)]
                    human.guard_target = classes.point_on_triangle(base_sector[0], base_sector[1], base_sector[2])

            #Runs if no humans left in human_group, chooses a point in base
            except IndexError:
                base_sector = config.base_triangles[random.randint(0, 7)]
                human.guard_target = classes.point_on_triangle(base_sector[0], base_sector[1], base_sector[2])

        #If guard is set to guard a point in a base
        elif type(human.guard_target) == tuple:
            #Tries to walk to point
            try:
                human.scavenge(human.guard_target[0], human.guard_target[1])
            
            #Runs if guard on point
            except ZeroDivisionError:
                None

            #If ammo left, guard tries to hunt nearby zombies
            if config.base_ammo > 0:
                for zombie in config.zombies:
                    if (human.x-zombie.x) ** 2 + (human.y-zombie.y) ** 2 < (config.gunning_distance + 10) ** 2:
                        human.guard_target = zombie
                        break

        #If target is dead, resets target
        elif (human.guard_target not in config.zombies) and (human.guard_target not in config.human_group):
            human.guard_target = False

        #If target is a zombie
        elif human.guard_target in config.zombies:
            #If ammo left, guard tries to attack zombie
            if config.base_ammo > 1:
                try:
                    human.attack(zombie)
                except ZeroDivisionError:
                    None
                except ValueError:
                    None
                    #Shouldn't run, but does sometimes, idk
            
            #If no ammo left, guard goes to guard point
            else:
                base_sector = config.base_triangles[random.randint(0, 7)]
                human.guard_target = classes.point_on_triangle(base_sector[0], base_sector[1], base_sector[2])

        #If target is human
        else:
            #If ammo left, checks for nearby zombies
            if config.base_ammo > 0:
                targetedzombie = False
                for zombie in config.zombies:
                    if (human.x - zombie.x) ** 2 + (human.y - zombie.y) ** 2 < (config.gunning_distance + 10) ** 2:
                        human.guard_target = zombie
                        targetedzombie = True
                        break

                #If no zombies nearby, tries to follow human
                if not targetedzombie:
                    try:
                        human.scavenge(human.guard_target.x + 10, human.guard_target.y + 10)
                    except ZeroDivisionError:
                        None
            #If no ammo, goes to guard point
            else:
                base_sector = config.base_triangles[random.randint(0, 7)]
                human.guard_target = classes.point_on_triangle(base_sector[0], base_sector[1], base_sector[2])
        
    #Runs for every human
    for human in config.humans:
        human.draw()
        
        #Random chance of dying (accident, etc.)
        if (config.simulation_time - 1 ) % config.fps == 0:
            if random.randint(0, 10000) < (100 * config.amount_of_dead_per_day):
                config.humans.remove(human)
                config.deaths += 1
                if human in config.human_group:
                    config.human_group.remove(human)

        classes.entrance(config.north_entrance, human)
        classes.entrance(config.east_entrance, human)
        classes.entrance(config.west_entrance, human)

        #If no food left, runs code that can kill humans
        if config.base_food == 0:
            if config.days_without_food == 1 or human.days_left == -1:
                #Every human has a random amount of days they can live without food
                human.days_left = random.randint(1, 12) + random.randint(1, 9) + random.randint(1, 11)
            elif config.simulation_time % (config.fps - 1) == 0:
                human.days_left -= 1
                if human.days_left == 0:
                    config.humans.remove(human)
                    config.deaths += 1

    #Runs for every active human (gatherers, immigrants and helpers)
    for human in config.human_group:
        
        if random.randint(0, 300) == 50:

            human.spawn = True
            
            if not human.homeward_bound and not human.goal:
                human.stored_position = random.choice(config.entrances)[0:2]
                (human.x, human.y) = human.stored_position
                human.set_goal()
            
                if not human.target:

                    if human.goal == 'food' and human.stored_position == config.entrances[1][0:2]:
                        human.target = config.curve
                        human.stored_position = config.curve
                    
                    elif human.goal == 'food':
                        human.target = classes.closest(config.forests, human)

                    elif human.stored_position == config.north_entrance[0:2]:
                        human.target = config.curve2
                        human.stored_position = config.curve2

                    else:

                        if human.stored_position == config.entrances[0][0:2]:
                            human.target = random.choice(config.buildings)
                        
                        elif human.stored_position == config.entrances[1][0:2]:
                            human.target = random.choice(config.buildings_east)

                        elif human.stored_position == config.entrances[2][0:2]:
                            human.target = random.choice(config.buildings_north)
                    
                    human.target = classes.random_centre(human.target)

        if human.spawn:

            try:
                human.scavenge(human.target[0], human.target[1])
                
            except ZeroDivisionError:

                if human.stored_position == config.curve:
                    human.target = config.forest_south
                    human.target = classes.random_centre(human.target)
                    human.stored_position = ()

                elif human.stored_position == config.curve2:
                    human.target = random.choice(config.buildings_north)
                    human.target = classes.random_centre(human.target)
                    human.stored_position = ()
                
                elif not human.homeward_bound:
                    human.homeward_bound = True
                    human.target = classes.closest(config.entrances, human)
                    human.target = classes.centre(human.target)


    #Info at the upper corners
    human_counter = config.font.render("Humans: " + str(config.amount_humans), 1, config.human_colour)
    config.window.blit(human_counter, (config.line_spacing, config.line_spacing))
    zombie_counter = config.font.render("Zombies: " + str(config.amount_zombies), 1, (config.zombie_colour))
    config.window.blit(zombie_counter, (config.line_spacing, config.line_spacing + config.font_size))
    time_counter = config.font.render("Time: " + str(int(config.simulation_time / (365 * (config.fps - 1)))) + " years " + str(int((config.simulation_time / (config.fps - 1)) % 365)) + " days", 1, config.blue)
    config.window.blit(time_counter, (config.width - 50 * config.line_spacing, config.line_spacing))
    
    #Checks what the user wants to see, and updates interface
    if fps:
        fps_counter = config.font.render("fps: " + str(int(config.clock.get_fps())), 1, config.fps_colour)
        config.window.blit(fps_counter, (config.width - 50 * config.line_spacing, config.height - config.line_spacing - config.font_size))
    if config.graph:
        classes.graph_draw()
    if base_stats:
        classes.base_stats_draw()

#By default fps and base_stats infotexts are off
fps = False
base_stats = False
main = True

while main:
    #Checks if user wants to quit or see new info on interface
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            main = False
            pygame.quit(); quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                config.graph = config.graphlist[config.graph - 1]
            elif event.key == pygame.K_f:
                fps = not fps
            elif event.key == pygame.K_b:
                base_stats = not base_stats

    #Checks amount of zombies/humans, updates time
    config.amount_humans = len(config.humans)
    config.amount_zombies = len(config.zombies)
    config.simulation_time += 1

    #Updates graph and base inventory
    classes.graph_update()
    classes.inventory()
    draw()

    #Immigration, birth, help and new zombie spawns can happen
    classes.immigration()
    classes.birth()
    classes.help()
    classes.zombie_spawn()

    # Sickness and medicine
    classes.res_growth()
    classes.medicine_effects()

    #Updates screen
    pygame.display.flip()
    config.clock.tick(config.fps)
    
