#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 02:04:10 2026

@author: anthony
"""

import random
import time

#print("Hello, welcome to binary practice!")

def binary_game(difficulty):
    playing = True
    while playing:
        answer = random.randint(1,difficulty)       #establishes answer
        random_binary = bin(answer)         #and coverts to binary
        print(random_binary)                #displays binary
        user_converted_answer = 0
        
        while user_converted_answer != answer:
            try:    
                user_converted_answer = int(input())
                if user_converted_answer != answer:
                    print("Sorry, that's not correct! Try again: ")
            except ValueError:
                print("integers only!")
        keep_playing = input("Correct! Would you like to keep playing? [y]/[n]: ")
        if keep_playing != "y" and keep_playing != "n":
            while keep_playing != "y" and keep_playing != "n":
                keep_playing = input("Sorry! I didn't get that. Would you like to keep playing? [y]/[n]: ")
        if keep_playing == "n":
            playing = False
        else:
            print("Yay! Lets keep going!")
    return "Thanks for playing!"

def main_menu():
    while True:
        main_menu_selection = input("Welcome to Binary Game 2: The Squeekquel! \nPlease type to make a selection: \n-Play\n-Leaderboards\n-Quit\n").lower()
        if main_menu_selection == "play":
            while True:
                difficulty = input("Please type a difficulty, or type 'back' to go back:\nEasy\nMedium\nHard\n").lower()
                if difficulty == "easy":
                    return binary_game(10)
                elif difficulty == "medium":
                    return binary_game(50)
                elif difficulty == "hard":
                    return binary_game(100)
                elif difficulty == "back":
                    break
                else:
                    print("Sorry! Please try again")
                    time.sleep(1.5)
        if main_menu_selection == "leaderboards":
            while True:
                print("Leaderboard goes here")
                leaderboards_exit = input("Type 'back' to return to the main menu:\n").lower()
                if leaderboards_exit == "back":
                    break
                else:
                    print("Sorry! Please try again")
                    time.sleep(1.5)
        if main_menu_selection == "quit":
            return "Thanks for playing!"
        
            
print(main_menu())