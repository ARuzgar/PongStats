import json
from channels.generic.websocket import AsyncWebsocketConsumer
#from .pong import Player, Ball

class GameMessage:
    def __init__(self, message_type, data=None):
        self.message_type = message_type
        self.data = data

class PlayerMoveMessage(GameMessage):
    def __init__(self, player_id, direction):
        super().__init__("player_move", {"player_id": player_id, "direction": direction})

class GameStateMessage(GameMessage):
    def __init__(self, players, ball):
        super().__init__("game_state", {"players": players, "ball": ball})