from paste.deploy import appconfig
from pylons import config

from thursdays.config.environment import load_environment

conf = appconfig('config:development.ini', relative_to='.')
load_environment(conf.global_conf, conf.local_conf)

from thursdays.model import *
