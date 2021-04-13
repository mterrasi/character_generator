# Character Generator

This program creates a character for the tabletop D&D game in accordance with the Revived ruleset, produced by Blacktower Games. This repository contains the generator program, text files which are used to create the tables that the attributes are pulled from, along with a standalone name generator.

# How the Program Works
The generator program is run in the command line and is meant to replicate the normal process of creating a D&D character. Normally, to create a character, one would roll a set of dice 15-20 times and reference a set of corresponding tables to determine the character’s various attributes and abilities. The generator program contains a dice rolling function, a function that creates indexible lists from the text files, as well as functions for each step laid out in the Revived ruleset. When run, the user is prompted to select a few options for the creation process such as character class and starting level, and then the program goes ahead and makes all of the necessary rolls, indexing of tables, and prints out the character’s stats to the command line.

# Dice Roll Function
The dice roll function simulates random rolls by using the built-in python library random. To further insure that the numbers generated are in fact random, the function uses the built-in python library os, and pulls 16 bytes of random data to use as the seed for the random library’s functions. To simulate a die roll the randint function is called to pick a number between 1 and t, t being the size or type of the “die.”

# Text Files
The included text files serve as both the list of possible outcomes for each roll as well as determine the probability of each of the different options. These options and probabilities are taken from the Revived ruleset. For outcomes that are more common, for example some professions are more common than others, the option is listed multiple times in the list. The dice roll function then “rolls” a die by randomly selecting a number between 1 and the length of the table. Therefore, if you would like to add your own attributes to the tables, or would like to make an option more or less likely, you can simply add or subtract items to the text files.

The text file listed as professions_list serves as a glossary for the professions listed in the professions_table file. In the generator function after the profession is determined, the function profession_definition creates a python dictionary with the professions and their definitions which is then queried to produce the definition to include in the output along with the rest of the character stats.

# Name Generator Program
This program contains the name generator function and dice roll function from the main program and is intended for name generation fun without having to create an entire character. (Enjoy attempting to pronounce the names that are created!)
