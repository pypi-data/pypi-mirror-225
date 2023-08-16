import random
from othello_ai_python.board import Board
from othello_ai_python.player import Player, RandomPlayer, reverse
import os
import sys
from io import StringIO
from othello_ai_python.config import *
import math
# import multiprocessing
# import threading
import concurrent.futures
import time

class Engine:
    def __init__(self):
        self.engine = Controller(1, epsilon=math.inf)

    def predict(self, board, color):
        return self.engine.population[0].policy(board, color)

class Controller:
    def __init__(self, population_size, learning_rate=0.0001, epsilon=2):
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
        self.multiprocessing_pool = concurrent.futures.ProcessPoolExecutor(max_workers=num_threads)

        self.population = [Player(i, 3, 'model_' + str(i + 1), self, learning_rate, epsilon)
                           for i in range(population_size)]
        # self.population = [OthelloPlayer(board_size, 0, 3, 'model_1', self, learning_rate, epsilon,
        #                                  epsilon_increment, debugging), OthelloPlayer(board_size, 1, 3, 'model_2', self, 0.00005, epsilon,
        #                                     epsilon_increment, debugging)]

        self.population.append(RandomPlayer())
        self.load()

    def play_two_ai(self, index1, index2):
        return self.play_two_ai_training(index1, index2, False)

    def play_two_ai_training(self, index1, index2, training):
        switch = 0

        if (training):
            # pass
            switch = random.randint(0, 58)
            print("Switch: " + switch)

        # Random Player Index
        rpi = len(self.population) - 1
        move_player = [self.population[rpi], self.population[rpi]]
        learn_player = [self.population[index1], self.population[index2]]

        d = {1: 0, -1: 1}
        colors = {0: 1, 1: -1}

        env = Board()

        # First array corresponds to the states faced by the first player
        # Same with second
        state_array = [[], []]

        for t in range(200):

            if (t == switch):
                move_player = [self.population[index1], self.population[index2]]

            # Chose a move and take it
            move = move_player[t % 2].policy(env, colors[t % 2])

            env, reward, done, info = env.step(move, colors[t % 2])

            observation = env.bits_to_board()

            # if (self.debugging):
            #     print(env.to_play)
            #     print("")
            #     print("Move")
            #     print(move)
            #     print("")
            #
            #     print("Observation")
            #     print(observation)
            #     print("")

            if (not done and t >= switch):
                if (env.to_play == 1):
                    state_array[0].append(observation)
                elif (env.to_play == -1):
                    state_array[1].append(reverse(observation))

            # Check if done. We're only training once we finish the entire
            # episode. Here, the model which makes the last move has number
            # model_num, and the reward it has is reward

            if done:
                if (reward == 0):
                    print("Draw")

                print("Episode finished after {} timesteps".format(t + 1))

                if (len(state_array[0]) == 0):
                    pass

                learn_player[0].add_to_history(state_array[0], reward)
                learn_player[1].add_to_history(state_array[1], -reward)

                return reward
        return reward

    def train(self, episodes):

        for player in self.population:
            player.depth = 1
            player.iterative = False

        # Number of training episodes
        for i in range(self.total_episodes + 1, self.total_episodes + episodes + 1):
            print("Episode: "+str(i))
            # One Round Robin Tournament
            tournament_pairs = []
            for j in range(len(self.population) - 1):
                for k in range(len(self.population) - 1):
                    tournament_pairs.append((j, k))
                    # self.play_two_ai(j, k)

            # futures = [self.thread_pool.submit(self.play_two_ai, *pairs) for pairs in tournament_pairs]
            #
            # for future in concurrent.futures.as_completed(futures):
            #     pass
            results = list(self.thread_pool.map(self.play_two_ai, *zip(*tournament_pairs)))
            # print(results)

            # results = self.thread_pool.map(play_two_ai, tournament_pairs)

            # futures = [self.multiprocessing_pool.submit(self.play_two_ai, *pairs) for pairs in tournament_pairs]
            #
            # for future in concurrent.futures.as_completed(futures):
            #     pass

            # threads = []
            #
            # # Create and start the threads
            # for pair in tournament_pairs:
            #     thread = threading.Thread(target=self.play_two_ai, args=pair)
            #     thread.start()
            #     threads.append(thread)
            #
            # # Wait for all threads to finish
            # for thread in threads:
            #     thread.join()

            # Everyone Trains

            for j in range(len(self.population) - 1):
                self.population[j].train_model()

            if (i % save_frequency == 0):
                self.total_episodes = i
                self.save()

            if (i % wipe_frequency == 0):
                for j in range(len(self.population) - 1):
                    self.population[j].wipe_history()
            # if(i % graph_frequency == 0):
            #     colors = {0: 'green', 1: 'blue'}
            #     total_history_X = []
            #     total_history_y = []
            #     for i in range(len(self.population) - 1):
            #         player = self.population[i]
            #         for game in player.total_history:
            #             for lesson in game:
            #                 total_history_X.append(lesson[0])
            #                 total_history_y.append(lesson[1])
            #         loss = player.model.evaluate(np.array(total_history_X), np.array(total_history_y))
            #         player.loss_tracker.append(loss)
            #         if(i == start_episode + episodes - 1):
            #             plt.plot([graph_frequency * i for i in range(len(player.loss_tracker))], player.loss_tracker, color=colors[i], label="Model "+str(i + 1))
            #     if (i == start_episode + episodes - 1):
            #         plt.xlabel("Epoch")
            #         plt.ylabel("Loss")
            #         plt.title("Loss Tracker")
            #         plt.legend()
            #         plt.show(block=False)  # Add block=False to prevent blocking behavior
            #         plt.pause(0.1)

    def save(self):
        if not os.path.exists(size_folder):
            # Create the folder
            os.makedirs(size_folder)
        for j in range(len(self.population) - 1):
            # create model folder
            model_folder = size_folder + self.population[j].path
            if not os.path.exists(model_folder):
                # Create the folder
                os.makedirs(model_folder)

            # check model version
            counter_file = model_folder+"/version_counter.txt"
            if os.path.exists(counter_file):
                with open(counter_file, "r") as file:
                    version_counter = int(file.read())
            else:
                version_counter = 1

            # create version folder
            version_folder_name = model_folder + "/version_" + str(version_counter)
            if not os.path.exists(version_folder_name):
                # Create the folder
                os.makedirs(version_folder_name)

            # save model
            file_name = version_folder_name + "/model"
            self.population[j].save(file_name)

            # write information file
            info_file = version_folder_name + "/info.txt"
            with open(info_file, "w") as file:
                # add any extra information here
                file.write("Version: " + str(version_counter))
                file.write("\nEpisode:" + str(self.total_episodes))
                # Save the original standard output
                original_stdout = sys.stdout
                # Redirect the standard output to a StringIO object
                stringio = StringIO()
                sys.stdout = stringio
                # Print the model summary
                self.population[j].model.summary()
                # Restore the original standard output
                sys.stdout = original_stdout
                # Get the model summary as a string
                model_summary = stringio.getvalue()
                # add any extra information here
                file.write("\nSummary:\n" + model_summary)
                # file.write("\nEpisode:" + str(episode))

            # Update the version counter file
            version_counter += 1
            with open(counter_file, "w") as file:
                file.write(str(version_counter))

        episode_file = size_folder + "/total_episodes.txt"
        with open(episode_file, "w") as file:
            file.write(str(self.total_episodes))

        print("models saved")

    def load(self):
        for j in range(len(self.population) - 1):
            # check if the model folder exists, and if it does
            # find the latest model version
            model_folder = size_folder + self.population[j].path
            if(os.path.exists(model_folder)):
                counter_file = model_folder + "/version_counter.txt"
                if os.path.exists(counter_file):
                    with open(counter_file, "r") as file:
                        version_counter = int(file.read())



                # Do this to counter the addition of the extra counter
                version_counter -= 1

                version_folder = model_folder+"/version_"+str(version_counter)
                file_name = version_folder + "/model"
                self.population[j].load(file_name)

        episode_file = size_folder + "/total_episodes.txt"
        if os.path.exists(episode_file):
            with open(episode_file, "r") as file:
                self.total_episodes = int(file.read())
        else:
            self.total_episodes = 0
        print("models loaded")
