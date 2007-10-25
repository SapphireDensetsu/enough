import pygame

# todo put this in a class

target_offset = [0,0]
cur_offset = [0,0]

def pos_offset(pos):
    return map(lambda a,b:a+b, pos, cur_offset)

def rect_offset(rect):
    return pygame.Rect(rect.x+cur_offset[0], rect.y+cur_offset[1], rect.width, rect.height)

def set_offset(new_offset):
    global target_offset
    target_offset = new_offset

def add_offset(amount):
    global target_offset
    target_offset = map(lambda a,b:a+b, amount, target_offset)

def step(amount=0.1):
    cur_offset[0] += (target_offset[0] - cur_offset[0])*amount
    cur_offset[1] += (target_offset[1] - cur_offset[1])*amount

