from game_componenets.game import Game
from agents.agent import Agent
from copy import deepcopy


class GameEngine:
    def __init__(self, isSimulation, game: Game, redPlayer: Agent = None, greenPlayer: Agent = None):
        self.isRedPlayerTurn = True
        self.game = game
        self.players = {False: greenPlayer,
                        True: redPlayer}
        self.isSimulationMode = isSimulation
        self.isPlayingMode = not isSimulation
        self.gamePlayCounts = 0
        game.prepare()
        # game.staticPrepareEvaluation()
    def play(self):
        gameAfterMove = self.players[self.isRedPlayerTurn].applyHeuristic(deepcopy(self.game))
        self.isRedPlayerTurn = not self.isRedPlayerTurn
        self.game = gameAfterMove
        self.gamePlayCounts += 1

    def playvsHuman(self):
        gameAfterMove = self.players[False].applyHeuristic(deepcopy(self.game))
        # self.isRedPlayerTurn = not self.isRedPlayerTurn
        self.game = gameAfterMove
        self.gamePlayCounts += 1

    def gameEnded(self):
        return (self.game.cityCount[True] == 0 or self.game.cityCount[False] == 0)
