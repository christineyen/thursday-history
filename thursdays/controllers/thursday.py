import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from thursdays.lib.base import BaseController, render
from thursdays.model import Venue, meta

from datetime import date

log = logging.getLogger(__name__)

class ThursdayController(BaseController):

    def index(self):
        # Return a rendered template
        print " HALLO"
        c.venues = meta.Session.query(Venue).all()
        return render('/thursday.mako')
        # or, return a response
        # return 'Hello World'

    def process_form(self):
        if (request):
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
