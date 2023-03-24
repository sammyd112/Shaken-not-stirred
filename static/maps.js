
let currentLocation = {lat: 36.778261, lng: -119.4179324}
let zoomLevel = 6
let map = null;
function initMap(){
        map = new google.maps.Map(document.getElementById('map'), {
        center: currentLocation,
        zoom: zoomLevel
        });
        if (zoomLevel != 6) {
         getBars(currentLocation)
        }
      }

let searchInput = 'search_input';
$(document).ready(function () {
    let autocomplete;
    autocomplete = new google.maps.places.Autocomplete((document.getElementById(searchInput)), {
         types : ['geocode'],
     });
        google.maps.event.addListener(autocomplete, 'place_changed', function () {
        let near_place = autocomplete.getPlace();
        let latt = document.getElementById('latitude_input').value = near_place.geometry.location.lat();
        let lngg = document.getElementById('longitude_input').value = near_place.geometry.location.lng();
        currentLocation = {lat: latt, lng : lngg}
        zoomLevel = 12
        console.log(currentLocation)
        initMap()
            })
});

function getBars(location){
    let pointless = new google.maps.LatLng(location['lat'], location['lng'])
    let request = {
        location: pointless,
        radius : '10000',
        type: ['bar']
    }
    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, callback);
}

function callback(results, status){
    if (status == google.maps.places.PlacesServiceStatus.OK){
        for (var i = 0; i < results.length; i++){
            var place = results[i];
            let price = createPrice(place.price_level);
            let content = `<h4>${place.name} </h4>
                            <p>Price: ${price}</br>
                            Rating: ${place.rating}</p>
                            <div>${place.vicinity}</div>`;
            var marker = new google.maps.Marker({
                position:place.geometry.location,
                map: map,
                title: place.name
            });
        var infowindow = new google.maps.InfoWindow({
            content: content
        });
        bindInfoWindow(marker, map, infowindow, content);
        marker.setMap(map);  
    }}}

function bindInfoWindow(marker, map, infowindow, html){
    marker.addListener('click', function() {
        infowindow.setContent(html);
        infowindow.open(map, this);
    });
}

function createPrice(level){
    if (level !="" && level != null){
        let out = "";
        for (var x = 0; x < level; x++) {
            out += "$";
    }
    return out;
    } else {
        return "?"
    }
}
