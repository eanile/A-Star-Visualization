import sys
import window


def main() -> int:
    """ Entry point of the program. """
    main_window = window.Window()
    main_window.root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
