var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];
var defaultlat = 48.149889;
var defaultlong = 11.585537;
var popup = L.popup();

function onMoveStart(e){
	map.stopLocate();
	alert('locate stop')
};

function initmap(){
	var tilelayer = new L.StamenTileLayer("terrain");
	tilelayer.options.maxZoom = 20;
	tilelayer.options.minZoom = 5; //12

	// map = new L.Map('map').setView([defaultlat, defaultlong], 12);
	map = L.map('map', {center: [defaultlat, defaultlong], zoom: 12, scrollWheelZoom: false});
	map.addLayer(tilelayer);

	map.on('click', onMapClick);

	map.once('focus', function() { map.scrollWheelZoom.enable(); });
}

function onMapClick(e) {
    var clicklocation = e.latlng.toString();
    var start = clicklocation.indexOf("(");
    var comma = clicklocation.indexOf(",");
    var end = clicklocation.indexOf(")");
    var lat = clicklocation.substring(start+1, comma)
    var lng = clicklocation.substring(comma+2, end)

    feedback_streettype = overpassapi(lat, lng)

        document.getElementById("lat").value = lat;
        document.getElementById("lng").value = lng;

    popup
        .setLatLng(e.latlng)
        .setContent('<div class="popupbutton"><a class="popuplink" rel="import" href="javascript: submitform()">go<a></div>' + "You clicked the map at Lat: " + lat + " and long: " + lng)
        .openOn(map);

}

function overpassapi (lat, lng){
    var baseurl = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&'
    var query = 'lat=' + lat + '&lon=' + lng + ''
    var resulturl = baseurl + query;
    //  [out:json];way(id:104178011,18916837);out tags;

    $.get(resulturl, function (osmDataAsJson) {
          var NOMresultstring = JSON.stringify(osmDataAsJson);

          // check if user picked a way
          var check_if_id = NOMresultstring.includes("osm_id");
          if (check_if_id == true){
           // if way slected get OSM ID to get surface type in the end
            var OSM_idstart = NOMresultstring.indexOf("osm_id");  // + 2
            var OSM_short = NOMresultstring.slice(OSM_idstart);
            var OSM_idend = OSM_short.indexOf(",");
            osm_id = OSM_short.substring(8, OSM_idend);
          }

    return osm_id
            });
}

function locate_user(){
	map.locate({watch: true, setView: false, maxZoom: 18, maximumAge: 60000, enableHighAccuracy: true})
	//map.locate()

	function onLocationFound(e){
		var radius = e.accuracy / 2;
		var heading = e.accuracy;
		var timestamp_act = e.timestamp;

		/* $("#location").style.color = '#007bff'; <- Funktioniert noch nicht */
		map.setView(e.latlng, 18);
		L.circle(e.latlng, radius).addTo(map);

		/* L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + heading + " meters from this point").openPopup(); */
        //map.on('movestart', onMoveStart);
	}
	map.on('locationfound', onLocationFound);
}
