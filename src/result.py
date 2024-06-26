#!/usr/bin/env python3

import time

from src.settings import Settings

class Result:
    def __init__(self, teamA : str, teamB : str, winner : str, time : float):
        self.teamA = teamA
        self.teamB = teamB
        self.winner = winner
        self.time = time
    
    def display(self):
        return f"Match {self.teamA} VS {self.teamB} winner {self.winner} in {time.strftime("%Mmin %Ss", time.gmtime(self.time))}\n"

class Duel:
    def __init__(self, teamA : str, teamB : str, settings : Settings):
        self.nb_match = (settings.needed_wins - 1) * 2 + 1
        self.scores = [[teamA, 0, 0], [teamB, 0, 0]]
        self.winner = None
        self.match_count = 0
    
    def add(self, result : Result):
        if result.winner == self.scores[0][0]:
            self.scores[0][1] += 1
            self.scores[0][2] += result.time
        elif result.winner == self.scores[1][0]:
            self.scores[1][1] += 1
            self.scores[1][2] += result.time
        else:
            self.scores[0][1] += 0.5
            self.scores[0][2] += result.time
            self.scores[1][1] += 0.5
            self.scores[1][2] += result.time
        self.match_count += 1
        if self.match_count >= self.nb_match:
            self.scores[0][2] /= self.nb_match
            self.scores[1][2] /= self.nb_match
            if self.scores[0][1] > self.scores[1][1]:
                self.winner = self.scores[0][0]
            elif self.scores[0][1] < self.scores[1][1]:
                self.winner = self.scores[1][0]
            else:
                self.winner = "Equality"

    def getTime(self, team : str):
        if team == self.scores[0][0]:
            return self.scores[0][2]
        return self.scores[1][2]
    
    def display(self):
        return f"Duel {self.scores[0][0]} VS {self.scores[1][0]} winner {self.winner}\n"

class ScoreBoard:
    def __init__(self, settings : Settings):
        self.scores = []
        for team in settings.teams:
            self.scores.append([team, 0, 0])
    
    def add(self, duel : Duel):
        for team in self.scores:
            if duel.winner == team[0]:
                team[1] += 1
                team[2] += duel.getTime(team[0])
            elif duel.winner == "Equality" and (team[0] == duel.scores[0][0] or team[0] == duel.scores[1][0]):
                team[1] += 0.5
                team[2] += duel.getTime(team[0])

    def display(self):
        is_sorted = False
        while not is_sorted:
            is_sorted = True
            last_pos = None
            i = 0
            for team in self.scores:
                if last_pos == None:
                    last_pos = i
                    i += 1
                    continue
                if team[1] > self.scores[last_pos][1]:
                    self.scores[last_pos], self.scores[i] = self.scores[i], self.scores[last_pos]
                    is_sorted = False
                i += 1
        output = ["=====================================","Results:"]
        i = 1
        for team in self.scores:
            output.append(f"{i}) {team[0]} score={team[1]} average_time={time.strftime("%Mmin %Ss", time.gmtime(team[2] / (len(self.scores) - 1)))}")
            i += 1
        return "\n".join(output)
