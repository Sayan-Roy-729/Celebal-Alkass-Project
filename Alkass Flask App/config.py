import os

from dotenv import load_dotenv

load_dotenv()

DEBUG                  = True
SECRET_KEY             = 'secret-key-for-the-app'
OPENAI_API_KEY         = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE        = os.getenv("OPENAI_API_BASE")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_API_TYPE        = os.getenv("OPENAI_API_TYPE")
OPENAI_API_VERSION     = os.getenv("OPENAI_API_VERSION")
