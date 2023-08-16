import gpt4docs.logger_config  # noqa: F401
from dotenv import load_dotenv
from gpt4docs import MainApplication


def run_app():
    load_dotenv()
    args = MainApplication.parse_args()
    app = MainApplication(args)
    app()


if __name__ == "__main__":
    run_app()
