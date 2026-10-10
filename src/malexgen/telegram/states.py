from aiogram.fsm.state import State, StatesGroup


class GenStates(StatesGroup):

    main_menu = State()
    waiting_legend = State()
    waiting_payload = State()
    waiting_name = State()
    confirming = State()


class C2States(StatesGroup):

    waiting_chat_id = State()
    waiting_session_choice = State()


class DemoStates(StatesGroup):

    waiting_demo_action = State()


__all__ = ["GenStates", "C2States", "DemoStates"]
