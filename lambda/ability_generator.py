#!/usr/bin/env python3
#---------------------
#Name: OD&D Revived Ability Generator for Lambda
#Version: 1.0
#Date: 2021-06-24
#---------------------

import os
import random

def d_roll(s, t = 6, c = 1, m = 0, l = False, h = False):
    #Dice rolling: (random integer in range from 1 -> t (dice type)
    #Default input, with s defined, yields roll = 1(d6)+0
    #d_roll with parameters set yield a roll = c(dt)+m
    #s is the seed for the RNG, use at LEAST 8 bytes of random data
    #l is the drop the lowest roll flag
    #h is the drop the highest roll flag
    #NOTE: either l, or h, may be set, not both; l takes precedence
    roll = 0
    random.seed(s)
    roll_sample = 0
    first_run = True
    roll_low = 0
    roll_high = 0
    
    if c > 0:
        for x in range(c):
            roll_sample = random.randint(1, t)
            if first_run:
                roll_low = roll_sample
                roll_high = roll_sample
                first_run = False
            elif roll_sample < roll_low:
                roll_low = roll_sample
            elif roll_sample > roll_high:
                roll_high = roll_sample
            roll += roll_sample
    elif c == 0:
        return(m)
    else:
        c = abs(c)
        for x in range(c):
            roll_sample = random.randint(1, t)
            if first_run:
                roll_low = roll_sample
                roll_high = roll_sample
                first_run = False
            elif roll_sample < roll_low:
                roll_low = roll_sample
            elif roll_sample > roll_high:
                roll_high = roll_sample
            roll -= roll_sample
    
    if l:
        roll -= roll_low
    elif h:
        roll -= roll_high
    
    return(roll + m)

def ability_generator():
    """
    This function generates the characters abilities.
    Returns the abilities as a list of tuples (ability as str, stat as int),
    """
    abilities = ['Strength', 'Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Charisma']
    stats = []
    for i in range(len(abilities)):
        result = d_roll(os.urandom(16), t = 6, c = 3, m = 0)
        stats.append((abilities[i], result))
    return stats

def lambda_handler(event, context):
	ability_scores = ability_generator()
	return {
		str(ability_scores[0][0]): ability_scores[0][1],
		str(ability_scores[1][0]): ability_scores[1][1],
		str(ability_scores[2][0]): ability_scores[2][1],
		str(ability_scores[3][0]): ability_scores[3][1],
		str(ability_scores[4][0]): ability_scores[4][1],
		str(ability_scores[5][0]): ability_scores[5][1],
	}
