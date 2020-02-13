# UnKickPy
## This is an unofficial KICKBASE python API which is under construction.

### steps to use it:
```python
from KickbaseAPI import KickbaseAPI
api = KickbaseAPI()
api.login(
    "myEmailAddress@provider.com",
    "myPassword"
)
if api.loggedIn:
    # you are now logged in and have full access to all information.
    # currently you will only have access to the leagues of the user and their markets
    # (the players you can buy)
    # which you can access as follows:
    
    # access user information:
    self.user
```

But what I will add later on, maybe in another repository is a bot which automatically
buys and sells players based on how good they are and if it's likely that they will play at the next match day.
But since I need an API to to the KICKBASE API I am currently working on this.

### Use this at your own risk!



Some of the attributes of the following classes aren't used right now, but will be in future releases.

#### User class:
```python
class User:
    accessToken: str = None

    name: str = None
    userId: str = None

    leagues: list = None # list of 'League' objects
    currentLeague: League = None
```

#### League class:
```python

class League:
    name: str = None
    leagueId: str = None

    creatorId: str = None
    creatorName: str = None

    userBalance: int = None
    userTeamValue: int = None

    team: list = None
    teamLineUp: dict = None

    currentMarket: list = None # list of 'Player' objects
```

#### League class:
```python
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
```
