import sys
import window


def main() -> None:
    """ Entry point of the program. """
    main_window = window.Window()
    main_window.root.mainloop()


if __name__ == "__main__":
    sys.exit(main())
