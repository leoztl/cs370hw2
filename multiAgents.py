# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pickle import NONE
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        #print("successorgamestate: ",successorGameState)
        newPos = successorGameState.getPacmanPosition()
        #print("newPos: ",newPos)
        newFood = successorGameState.getFood()
        #print("newFood: ",newFood.asList())
        newGhostStates = successorGameState.getGhostStates()
        #print("newGhostStates: ",type(newGhostStates[0]))
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        aveFoodDistance = self.averageDis(newPos,newFood)
        minGhoustDistance = self.minGhoustDis(newPos,newGhostStates)
        warning = self.ghostWarning(newPos,newGhostStates)
        return successorGameState.getScore() - 0.5*minGhoustDistance - aveFoodDistance + warning
    
    def averageDis(self,pacpos,newFood):
        # average distance from food point to pacman
        if len(newFood.asList()) == 0:
            return 1
        sum = 0
        for food in newFood.asList():
            sum += util.manhattanDistance(pacpos,food)
        return sum/len(newFood.asList())
    
    def minGhoustDis(self,pacpos,newGhostStates):
        # minimum ghost distance
        minimum = util.manhattanDistance(pacpos,newGhostStates[0].getPosition())
        for ghost in newGhostStates:
            dis = util.manhattanDistance(pacpos,ghost.getPosition())
            if dis < minimum:
                minimum = dis
        if dis == 0:
            return 1
        return dis
    
    def ghostWarning(self,pacpos, newGhostStates):
        # warning if the ghost is too close (<2)
        minDis = self.minGhoustDis(pacpos,newGhostStates)
        if minDis < 2:
            return -100
        else:
            return 0

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        value,action = self.max_value(gameState,0)
        return action
        
        
    def max_value(self,gameState,depth):
        if depth == self.depth:
            return self.evaluationFunction(gameState), None
        value = float('-inf')
        move = None
        actionlist = gameState.getLegalActions(0)
        if actionlist == []:
            return self.evaluationFunction(gameState), None
        for action in actionlist:
            newState = gameState.generateSuccessor(0, action)
            newValue, _ = self.min_value(newState,depth,1)
            if newValue > value:
                value = newValue
                move = action
        return value, move
            
            
    def min_value(self, gameState,depth,index):
        if depth == self.depth:
            return self.evaluationFunction(gameState), None
        value = float('inf')
        move = None
        actionlist = gameState.getLegalActions(index)
        if actionlist == []:
            return self.evaluationFunction(gameState), None
        for action in actionlist:
            newState = gameState.generateSuccessor(index, action)
            if index == gameState.getNumAgents()-1:
                newValue, _ = self.max_value(newState,depth+1)
            else:
                newValue, _ = self.min_value(newState,depth,index+1)
            if newValue < value:
                value = newValue
                move = action
        return value, move
    
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value,action = self.max_value(gameState,float('-inf'),float('inf'),0)
        return action
    
    def max_value(self,gameState,alpha,beta,depth):
        #print(0,alpha,beta)
        if depth == self.depth:
            return self.evaluationFunction(gameState), None
        value = float('-inf')
        move = None
        actionlist = gameState.getLegalActions(0)
        if actionlist == []:
            return self.evaluationFunction(gameState), None
        for action in actionlist:
            newState = gameState.generateSuccessor(0, action)
            newValue, _ = self.min_value(newState,alpha,beta,depth,1)
            if newValue > value:
                value = newValue
                move = action
            alpha = max(alpha,value)
            if value > beta:
                #print(value,beta)
                return value,move
        return value, move
    
    def min_value(self, gameState,alpha,beta,depth,index):
        #print(index,alpha,beta)
        if depth == self.depth:
            return self.evaluationFunction(gameState), None
        value = float('inf')
        move = None
        actionlist = gameState.getLegalActions(index)
        if actionlist == []:
            return self.evaluationFunction(gameState), None
        for action in actionlist:
            newState = gameState.generateSuccessor(index, action)
            if index == gameState.getNumAgents()-1:
                newValue, _ = self.max_value(newState,alpha,beta,depth+1)
            else:
                newValue, _ = self.min_value(newState,alpha,beta,depth,index+1)
            if newValue < value:
                value = newValue
                move = action
            beta = min(value, beta)
            if value < alpha:
                return value,move
        return value, move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        value,action = self.max_value(gameState,0)
        return action
    
    def max_value(self,gameState,depth):
        if depth == self.depth:
            return self.evaluationFunction(gameState), None
        value = float('-inf')
        move = None
        actionlist = gameState.getLegalActions(0)
        if actionlist == []:
            return self.evaluationFunction(gameState), None
        for action in actionlist:
            newState = gameState.generateSuccessor(0, action)
            newValue, _ = self.min_value(newState,depth,1)
            if newValue > value:
                value = newValue
                move = action
        return value, move
            
            
    def min_value(self, gameState,depth,index):
        if depth == self.depth:
            return self.evaluationFunction(gameState), None
        value = 0
        move = None
        actionlist = gameState.getLegalActions(index)
        if actionlist == []:
            return self.evaluationFunction(gameState), None
        prob = 1/len(actionlist)
        for action in actionlist:
            newState = gameState.generateSuccessor(index, action)
            if index == gameState.getNumAgents()-1:
                newValue, _ = self.max_value(newState,depth+1)
            else:
                newValue, _ = self.min_value(newState,depth,index+1)
            value += newValue * prob
            move = action
        return value, move

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPosition = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    Ghost = currentGameState.getGhostStates()
        
    averageFoodDistance = averageDis(pacmanPosition,Food)
    minimumGhostDistance = minGhoustDis(pacmanPosition,Ghost)
    
    return currentGameState.getScore() - averageFoodDistance - 0.5*minimumGhostDistance
    
def averageDis(pacpos,newFood):
        # average distance from food point to pacman
        if len(newFood.asList()) == 0:
            return 1
        sum = 0
        for food in newFood.asList():
            sum += util.manhattanDistance(pacpos,food)
        return sum/len(newFood.asList())

def minGhoustDis(pacpos,newGhostStates):
        # minimum ghost distance
        minimum = util.manhattanDistance(pacpos,newGhostStates[0].getPosition())
        for ghost in newGhostStates:
            dis = util.manhattanDistance(pacpos,ghost.getPosition())
            if dis < minimum:
                minimum = dis
        if dis == 0:
            return 1
        return dis
# Abbreviation
better = betterEvaluationFunction