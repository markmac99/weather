<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Tackley - Weather overlay on an OSM map</title>

	<link rel="stylesheet" href="css/leaflet.css" >
	<script src="js/leaflet.js" type="text/javascript"></script>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- MetisMenu CSS -->
    <link href="css/plugins/metisMenu/metisMenu.min.css" rel="stylesheet">

    <!-- Timeline CSS -->
    <link href="css/plugins/timeline.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/dragontail.css" rel="stylesheet">

    <!-- Morris Charts CSS -->
    <link href="css/plugins/morris.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="font-awesome-4.5.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
		<script type="text/javascript" src="js/OpenLayers.js"></script>
		<script type="text/javascript" src="https://www.openstreetmap.org/openlayers/OpenStreetMap.js"></script>
<script type="text/javascript">
function pad2(number) {

    var str = '' + number;
    while (str.length < 2) {
        str = '0' + str;
    }
    return str;
}
</script>
<script type="text/javascript">
function initmap() {
    var maxBounds = [[48,-12], [61,5]];
    var imageBounds = [[48,-12], [61,5]];
    var map = L.map('map',{center:new L.LatLng(54, -2),zoom:6,maxBounds:maxBounds});
    var osmAttrib='Map data &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap contributors<\/a>';
    var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution: osmAttrib});

    var seconds = Math.round((new Date()).getTime() / 1000);
	var rounded_seconds = Math.floor((seconds-600) / (15 * 60)) * (15 * 60);
	var dt=new Date(rounded_seconds*1000);
	var lastRainTime = dt.getFullYear()
	    + '-' + pad2(dt.getMonth()+1)
	    + '-' + pad2(dt.getDate())
	    + 'T' + pad2(dt.getHours())
	    + ':' + pad2(dt.getMinutes())
    + ':' + pad2(dt.getSeconds());

    //you will need to replace {key}  with your actual API key
    var RainImageUrl = 'http://datapoint.metoffice.gov.uk/public/data/layer/wxobs/RADAR_UK_Composite_Highres/png?TIME='+lastRainTime+'Z&key=fb499195-a28b-438c-992a-ac533ccce2c9';
    var rainLayer = L.imageOverlay(RainImageUrl, imageBounds);

	lastRainTime = dt.getFullYear()
	    + '-' + pad2(dt.getMonth()+1)
	    + '-' + pad2(dt.getDate())
	    + 'T' + pad2(dt.getHours()-1)
	    + ':' + pad2(dt.getMinutes())
    + ':' + pad2(dt.getSeconds());
    var RainImageUrl1 = 'http://datapoint.metoffice.gov.uk/public/data/layer/wxobs/RADAR_UK_Composite_Highres/png?TIME='+lastRainTime+'Z&key=fb499195-a28b-438c-992a-ac533ccce2c9';
    var rainLayer1 = L.imageOverlay(RainImageUrl1, imageBounds);
    var lastLightningTime =lastRainTime;
    //you will need to replace {key}  with your actual API key
    var LightningImageUrl = 'http://datapoint.metoffice.gov.uk/public/data/layer/wxobs/ATDNET_Sferics/png?TIME='+lastLightningTime+'Z&key=fb499195-a28b-438c-992a-ac533ccce2c9'
    var lightningLayer = L.imageOverlay(LightningImageUrl, imageBounds);
	var lastIRTime =lastRainTime;
    //you will need to replace {key}  with your actual API key
    var IRImageUrl = 'http://datapoint.metoffice.gov.uk/public/data/layer/wxobs/SATELLITE_Infrared_Fulldisk/png?TIME='+lastIRTime+'Z&key=fb499195-a28b-438c-992a-ac533ccce2c9'
    var IRLayer = L.imageOverlay(IRImageUrl, imageBounds);

    var overlays = {
        "Rain": rainLayer,
        "Rain T-60": rainLayer1,
        "Lightning":lightningLayer
		//"Infrared":IRLayer // not available I think
    };

    map.addLayer(osm);
    map.addLayer(rainLayer);
    L.control.layers('',overlays,{collapsed:false}).addTo(map);
	// rotate(4, map);
}

function rotate(idx, map) {
if(idx>=4) {
	idx=0;
    }
    var imageBounds = [[48,-12], [61,5]];
    var lastRainTime;
    if (idx==0) lastRainTime='2018-01-23T15:00:00';
    if (idx==1) lastRainTime='2018-01-23T15:15:00';
    if (idx==2) lastRainTime='2018-01-23T15:30:00';
    if (idx==4) lastRainTime='2018-01-23T15:45:00';

    var RainImageUrl = 'http://datapoint.metoffice.gov.uk/public/data/layer/wxobs/RADAR_UK_Composite_Highres/png?TIME='+lastRainTime+'Z&key=fb499195-a28b-438c-992a-ac533ccce2c9';
    var rainLayer = L.imageOverlay(RainImageUrl, imageBounds);
    map.addLayer(rainLayer);
    idx++;
	timerID=setTimeout(rotate(idx,map), 4000);
}
</script>

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-18220487-1', 'auto');
  ga('send', 'pageview');

</script>
</head>
    <div id="wrapper">

        <!-- Navigation -->
        <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-on5ly">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.html"><img src="images/maryslogo.png" alt="Mary McIntyre, Logo"/></a>
            </div>
            <!-- /.navbar-header -->

            <ul class="nav navbar-top-links navbar-right">
                <li class="dropdown">
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                        <i class="fa fa-envelope fa-fw"></i>  <i class="fa fa-caret-down"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-messages">
                        <li>
                            <a href="#">
                                <div>
                                    <strong>Email me </strong>
                                    <span class="pull-right text-muted">
                                        <em>mark.jm.mcintyre@cesmail.net</em>
                                    </span>
                                </div>
                                <div>Email me with questions etc</div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a class="text-center" href="#">
                                <strong><a href="mailto:mark.jm.mcintyre@cesmail.net?Subject=Communication from Web Site" target="_top">Send Mail</a></strong>
                                <i class="fa fa-angle-right"></i>
                            </a>
                        </li>
                    </ul>
                    <!-- /.dropdown-messages -->
                </li>
                <!-- /.dropdown -->
                <li class="dropdown">
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                        <i class="fa fa-bell fa-fw"></i>  <i class="fa fa-caret-down"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-alerts">
                        <li>
                            <a href="#">
                                <div>
                                    <i class="fa fa-comment fa-fw"></i> Coldest in last 12 hrs
                                    <span class="pull-right text-muted small" id = lowest_temp></span>
                                </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a href="#">
                                <div>
                                    <i class="fa fa-comment fa-fw"></i> Warmest in last 12 hrs
                                    <span class="pull-right text-muted small" id = highest_temp></span>
                                </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a href="#">
                                <div>
                                    <i class="fa fa-tasks fa-fw"></i> Last Update
                                    <span class="pull-right text-muted small"id = 104></span>
                                </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                    </ul>
                    <!-- /.dropdown-alerts -->
                </li>
                <!-- /.dropdown -->
                <li class="dropdown">
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                        <i class="fa fa-user fa-fw"></i>  <i class="fa fa-caret-down"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-user">
                        <li><a href="#"><i class="fa fa-upload fa-fw"></i> Link *****</a>
                        </li>
                        <li class="divider"></li>
						<li><a href="about.html"><i class="fa fa-user fa-fw"></i> About</a>
                        </li>

                    </ul>
                    <!-- /.dropdown-user -->
                </li>
                <!-- /.dropdown -->
            </ul>
            <!-- /.navbar-top-links -->

            <div class="navbar-default sidebar" role="navigation">
                <div class="sidebar-nav navbar-collapse">
                    <ul class="nav" id="side-menu">
                        <li>
                            <a href="index.html"><i class="fa fa-dashboard fa-fw"></i> Dashboard</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-bar-chart-o fa-fw"></i> Charts<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="temperature_graphs.html">Temperature</a>
                                </li>
                                <li>
                                    <a href="rainfall_graphs.html">Rainfall</a>
                                </li>
                                <li>
                                    <a href="wind_graphs.html">Wind</a>
                                </li>
                                <li>
                                    <a href="pressure_graphs.html">Pressure</a>
                                </li>
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>
                        <li>
                            <a href="tables.html"><i class="fa fa-table fa-fw"></i> Tables</a>
                        </li>
                        <li>
                        	<a href="map_rain.php">Rain/Lightning Map</a>
                        </li>
                    </ul>
                </div>
                <!-- /.sidebar-collapse -->
            </div>
            <!-- /.navbar-static-side -->
        </nav>
        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">Current Rain/Lightning</h1>
					<p align="left">Based on data from the met office </p>
					  <div class="feature">
					<div id="map" style="width:680px; height:800px;"></div>
					</div>
					<p style="font-size:11px">Rain and Lightning layers contain public sector information
					licensed under the <a href="http://www.nationalarchives.gov.uk/doc/open-government-licence/" target="_blank">
					Open Government Licence.</a> <br>
					Overlay data up to 15 minutes old.<br>
					<script  type="text/javascript">
						initmap();
					</script>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->
    </div>
    <!-- /#wrapper -->

    <!-- jQuery -->
    <script src="js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

    <!-- Metis Menu Plugin JavaScript -->
    <script src="js/plugins/metisMenu/metisMenu.min.js"></script>

    <!-- Custom Theme JavaScript -->
    <script src="js/sb-admin-2.js"></script>
	<script>

		$( "#current_temp" ).load( "data/dragontailcurrenttemp.txt" );
		$( "#forecastbbc" ).load( "data/dragontailforecastbbc.txt" );
		$( "#lastupdated" ).load( "data/dragontail-updatetime.txt" );
		$.get( "data/dragontail-last24hr-table.txt", ReadMinMax);

		function ReadMinMax( data ) {
			var datums = data.split(/\n/);
			var min24 = 200;
			var min12 = 200;
			var max12 = 0;
			var maxgust = 0;
			var num_rows = 24;
			var rain24 = 0;
			if (datums.length-1<num_rows)
				num_rows=datums.length
				for(i=0;i<num_rows-1;i++){
					min24 = Math.min(min24, Number(datums[i].split(",")[1]))
					//added rain totals for 24 hours
					rain24 = rain24 + Number(datums[i].split(",")[3])
					if (i<12)
						min12 = Math.min(min12, Number(datums[i].split(",")[1]))
						max12 = Math.max(max12, Number(datums[i].split(",")[1]))
						//added for wind gust
						maxgust = Math.max(maxgust, Number(datums[i].split(",")[2]))
				}

				$( "#night_temp" ).html( parseFloat(Math.round(min24 * 10) / 10).toFixed(1) );
				$( "#lowest_temp" ).html( parseFloat(Math.round(min12 * 10) / 10).toFixed(1) );
				$( "#highest_temp" ).html( parseFloat(Math.round(max12 * 10) / 10).toFixed(1) );
				//added for wind gust
				$( "#recent_wind" ).html(parseFloat(Math.round(maxgust * 10) / 10).toFixed(1) );
				//added recent rain
				$( "#recent_rain" ).html(parseFloat(Math.round(rain24 * 10) / 10).toFixed(1) );
		}
	</script>
</body>

</html>
