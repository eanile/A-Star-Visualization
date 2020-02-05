import sys
import window


def main() -> int:
    """ Entry point of the program. """
    win_root = window.Window()
    win_root.activate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
