function draw_features(features){
	/* Features is a list of feature objects.
		feature objects contain:
		geom
		geomtype   (1=Point, 2=Path, 3= Polygon)	
	*/
	for (var i=0;i<features.length;i++){
		
		var f=features[i];
		var PROJECT_COLOR='#33FF11';
		var FEATURE_COLOR ='#FF6655';
		var geom = f.geom;
				
		//html = infowindowHTML(f);
		
		var infowindow = new google.maps.InfoWindow({
			content:f.html,
		});
		
		switch (f.geomtype){		
			case 1:			//Point geometry
				var marker = new google.maps.Marker({
					position:new google.maps.LatLng(geom[0],geom[1]),
					map:Map.map,
					index:i,
				});
											
				Map.layers[0].geom[i] = marker;
				Map.layers[0].geom[i].infowindow = infowindow; 
				google.maps.event.addListener(marker, 'click', function(){
					Map.layers[0].geom[this.index].infowindow.open(Map.map,this);
				});
				break;
			case 3:			// Polygon
				var mapObj = Map.list2polygon(geom);
				var color = PROJECT_COLOR
				var zIndex = -10;
				var opacity=0;
				if (f.feature_of) {
				  var color = FEATURE_COLOR
				  var zIndex=0;
				  var opacity = .1;
				}				

				Map.layers[0].geom[i] = mapObj;
				Map.layers[0].geom[i].setOptions({
					'strokeColor':color,
					'fillColor':color,
					'fillOpacity':.1,
					'index':i,
					'zIndex':zIndex,
					'fillOpacity':opacity,
					
				});
				Map.layers[0].geom[i].setMap(Map.map);
								
				Map.layers[0].geom[i].infowindow = infowindow;    
				google.maps.event.addListener(mapObj, 'click', function(){
					p = new google.maps.Marker({
						position:this.getPath().getAt(0),
						map:Map.map,
						visible:false,
					});
					Map.layers[0].geom[this.index].infowindow.open(Map.map,p);
				});
				
				break;
		};	
	}
}


function infowindowHTML(feature){
	// Input -  feature <-feature obj
	// Output - html <- html string to put in the infowindow content option.
	var width = '280x';
	var height = '280px';
	var html = "<div style='width:"+width+"; height:"+height+"'>";
	html += "<h4>"+feature.title+"<h4>";			
	if (feature.image){ html += "<img src='"+feature.image+"'></img>";}
	html += "</div>";
	return html
}



