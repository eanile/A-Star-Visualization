""" Entry point of the program.
"""

import sys
import window


def main() -> None:
    win_root = window.Window()
    win_root.activate()


if __name__ == "__main__":
    sys.exit(main())
