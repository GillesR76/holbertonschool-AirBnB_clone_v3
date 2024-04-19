#!/usr/bin/python3
"""init constructor"""


from flask import Blueprint



app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
# fmt: off
from api.v1.views.index import *
from api.v1.views.states import *
# fmt: on