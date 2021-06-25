#!/usr/bin/env python3
#---------------------
#Name: OD&D Revived Attribute Generator for Lambda
#Version: 1.0
#Date: 2021-06-24
#---------------------

import os
import random
import json
from datetime import datetime

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

def experience_boost_determination(ability_scores, prime_ability):
    """
    This function determines any applicable experience boost.
    Assumes abilities is a list of tuples (ability as str, stat as int)
    Assumes prime_ability is a string.
    Returns a percentage as a str.
    """
    abilities = ['Strength', 'Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Charisma']
    stats = ability_scores
    prime = abilities.index(prime_ability) 
    if stats[prime][1] == 13 or stats[prime][1] == 14:
        experience_boost = '5%'
    elif stats[prime][1] >= 15:
        experience_boost = '10%'
    else:
        experience_boost = '0%'
    return experience_boost

def ability_adjustments(prime_ability, ability_scores, char_level):
    """
    This function produces any ability adjustments for the character
    based upon the rolled ability scores.
    Assumes prime ability is a string, ability_scores the stats returned from ability_generator, 
    and char_level and int.
    Returns: a list of all ability adjustments, listed as strings.
    """
    adjustments = []
    abilities = ['Strength', 'Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Charisma']
    prime = abilities.index(prime_ability) 
    ability_scores_with_prime = ability_scores[:]
    ability_scores_with_prime[prime] = (prime_ability, (ability_scores[prime][1] + char_level))
    if ability_scores_with_prime[0][1] >= 14:
        adjustments.append('+1 to Melee and Thrown Weapon Damage')
    if ability_scores_with_prime[1][1] > 10:
        num_langs = ability_scores_with_prime[1][1] - 10
        adjustments.append('+{} Languages'.format(num_langs))
    if ability_scores_with_prime[2][1] > 10:
        comp_chance = (ability_scores_with_prime[2][1] - 10) * 10
        adjustments.append('+{}% Chance Comprehend Spoken Language'.format(comp_chance))
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
    Returns: system_shock, hit_dice, hit_points, char_saves, and melee and missile to-hit 
    """
    saves = ['Death Ray/Poison', 'Wand/Paralysis/Polymorph', 'Petrification/Turn to Stone',
             'Dragon Breath/Area of Effect', 'Spells/Rods/Staves']
    char_saves = []
    #First indexing number is because of addition of experience bonus to ability scores.
    constitution = ability_scores[4][1]
    #Calculate System Shock
    system_shock = (20 - (constitution + char_level))
    #Hit Dice, Hit Points, To-Hit
    hit_points = 0
    if char_level == 0:
            if char_type == 'Fighter':
                whole_hit_dice = 1
                hit_dice = whole_hit_dice
                hit_points = 6
                to_hit = '+1, +1'
            else:
                whole_hit_dice = 1
                hit_dice = '1/2'
                hit_points = 3
                to_hit = '+1, +1'
    else:
        if char_type == 'Fighter':
            whole_hit_dice = char_level
            hit_dice_modifier = char_level
            hit_dice = '{}+{}'.format(whole_hit_dice, hit_dice_modifier)
            if char_level > 1:
                hit_points = d_roll(os.urandom(16), t = 6, c = (whole_hit_dice - 1), m = (whole_hit_dice - 1))
            hit_points += 7
            to_hit = '+{}, +{}'.format((whole_hit_dice + 1), (whole_hit_dice + 1))
        elif char_type == 'Cleric':
            whole_hit_dice = char_level
            hit_dice = whole_hit_dice
            if char_level > 1:
                hit_points = d_roll(os.urandom(16), t = 6, c = (hit_dice - 1), m = 0)
            hit_points += 6
            to_hit = '+{}, +{}'.format(hit_dice, hit_dice)
        elif char_type == 'Magic User':
            if char_level > 1:
                if char_level % 2 == 0:
                    whole_hit_dice = char_level // 2
                    hit_dice = '{}+1'.format(whole_hit_dice)
                    hit_points = d_roll(os.urandom(16), t = 6, c = whole_hit_dice, m = 0)
                    to_hit = '+{}, +{}'.format((whole_hit_dice + 1), (whole_hit_dice + 1))
                else:
                    whole_hit_dice = (char_level // 2) + 1
                    hit_dice = whole_hit_dice
                    hit_points = d_roll(os.urandom(16), t = 6, c = hit_dice, m = 1)
                    to_hit = '+{}, +{}'.format(hit_dice, hit_dice)
            else:
                whole_hit_dice = char_level
                hit_dice = whole_hit_dice
                to_hit = '+{}, +{}'.format(hit_dice, hit_dice)
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
    return system_shock, hit_dice, hit_points, char_saves, to_hit

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
    This function generates the character's:
    profession,
    maximum load,
    and alignment.
    """
    if sex_choice == 'random':
        sex_roll = d_roll(os.urandom(16), t = 2, c = 1, m = 0)
        if sex_roll == 1:
            sex = 'female'
        else:
            sex = 'male'
    elif sex_choice == 'male':
        sex = 'male'
    elif sex_choice == 'female':
        sex = 'female'
    if not older:
        age_roll = d_roll(os.urandom(16), t = 6, c = 2, m = 0)
        age = 11 + char_level + age_roll
    elif older:
        age_roll = d_roll(os.urandom(16), t = 6, c = 3, m = 0)
        age = 21 + char_level + age_roll
    height_roll = d_roll(os.urandom(16), t = 20, c = 1, m = 0)
    if sex == 'male':
        if height_roll == 1:
            height = 'Very Short (4ft 8in - 4ft 11in)'
        elif height_roll < 6:
            height = 'Short (5ft - 5ft 3in)'
        elif height_roll < 16:
            height = 'Average (5ft 4in - 5ft 8in)'
        elif height_roll < 20:
            height = 'Tall (5ft 9in - 6ft)'
        else:
            height = 'Very Tall (6ft 1in - 6ft 4in)'
    elif sex == 'female':
        if height_roll == 1:
            height = 'Very Short (4ft 6in - 4ft 9in)'
        elif height_roll < 6:
            height = 'Short (4ft 10in - 5ft 1in)'
        elif height_roll < 16:
            height = 'Average (5ft 2in - 5ft 6in)'
        elif height_roll < 20:
            height = 'Tall (5ft 7in - 5ft 10in)'
        else:
            height = 'Very Tall (5ft 11in - 6ft 2in)'
    #Weight = (str + con)
    weight = ability_scores[0][1] + ability_scores[4][1]
    if sex == 'male':
        if weight_choice == 'light':
            weight *= 7
        elif weight_choice == 'average':
            weight *= 8
        else:
            weight *= 9
    else:
        if weight_choice == 'light':
            weight *= 6
        elif weight_choice == 'average':
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
    #maximum load
    maximum_load = '{} cn'.format(ability_scores[0][1] * 150)
    #alignment
    alignment_roll = d_roll(os.urandom(16), t = 20, c = 1, m = 0)
    if alignment_roll < 5:
        alignment = 'Chaotic'
    elif alignment_roll < 17:
        alignment = 'Neutral'
    else:
        alignment = 'Lawful'
    #identifying quality
    if id_quality and ability_scores[5][1] < 7:
        id_quality_table = attribute_table_generator('identifying_quality_table.txt')
        id_quality_roll_1 = d_roll(os.urandom(16), t = len(id_quality_table), c = 1, m = 0)
        id_quality_1 = id_quality_table[id_quality_roll_1 - 1]
        id_quality_roll_2 = d_roll(os.urandom(16), t = len(id_quality_table), c = 1, m = 0)       
        id_quality_2 = id_quality_table[id_quality_roll_2 - 1] 
        id_quality = '{}, and {}'.format(id_quality_1, id_quality_2)
    elif ability_scores[5][1] < 7:
        id_quality_table = attribute_table_generator('identifying_quality_table.txt')
        id_quality_roll = d_roll(os.urandom(16), t = len(id_quality_table), c = 1, m = 0)
        id_quality = id_quality_table[id_quality_roll - 1] 
    elif id_quality:
        id_quality_table = attribute_table_generator('identifying_quality_table.txt')
        id_quality_roll = d_roll(os.urandom(16), t = len(id_quality_table), c = 1, m = 0)
        id_quality = id_quality_table[id_quality_roll - 1]
    return (sex, age, height, weight, eye_color, hair_color, hair_type,
            hair_length, skin_color, handedness, dental_status, profession,
            maximum_load, id_quality, alignment)

def get_profession_definition(filename, profession):
    """
    This function reads a txt file and creates a list object containing the
    table used to pick attributes.
    Returns: a list
    """
    prof_def_doc = open(filename, 'r')
    prof_dict = {}
    for line in prof_def_doc:
        new_line = line.split(':')
        prof_dict[new_line[0]] = new_line[1].strip()
    prof_def_doc.close()
    return prof_dict[profession]

def magical_capabilities(char_type, char_level, name_deity = False):
    """
    This function generates the character's magical capabilities or holy powers.
    """
    if char_type == 'Cleric':
        if name_deity == True:
            deity_name = name_generator(Title = False, Mult_Barr = False)
        else:
            deity_name = 'TBD'
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
        if char_level == 0:
            turning_events = 'N/A'
        else:
            turning_events = turning_events_table[char_level - 1]
        spell_slots_table = attribute_table_generator('cleric_spell_slots_table.txt')
        if char_level == 0:
            spell_slots = 'N/A'
        else:
            spell_slots = spell_slots_table[char_level - 1]
    elif char_type == 'Magic User':
        spell_table = attribute_table_generator('spell_table.txt')
        if char_level > 0:
            starting_spell_roll = d_roll(os.urandom(16), t = len(spell_table), c = 1, m = 0)
            starting_spell = spell_table[starting_spell_roll - 1]
        else:
            starting_spell = 'N/A'
        spell_slots_table = attribute_table_generator('magic_user_spell_slots_table.txt')
        if char_level == 0:
            spell_slots = 'N/A'
        else:
            spell_slots = spell_slots_table[char_level - 1]
    if char_type == 'Cleric':
        return deity_name, domain, edict, anathema, turning_events, spell_slots
    else:
        return starting_spell, spell_slots

def get_starting_gold():
    """
    This function generates and returns the character's starting gold as an int.
    """
    roll = d_roll(os.urandom(16), t = 6, c = 3, m = 0)
    return roll * 10

def name_generator(Title = False, Mult_Barr = False):
    """
    This function creates a randomly generated name based on the parameters
    laid out in the revived rulebook
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

def lambda_handler(event, context):
    ability_scores = [('Strength', event['Strength']), ('Intelligence', event['Intelligence']), ('Wisdom', event['Wisdom']), ('Dexterity', event['Dexterity']), ('Constitution', event['Constitution']), ('Charisma', event['Charisma'])]

    if event['char_type'] == 'fighter':
        char_type = 'Fighter'
        prime_ability = 'Strength'
    elif event['char_type'] == 'cleric':
        char_type = 'Cleric'
        prime_ability = 'Wisdom'
    elif event['char_type'] == 'magic user':
        char_type = 'Magic User'
        prime_ability = 'Intelligence'
    elif event['char_type'] == 'random':
        char_type_roll = d_roll(os.urandom(16), t = 3, c = 1, m = 0)
        if char_type_roll == 1:
            char_type = 'Fighter'
            prime_ability = 'Strength'
        elif char_type_roll == 2:
            char_type = 'Cleric'
            prime_ability = 'Wisdom' 
        else:
            char_type = 'Magic User'
            prime_ability = 'Intelligence'

    experience_boost = experience_boost_determination(ability_scores, prime_ability)

    adjustments = ability_adjustments(prime_ability, ability_scores, event['char_level'])

    system_shock, hit_dice, hit_points, char_saves, to_hit = hit_dice_hit_points_and_saves(char_type, event['char_level'], ability_scores)

    sex, age, height, weight, eye_color, hair_color, hair_type, hair_length, skin_color, handedness, dental_status, profession, maximum_load, id_quality, alignment = attributes(char_type, ability_scores, event['char_level'], event['sex_choice'], event['weight_choice'], event['older'], event['id_quality'])

    profession_definition = get_profession_definition('professions_list.txt', profession)

    if char_type == 'Cleric':
        deity_name, domain, edict, anathema, turning_events, spell_slots = magical_capabilities(char_type, event['char_level'], event['name_deity'])
    elif char_type == 'Magic User':
        starting_spell, spell_slots = magical_capabilities(char_type, event['char_level'])

    starting_gold = get_starting_gold()

    if event['char_name'] == 'random':
        name = name_generator()
    else:
        name = event['char_name']

    #translates level into experience points for json output
    if event['char_level'] > 1:
        if char_type == 'Fighter' or char_type == 'Cleric':
            level_xp = (2000 * 2**(event['char_level'] - 2))
        elif char_type == 'Magic User':
            level_xp = (2500 * 2**(event['char_level'] - 2))
    else:
        level_xp = 0

    #hight for json
    if sex == 'male':
        if height == 'Very Short (4ft 8in - 4ft 11in)':
            height_foot = 4
            height_inch = 10
        elif height == 'Short (5ft - 5ft 3in)':
            height_foot = 5
            height_inch = 2
        elif height == 'Average (5ft 4in - 5ft 8in)':
            height_foot = 5
            height_inch = 7
        elif height == 'Tall (5ft 9in - 6ft)':
            height_foot = 5
            height_inch = 11
        else:
            height_foot = 6
            height_inch = 3
    else:
        if height == 'Very Short (4ft 6in - 4ft 9in)':
            height_foot = 4
            height_inch = 8
        elif height == 'Short (4ft 10in - 5ft 1in)':
            height_foot = 5
            height_inch = 0
        elif height == 'Average (5ft 2in - 5ft 6in)':
            height_foot = 5
            height_inch = 5
        elif height == 'Tall (5ft 7in - 5ft 10in)':
            height_foot = 5
            height_inch = 9
        else:
            height_foot = 6
            height_inch = 1

    #inputs starting spell into json
    if char_type == 'Magic User' and event['char_level'] > 0:
        spells = [{"level": 1, "name": starting_spell}]
    elif char_type == 'Cleric' and event['char_level'] > 1:
        spells_level = event['char_level'] // 2
        if spells_level > 5:
            spells_level = 5
        cleric_spell_filename = 'cleric_spells_level_' + str(spells_level) + '.json'
        cleric_spell_file = open(cleric_spell_filename, 'r')
        spells = json.load(cleric_spell_file)
        cleric_spell_file.close()
    else:
        spells = []

    if char_type == 'Cleric':
        turning_event_stats = '\n' + 'Turning Events: ' + turning_events
        god_stats = '\n' + 'Deity Name: ' + deity_name + ', ' + 'Domain: ' + domain + ', ' + 'Edict: ' + edict + ', ' + 'Anathema: ' + anathema
    else:
        turning_event_stats = None
        god_stats = None

    if id_quality == False:
        id_quality = None
    else:
        id_quality = '\n' + 'Identifying Quality: ' + id_quality

    return {
        "character": {
            "abilities": {
                "strength": ability_scores[0][1],
                "intelligence": ability_scores[1][1],
                "wisdom": ability_scores[2][1],
                "dexterity": ability_scores[3][1],
                "constitution": ability_scores[4][1],
                "charisma": ability_scores[5][1]
            },
            "saving_throws": {
                "system_shock": system_shock,
                "poison": char_saves[0][1],
                "paralysis": char_saves[1][1],
                "petrification": char_saves[2][1],
                "dragon_breath": char_saves[3][1],
                "spell": char_saves[4][1] 
            },
            "experience": [
                {
                    "experiences": [
                        {
                            "points": level_xp
                        }
                    ],
                    "class": char_type,
                    "prime": prime_ability.lower(),
                    "spellbook": {
                        "spells": spells
                    },
                    "spells": [],
                    "bonus_xp": experience_boost
                }
            ],
            "purse": {
                "platinum": 0,
                "gold": starting_gold,
                "silver": 0,
                "copper": 0,
                "gems": []
            },
            "magic_items": [],
            "known_languages": [
                "Common"
            ],
            "weapons": [],
            "armor": [],
            "slung_items": [],
            "spellbook": None,
            "mounts": [],
            "deleted": False,
            "name": name,
            "race": "Human",
            "base_movement": 60,
            "current_hp": hit_points,
            "total_hp": hit_points,
            "armor_class": 9,
            "hirelings": [],
            "age": age,
            "sex": sex,
            "alignment": alignment,
            "profession": profession,
            "height_foot": height_foot,
            "height_inch": height_inch,
            "weight": weight,
            "hair_color": hair_color,
            "hair_length": hair_length,
            "hair_style": hair_type,
            "eye_color": eye_color,
            "skin_color": skin_color,
            "appearance": [
                'Dental status: ' + dental_status, 
                '\n' + handedness,
                id_quality,
                '\n' + profession + ': ' + profession_definition,
                turning_event_stats,
                god_stats
            ]
        },
        "notes": [],
        "sessions": []
    }
    