import random
import numpy as np


def ai_make_decision(strategy, ai_coins, ai_number):
    return strategy[ai_coins, ai_number]


def take_players_coin(players_coins, quota):
    players_coins -= 1
    quota += 1
    return players_coins, quota


def take_ais_coin(ai_coins, quota):
    ai_coins -= 1
    quota += 1
    return ai_coins, quota


def reward_winner(winners_coins, quota):
    winners_coins += quota
    quota = 0
    return winners_coins, quota


def coin_game():
    print("Both players start with 10 coins.")
    strategy = np.load("strategy.npy", allow_pickle=True)
    number_values = [i / 100 for i in range(101)]
    players_coins = 10
    ai_coins = 10
    quota = 0
    turn = 1
    next_player_number = 0
    remember = False
    while players_coins > 1 and players_coins < 19 and ai_coins > 1 and ai_coins < 19:
        # system
        if remember:
            player_number = next_player_number
        else:
            input("\nPRESS ANY BUTTON TO CONTINUE\n")
            print(f" --------- TURN {turn} ---------\n"
                  f"Your coins: {players_coins};\n"
                  f"Opponents coins: {ai_coins};\n"
                  f"Coins in quota: {quota}.\n")
            player_number = random.choice(number_values)
            players_coins, quota = take_players_coin(players_coins, quota)
            print(f" --- You paid 1 coin and drew number {player_number}")
        remember = False
        print(f"You have {players_coins} coins. Do you continue playing?")
        play = input(f"Type: 'play', 'pass' or 'end' to proceed\n")

        # if player input correct word
        if play.lower() not in ["play", "pass", "end"]:
            remember = True
            print("I don't understand. repeat your decision.\n")
            next_player_number = player_number
            pass

        # ai's decision after successful game continuation
        ai_number = random.choice(number_values)
        ai_coins, quota = take_ais_coin(ai_coins, quota)
        ai_decision = ai_make_decision(strategy, ai_coins, int(ai_number * 100))

        # PLAYER decides to play
        if play.lower() == "play":
            print(f" - You pay additional coin and enter the game with number {player_number}.")
            players_coins, quota = take_players_coin(players_coins, quota)

            # AI decides to pass
            if ai_decision == "pass":
                print(f" --- Opponent drew a number {ai_number} and passed this turn. You win {quota} coins!")
                players_coins += quota
                quota = 0

            # AI decides to play
            elif ai_decision == "play":
                ai_coins, quota = take_ais_coin(ai_coins, quota)
                print(f" - Opponent drew a number {ai_number} and decided to play.")

                # outcomes of the clash!
                if player_number > ai_number:
                    print(f" --- You won! You gain {quota} coins! :D")
                    players_coins, quota = reward_winner(players_coins, quota)
                elif player_number == ai_number:
                    print(f" --- DRAW!!! :O {quota} coins remain in the quota for the upcoming round.")
                else:
                    print(" --- You lost and lose 2 coins ;(")
                    ai_coins, quota = reward_winner(ai_coins, quota)
        # PLAYER decides to pass
        elif play.lower() == "pass":
            # AI decides to pass
            if ai_decision == "pass":
                print(f" - Opponent drew a number {ai_number} and also decided to pass!!!\n"
                      f" --- {quota} coins remain in the quota for the upcoming round.")
            # AI decides to play
            elif ai_decision == "play":
                ai_coins, quota = take_ais_coin(ai_coins, quota)
                print(f" --- Opponent has decided to play with number {ai_number} and won {quota} coins this round.")
                ai_coins, quota = reward_winner(ai_coins, quota)
        # PLAYER quits the game
        elif play.lower() == "end":
            print("You ended the game out of shame or something really important. At least I hope :{ ...!")
            break
        turn += 1
    # end of the game text
    print()
    if players_coins < 2:
        if ai_coins < 2:
            print(" --------- DRAW!!! Both players don't have enough coins to play any longer!")
        else:
            print(" --------- You don't have enough coines and LOST this game :(")
    elif players_coins > 18:
        print(" --------- You WON! Congratulations! :D")
    elif ai_coins > 18:
        print(" --------- You LOST! Good luck next time.")
    elif ai_coins < 2:
        print(" --------- Your opponent have run out of coins! You WON!!!")


coin_game()
