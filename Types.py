from typing import List

class Offer:
    playerID: str = None
    offerID: str = None
    userID: str = None
    userName: str = None
    price: int = None

    @staticmethod
    def fromJSON(json: dict, playerID: str):
        offer = Offer()

        offer.offerID = json["id"]
        offer.userID = json["userId"]
        offer.userName = json["userName"]
        offer.price = json["price"]
        offer.playerID = playerID

        return offer

class Player:
    playerID: str = None
    teamID: str = None
    firstName: str = None
    lastName: str = None

    status: int = None
    position: int = None
    number: int = None

    totalPoints: int = None
    averagePoints: int = None

    marketValue: int = None
    price: int = None

    offers: List[Offer] = None

    expiryInSeconds: int = None

    @staticmethod
    def getFromJSON(json: dict):
        pla = Player()
        pla.playerID        = json["id"]
        pla.teamID          = json["teamId"]
        pla.firstName       = json["firstName"]
        pla.lastName        = json["lastName"]
        pla.status          = json["status"]
        pla.position        = json["position"]
        pla.number          = json["number"]
        pla.totalPoints     = json["totalPoints"]
        pla.averagePoints   = json["averagePoints"]
        pla.marketValue     = json["marketValue"]
        pla.offers = []
        try:
            for offer in json["offers"]:
                pla.offers.append(Offer.fromJSON(offer, pla.playerID))
            pla.offers = offers
        except Exception:
            pass
        try:
            pla.price           = json["price"]
            pla.expiryInSeconds = json["expiry"]
        except Exception:
            pass
        return pla


class League:
    name: str = None
    leagueID: str = None

    creatorId: str = None
    creatorName: str = None

    userBalance: int = None
    userTeamValue: int = None

    team: List[Player] = None
    teamLineUp: List[Player] = None
    teamLineFormation: str = None

    market: List[Player] = None
    
    ownOffers: List[Offer] = None

class User:
    accessToken: str = None

    name: str = None
    userID: str = None

    leagues: List[League] = None
    currentLeague: League = None

class LoginException(Exception):
    pass
