
class League:
    name: str = None
    leagueId: str = None

    creatorId: str = None
    creatorName: str = None

    userBalance: int = None
    userTeamValue: int = None

    team: list = None
    teamLineUp: dict = None

    currentMarket: list = None

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

    expiryInSeconds: int = None

class User:
    accessToken: str = None

    name: str = None
    userId: str = None

    leagues: list = None
    currentLeague: League = None

class LoginException(Exception):
    pass
