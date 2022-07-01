#  Copyright (c)  2022. Andrea Antonio Perrelli.
#   All rights reserved.

from riotwatcher import LolWatcher
import os

watcher = LolWatcher(str(os.environ['RIOT_API_KEY']))



def get_rank_by_summoner(summoner):
    # Return the rank status for given summoner object
    my_ranked_stats = watcher.league.by_summoner(str(os.environ['RIOT_REGION']), summoner['id'])
    return my_ranked_stats


def get_summoner_by_summoner_name():
    return watcher.summoner.by_name(str(os.environ['RIOT_REGION']), str(os.environ['RIOT_SUMMONER_NAME']))

def output_summoner_stats(ranked_stats):
    ranked_stat = ranked_stats[0]
    summonerName = ranked_stat['summonerName']
    queueType = ranked_stat['queueType']
    tier = ranked_stat['tier']
    rank = ranked_stat['rank']
    leaguePoints = ranked_stat['leaguePoints']
    wins = ranked_stat['wins']
    losses = ranked_stat['losses']
    total = wins+losses
    win_percentage = (wins / total) * 100

    return 'Nome Evocatore: ' + summonerName + ' ; ' + 'Rank : ' + tier + ' ' + rank + ' ' + str(leaguePoints) + 'LP, ' + str(round(win_percentage, 2)) + '%WR ' + '(' + str(wins) + 'W ' + str(losses) + 'L)'

