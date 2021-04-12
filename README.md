# Character Generator

This program creates a character for the OSR tabletop D&D game in accordance with the Revived ruleset, produced by Blacktower Games. This repository contains the generator program, text files which are used as to create the tables that the attributes are pulled from, along with a separate name generator.

# How the Program Works
The generator program is run in the command line and is meant to replicate normal the process of creating a D&D character. Normally, to create a character, one would roll a set of dice 15-20 times and reference a set of corresponding tables to determine the character’s various attributes and abilities. The generator program contains a dice rolling function, as well as a function that creates indexible lists from the text files, as well as functions for each step laid out in the Revived ruleset. When run, the user is prompted to select a few options for the creation process such as character class, and a starting level, and then the program goes ahead and makes all of the necessary rolls, indexes tables, and prints out the character’s stats to the command line.

# Dice Roll Function
The dice roll function simulates random rolls by using the built-in python library random. To further insure that the numbers generated are in fact random, the function uses the built-in python library os, and pulls 16 bytes of random data to use as the seed for the random library’s functions.

# Name Generator Program
This program is the name generator function taken from the main program for creating fun names without creating an entire character. The program also includes a dice roll function to service the name generator function.
