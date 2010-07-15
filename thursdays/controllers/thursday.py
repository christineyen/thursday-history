import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from sqlalchemy.sql.expression import desc

from thursdays.lib.base import BaseController, render
from thursdays.model import Venue, meta

from datetime import date

log = logging.getLogger(__name__)

class ThursdayController(BaseController):

    def index(self):
        c.venues = meta.Session.query(Venue).order_by(desc(Venue.date)).all()
        if request.params.has_key('limit'):
            c.limit = request.params['limit']
        else:
            c.limit = len(c.venues)

        return render('/thursday.mako')

    def process_form(self):
        if request:
            new_venue = Venue()
            new_venue.name = request.params['name']
            new_venue.address = request.params['address']

            date_arr = [int(x.strip()) for x in request.params['date'].split('/')]
            year = date_arr.pop()
            date_arr.insert(0, year)

            new_venue.date = date(*date_arr)
            meta.Session.add(new_venue)
            meta.Session.commit()
            redirect_to(action = 'index')

    def set_location(self):
        if request:
            venue = meta.Session.query(Venue).filter(Venue.id == request.params['id']).one()
            if venue and request.params['latitude'] and request.params['longitude']:
                venue.latitude = request.params['latitude']
                venue.longitude = request.params['longitude']
                meta.Session.commit()

    def delete_venue(self):
        if request and request.params['id']:
            venue = meta.Session.query(Venue).filter(Venue.id == request.params['id']).one()
            meta.Session.delete(venue)
            meta.Session.commit()

