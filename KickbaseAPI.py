from  requests_html import HTMLSession
from threading import Thread
from Types import *
import os


class KickBaseBot:
    def __init__(self):
        self.urls = {
            "market": "https://api.kickbase.com/leagues/{leagueID}/market",
            "buy": "https://api.kickbase.com/leagues/{leagueID}/market/{playerID}/offers",
            "lineUp": "https://api.kickbase.com/leagues/{leagueID}/lineupex",
            "leagues": "https://api.kickbase.com/leagues?ext=true"
        }
        self.session = HTMLSession()
        self.user = User()
        self.loggedIn = False
    
    def _get(self, url, asJson=True):
        if self.loggedIn:
            response = self.session.get(
                url,
                headers={
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Authorization": f"Bearer {self.user.accessToken}"
                }
            )
            if response.status_code == 200:
                if asJson:
                    return response.json()
                else:
                    return response
            else:
                None
        else:
            raise LoginException("User not logged in.")

    def _getUserLeagues(self):
        response = self._get(
            self.urls["leagues"]
        )
        if isinstance(response, dict):
            leagues = []
            for league in response["leagues"]:
                lea = League()
                lea.name = league["name"]
                lea.leagueId = league["id"]
                lea.creatorName = league["creator"]
                lea.creatorId = league["creatorId"]
                lea.userBalance = league["lm"]["budget"]
                lea.userTeamValue = league["lm"]["teamValue"]
                leagues.append(lea)
            return leagues

    def _getLeagueMarket(self, leagueID):
        response = self._get(self.urls["market"].format(leagueID=leagueID))
        if isinstance(response, dict):
            players = []
            for player in response["players"]:
                pla = Player()

                pla.playerID        = player["id"]
                pla.teamID          = player["teamId"]
                pla.firstName       = player["firstName"]
                pla.lastName        = player["lastName"]
                pla.status          = player["status"]
                pla.position        = player["position"]
                pla.number          = player["number"]
                pla.totalPoints     = player["totalPoints"]
                pla.averagePoints   = player["averagePoints"]
                pla.marketValue     = player["marketValue"]
                pla.price           = player["price"]
                pla.expiryInSeconds = player["expiry"]

                players.append(pla)
            
            for league in self.user.leagues:
                if str(league.leagueId) == str(leagueID):
                    return players
            else:
                raise f"There is no league with id '{leagueID}'."

    def login(self, email, password):
        self.loggedIn = False
        loginResult = self.session.post(
            "https://kickbase.com/api/v1/user/login",
            json={
                "email": email,
                "password": password
            }
        )
        if loginResult.status_code in [200, 302]:
            self.user.accessToken = loginResult.json()["user"]["accessToken"]
            self.user.name = loginResult.json()["user"]["name"]
            self.user.userId = loginResult.json()["user"]["id"]
            self.loggedIn = True

            self.user.leagues = self._getUserLeagues()
            for league in self.user.leagues:
                league: League = league
                league.currentMarket = self._getLeagueMarket(league.leagueId)
            
        elif loginResult.status_code in [403, 500]:
            # wrong login data
            LoginException("An internal Server Error occurred when trying to login (mostly happens, if login data are wrong).")
        else:
            raise LoginException("Unknown Error when trying to login.")



if __name__ == "__main__":
    bot = KickBaseBot()
    bot.login(
        os.getenv("KICKBASE_EMAIL"),
        os.getenv("KICKBASE_PASSWORD")
    )
    if bot.loggedIn:
        input()