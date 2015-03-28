window.Robot = window.Robot || {};

var Robot = Robot || {};

var Camera = function() {
    this.timer = null;
    this.count = 0;
    this.image = null;

    this.drawingCanvas = document.getElementById("cam");
};

Camera.prototype.streaming = function(on) {
    var camera = this;

    console.log("camera streaming:", on);

    /*var updatetimer = function() {
        //do stuff

        console.log(0);

        // By the way, can just pass in the function name instead of an anonymous
        // function unless if you want to pass parameters or change the value of 'this'
        camera.timer = setTimeout(updatetimer, 1000);
    };*/

    if (on) {
    	//updatetimer();
    } else {
        // Since the timeout is assigned to a variable, we can successfully clear it now
    	//clearTimeout(camera.timer);
        //clearTimeout(camera.timeout);
    }

    function reload() {
	    camera.image = new Image();
	    //camera.image.id = "c" + camera.count;
	    //camera.image.name = image.id;
	    camera.image.onload = load;
	    camera.image.src = robot.urls.camera_image_url + "?u=" + camera.count;
	    camera.count++;
    }

    function load() {
	    if (camera.drawingCanvas.getContext) {
		    var context = camera.drawingCanvas.getContext("2d");
		    context.drawImage(camera.image,0,0,640,480,0,0,300,150);
	    }

	    setTimeout(reload, camera.timer);
    }

    setTimeout(reload, camera.timer);


};

Robot.Camera = Robot.Camera || new Camera();







///////////////////////////////////////////////////////


init();
var count = 0;

function init() {
  if (window.DeviceOrientationEvent) {
    // Listen for the deviceorientation event and handle the raw data
    window.addEventListener("deviceorientation", function(eventData) {

      // gamma is the left-to-right tilt in degrees, where right is positive
      var tiltLR = eventData.gamma;
      
      // beta is the front-to-back tilt in degrees, where front is positive
      var tiltFB = eventData.beta;
      
      // alpha is the compass direction the device is facing in degrees
      var dir = eventData.alpha
      
      // call our orientation event handler
      deviceOrientationHandler(tiltLR, tiltFB, dir);

      }, false);
  } else {
    document.getElementById("doEvent").innerHTML = "Not supported on your device or browser. Sorry."
  }
}

function deviceOrientationHandler(tiltLR, tiltFB, dir) {

    if (robot.mobile == false) {
        return;
    }

    var direction = Math.round(dir);
    var tiltLeftRight = Math.round(tiltLR);
    var tiltFrontBack = Math.round(tiltFB);

    robot.elements.rotate_head.val(direction);
    robot.elements.rotate_head.change();

    robot.elements.angle_head.val(tiltLeftRight);
    $(".js-front-back-tilt").find(".readout").text(tiltLeftRight);

    $(".js-left-right-tilt").find(".readout").text(tiltFrontBack);
}


// Some other fun rotations to try...
//var rotation = "rotate3d(0,1,0, "+ (tiltLR*-1)+"deg) rotate3d(1,0,0, "+ (tiltFB*-1)+"deg)";
//var rotation = "rotate("+ tiltLR +"deg) rotate3d(0,1,0, "+ (tiltLR*-1)+"deg) rotate3d(1,0,0, "+ (tiltFB*-1)+"deg)";
