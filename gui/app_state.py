"""Small in-memory state holder for the active desktop application."""

active_user = None


def set_active_user(user):
    global active_user
    active_user = user


def get_active_user():
    return active_user


def clear_active_user():
    global active_user
    active_user = None
