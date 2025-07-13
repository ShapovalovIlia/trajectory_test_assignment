from cyclopts import App

from trajectory_test_assignment.presentation.cli.handlers import f


def main() -> None:
    app = create_cli_app()
    app()


def create_cli_app() -> App:
    app = App(
        name="pizda_parnya",
        help_format="rich",
    )

    app.command(f)
    return app


if __name__ == "__main__":
    main()
