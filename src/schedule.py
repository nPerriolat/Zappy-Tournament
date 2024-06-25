#!/usr/bin/env python3

from src.settings import Settings

def scheduling(settings : Settings):
    schedule = []
    teams_cpy = settings.teams[:]
    for team in settings.teams:
        teams_cpy.pop(0)
        if teams_cpy == []:
            break
        schedule.append([team, teams_cpy[:]])
    return schedule