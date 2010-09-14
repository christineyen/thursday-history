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

        # Super janky way of removing / hiding UI to mess with the DB - in lieu
        # of a totally unnecessary user auth system.
        if request.params.has_key('verify'):
            c.verified = True

        return render('/thursday.mako')

    def process_form(self):
        ''' Create a new Venue. Poorly named method, I know. '''
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
        ''' A location was found for a particular Venue and the application's
            requesting to set it.'''
        if request:
            venue = meta.Session.query(Venue).filter(Venue.id == request.params['id']).one()
            if venue and request.params['latitude'] and request.params['longitude']:
                venue.latitude = request.params['latitude']
                venue.longitude = request.params['longitude']
                meta.Session.commit()

    def delete_venue(self):
        ''' Delete a venue from the list.'''
        if request and request.params['id']:
            venue = meta.Session.query(Venue).filter(Venue.id == request.params['id']).one()
            meta.Session.delete(venue)
            meta.Session.commit()

    def handle_email(self):
        ''' Handler for incoming emails (in theory), via smtp2web'''
        print str(dir(request))
        print str(request.body)

