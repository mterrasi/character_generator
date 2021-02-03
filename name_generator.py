#!/usr/bin/env python3
#---------------------
#Name: OD&D Revived Name Generator
#Version: 1.0
#Date: 2020-12-17
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

def name_generator(Title = False, Mult_Barr = False):
    """
    This function creates a randomly generated name based on the parameters
    laid out in the revived rulebook
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
    if Mult_Barr:
        barr_roll = d_roll(os.urandom(16), t = 3, c = 1, m = 0)
        if barr_roll != 1:
            for i in range(barr_roll - 1):
                name += '-'
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
    if Title:
        titles = [' the Jocund', ' the Pure', ' the Wise', ' the White',
                    ' the Gray', ' the Black', ' the Steadfast', ' the Nimble',
                    ' the Brave', ' the Lion', ' the Fox', ' the Bear',
                    ' the Swift', ' the Just', ' the Bold', ' the Boar',
                    ' the Bat', ' the Wolf', ' the Potent', ' the Auspicious']
        title_roll = d_roll(os.urandom(16), t = 20, c = 1, m = 0)
        name += titles[title_roll - 1]
    return name

print(name_generator(Title = False, Mult_Barr = False))