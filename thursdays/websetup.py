"""Setup the thursdays application"""
import logging

from thursdays.config.environment import load_environment
from thursdays.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup thursdays here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    # meta.metadata.drop_all(bind=meta.engine, checkfirst=True)
    meta.metadata.create_all(bind=meta.engine)
