from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    age = State()


class PollChoose(StatesGroup):
    choose = State()


class MarkChoose(StatesGroup):
    mark = State()


class LLM(StatesGroup):
    helping = State()
