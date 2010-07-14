<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

  <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
  <link href="/stylesheets/style.css" rel="stylesheet" type="text/css"/>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>

<script src="/javascript/placeholder.js"></script>

<script type="text/javascript">
  var geocoder;
  var map;
  var infoWindow;
  var markers = {};
  var listIndexToVenueId = {};

  var venueData = [
    % for v in reversed(c.venues):
      ${venuetojs(v)}
    % endfor
  ];

  var initialize = function() {
    console.log("initializing");
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

    for (var i = 0; i < venueData.length; i++) {
      listIndexToVenueId[i] = venueData[i].id;
      var hide = (i < venueData.length - ${c.limit});
      codeAddress(venueData[i], hide);
    }

    infoWindow = new google.maps.InfoWindow();
  };

  var codeAddress = function(venue, hide) {
    var marker;
    if (venue.location) {
      marker = getMarker(venue);
    } else if (venue.latitude && venue.longitude) {
      venue.location = new google.maps.LatLng(venue.latitude, venue.longitude);
      marker = getMarker(venue);
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

            marker = getMarker(venue);
          } else {
            alert("Geocode was not successful for the following reason: " + status);
          }
        });
    }
    if (hide) {
      hideVenue(venue.id, marker);
    }
    markers[venue.id] = marker;
  };

  var getMarker = function(venue) {
    return new google.maps.Marker({
      map: map,
      position: venue.location,
      title: venue.name + ', at ' + venue.address,
    });
  };

  var hideVenue = function(venueId, mark) {
    if (!mark) {
      mark = markers[venueId];
    }
    mark.setVisible(false);
    $('#venue-' + venueId).css('display', 'none');
  }
  var showVenue = function(venueId) {
    var mark = markers[venueId];
    mark.setVisible(true);
    $('#venue-' + venueId).css('display', 'block');
  }

</script>
<script>
$(document).ready(function() {

  // set up slider
  var maxValue = venueData.length - 1;
  $('#slider').slider({
      min: 0,
      max: maxValue,
      values: [maxValue - ${c.limit}, maxValue],
      start: function(e,ui){
      },
      stop: function(e,ui){
        var min = Math.min(ui.values[0], ui.values[1]);
        var max = Math.max(ui.values[0], ui.values[1]);
        for (var i = 0; i <= maxValue; i++) {
          var venueId = listIndexToVenueId[i];
          var mark = markers[venueId];
          if (mark.getVisible() && (i < min || i > max)) {
            hideVenue(venueId);
          } else if (!mark.getVisible() && (i > min && i < max)) {
            showVenue(venueId);
          }
        }
      },
      slide: function(e,ui){
      }
  });
  $(".venue-delete").click(function() {
    var venueId = $(this).parent().attr('venue-id');

    $.post('/thursday/delete_venue', { id: venueId });
    hideVenue(venueId);
    return false; // takes precedence over .venue clicks
  });
  $('.venue').click(function() {
    var venueId = $(this).attr('venue-id');
    infoWindow.setContent(markers[venueId].getTitle());
    infoWindow.open(map, markers[venueId]);
  });
  $("input").each(function() {
    $(this).placeholder();
  });
});
</script>
</head>
<body onload="initialize()">
  <div id="venueform">
    <form name="test" method="GET" action="/thursday/process_form">
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
    % for v in c.venues:
      ${venuetodiv(v)}
    % endfor
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
    
