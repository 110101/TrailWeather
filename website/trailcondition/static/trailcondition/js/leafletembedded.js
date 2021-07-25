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
	// var tilelayer = new L.StamenTileLayer("terrain");
	//tilelayer.options.maxZoom = 18;
	//tilelayer.options.minZoom = 4; //12

	// map = new L.Map('map').setView([defaultlat, defaultlong], 12);
	map = L.map('map', {center: [defaultlat, defaultlong], zoom: 13, scrollWheelZoom: false});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

	//map.addLayer(tilelayer);

	// adding additional control button
	var container = L.DomUtil.create('input');
  container.type="button";

	//map.on('click', onMapClick);

    //    map.on('click', function() { map.scrollWheelZoom.enable(); });
}
// https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=48.143067&lon=11.58371
function overpassapi (lat, lng){
    var baseurl = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&'
    var query = 'lat=' + lat + '&lon=' + lng + '&extratags=1'
    var resulturl = baseurl + query;
    //alert(resulturl);
    var Road_name = "n/a"
    var Surface_name = "unknown"
    //  [out:json];way(id:104178011,18916837);out tags;

    $.get(resulturl, function (osmDataAsJson) {
        var NOMresultstring = JSON.stringify(osmDataAsJson);
        //alert(NOMresultstring);
          // check if user picked a way
/*        var check_if_id1 = NOMresultstring.includes("road");
        if (check_if_id1 == true){
           // if way slected get OSM ID to get surface type in the end
            var Road_idstart = NOMresultstring.indexOf("road");  // + 2
            var Road_short = NOMresultstring.slice(Road_idstart);
            var Road_idend = Road_short.indexOf(",") - 1;
            Road_name = Road_short.substring(7, Road_idend);
            //alert("R:" + Road_name);
        }*/

        var check_if_id2 = NOMresultstring.includes("surface");
        if (check_if_id2 == true){
           // if way slected get OSM ID to get surface type in the end
            var Surface_idstart = NOMresultstring.indexOf("surface");  // + 2

            var Surface_short = NOMresultstring.slice(Surface_idstart);

            var Surface_idend = Surface_short.indexOf(",") - 1;
            Surface_name = Surface_short.substring(10, Surface_idend);
            // alert(Surface_name);
            if (Surface_name.includes(",") == true){
                Surface_name = "unknown";
            }
            else if (Surface_name.includes("_") == true){
                Surface_name = Surface_name.replace(/_/g, " ");
            }
        }
    });
    return Surface_name;
}

function onMapClick(e) {
    var clicklocation = e.latlng.toString();
    var start = clicklocation.indexOf("(");
    var comma = clicklocation.indexOf(",");
    var end = clicklocation.indexOf(")");
    var lat = clicklocation.substring(start+1, comma);
    var lng = clicklocation.substring(comma+2, end);
    var osm_data_return = "";

    map.scrollWheelZoom.enable();


        document.getElementById("lic").style.visibility = "visible";
        document.getElementById("lat").value = Number(( parseFloat(lat) ).toFixed(4));
        document.getElementById("lng").value = Number(( parseFloat(lng) ).toFixed(4));
        osm_data_return = overpassapi(lat, lng);
        //alert("return:" + osm_data_return);
        document.getElementById("type").value = osm_data_return.toString();

    var popup = L.popup({closeButton: false})
        .setLatLng(e.latlng)
        .setContent('<div class="popupbutton"><a class="popuplink" rel="import" href="javascript: submitform()">select<a></div>')
        .openOn(map);
}



function locate_user(){
	function onLocationFound(e){
		var radius = e.accuracy / 2;
		var heading = e.accuracy;
		var timestamp_act = e.timestamp;

		/* $("#location").style.color = '#007bff'; <- Funktioniert noch nicht */
		map.setView(e.latlng, 17);

		onMapClick(e);
		// document.getElementById("lat").value = lat;
		// document.getElementById("lng").value = lng;
		//
		// var popup = L.popup({closeButton: false})
		// 		.setLatLng(e.latlng)
		// 		.setContent('<div class="popupbutton"><a class="popuplink" rel="import" href="javascript: submitform()">select<a></div>')
		// 		.openOn(map);

	}

	map.locate({watch: false, setView: false, maxZoom: 18, maximumAge: 60000, enableHighAccuracy: true})

	map.on('locationfound', onLocationFound);
}
