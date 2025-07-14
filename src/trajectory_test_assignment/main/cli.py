from cyclopts import App

from trajectory_test_assignment.presentation import (
    get_busy_slots,
    get_free_slots,
    is_time_available,
)


def main() -> None:
    app = create_cli_app()
    app()


def create_cli_app() -> App:
    app = App(
        name="Trajectory Test Assignment CLI",
        help_format="rich",
    )

    app.command(get_busy_slots)
    app.command(get_free_slots)
    app.command(is_time_available)

    return app


if __name__ == "__main__":
    main()
