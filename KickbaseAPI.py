from  requests_html import HTMLSession
from threading import Thread
from Types import Player, User, League, LoginException, Offer
import os


class KickBaseBot:
    def __init__(self):
        self.urls = {
            "market": "https://api.kickbase.com/leagues/{leagueID}/market",
            "marketCancelSell": "https://api.kickbase.com/leagues/{leagueID}/market/{playerID}",
            "marketOffer": "https://api.kickbase.com/leagues/{leagueID}/market/{playerID}/offers",
            "marketCancelOffer": "https://api.kickbase.com/leagues/{leagueID}/market/{playerID}/offers/{offerID}",
            "buy": "https://api.kickbase.com/leagues/{leagueID}/market/{playerID}/offers",
            "lineUp": "https://api.kickbase.com/leagues/{leagueID}/lineupex",
            "leagues": "https://api.kickbase.com/leagues?ext=true"
        }
        self.session = HTMLSession()
        self.user = User()
    
    def _delete(self, url, asJson=True, **kwargs):
        response = self.session.delete(
            url,
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
                "Authorization": f"Bearer {self.user.accessToken}"
            },
            **kwargs
        )
        if response.status_code == 200:
            if asJson:
                return response.json()
            else:
                return response
        else:
            return None

    def _post(self, url, json={}, headers={}, asJson=True):
        response = self.session.post(
            url,
            json=json,
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
            return None

    def _get(self, url, asJson=True):
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
            return None

    def getUserLeagues(self):
        response = self._get(
            self.urls["leagues"]
        )
        if isinstance(response, dict):
            leagues = []
            for league in response["leagues"]:
                lea = League()
                lea.name = league["name"]
                lea.leagueID = league["id"]
                lea.creatorName = league["creator"]
                lea.creatorId = league["creatorId"]
                lea.userBalance = league["lm"]["budget"]
                lea.userTeamValue = league["lm"]["teamValue"]
                leagues.append(lea)
            return leagues

    def getLeagueMarket(self, league: League):
        success = False
        response = self._get(self.urls["market"].format(leagueID=league.leagueID))
        if isinstance(response, dict):
            players = []
            for player in response["players"]:
                player = Player.getFromJSON(player)
                players.append(player)
            
            league.market = players
            success = True
        return success

    def login(self, email, password):
        success = False
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
            self.user.userID = loginResult.json()["user"]["id"]
            success = True

            self.user.leagues = self.getUserLeagues()
            if len(self.user.leagues) >= 1:
                self.user.currentLeague = self.user.leagues[0]
            else:
                print("User not in any league currently")
    
            for league in self.user.leagues:
                self.getLeagueMarket(league)
                self.getUsersTeam(league)
                ownLeagueOffers = []
                for player in league.market:
                    for offer in player.offers:
                        if offer.userID == self.user.userID:
                            ownLeagueOffers.append(offer)
                league.ownOffers = ownLeagueOffers
            
        elif loginResult.status_code in [403, 500]:
            # wrong login data
            pass
        else:
            raise LoginException("Unknown Error when trying to login.")
        return success

    def getUsersTeam(self, league: League):
        success = False
        response = self._get(self.urls["lineUp"].format(leagueID=league.leagueID))
        if isinstance(response, dict):
            leaguePlayers = []
            for player in response["players"]:
                player = Player.getFromJSON(player)
                leaguePlayers.append(player)
            lineUp = []
            for playerID in response["lineup"]:
                try:
                    player = list(filter(lambda player: player.playerID == playerID, leaguePlayers))[0]
                    lineUp.append(player)
                except IndexError:
                    print(f"Didnt find a player with playerID '{playerID}'")

            league.team = leaguePlayers
            league.teamLineFormation = response["type"]
            league.teamLineUp = lineUp
            success = True

    def makeOffer(self, league: League, player: Player, price: int) -> str:
        response = self._post(
            self.urls["marketOffer"].format(
                leagueID=league.leagueID,
                playerID=player.playerID
            ),
            json={
                "price": price
            }
        )
        if isinstance(response, dict):
            return response["offerId"]
        return None

    def deleteOffer(self, league: League, player: Player, offerID: str):
        success = False
        response = self._delete(
            self.urls["marketCancelOffer"].format(
                leagueID=league.leagueID,
                playerID=player.playerID,
                offerID=offerID
            )
        )
        if isinstance(response, dict):
            if response["err"] == 0:
                success = True
        return success

    def sellPlayer(self, league: League, player: Player, price: int):
        success = False
        response = self._post(
            self.urls["market"].format(league.leagueID),
            json={
                "playerId": player.playerID,
                "price": price
            }
        )
        if isinstance(response, dict):
            if response["err"] == 0:
                success = True
        return success

    def cancelSellPlayer(self, league: League, player: Player):
        success = False
        response = self._delete(
            self.urls["marketCancelSell"].format(
                leagueID=league.leagueID,
                playerID=player.playerID
            )
        )
        if isinstance(response, dict):
            if response["err"] == 0:
                success = True
        return success


if __name__ == "__main__":
    bot = KickBaseBot()
    if bot.login(os.getenv("KICKBASE_EMAIL"), os.getenv("KICKBASE_PASSWORD")):
        # logged in 
        ownOffersPlayerIDs = list(map(lambda offer: offer.playerID, bot.user.currentLeague.ownOffers))
        for player in bot.user.currentLeague.market:
            if player.totalPoints >= 1000 and player.playerID not in ownOffersPlayerIDs:
                offerPrice = player.marketValue // 1.1
                success = bot.makeOffer(
                    bot.user.currentLeague,
                    player,
                    offerPrice
                )
                print(f"Making an offer for  player {player.firstName} {player.lastName} for a price of {offerPrice}€ was {'not ' if not success else ''}successfull.")
        