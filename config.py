import pygame
import os
import matplotlib.pyplot

pygame.font.init()

# Simulation
clock = pygame.time.Clock()
fps = 60
simulation_time = 0
(width, height) = (1280, 720)
window = pygame.display.set_mode((width, height))
caption = pygame.display.set_caption('Zombie Apocalypse')
line_spacing = 10
font_size = 30 
font = pygame.font.Font(pygame.font.get_default_font(), font_size)
background = pygame.image.load(os.path.join('map.png')).convert()
human_base = pygame.image.load(os.path.join('human_base.png')).convert_alpha()

# Colours
blue = (0, 0, 255)
deep_blue = (0, 65, 106)
white = (255, 255, 255)
fps_colour = (255, 128, 0)

# Human settings
humans = []
amount_humans = 500
human_width = 2
human_height = 6
human_wandering_speed = 1
human_running_speed = 4
human_colour = (255, 0, 0)
human_group = []
human_move_errand_speed_multiplier = 1.5
reproduction_level_perhuman = 10 * 0.486
life_expectancy = 60
death_rate = 2 / 1000
amount_kids_per_day = ((amount_humans * reproduction_level_perhuman) / (life_expectancy * 365))
amount_of_dead_per_day = ((amount_humans * death_rate) / 365)
chance_medicine = [1, 0, 0, 0, 0]
chance_ammo = [1, 2, 3, 0, 0]
human_slowness = 4
human_guards = []
gunning_distance = 50
time_since_help = 30
guard_colour = (128, 0, 0)

# Zombie settings
zombies = []
amount_zombies = 25
zombie_width = 2
zombie_height = 5
zombie_attack_speed_multiplier = 2
zombie_wandering_speed = 3
zombie_tracking_distance = 50
zombie_colour = (0, 255, 0)

# Base settings
base_stats_colour = (85, 85, 85)
base_center = (581, 349)
base_food = 5000
days_without_food = 0
base_medicine = 30
base_ammo = 100
base = ((417, 442 - human_height / 2), (519, 269 - human_height / 2), (493, 210 - human_height / 2), (573 - human_width / 2, 176), (801 - human_width, 310), (722 - human_width, 444 - human_height), (643 - human_width, 431 - human_height), (489 - human_width / 2, 539 - human_height))
base_triangles = []
for i in range(len(base)):
    base_triangles.append((base[i-1], base[i], base_center))

# Forests
forest_south = (55, 449, 292, 217)
forest_north = (1037, 47, 180, 138)
forests = [forest_south, forest_north]
zombie_spawn_north = (422, 83)
zombie_spawn_south = (807, 610)

# Buildings
building_north_1 = (18, 54, 45, 81)
building_north_2 = (84, 22, 19, 31)
building_north_3 = (157, 27, 78, 42)
building_north_4 = (85, 94, 71, 37)
buildings_north = [building_north_1, building_north_2, building_north_3, building_north_4]
building_east_1 = (754, 407, 65, 35)
building_east_2 = (848, 316, 40, 67)
building_east_3 = (919, 340, 19, 27)
building_east_4 = (906, 430, 21, 31)
building_east_5 = (981, 385, 45, 80)
building_east_6 = (982, 293, 76, 41)
buildings_east = [building_east_1, building_east_2, building_east_3, building_east_4, building_east_5, building_east_6]
buildings = [building_north_1, building_north_2, building_north_3, building_north_4, building_east_1, building_east_2, building_east_3, building_east_4, building_east_5, building_east_6]

# Forest food amount
forest_food = 50000

# House resources
house_food = 10000
house_ammo = 30000
house_medicine = 10000

# Entrances
'''
north_entrance = (765, 279, 30, 30)
east_entrance = (625, 424, 30, 30)
west_entrance = (450, 335, 37, 28)
'''
north_entrance = (783, 290, 2, 2)
east_entrance = (642, 440, 2, 2)
west_entrance = (466, 347, 2, 2)
entrances = [north_entrance, east_entrance, west_entrance]
road_entry = ((745, 6), (1278, 714), (2, 293))
curve = (475, 554, 21, 21)
curve2 = (581, 132, 37, 37)

# Graph
graph_humans = []
graph_zombies = []
figure = matplotlib.pyplot.figure(figsize=[3.2, 3.2]) # 300 x 300
axis = figure.gca()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(figure)
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()
size = canvas.get_width_height()
surface = pygame.image.fromstring(raw_data, size, "RGB")
graphlist = (0, 1, 2)
graph = 0

# Graph2
graph_birth = []
graph_death = []
figure2 = matplotlib.pyplot.figure(figsize=[3.2, 3.2]) # 300 x 300
axis2 = figure2.gca()
canvas2 = matplotlib.backends.backend_agg.FigureCanvasAgg(figure2)
renderer2 = canvas2.get_renderer()
raw_data2 = renderer2.tostring_rgb()
size2 = canvas2.get_width_height()
surface2 = pygame.image.fromstring(raw_data2, size2, "RGB")
births = 0
deaths = 0