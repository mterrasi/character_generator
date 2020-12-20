#!/usr/bin/env python3
#---------------------
#Name: OD&D Revived Character Generator
#Version: 1.0
#Date: 2020-12-19
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

def ability_generator(prime_ability):
    """
    This function generates the characters abilities using either
    the classic method or the revived method.
    Determines any experience boost, if applicable.
    Assumes prime_ability is a string.
    Returns the abilities as a list of tuples (ability as str, stat as int),
    and any applicable experience boost.
    """
    abilities = ['Strength', 'Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Charisma']
    stats = []
    for i in range(len(abilities)):
        result = d_roll(os.urandom(16), t = 6, c = 3, m = 0)
        stats.append((abilities[i], result))
    prime = abilities.index(prime_ability) 
    if stats[prime][1] == 13 or stats[prime][1] == 14:
        experience_boost = '5%'
    elif stats[prime][1] >= 15:
        experience_boost = '10%'
    else:
        experience_boost = '0%'
    return stats, experience_boost

def ability_adjustments(prime_ability, ability_scores, char_level):
    """
    This function produces any ability adjustments for the character
    based upon the rolled ability scores.
    Assumes prime ability is a string, ability_scores the stats returned from ability_generator, 
    and char_level and int.
    """
    adjustments = []
    abilities = ['Strength', 'Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Charisma']
    prime = abilities.index(prime_ability) 
    ability_scores_with_prime = ability_scores
    ability_scores_with_prime[prime] = (prime_ability, (ability_scores[prime][1] + char_level))
    if ability_scores_with_prime[0][1] >= 14:
        adjustments.append('+1 to Melee and Thrown Weapon Damage')
    if ability_scores_with_prime[1][1] > 10:
        num_langs = 10 - ability_scores_with_prime[1][1]
        adjustments.append('+{} Languages'.format(num_langs))
    if ability_scores_with_prime[2][1] > 10:
        comp_chance = 10 - ability_scores_with_prime[2][1]
        adjustments.append('+{}% Chance Comprehend Spoken Language'. format(comp_chance))
    if ability_scores_with_prime[3][1] > 13:
        adjustments.append('+1 Missle Weapon Damage')
    if ability_scores_with_prime[4][1] > 13:
        adjustments.append('+1 Hit Point per whole Hit Die')
    if ability_scores_with_prime[5][1] > 13:
        adjustments.append('+1 to Loyalty Base and Reaction Checks')
    if ability_scores_with_prime[1][1] < 8:
        adjustments.append('Inability to Read and Write')
    if ability_scores_with_prime[4][1] < 6:
        adjustments.append('Persistent Ailment/Allergy/Infirmity')
    if ability_scores_with_prime[5][1] < 7:
        adjustments.append('Additional or Mandatory Identifying Quality')
    return adjustments

def hit_dice_hit_points_and_saves(char_type, char_level, ability_scores):
    """
    This function shows the character's hit dice,
    generates the character's hit points,
    and produces the character's saves.
    Inputs:
        char_type - str
        char_level - int
        ability_scores - list of tuples
    """
    #Get list of hit dice, saves, (and possibly to hit) from file.
    saves = ['Death Ray/Poison', 'Wand/Paralysis/Polymorph', 'Petrification/Turn to Stone',
             'Dragon Breath/Area of Effect', 'Spells/Rods/Staves']
    char_saves = []
    #First indexing number is because of addition of experience bonus to ability scores.
    constitution = ability_scores[0][4][1]
    #Calculate System Shock
    system_shock = (20 - (constitution + char_level))
    #Hit Dice, Hit Points
    if char_level == 0:
            if char_type == 'Fighter':
                hit_dice = '1'
                hit_points = 6
            else:
                hit_dice = '1/2'
                hit_points = 3
    else:
        if char_type == 'Fighter':
            whole_hit_dice = char_level
            hit_dice_modifier = char_level
            hit_dice = '{} + {}'.format(whole_hit_dice, hit_dice_modifier)
            if char_level > 1:
                hit_points = d_roll(os.urandom(16), t = 6, c = (whole_hit_dice - 1), m = (whole_hit_dice - 1))
            hit_points += 7
        elif char_type == 'Cleric':
            whole_hit_dice = char_level
            if char_level > 1:
                hit_points = d_roll(os.urandom(16), t = 6, c = (hit_dice - 1), m = 0)
            hit_points += 6
        elif char_type == 'Magic User':
            if char_level % 2 == 1:
                whole_hit_dice = (char_level // 2) + 1
                hit_dice = '{} + 1'.format(whole_hit_dice)
                hit_points = d_roll(os.urandom(16), t = 6, c = whole_hit_dice, m = 0)
            else:
                hit_dice = char_level // 2
                hit_points = d_roll(os.urandom(16), t = 6, c = hit_dice, m = 1)
            hit_points += 6
    if ability_scores[4][1] > 13:
        hit_points += whole_hit_dice
    #Calculate Saves
    if char_type == 'Fighter':
        if char_level == 0:
            save_scores = [14, 15, 16, 17, 18]
        elif char_level < 4:
            save_scores = [12, 13, 14, 15, 16]
        elif char_level < 7:
            save_scores = [10, 11, 12, 13, 14]
        elif char_level < 10:
            save_scores = [8, 9, 10, 11, 12]
        elif char_level < 13:
            save_scores = [6, 7, 8, 9, 10]
        elif char_level < 19:
            save_scores = [4, 5, 6, 7, 8]
        else:
            save_scores= [2, 3, 4, 5, 6]
    elif char_type == 'Cleric':
        if char_level == 0:
                save_scores = [13, 14, 16, 18, 17]
        elif char_level < 5:
            save_scores = [11, 12, 14, 16, 15]
        elif char_level < 9:
            save_scores = [9, 10, 12, 14, 13]
        elif char_level < 13:
            save_scores = [7, 8, 10, 12, 11]
        elif char_level < 17:
            save_scores = [5, 6, 8, 10, 9]
        else:
            save_scores= [3, 4, 6, 8, 7]
    elif char_type == 'Magic User':
        if char_level == 0:
            save_scores = [15, 16, 15, 18, 13]
        elif char_level < 6:
            save_scores = [13, 14, 13, 16, 11]
        elif char_level < 11:
            save_scores = [11, 12, 11, 14, 9]
        elif char_level < 16:
            save_scores = [9, 10, 9, 12, 7]
        else:
            save_scores = [7, 8, 7, 10, 5]
    for i in range(len(saves)):
        char_saves.append((saves[i], save_scores[i]))
    return system_shock, hit_dice, hit_points, char_saves

def attribute_table_generator(filename):
    """
    This function reads a txt file and creates a list object containing the
    table used to pick attributes.
    Returns: a list
    """
    table_doc = open(filename, 'r')
    table = []
    for line in table_doc:
        table.append(line.strip())
    table_doc.close()
    return table

def attributes(char_type, ability_scores, char_level, sex_choice,
                 weight_choice, older = False, id_quality = False):
    """
    This function generages the character's:
    profession,
    maximum load,
    and allignment.
    """
    if sex_choice == 'Random':
        sex_roll = d_roll(os.urandom(16), t = 2, c = 1, m = 0)
    if sex_roll == 0:
        sex = 'Female'
    else:
        sex = 'Male'
    if not older:
        age_roll = d_roll(os.urandom(16), t = 6, c = 2, m = 0)
        age = 11 + char_level + age_roll
    elif older:
        age_roll = d_roll(os.urandom(16), t = 6, c = 3, m = 0)
        age = 21 + char_level + age_roll
    height_roll = d_roll(os.urandom(16), t = 20, c = 1, m = 0)
    if height_roll == 1:
        height = 'Very Short'
    elif height_roll < 6:
        height = 'Short'
    elif height_roll < 16:
        height = 'Average'
    elif height_roll < 20:
        height = 'Tall'
    else:
        height = 'Very Tall'
    #Weight = (str + con)
    weight = ability_scores[0][1] + ability_scores[4][1]
    if sex == 'Male':
        if weight_choice == 'Light':
            weight *= 7
        elif weight_choice == 'Average':
            weight *= 8
        else:
            weight *= 9
    else:
        if weight_choice == 'Light':
            weight *= 6
        elif weight_choice == 'Average':
            weight *= 7
        else:
            weight *= 8
    #eye color
    eye_color_table = attribute_table_generator('eye_color_table.txt')
    eye_roll = d_roll(os.urandom(16), t = len(eye_color_table), c = 1, m = 0)
    eye_color = eye_color_table[eye_roll - 1]
    #hair color
    hair_color_table = attribute_table_generator('hair_color_table.txt')
    hair_color_roll = d_roll(os.urandom(16), t = len(hair_color_table), c = 1, m = 0)
    hair_color = hair_color_table[hair_color_roll - 1]
    #hair type
    hair_type_table = attribute_table_generator('hair_type_table.txt')
    hair_type_roll = d_roll(os.urandom(16), t = len(hair_type_table), c = 1, m = 0)
    hair_type = hair_type_table[hair_type_roll - 1]
    #hair length
    hair_length_table = attribute_table_generator('hair_length_table.txt')
    hair_length_roll = d_roll(os.urandom(16), t = len(hair_length_table), c = 1, m = 0)
    hair_length = hair_length_table[hair_length_roll - 1]
    #skin color
    skin_color_table = attribute_table_generator('skin_color_table.txt')
    skin_color_roll = d_roll(os.urandom(16), t = len(skin_color_table), c = 1, m = 0)
    skin_color = skin_color_table[skin_color_roll - 1]
    #handedness
    handedness_roll = d_roll(os.urandom(16), t = 20, c = 1, m = 0)
    if handedness_roll < 3:
        handedness = 'Left Handed'
    elif handedness_roll < 20:
        handedness = 'Right Handed'
    else:
        handedness = 'Ambidextrous'
    #dental status
    dental_table = attribute_table_generator('dental_status_table.txt')
    dental_roll = d_roll(os.urandom(16), t = len(dental_table), c = 1, m = 0)
    dental_status = dental_table[dental_roll - 1]
    #profession
    profession_table = attribute_table_generator('professions_table.txt') 
    profession_roll = d_roll(os.urandom(16), t = len(profession_table), c = 1, m = 0)
    profession = profession_table[profession_roll - 1]
    #maxmium load
    maximum_load = '{} cn'.format(ability_scores[0][1] * 150)
    #alignmet
    alignment_roll = d_roll(os.urandom(16), t = 20, c = 1, m = 0)
    if alignment_roll < 5:
        alignment = 'Chaotic'
    elif alignment_roll < 17:
        alignment = 'Neutral'
    else:
        alignment = 'Lawful'
    #identifying quality
    if id_quality:
        id_quality_table = attribute_table_generator('identifying_quality_table.txt')
        id_quality_roll = d_roll(os.urandom(16), t = len(id_quality_table), c = 1, m = 0)
        id_quality = id_quality_table[id_quality_roll - 1]
    return (sex, age, height, weight, eye_color, hair_color, hair_type,
            hair_length, skin_color, handedness, dental_status, profession,
            maximum_load, id_quality, alignment)

def magical_capabilities(char_type, char_level, name_deity = False):
    """
    This function generates the character's magical capabilities or holy powers.
    """
    if char_type == 'Cleric':
        if name_deity == True:
            deity_name = name_generator(Title = False, Mult_Barr = False)
        #domain
        domain_table = attribute_table_generator('domain_table.txt')
        domain_roll = d_roll(os.urandom(16), t = len(domain_table), c = 1, m = 0)
        domain = domain_table[domain_roll - 1]
        #edict
        edict_table = attribute_table_generator('edict_table.txt')
        edict_roll = d_roll(os.urandom(16), t = len(edict_table), c = 1, m = 0)
        edict = edict_table[edict_roll - 1]
        #anathema
        anathema_table = attribute_table_generator('anathema_table.txt')
        anathema_roll = d_roll(os.urandom(16), t = len(anathema_table), c = 1, m = 0)
        anathema = anathema_table[anathema_roll - 1]
        #turning events
        turning_events_table = attribute_table_generator('turning_events.txt')
        turning_events = turning_events_table[char_level - 1]
#        spells = 
        spell_slots_table = attribute_table_generator('cleric_spell_slots_table.txt')
        spell_slots = spell_slots_table[char_level - 1]
    elif char_type == 'Magic User':
        spell_table = attribute_table_generator('spell_table.txt')
        starting_spell_roll = d_roll(os.urandom(16), t = len(spell_table), c = 1, m = 0)
        starting_spell = spell_table[starting_spell_roll - 1]
        spell_slots_table = attribute_table_generator('magic_user_spell_slots_table.txt')
        spell_slots = spell_slots_table[char_level - 1]
    if char_type == 'Cleric':
        if name_deity:
            return deity_name, domain, edict, anathema, turning_events, spell_slots
        else:
            return domain, edict, anathema, turning_events, spell_slots
    else:
        return starting_spell, spell_slots

def starting_gold():
    """
    This function generages and returns the character's starting gold as an int.
    """
    roll = d_roll(os.urandom(16), t = 6, c = 3, m = 0)
    return roll * 10

def name_generator(Title = False, Mult_Barr = False):
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
