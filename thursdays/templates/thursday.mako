<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

  <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
  <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>

<script type="text/javascript">
  var geocoder;
  var map;
  var markers = [];

  var tempPast = [
    % for v in c.venues:
      ${venuetojs(v)}
    % endfor
  ];

  function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(37.78, -122.445);
    var myOptions = {
      zoom: 12,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      navigationControl: true,
      scaleControl: true,
    };
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    for (var i = 0; i < tempPast.length; i++) {
      codeAddress(tempPast[i]);
    }
  }

  function codeAddress(venue) {
    if (venue.location) {
      markers.push(getMarker(venue));
    } else if (venue.latitude && venue.longitude) {
      venue.location = new google.maps.LatLng(venue.latitude, venue.longitude);
      markers.push(getMarker(venue));
    } else if (geocoder) {
      geocoder.geocode( { 'address': venue.address + ', San Francisco, CA'},
        function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
            venue.location = results[0].geometry.location;

            // save the lat/long for later
            $.post('/thursday/set_location',
              { id: venue.id,
                latitude: venue.location.lat(),
                longitude: venue.location.lng() });

            markers.push(getMarker(venue));
          } else {
            alert("Geocode was not successful for the following reason: " + status);
          }
        });
    }
  }

  function getMarker(venue) {
    return new google.maps.Marker({
      map: map,
      position: venue.location,
      title: venue.name + ', at ' + venue.address,
    });
  }

</script>
<script>
$(document).ready(function() {
  var maxValue = tempPast.length - 1;
    $('#slider').slider({
        min: 0,
        max: maxValue,
        values: [0, maxValue],
        start: function(e,ui){
        },
        stop: function(e,ui){
          for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(null);
            delete(markers[i]);
          }
          markers = [];

          for (var i = ui.values[0]; i <= ui.values[1]; i++) {
            codeAddress(tempPast[i]);
          }
        },
        slide: function(e,ui){
        }
    });
  });
</script>
<style type="text/css">
  <!--
    #container {
      width: 600px;
      margin-right: 15px;
      float: left;
    }

    #map_canvas {
      width: 600px;
      height: 400px;
    }
    #slider {
      width: 600px;
    }
  //-->
</style>
</head>
<body onload="initialize()">
  <div id="container">
    <div id="map_canvas"></div>
    <div id="slider"></div>
  </div>

  <div id="venuelist">
    % for v in c.venues:
      ${venuetodiv(v)}
    % endfor
  </div>

  <form name="test" method="GET" action="/thursday/process_form">
  name of place: <input type="text" name="name" /><br />
  location: <input type="text" name="address" /><br />
  date (m/d/y): <input type="text" name="date" /><br />
  <input type="submit" name="submit" value="Submit" />
</form>
</body>
</html>

<%def name="venuetojs(venue)" filter="n">
    { id: ${venue.id},
      name: '${venue.name.replace("'", "\\\'")}',
      address: '${venue.address}',
      date: new Date('${venue.date.strftime('%B %d, %Y')}'),
      latitude: '${venue.latitude}',
      longitude: '${venue.longitude}',
     },
</%def>

<%def name="venuetodiv(venue)">
  <div class="venue">
    <b>${venue.name}</b><br />
    ${venue.pretty_date()}<br />
    ${venue.address}<br />
  </div>
</%def>
    
