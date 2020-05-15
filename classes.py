import pygame
import math
import random
import matplotlib.pyplot
import config

class human:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vector_x = 0
        self.vector_y = 0
        self.target = False
        self.passive = False
        self.target = False
        self.exceptions = []
        self.homeward_bound = False
        self.goal = False
        self.days_left = -1
        self.stored_position = ()
        self.targeted = False
        self.val_save = 0
        self.delete = False
        self.target_area = (0, 0)
        self.guard_target = False
        self.spawn = False
        self.colour = config.human_colour
    
    def scavenge(self, target_x, target_y):
        if not human in config.human_guards:
            if not config.simulation_time % config.human_slowness == 0:
                self.scavenge_move(target_x, target_y)
        if human in config.human_guards:
            self.scavenge_move(target_x, target_y)
    
    def scavenge_move(self, target_x, target_y):
        self.vector_x = target_x - self.x
        self.vector_y = target_y - self.y
        distance = math.hypot(self.vector_x, self.vector_y)
        self.vector_x = self.vector_x / distance
        self.vector_y = self.vector_y / distance
        self.x += int(self.vector_x * config.human_move_errand_speed_multiplier)
        self.y += int(self.vector_y * config.human_move_errand_speed_multiplier)
            
    def set_goal(self):
        if config.base_food < (config.amount_humans * 30):
            self.goal = 'food'

        elif config.base_ammo < 20:
            self.goal = 'ammo'

        elif (config.base_food / (300 * config.base_medicine)) > 0:
            self.goal = 'medicine'

        else:
            self.goal = 'food'

    def move(self, x, y):
        if self.passive:
            for i in range(len(config.base)):
                if intersect((self.x, self.y), (self.x + x, self.y + y), config.base[i - 1], config.base[i]) or onsegment((self.x + x, self.y + y), config.base[i - 1], config.base[i]):
                    self.x -= x
                    self.y += y
                    break
        self.x += x
        self.y -= y
        

        if self.x > config.width - config.human_width:
            self.x = config.width - config.human_width

        elif self.x < 0:
            self.x = 0
        
        if self.y > config.height - config.human_height:
            self.y = config.height - config.human_height

        elif self.y < 0:
            self.y = 0

    def attack(self, target):
        if (self.x-target.x) ** 2 +(self.y + target.y) < config.gunning_distance ** 2:
            if config.simulation_time % 20 == 0:
                config.base_ammo -= 1
                if random.randint(0, 3) > 1:
                    config.zombies.remove(target)
            elif config.simulation_time % 3 == 0:
                self.scavenge(target.x, target.y)
        else:
            self.scavenge(target.x, target.y)

    def draw(self):
        pygame.draw.rect(config.window, self.colour, (self.x, self.y, config.human_width, config.human_height), 0)

class zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vector_x = 0
        self.vector_y = 0
        self.target = 0
        self.steps = 0
        self.set_steps = 0
        self.direction = ()

    def move(self, x, y):
        if 416 < self.x < 802 and 177 < self.y < 540 and config.base_ammo > 0:
            for i in range(len(config.base)):
                if intersect((self.x, self.y), (self.x + x, self.y + y), config.base[i - 1], config.base[i]) or onsegment((self.x + x, self.y + y), config.base[i - 1], config.base[i]):
                    config.zombies.remove(self)
                    config.base_ammo -= 1
                    break
        self.x += x
        self.y -= y

        if self.x > config.width - config.zombie_width:
            self.x = config.width - config.zombie_width

        elif self.x < 0:
            self.x = 0
        
        if self.y > config.height - config.zombie_height:
            self.y = config.height - config.zombie_height

        elif self.y < 0:
            self.y = 0
        
    def attack(self, human):
        self.vector_x = human.x - self.x
        self.vector_y = human.y - self.y
        distance = math.hypot(self.vector_x, self.vector_y)
        self.vector_x = self.vector_x / distance
        self.vector_y = self.vector_y / distance
        self.move(int(self.vector_x * config.zombie_attack_speed_multiplier), -int(self.vector_y * config.zombie_attack_speed_multiplier))

    def draw(self):
        pygame.draw.rect(config.window, config.zombie_colour, (self.x, self.y, config.human_width, config.human_height), 0)

def background_draw():
    config.window.blit(pygame.transform.scale(config.background, (config.width, config.height)), (0, 0))  
    config.window.blit(pygame.transform.scale(config.human_base, (config.width, config.height)), (0, 0))

def graph_draw():
    if config.graph == 2:
        if (config.simulation_time + config.fps - 1 ) % (config.fps) == 0:
            config.axis.plot(config.graph_humans, color = 'red')
            config.axis.plot(config.graph_zombies, color = 'green')
            config.axis.set_ylabel('Amount')
            config.axis.set_xlabel('Time (days)')
            config.axis.set_title('Human(red)/Zombie(green) population')
            config.canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(config.figure)
            config.canvas.draw()
            config.renderer = config.canvas.get_renderer()
            config.raw_data = config.renderer.tostring_rgb()
            config.size = config.canvas.get_width_height()
            config.surface = pygame.image.fromstring(config.raw_data, config.size, "RGB")
        config.window.blit(config.surface, (config.width - 320, config.height - 320))
    
    if config.graph == 1:
        if (config.simulation_time + config.fps - 1 ) % (config.fps) == 0:
            config.axis2.plot(config.graph_birth, color = 'blue')
            config.axis2.plot(config.graph_death, color = 'red')
            config.axis2.set_title('Birth-(blue)/Deathrate(red)')
            config.canvas2 = matplotlib.backends.backend_agg.FigureCanvasAgg(config.figure2)
            config.canvas2.draw()
            config.renderer2 = config.canvas2.get_renderer()
            config.raw_data2 = config.renderer2.tostring_rgb()
            config.size2 = config.canvas2.get_width_height()
            config.surface2 = pygame.image.fromstring(config.raw_data2, config.size2, "RGB")
        config.window.blit(config.surface2, (config.width - 320, config.height - 320))

def graph_update():
    if (config.simulation_time + config.fps - 1 ) % config.fps == 0:
        config.graph_zombies.append(config.amount_zombies)
        config.graph_humans.append(config.amount_humans)
        config.graph_birth.append(config.births)
        config.graph_death.append(config.deaths)
        config.births, config.deaths = (0, 0)

        #if (config.simulation_time + config.fps - 1 ) % (config.fps * 365) == 0:
            #config.graph_humans = []
            #config.graph_zombies = []
            

def base_stats_draw():
    food_counter = config.font.render("Food: " + str(config.base_food), 1, config.base_stats_colour)
    medicine_counter = config.font.render("Medicine: " + str(config.base_medicine), 1, config.base_stats_colour)
    ammo_counter = config.font.render("Ammo: " + str(config.base_ammo), 1, config.base_stats_colour)
    config.window.blit(food_counter, (config.width - 20 * config.line_spacing, config.height / 2))
    config.window.blit(medicine_counter, (config.width - 20 * config.line_spacing, config.height / 2 - config.line_spacing - config.font_size))
    config.window.blit(ammo_counter, (config.width - 20 * config.line_spacing, config.height / 2 - 2 * config.line_spacing - 2 * config.font_size))

def inventory():
    if config.simulation_time % (config.fps - 1) == 0:
        if config.base_food - config.amount_humans > 0:
            config.base_food -= config.amount_humans
        else :
            for human in random.sample(config.humans, config.base_food):
                human.days_left = -1
            config.base_food = 0
            config.days_without_food += 1
                
def birth():
    amount_kids_per_day = (config.amount_humans * config.reproduction_level_perhuman) / (config.life_expectancy * 365)
    if random.randint(0, 10000) < (100 * amount_kids_per_day):
        mother = random.choice(config.humans)
        config.humans.append(human(mother.x, mother.y))
        config.births += 1
        
class textInput :
    def __init__(self, x, y, width, height, unit, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = config.deep_blue
        self.unit = unit
        self.text = str(text)
        self.textSurface = config.font.render(self.text + self.unit, True, self.colour)
        self.active = False
            
    def text_function(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
               
                self.active = True
                self.colour = config.blue
            else:
               
                self.active = False
                self.colour = config.deep_blue
                
        if event.type == pygame.KEYDOWN:

            if self.active:

                if event.key == pygame.K_BACKSPACE:

                    self.text = self.text[:-1]
                else:
                   
                    self.text += event.unicode
            
                self.textSurface = config.font.render(self.text + self.unit, True, self.colour)
                
    def update(self):
        width = max(200, self.textSurface.get_width() + 10)
        self.rect.w = width
        
    def draw(self, window):
        window.blit(self.textSurface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(window, self.colour, self.rect, 2)

#gammel versjon ikke bruk
'''
def entrance(entrancex, entrancey, size, human):
    if entrancex < human.x < entrancex + size:
        if entrancey < human.y < entrancey + size:
            human.passive = True
            human.x = random.randint(527, 697)
            human.y = random.randint(255, 425)
'''


def entrance(entrance, human):
    if human.homeward_bound:
        if entrance[0] < human.x < entrance[0] + entrance[2]:
            if entrance[1] < human.y < entrance[1] + entrance[3]:
                #print(human)
                #human.x = random.randint(527, 697)
                #human.y = random.randint(255, 425)
                base_sector = config.base_triangles[random.randint(0, 7)]
                spawn_point = point_on_triangle(base_sector[0], base_sector[1], base_sector[2])
                human.x, human.y = (int(spawn_point[0]), int(spawn_point[1]))
                
                if config.base_food == 0:
                    config.days_without_food = 0

                if human.goal == 'food':
                    if config.forest_food > 0:
                        human.val_save = random.randint(50, 100) + random.randint(50, 150) + random.randint(20, 100)
                        config.base_food += human.val_save
                        config.forest_food -= human.val_save
                
                elif human.goal == 'immigrate':
                    config.human_group.remove(human)
                    config.base_food += random.randint(5, 30)
                    config.base_ammo += random.choice(config.chance_ammo)
                    config.base_medicine += random.choice(config.chance_medicine)
                
                elif human.goal == 'help':
                    config.human_group.remove(human)
                    config.base_food += random.randint(50, 300)
                    config.base_ammo += random.choice(config.chance_ammo) * 10
                    config.base_medicine += random.choice(config.chance_medicine) * 10


                elif human.goal:
                    if config.house_food > 0:
                        human.val_save = random.randint(5, 30)
                        config.base_food += human.val_save
                        config.house_food -= human.val_save

                    if config.house_ammo > 0:
                        human.val_save = random.choice(config.chance_ammo)
                        config.base_ammo += human.val_save
                        config.house_ammo -= human.val_save

                    if config.house_medicine > 0:
                        human.val_save = random.choice(config.chance_medicine)
                        config.base_medicine += human.val_save
                        config.house_medicine -= human.val_save

                
                if human.delete and human.goal:
                    try:
                        config.human_group.remove(human)
                    except ValueError:
                        None
                    human.delete = False
                
                
                human.homeward_bound = False
                human.target = False
                human.goal = False
                human.spawn = False


class startBox :
    def __init__(self, x, y, b, h):
        self.rect = pygame.Rect(x, y, b, h)
        self.colour = config.deep_blue
        self.textSurface = config.font.render('Start', True, self.colour)
    
    def start(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.colour = config.blue
                return True
    
    def draw(self, window):
        window.blit(self.textSurface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(window, self.colour, self.rect, 2)

def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def inArea(points, obj):
    intersections = 0
    for i in range(len(points)):
        if intersect((points[i-1][0], points[i-1][1]), (points[i][0], points[i][1]), (obj.x, obj.y), (config.width, obj.y)):
            intersections += 1
            
    return intersections % 2 != 0

def squared_distance(A, B):
    return (A[0] - B[0]) ** 2 +(A[1] - B[1]) ** 2

def onsegment(point, A, B):
    return round(squared_distance(point, A) + squared_distance(point, B), 2) == round(squared_distance(A, B), 2)

def point_on_triangle(pt1, pt2, pt3):
    s, t = sorted([random.random(), random.random()])
    return (s * pt1[0] + (t - s) * pt2[0] + (1 - t) * pt3[0],
            s * pt1[1] + (t - s) * pt2[1] + (1 - t) * pt3[1])

def closest(list, human):
    closest = 999999

    for n in list:

        if (((n[0] + n[2] / 2) - human.x) ** 2 + ((n[1] + n[3] / 2) - human.y) ** 2) ** 0.5 < closest and n not in human.exceptions:
            closest = (((n[0] + n[2]/2) - human.x) ** 2 + ((n[1] + n[3] / 2) - human.y) ** 2) ** 0.5
            closest_place = n

    return closest_place

def centre(zone):
    return (zone[0] + zone[2] // 2, zone[1] + zone[3] // 2)

def immigration():
    if config.simulation_time % 120 == 0:
        if random.randint(0, 100) > 75:
            side = random.randint(0, 2)
            x, y  = config.road_entry[side]
            config.humans.append(human(x, y))
            man = config.humans[-1]
            man.goal = 'immigrate'
            man.target = config.entrances[side]
            man.homeward_bound = True
            config.human_group.append(man)


def help():
    if config.simulation_time % 60 == 0:
        config.time_since_help += 1
        if (config.base_food < config.amount_humans * 7) and (config.time_since_help > 30) and config.amount_humans > 50:
            config.time_since_help = 0
            side = random.randint(-1, 0)
            x, y = config.road_entry[side]
            append_new_human(side, 'help')
            delivererposition = len(config.humans)-1
            for i in range(random.randint(1,4)):
                append_new_human(side, delivererposition)

def append_new_human(side, goal):
    x, y = config.road_entry[side]
    config.humans.append(human(x-random.randint(3, 10), y+random.randint(3, 10)))
    man = config.humans[-1]
    if goal in ('immigrate', 'help'):
        man.goal = goal
        man.target = config.entrances[side]
        man.homeward_bound = True
        config.human_group.append(man)
    elif type(goal) == int:
        config.human_guards.append(man)
        man.guard_target = config.humans[goal]
        #print(goal)

def res_growth():
    if config.simulation_time % 360 == 0:
        config.forest_food += 1000
        config.house_food += 500
        config.house_ammo += 10
        config.house_medicine += 2

def random_centre(t):
    return (t[0] + (random.randint(0, t[2])), t[1] + (random.randint(0, t[3])))

def medicine_effects():
    if config.simulation_time % 120 == 0:
        try:
            if random.randint(0, 1000//config.amount_humans) == 0:
                if config.base_medicine > 0:
                    config.base_medicine -= 1
                else:
                    human = random.choice(config.humans)
                    config.humans.remove(human)
                    config.deaths += 1
                    if human in config.human_group:
                        config.human_group.remove(human)
                    elif human in config.human_guards:
                        config.human_guards.remove(human)
        except ZeroDivisionError:
            print('Humans died')

def zombie_spawn():
    spawningday = 10800
    if config.simulation_time % (spawningday) == 0:
        spawningday += 1
        if spawningday == 10820:
            spawningday = 10800
        spawn_area = random.choice((config.zombie_spawn_south, config.zombie_spawn_north))
        config.zombies.append(zombie(spawn_area[0] + random.randint(-100, 100), spawn_area[1]+random.randint(-100, 100)))