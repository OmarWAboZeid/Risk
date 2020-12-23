from typing import List, Any

from city import City
from game import Game

HIS_WEAK_CITY_WEIGHT = 1
HIS_STRONG_CITY_WEIGHT = 0

MY_WEAK_CITY_WEIGHT = 0
MY_STRONG_CITY_WEIGHT = 1


class HeuristicsManager:
    def __init__(self):
        pass

    def mySoldiersCount(self, isRedPlayer: bool, game: Game):
        return game.soldiersCount[isRedPlayer]

    def hisSoldiersCount(self, isRedPlayer: bool, game: Game):
        return game.cityCount[isRedPlayer]

    def mySecuredCities(self, isRedPlayer: bool, game: Game):
        return self.__onConflictingPairs(isRedPlayer, game, self.__mySecuredCityWeightCalculator)

    def hisCitiesICanAttack(self, isRedPlayer: bool, game: Game):
        return self.__onConflictingPairs(isRedPlayer, game, self.__hisCityICanAttackWeighCalculator)

    def defensiveAndAttacking(self, isRedPlayer: bool, game: Game):
        return self.mySecuredCities(isRedPlayer, game) + self.hisCitiesICanAttack(
            isRedPlayer, game)

    def differenceOfDefensiveAndAttacking(self, isRedPlayer: bool, game: Game):
        return self.defensiveAndAttacking(isRedPlayer, game) - self.defensiveAndAttacking(not isRedPlayer, game)

    def __onConflictingPairs(self, isRedPlayer: bool, game: Game, calculate) -> int:
        result: int = 0
        myCities: [int] = game.citiesOf(isRedPlayer)
        for myCityId in myCities:
            for adjCityId in game.map.graph[myCityId]:
                if game.cityList[adjCityId].isRedArmy != isRedPlayer:
                    enemyCityId: int = adjCityId
                    result += calculate(isRedPlayer, game, myCityId, enemyCityId)
        return result

    def __mySecuredCityWeightCalculator(self, isRedPlayer: bool, game: Game, myCityId: int, enemyCityId: int):
        hisBonus = game.bonusSoldiers(not isRedPlayer)
        return MY_STRONG_CITY_WEIGHT if (game.cityList[myCityId].armyCount >= game.cityList[
            enemyCityId].armyCount + hisBonus) else MY_WEAK_CITY_WEIGHT

    def __hisCityICanAttackWeighCalculator(self, isRedPlayer: bool, game: Game, myCityId: int, enemyCityId: int):
        return HIS_WEAK_CITY_WEIGHT if (game.cityList[myCityId].armyCount > game.cityList[
            enemyCityId].armyCount + 1) else HIS_STRONG_CITY_WEIGHT
