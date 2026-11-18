from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from magicbot import MagicRobot

from .state_machine import StateMachine

import wpilib


class PeriodicOpMode(wpilib.PeriodicOpMode):
    def __init__(self, robot: MagicRobot):
        super().__init__()
        self.robot = robot


class AutonomousOpMode(StateMachine, PeriodicOpMode):
    """
    This is a specialized version of the StateMachine that is designed
    to be used as an autonomous mode. There are a few key differences:

    - The :func:`.engage` function is always called, so the state machine
      will always run to completion unless done() is called
    - VERBOSE_LOGGING is set to True, so a log message will be printed out upon
      each state transition

    """

    VERBOSE_LOGGING = True

    def __new__(cls, _) -> Self:
        return StateMachine.__new__(cls)

    def __init__(self, robot):
        PeriodicOpMode.__init__(self, robot)

    def start(self):
        self._timer = wpilib.Timer()
        self._timer.restart()
        self.on_enable()

    def periodic(self) -> None:
        self.on_iteration(self._timer.get())

    def end(self):
        self.on_disable()

    def on_enable(self) -> None:
        super().on_enable()
        self.__engaged = True

    def on_iteration(self, tm: float) -> None:
        # TODO, remove the on_iteration function in 2017?

        # Only engage the state machine until its execution finishes, otherwise
        # it will just keep repeating
        #
        # This is because if you keep calling engage(), the state machine will
        # loop. I'm tempted to change that, but I think it would lead to unexpected
        # side effects. Will have to contemplate this...

        if self.__engaged:
            self.engage()
            self.execute()
            self.__engaged = self.is_executing

    def done(self) -> None:
        super().done()
        self._StateMachine__should_engage = False
        self.__engaged = False
