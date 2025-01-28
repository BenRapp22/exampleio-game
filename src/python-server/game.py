import constants

from player import Player
from collisions import applyCollisions

import datetime
import random
import threading
import time

class Game:
    def __init__(self):
        self.sockets = {}
        self.players = {}
        self.bullets = {}
        self.lastUpdateTime = int(datetime.datetime.now().timestamp() * 1000)
        self.shouldSendUpdate = False
        self.running=True
        self.start_interval(1/60)

    
    def addPlayer(self, socket, username):
        self.sockets[socket.id] = socket

        x = constants.MAP_SIZE * (0.25 + random.random() * 0.5)
        y = constants.MAP_SIZE * (0.25 + random.random() * 0.5)
        self.players[socket.id] = Player(socket.id, username, x, y)

    def removePlayer(self, socket):
        del self.sockets[socket.id]
        del self.players[socket.id]
    
    def handleInput(self, socket, dir):
        if self.players[socket.id]:
            self.players[socket.id].setDirection(dir)
    
    def update(self):
        # Calculate elapsed time
        now = int(datetime.datetime.now().timestamp() * 1000)
        dt = (now - self.lastUpdateTime) / 1000
        self.lastUpdateTime = now

        # Update each bullet
        bulletsToRemove = []
        for bullet in self.bullets:
            if bullet.update(dt):
                bulletsToRemove.insert(0, bullet)
        self.bullets = [b for b in self.bullets if b not in bulletsToRemove]

        # Update each player
        for playerID in self.sockets.keys():
            player = self.players[playerID]
            newBullet = player.update(dt)
            if newBullet:
                self.bullets.append(newBullet)

        # Apply collisions, update scores 
        destroyedBullets = applyCollisions(self.players.values(), self.bullets)
        for b in destroyedBullets:
            if self.players[b.parentID]:
                self.players[b.parentID].onDealtDamage()
        self.bullets = [b for b in self.bullets if b not in destroyedBullets]

        # Check if anybody is dead
        for playerID in self.sockets.keys():
            socket = self.sockets[playerID]
            player = self.players[playerID]
            if player.hp <= 0:
                socket.emit(constants.MSG_TYPES["GAME_OVER"])
                self.removePlayer(socket)
        
        # Send a game update to each player every other time 
        if self.shouldSendUpdate:
            leaderboard = self.getLeaderboard()
            for playerID in self.sockets.keys():
                socket = self.sockets[playerID]
                player = self.players[playerID]
                socket.emit(constants.MSG_TYPES["GAME_UPDATE"], self.createUpdate(player, leaderboard))
            self.shouldSendUpdate = False
        else:
            self.shouldSendUpdate = True


    def getLeaderboard(self):
        return sorted(
            [{"username": player["username"], "score": round(player["score"])} for player in self.players.values()],
            key=lambda p: p["score"],
            reverse=True
        )[:5]
    
    def createUpdate(self, player, leaderboard):
        nearbyPlayers = [
            p for p in self.players if (p!=player) and (p.distanceTo(player) <= constants.MAP_SIZE/2)
        ]
        nearbyBullets = [
            b for b in self.bullets if b.distanceTo(player) <= constants.MAP_SIZE
        ]

        return {
            "t": int(datetime.datetime.now().timestamp() * 1000),
            "me": player.serializeForUpdate(),
            "others": [x.serializeForUpdate() for x in nearbyPlayers],
            "bullets": [x.serializeForUpdate() for x in nearbyBullets],
            "leaderboard":leaderboard
        }
    
    def start_interval(self, interval):
        def loop():
            while self.running:
                self.update()
                time.sleep(interval)
            
        threading.Thread(target=loop, daemon=True).start()