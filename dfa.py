#!/usr/bin/env python3

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

            print("DFA", "=>", status.__name__)
            if callable(status):
                # DFA Stauts
                if issubclass(status, BaseDFAStatus):
                    status = status().do()
                # Raw function
                else:
                    status = status()
            # Unknown
            else:
                raise UnknownDFAStatusException()
                break


class BaseDFAStatus(metaclass=ABCMeta):
    @abstractmethod
    def do(self):
        pass


class UnknownDFAStatusException(Exception):
    pass
