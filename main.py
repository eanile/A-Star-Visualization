import sys
import window


def main() -> None:
    """ Entry point of the program. """
    win_root = window.Window()
    win_root.activate()


if __name__ == "__main__":
    sys.exit(main())
