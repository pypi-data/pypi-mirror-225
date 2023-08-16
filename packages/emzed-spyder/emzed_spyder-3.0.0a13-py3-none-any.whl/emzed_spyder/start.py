#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>


def main():
    from . import patch_all  # noqa F401 isort: skip
    from setproctitle import setproctitle

    from spyder.app.start import main

    setproctitle("emzed.spyder")

    main()


if __name__ == "__main__":
    main()
