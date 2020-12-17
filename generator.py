#!/usr/bin/env python3
#---------------------
#Name: OD&D Character Generator
#Version: 1.0
#Date: 2020-12-16
#---------------------
#max line = 79

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
    This function generates the characters abilities using either
    the classic method or the revived method.
    Returns the abilities as a list of tuples, (ability as str, stat as int).
    """
    abilities = ['Strength', 'Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Charisma']
    stats = []
    for i in range(len(abilities)):
        result = d_roll(os.urandom(16), t = 6, c = 3, m = 0)
        stats.append((abilities[i], result))
    return stats

def ability_adjustments(char_type, ability_scores):
    """
    This function produces any ability adjustments for the character
    based upon the rolled ability scores.
    """
#    if char_type == 'Fighter':
#    elif char_type == 'Cleric':
#    elif char_tupe == 'Magic User':

def hit_dice_hit_points_and_saves(char_type, ability_scores):
    """
    This function shows the character's hit dice,
    generates the character's hit points,
    and produces the character's saves.
    """

def attributes_and_magical_capabilities(char_type, ability_scores):
    """
    This function generages the character's:
    profession,
    maximum load,
    any magical capabilities or holy powers,
    and allignment.
    """

def starting_gold():
    """
    This function generages and returns the character's starting gold as an int.
    """
    roll = d_roll(os.urandom(16), t = 6, c = 3, m = 0)
    return roll * 10

def name_generator():
    """
    This function creates a randomly generated name based on the parameters
    layed out in the revived rulebook
    returns a string
    """
    name = ''
    vowels = 'aeiouy'
    consonants = 'bcdfghjklmnpqrstvwxz'
    name_length = d_roll(os.urandom(16), t = 6, c = 2, m = 0)
    for i in range(name_length):
        vowel_roll = d_roll(os.urandom(16), t = 6, c = 1, m = 0)
        consonant_roll = d_roll(os.urandom(16), t = 20, c = 1, m = 0)
        if (vowel_roll + consonant_roll) % 2 == 0:
            try:
                if name[-2] in vowels and name[-1] in vowels:
                    name += consonants[consonant_roll - 1]
                else:
                    name += vowels[vowel_roll - 1]
            except IndexError:
                name += vowels[vowel_roll - 1]
        else:
            try:
                if name[-3] in consonants and name[-2] in consonants and name[-1] in consonants:
                    name += vowels[vowel_roll - 1]
                else:
                    name += consonants[consonant_roll - 1]
            except IndexError:
                name += consonants[consonant_roll - 1]
    return name




#ask for generation method 
#generation_method = 
#if generation_method == 'Classic':
#    #ask for character class
#    char_type = ''
#    ability_generator()
#    #set experience boost
#    ability_adjustments(char_type, ability_scores)
#    hit_dice_hit_points_and_saves(char_type, ability_scores)
#    attributes_and_magical_capabilities(char_type, ability_scores)
#    starting_gold()
#    ask for custom name or random name
#    name_generator()
#else:
#    ability_generator()
#    # show abilities and ask for character class
#    char_type = ''
#    #set experience boost
#    hit_dice_hit_points_and_saves(char_type, ability_scores)
#    attributes_and_magical_capabilities(char_type, ability_scores)
#    starting_gold()
#    ask for custom name or random name
#    name_generator()



