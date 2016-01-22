#!/usr/bin/env python3

import traceback
from abc import ABCMeta, abstractmethod


class BaseDFA(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        pass

    def run(self):
        status = self.start
        while True:
            # DFA End
            if status is None:
                break
            # DFA Stauts
            elif issubclass(status, BaseDFAStatus):
                status = status().do()
            # Raw function
            elif callable(status):
                status = status()


class BaseDFAStatus(metaclass=ABCMeta):
    @abstractmethod
    def do(self):
        pass
