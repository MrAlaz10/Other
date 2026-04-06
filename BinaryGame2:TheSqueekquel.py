#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 02:04:10 2026

@author: anthony
"""

import random
import time

def binary_game(difficulty,name):
    playing = True
    score = 0
    while playing:
        answer = random.randint(1,difficulty)   #establishes answer
        random_binary = bin(answer)             #and coverts to binary
        print(random_binary)                    #displays binary
        user_converted_answer = 0

        while user_converted_answer != answer:
            try:    
                user_converted_answer = int(input())
                if user_converted_answer != answer:
                    print(f"Sorry {name}, that's not correct! Score: {score}")
                    time.sleep(3)
                    return score
            except ValueError:
                print("integers only!")
        score += 1
        print(f"Correct! Score: {score}")
    return "Thanks for playing!"

def main_menu():

    while True:
        main_menu_selection = input("Welcome to Binary Game 2: The Squeekquel! \nPlease type to make a selection: \n-Play\n-Leaderboards\n-Quit\n").lower()
        if main_menu_selection == "play":
            while True:
                name = input("Please type your name: ").lower()
                break
            while True:
                difficulty = input("Please type a difficulty, or type 'back' to go back:\nEasy\nMedium\nHard\n").lower()
                if difficulty == "easy":
                    saved = binary_game(10,name)
                    with open("leaderboardseasy.txt", "a") as file:
                        file.write(f"{name},{saved}\n")
                    break
                elif difficulty == "medium":
                    saved = binary_game(50,name)
                    with open("leaderboardsmedium.txt", "a") as file:
                        file.write(f"{name},{saved}\n")
                    break
                elif difficulty == "hard":
                    saved = binary_game(100,name)
                    with open("leaderboardshard.txt", "a") as file:
                        file.write(f"{name},{saved}\n")
                    break
                elif difficulty == "back":
                    break
                else:
                    print("Sorry! Please try again")
                    time.sleep(1.5)
        if main_menu_selection == "leaderboards":
            leaderboards = []
            leaderboard_loop = True
            while leaderboard_loop == True:
                which_leaderboard = input("Which leaderboard would you like to view?\n-Easy\n-Medium\n-Hard\n-Back\n").lower()
                if which_leaderboard == "easy":
                    try:
                        with open("leaderboardseasy.txt", "r") as file:
                            for line in file:
                                line = line.strip()
                                line = line.split(",")
                                saved_name = line[0]
                                saved_score = int(line[1])
                                leaderboards.append([saved_name,saved_score])
                        leaderboard_loop = False
                    except FileNotFoundError:
                        print("Error! You must play the game to view the leaderboard.")

                elif which_leaderboard == "medium":
                    try:
                        with open("leaderboardsmedium.txt", "r") as file:
                            for line in file:
                                line = line.strip()
                                line = line.split(",")
                                saved_name = line[0]
                                saved_score = int(line[1])
                                leaderboards.append([saved_name,saved_score])
                        leaderboard_loop = False
                    except FileNotFoundError:
                        print("Error! You must play the game to view the leaderboard.")
                elif which_leaderboard == "hard":
                    try:
                        with open("leaderboardshard.txt", "r") as file:
                            for line in file:
                                line = line.strip()
                                line = line.split(",")
                                saved_name = line[0]
                                saved_score = int(line[1])
                                leaderboards.append([saved_name,saved_score])
                        leaderboard_loop = False
                    except FileNotFoundError:
                        print("Error! You must play the game to view the leaderboard.")
                elif which_leaderboard == "back":
                    break
                else:
                    print("Sorry! Please try again")
                    time.sleep(1.5)
            leaderboards.sort(key=lambda x: x[1], reverse=True)
            while True:
                for record in leaderboards:
                    print(f"Name: {record[0]}, Score: {record[1]}")
                leaderboards_exit = input("Type 'back' to return to the main menu:\n").lower()
                if leaderboards_exit == "back":
                    break
                else:
                    print("Sorry! Please try again")
                    time.sleep(1.5)
        if main_menu_selection == "quit":
            return "Thanks for playing!"
        
            
print(main_menu())
