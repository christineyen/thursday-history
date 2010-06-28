# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1277698827.96538
_template_filename='/var/www/cyyen.mit.edu/thursdays/thursdays/templates/thursday.mako'
_template_uri='/thursday.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['venuetodiv', 'venuetojs']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def venuetodiv(venue):
            return render_venuetodiv(context.locals_(__M_locals),venue)
        c = context.get('c', UNDEFINED)
        def venuetojs(venue):
            return render_venuetojs(context.locals_(__M_locals),venue)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<html>\n<head>\n<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>\n\n  <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>\n\n<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>\n  <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>\n\n<script type="text/javascript">\n  var geocoder;\n  var map;\n  var markers = [];\n\n  var tempPast = [\n')
        # SOURCE LINE 17
        for v in c.venues:
            # SOURCE LINE 18
            __M_writer(u'      ')
            __M_writer(escape(venuetojs(v)))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 20
        __M_writer(u'  ];\n\n  function initialize() {\n    geocoder = new google.maps.Geocoder();\n    var latlng = new google.maps.LatLng(37.78, -122.445);\n    var myOptions = {\n      zoom: 12,\n      center: latlng,\n      mapTypeId: google.maps.MapTypeId.ROADMAP,\n      navigationControl: true,\n      scaleControl: true,\n    };\n    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n\n    for (var i = 0; i < tempPast.length; i++) {\n      codeAddress(tempPast[i]);\n    }\n  }\n\n  function codeAddress(venue) {\n    if (geocoder) {\n      geocoder.geocode( { \'address\': venue.address + \', San Francisco, CA\'}, function(results, status) {\n        if (status == google.maps.GeocoderStatus.OK) {\n          venue.location = results[0].geometry.location;\n          markers.push(getMarker(venue));\n        } else {\n          alert("Geocode was not successful for the following reason: " + status);\n        }\n      });\n    }\n  }\n\n  function getMarker(venue) {\n    return new google.maps.Marker({\n      map: map,\n      position: venue.location,\n      title: venue.name + \', at \' + venue.address,\n    });\n  }\n\n</script>\n<script>\n$(document).ready(function() {\n  var maxValue = tempPast.length - 1;\n    $(\'#slider\').slider({\n        min: 0,\n        max: maxValue,\n        values: [0, maxValue],\n        start: function(e,ui){\n        },\n        stop: function(e,ui){\n          for (var i = 0; i < markers.length; i++) {\n            markers[i].setMap(null);\n            delete(markers[i]);\n          }\n          markers = [];\n\n          for (var i = ui.values[0]; i <= ui.values[1]; i++) {\n            window.console.log(tempPast[i]);\n            if (tempPast[i].location) {\n              markers.push(getMarker(tempPast[i]));\n            } else {\n              codeAddress(tempPast[i]);\n            }\n          }\n        },\n        slide: function(e,ui){\n        }\n    });\n  });\n</script>\n<style type="text/css">\n  <!--\n    #container {\n      width: 600px;\n      margin-right: 15px;\n      float: left;\n    }\n\n    #map_canvas {\n      width: 600px;\n      height: 400px;\n    }\n    #slider {\n      width: 600px;\n    }\n  //-->\n</style>\n</head>\n<body onload="initialize()">\n  <div id="container">\n    <div id="map_canvas"></div>\n    <div id="slider"></div>\n  </div>\n\n  <div id="venuelist">\n')
        # SOURCE LINE 116
        for v in c.venues:
            # SOURCE LINE 117
            __M_writer(u'      ')
            __M_writer(escape(venuetodiv(v)))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 119
        __M_writer(u'  </div>\n\n  <form name="test" method="GET" action="/thursday/process_form">\n  name of place: <input type="text" name="name" /><br />\n  location: <input type="text" name="address" /><br />\n  date (m/d/y): <input type="text" name="date" /><br />\n  <input type="submit" name="submit" value="Submit" />\n</form>\n</body>\n</html>\n\n')
        # SOURCE LINE 134
        __M_writer(u'\n\n')
        # SOURCE LINE 142
        __M_writer(u'\n    \n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_venuetodiv(context,venue):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 136
        __M_writer(u'\n  <div class="venue">\n    <b>')
        # SOURCE LINE 138
        __M_writer(escape(venue.name))
        __M_writer(u'</b><br />\n    ')
        # SOURCE LINE 139
        __M_writer(escape(venue.pretty_date()))
        __M_writer(u'<br />\n    ')
        # SOURCE LINE 140
        __M_writer(escape(venue.address))
        __M_writer(u'<br />\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_venuetojs(context,venue):
    context.caller_stack._push_frame()
    try:
        context._push_buffer()
        __M_writer = context.writer()
        # SOURCE LINE 130
        __M_writer(u"\n    { name: '")
        # SOURCE LINE 131
        __M_writer(escape(venue.name.replace("'", "\\\'")))
        __M_writer(u"',\n      address: '")
        # SOURCE LINE 132
        __M_writer(escape(venue.address))
        __M_writer(u"',\n      date: new Date('")
        # SOURCE LINE 133
        __M_writer(escape(venue.date.strftime('%B %d, %Y')))
        __M_writer(u"') },\n")
    finally:
        __M_buf, __M_writer = context._pop_buffer_and_writer()
        context.caller_stack._pop_frame()
    __M_writer(__M_buf.getvalue())
    return ''


