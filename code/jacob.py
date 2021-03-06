# Imports.


import numpy as np
import numpy.random as npr

from SwingyMonkey import SwingyMonkey


VERBOSE = False
ITERS = 20
TICK_LENGTH = 1


class Learner(object):
    '''
    This agent jumps randomly.
    '''

    def __init__(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        #CHANGED
        self.last_velocity = None
        self.old_action = None

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

    def action_callback(self, state):
        if VERBOSE:
            print(state)

        '''
        Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.
        '''

        # You might do some learning here based on the current state and the last state.

        # You'll need to select and action and return it.
        # Return 0 to swing and 1 to jump.
        vdist = state['monkey']['bot'] - state['tree']['bot']
        current_velocity = state['monkey']['vel']

        new_action = 0
        # Jump if we would fall below the tree in the next round)
        if vdist + current_velocity < 10:
            new_action = 1

        new_state  = state

        self.last_action = new_action
        self.last_state  = new_state

        #CHANGED
        if (self.old_action and self.old_action == 10 and self.last_velocity):
            self.gravity = self.last_velocity - current_velocity
            #print((self.gravity))
        self.last_velocity = current_velocity
        self.old_action = new_action + 10


        return self.last_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''

        self.last_reward = reward


def run_games(learner, hist, iters = 100, t_len = 100):
    '''
    Driver function to simulate learning by having the agent play a sequence of games.
    '''
    
    for ii in range(iters):
        # Make a new monkey object.
        swing = SwingyMonkey(sound=False,                  # Don't play sounds.
                             text="Epoch %d" % (ii),       # Display the epoch on screen.
                             tick_length = t_len,          # Make game ticks super fast.
                             action_callback=learner.action_callback,
                             reward_callback=learner.reward_callback)

        # Loop until you hit something.
        while swing.game_loop():
            pass
        
        # Save score history.
        hist.append(swing.score)

        # Reset the state of the learner.
        learner.reset()

    return

if __name__ == '__main__':

    # Select agent.
    agent = Learner()

    # Empty list to save history.
    hist = []

    # Run games. 
    run_games(agent, hist, iters=ITERS, t_len=TICK_LENGTH)

    # Print stats
    scores = sorted(hist)

    print("Num iters:", ITERS)
    print("Average:", sum(scores) / (len(scores) + 0.))
    print("Median:", scores[len(scores) / 2])
    print("Max:", scores[-1])

    # Save history. 
    np.save('hist',np.array(hist))


