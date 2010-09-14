<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

<link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
<link href="stylesheets/style.css" rel="stylesheet" type="text/css"/>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>

<script src="javascript/placeholder.js"></script>
<script src="javascript/markers.js"></script>

<script type="text/javascript">
  var limit = ${c.limit};
  var venueData = [
    % for v in reversed(c.venues):
      ${venuetojs(v)}
    % endfor
  ];
</script>
</head>
<body>
  <div id="header">
    <p class="big">Started as a weekly bar night for a group of friends,</p>
    <p class="medium">our Thursdays have traversed the city of San Francisco in pursuit of the next interesting place to sit down, hang out, and have a beer.</p>
    <p>Poke around to see where we've been, play with the slider (below the map) to limit locations by time, and (if you were allowed to) add/delete new venues.</p>
  </div>

  <div id="venueform">
    % if c.verified: # Janky / temp way of preventing unauthorized data modification
      <form name="test" method="POST" action="thursday/process_form">
    % endif
      enter new venue:
      <input type="text" name="name" placeholder="name of venue" />
      <input type="text" name="address" placeholder="location" />
      <input type="text" name="date" placeholder="date (m/d/y)" />
    % if c.verified:
        <input type="submit" name="submit" value="Submit" />
      </form>
    % else:
        <input type="submit" name="submit" value="Submit" disabled="true" />
    % endif
  </div>

  <div id="container">
    <div id="map_canvas"></div>
    <div id="slider"></div>
  </div>

  <div id="venuelist">
    <div id="venuelist-venues">
      % for v in c.venues:
        ${venuetodiv(v)}
      % endfor
    </div>
    <div id="venuelist-showall" style="display:none">
      <div id="venuelist-dates"></div>
      reveal all venues
    </div>
  </div>
</body>
</html>

<%def name="venuetojs(venue)" filter="n">
	{ id: ${venue.id},
	  name: '${venue.name.replace("'", "\\\'")}',
	  address: '${venue.address.replace("'", "\\\'")}',
	  date: new Date('${venue.date.strftime('%B %d, %Y')}'),
	  latitude: '${venue.latitude}',
	  longitude: '${venue.longitude}',
	 },
</%def>

<%def name="venuetodiv(venue)">
  <div class="venue" id="venue-${venue.id}" venue-id="${venue.id}">
    % if c.verified:
      <span class="venue-delete">x</span>
    % endif
    <b>${venue.name}</b><br />
    ${venue.pretty_date()}<br />
    ${venue.address}<br />
  </div>
</%def>
    
