from dotenv import load_dotenv
from api.helpers.logger_builder import LoggerBuilder
from api.config import settings

load_dotenv()
LoggerBuilder.build(settings.project_name)
