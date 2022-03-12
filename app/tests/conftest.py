import flask_unittest

from app import init_app
from dotenv import load_dotenv
import os
from os.path import join, dirname

current_dir = os.path.dirname(os.path.realpath(__file__))
dotenv_path = join(dirname(dirname(current_dir)), '.env.test')
load_dotenv(dotenv_path)

config = 'config.Config'


class TestBase(flask_unittest.AppClientTestCase):
    def create_app(self):
        app = init_app(config)
        ctx = app.app_context()
        ctx.push()
        yield app
        ctx.pop()
