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
  <div id="venueform">
    <form name="test" method="GET" action="thursday/process_form">
      enter new venue:
      <input type="text" name="name" placeholder="name of venue" />
      <input type="text" name="address" placeholder="location" />
      <input type="text" name="date" placeholder="date (m/d/y)" />
      <input type="submit" name="submit" value="Submit" />
    </form>
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
    <span class="venue-delete">x</span>
    <b>${venue.name}</b><br />
    ${venue.pretty_date()}<br />
    ${venue.address}<br />
  </div>
</%def>
    
