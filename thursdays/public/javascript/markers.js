var geocoder;
var map;
var infoWindow;
var markers = {};
var listIndexToVenueId = {};

/*
 * Set up the Google Map, center it on the northern 2/3 of
 * San Francisco, set the zoom levels, etc.
 */
var initMap = function() {
  var latlng = new google.maps.LatLng(37.78, -122.445);
  var myOptions = {
    zoom: 12,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    navigationControl: true,
    scaleControl: true,
  };
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
};

/*
 * Set up the slider to default values depending on what the
 * requested limit on the items are, set up handlers to show/
 * hide venues as necessary
 */
var initSlider = function() {
  var maxValue = venueData.length - 1;
  var minValue = venueData.length - limit;
  $('#slider').slider({
      min: 0,
      max: maxValue,
      values: [minValue, maxValue],
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
          } else if (!mark.getVisible() && (i >= min && i <= max)) {
            showVenue(venueId);
          }
        }
        printDisplayedDates(min, max);
      },
      slide: function(e,ui){
      }
  });
  if (minValue != 0) {
    printDisplayedDates(minValue, maxValue);
  }
};

/*
 * Utility function to actually make the marker appear on the
 * map - may involve asking the geocoder for the Lat/Long and
 * saving it to the database.
 */
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
          $.post('/thursdays/thursday/set_location',
            { id: venue.id,
              latitude: venue.location.lat(),
              longitude: venue.location.lng() });

          markers[venue.id] = getMarker(venue);
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
  var marker = new google.maps.Marker({
    map: map,
    position: venue.location,
    title: venue.name + ', at ' + venue.address,
  });
  google.maps.event.addListener(marker, 'click', function() {
    infoWindow.setContent(marker.getTitle());
    infoWindow.open(map, marker);
  });
  return marker;
};

var hideVenue = function(venueId, mark) {
  if (!mark) {
    mark = markers[venueId];
  }
  mark.setVisible(false);
  $('#venue-' + venueId).css('display', 'none');

  // ugly, clean up later
  if ($('#venuelist-showall').css('display') == 'none') {
    $('#venuelist-venues').css('height', 355);
    $('#venuelist-showall').css('display', 'block');
  }
};

var printDisplayedDates = function(minIndex, maxIndex) {
  $('#venuelist-dates').text('showing: ' +
    formatDate(venueData[minIndex].date) +
    ' through ' +
    formatDate(venueData[maxIndex].date));
};

var formatDate = function(date) {
  return (date.getMonth() + 1) + '/' + date.getDate() + '/' +
    date.getFullYear().toString().substring(2);
};

var showVenue = function(venueId) {
  var mark = markers[venueId];
  mark.setVisible(true);
  $('#venue-' + venueId).css('display', 'block');
};

var showAllVenues = function() {
  for (index in listIndexToVenueId) {
    showVenue(listIndexToVenueId[index]);
  }
  $('#slider').slider('values', [0, venueData.length - 1]);
  $('#venuelist-venues').css('height', 410);
  $('#venuelist-showall').css('display', 'none');
  return false;
};


$(document).ready(function() {
  if (limit == undefined) { limit = venueData.length; }
  
  // Initialize pieces of the UI
  geocoder = new google.maps.Geocoder();
  infoWindow = new google.maps.InfoWindow();
  
  initMap();

  for (var i = 0; i < venueData.length; i++) {
    listIndexToVenueId[i] = venueData[i].id;
    var hide = (i < venueData.length - limit);
    codeAddress(venueData[i], hide);
  }

  initSlider();

  // Set handlers for 'delete venue' links, takes precedence
  // over .venue clicks  
  $(".venue-delete").click(function() {
    var venueId = $(this).parent().attr('venue-id');

    $.post('thursdays/thursday/delete_venue', { id: venueId });
    hideVenue(venueId);
    return false;
  });
  
  // Set handlers for venue information divs
  $('.venue').click(function() {
    var venueId = $(this).attr('venue-id');
    infoWindow.setContent(markers[venueId].getTitle());
    infoWindow.open(map, markers[venueId]);
    return false;
  });
  
  // Set handler for 'reveal all venues' link
  $('#venuelist-showall').click(showAllVenues);
  
  // Call the jQuery.placeholder() magic on inputs
  $("input").each(function() {
    $(this).placeholder();
  });
});
