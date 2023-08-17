import os


def get_board_path(board_name=None):
    if board_name:
        return os.path.join(os.path.dirname(__file__), board_name)
    else:
        return os.path.dirname(__file__)


def get_proto_board_data():
    return os.path.dirname(__file__)


__all__ = ["get_board_path", "get_proto_board_data"]
