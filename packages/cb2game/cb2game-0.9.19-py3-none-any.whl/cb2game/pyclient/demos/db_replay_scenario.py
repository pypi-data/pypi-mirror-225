import logging
from datetime import datetime, timedelta
from time import sleep
from typing import List

import fire
from tqdm import tqdm

from cb2game.pyclient.game_endpoint import Action
from cb2game.pyclient.remote_client import RemoteClient
from cb2game.agents.agent import Agent, RateLimitException, Role
from cb2game.agents.config import (
    AgentConfigData,
    LoadAgentFromConfig,
    ReadAgentConfigOrDie,
    SerializeAgentConfig,
)
from cb2game.eval.eval_schema import Eval, InstructionEvaluation, RunSource
from cb2game.pyclient.endpoint_pair import EndpointPair
from cb2game.pyclient.local_game_coordinator import LocalGameCoordinator
from cb2game.server.card import Card
from cb2game.server.config.config import Config, ReadServerConfigOrDie
from cb2game.server.db_tools.db_utils import ListGames
from cb2game.server.lobbies.open_lobby import OpenLobby
from cb2game.server.lobby_consts import LobbyInfo, LobbyType
from cb2game.server.messages.objective import ObjectiveMessage
from cb2game.server.messages.prop import PropType
from cb2game.server.messages.turn_state import TurnState
from cb2game.server.scenario_util import (
    GameStateFromScenario,
    ReconstructScenarioFromEvent,
)
from cb2game.server.schemas import base
from cb2game.server.schemas.event import Event, EventType
from cb2game.server.state_utils import (
    FOLLOWER_MOVES_PER_TURN,
    FOLLOWER_SECONDS_PER_TURN,
)
from cb2game.server.util import GetCommitHash, PackageVersion

logger = logging.getLogger(__name__)

def get_active_instruction(instructions):
    for instruction in instructions:
        if not instruction.completed and not instruction.cancelled:
            return instruction
    return None

REFRESH_RATE_HZ = 10

class DbReplayer(object):
    def __init__(self, game_endpoint, pause_per_turn):
        self.game = game_endpoint
        self.exc = None
        self.pause_per_turn = pause_per_turn

        # Load games from DB.
        games = ListGames()
        game_ids = [game.id for game in games]
        instructions_done = Event.select().where(
            (Event.type == EventType.INSTRUCTION_DONE) & (Event.game_id << game_ids)
        )
        

    def run(self):
        try:
            (
                map,
                cards,
                turn_state,
                instructions,
                actors,
                live_feedback,
            ) = self.game.initial_state()
            logger.info(f"Initial instructions: {instructions}")
            if self.scenario_data:
                logger.info(f"Loading scenario...")
                self.game.step(Action.LoadScenario(self.scenario_data))
            while not self.game.over():
                sleep(self.pause_per_turn)
                (
                    map,
                    cards,
                    turn_state,
                    instructions,
                    actors,
                    live_feedback,
                ) = self.game.step(Action.NoopAction())
                logger.info(f"Instructions: {instructions}")
            print(f"Game over. Score: {turn_state.score}")
        except Exception as e:
            self.exc = e

    def join(self):
        if self.exc:
            raise self.exc


def main(host, scenario_id="", render=False, lobby="scenario-lobby", scenario_file=""):
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("peewee").setLevel(logging.INFO)
    logger.info(f"Connecting to {host} (render={render}) (scenario_id={scenario_id})")
    client = RemoteClient(host, render, lobby_name=lobby)
    connected, reason = client.Connect()
    assert connected, f"Unable to connect: {reason}"

    # Iterate until Ctrl-C is pressed.
    while True:
        game, reason = client.AttachToScenario(
            scenario_id=scenario_id,
            timeout=timedelta(minutes=5),
        )

        assert game is not None, f"Unable to join game: {reason}"
        monitor = DbReplayer(
            game, pause_per_turn=(1 / REFRESH_RATE_HZ)
        )
        monitor.run()
        monitor.join()


if __name__ == "__main__":
    fire.Fire(main)
