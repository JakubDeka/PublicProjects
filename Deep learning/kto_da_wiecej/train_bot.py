from generate_objects import *


def train_bot(number_of_coins=20, number_of_values=101, gamma=0.8, epsilon=10 ** (-2), max_iter=10 ** 3):
    play_probabilities = generate_play_transition_matrix(number_of_coins=number_of_coins,
                                                         number_of_values=number_of_values)
    pass_probabilities = generate_pass_transition_matrix(number_of_coins=number_of_coins,
                                                         number_of_values=number_of_values)
    rewards = generate_reward_list(number_of_coins=number_of_coins)

    states = [i for i in range(len(play_probabilities))]
    values = np.zeros(len(play_probabilities))

    delta = 1
    iteration = 0
    while delta > epsilon and iteration < max_iter:
        delta = 0
        iteration += 1
        for state in states:
            prev_values = values[state]
            values[state] = rewards[state % (number_of_coins + 1)] + gamma * max(play_probabilities[state] @ values,
                                                                                 pass_probabilities[state] @ values)
            delta = max(delta, abs(prev_values - values[state]))

    strategy = np.full((number_of_coins + 1, number_of_values), "play", dtype=object)

    for state in states:
        if play_probabilities[state] @ values >= pass_probabilities[state] @ values:
            strategy[state % (number_of_coins + 1), state // number_of_values] = "play"
        else:
            strategy[state % (number_of_coins + 1), state // number_of_values] = "pass"
    print(f"liczba iteracji do wyuczenia bota to {iteration}.")
    print(f"Zmiana dla ostatniej iteracji wynosiła {delta}.")
    np.save("strategy.npy", strategy)


train_bot(max_iter=100, gamma=1)

print(np.load("strategy.npy", allow_pickle=True)[4, :40])