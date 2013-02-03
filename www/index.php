<html lang="en"><head>
    <meta charset="utf-8">
    <title>Interface</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="./bootstrap/css/bootstrap.css" rel="stylesheet">
    <link href="./bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
	<script type="text/javascript" src="./bootstrap/js/bootstrap.min.js"></script>
  </head>

<body>
<div class="navbar navbar-inverse navbar-fixed-top">
    <div class="navbar-inner">
		<div class="container">
			<a class="brand" href="#">Salvius Interface</a>
			<div class="nav-collapse collapse">
			<ul class="nav">
				<li class="active"><a href="./index.php">GUI</a></li>
				<li><a href="./cli.php">CLI</a></li>
				<li><a href="./settings.php">Settings</a></li>
				<li><div class="pull-right">
						<div class="btn-group">
							<button class="btn btn-warning">Teleoperated</button>
							<button class="btn btn-success">Autonomus</button>
						</div>
			<button type="submit" class="btn btn-primary">Reset</button>
			</div></li>
			</ul>
          </div>
        </div>
      </div>
    </div>

<div class="container">
<div class="hero-unit">
	<div class="well well-large">
	<!-- <iframe class="media" src="./include/camera.php" width="150px" height="280px"></iframe> -->
	<center>
	<div class="btn-group">
		<button class="btn btn-danger">Infrarred</button>
		<button class="btn btn-inverse">Off</button>
		<button class="btn btn-primary">Ultraviolet</button>
	</div>
	
	<div id="slider">
		Left <input id="slide" type="range"
		min="0" max="100" step="5" value="50"
		onchange="updateSlider(this.value)" />
		Right
	</div>
		
	<input type="text" class="search-query" placeholder="Type to speak..." />
	</center>
	</div>
		
		<div class="well well-large">
			<iframe class="media" src="http://192.168.1.177/" width="300px" height="280px"></iframe>
			<div class="btn-group btn-toolbar">
				<form method=get name=NAV>
				<button class="btn" type=submit name=N3 value=LEFT>&larr; Left</button>
				<div class="btn-group btn-group-vertical">
					<button class="btn" type=submit name=N1 value=FORWARD>Forward</button>
					<button class="btn btn-danger" type=submit value=STOP>Stop</button>
					<button class="btn" type=submit name=N2 value=BACKWARD>Backward</button>
				</div>
			<button class="btn" type=submit name=N4 value=RIGHT>Right &rarr;</button>
			<form class="navbar-search pull-left" />
			</div>
		</div>
		
	</div>
</div>
	
    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="./bootstrap/js/jquery.js"></script>
    <script src="./bootstrap/js/bootstrap-transition.js"></script>
    <script src="./bootstrap/js/bootstrap-alert.js"></script>
    <script src="./bootstrap/js/bootstrap-modal.js"></script>
    <script src="./bootstrap/js/bootstrap-dropdown.js"></script>
    <script src="./bootstrap/js/bootstrap-scrollspy.js"></script>
    <script src="./bootstrap/js/bootstrap-tab.js"></script>
    <script src="./bootstrap/js/bootstrap-tooltip.js"></script>
    <script src="./bootstrap/js/bootstrap-popover.js"></script>
    <script src="./bootstrap/js/bootstrap-button.js"></script>
    <script src="./bootstrap/js/bootstrap-collapse.js"></script>
    <script src="./bootstrap/js/bootstrap-carousel.js"></script>
    <script src="./bootstrap/js/bootstrap-typeahead.js"></script>
  
</body></html>