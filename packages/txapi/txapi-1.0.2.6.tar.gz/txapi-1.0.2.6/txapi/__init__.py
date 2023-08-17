# -*- coding:utf -*-
from . import api2
from . import api3


class API(object):
    v2 = api2.Api2Client
    v3 = api3.Api3Client
