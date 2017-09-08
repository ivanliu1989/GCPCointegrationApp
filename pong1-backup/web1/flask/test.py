from flask import Flask, request, url_for, Response
import re
import web.template as template
import src.lib.connecttodb as connecttodb
import src.lib.getpair as getpair
import src.lib.savechart as savechart
import pygal
from pygal.style import DarkStyle
from datetime import datetime
import pandas
import numpy as np
from datetime import date
from datetime import timedelta
id = '2993'
body = template.getcointtemplate()
values = connecttodb.selectforecastbyid(id)
print(values)
import flaskapp
flaskapp.getfxdata(values)