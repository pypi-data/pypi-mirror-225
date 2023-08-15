import gpt4docs.logger_config  # noqa: F401
import asyncio
from dotenv import load_dotenv
from gpt4docs import MainApplication

load_dotenv()


if __name__ == "__main__":
    args = MainApplication.parse_args()
    app = MainApplication(args)
    asyncio.run(app.run())
