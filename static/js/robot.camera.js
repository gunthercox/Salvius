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






var timer = 100;
var count = 0;
var image;

function reload() {
	image = new Image();
	image.id = "camimg" + count;
	image.name = image.id;
	image.onload = load;
	image.src = "/camera/?u=" + count;
	count++;
}

var isDark = false;

    function rgbToHsl(r, g, b){
        r /= 255, g /= 255, b /= 255;
        var max = Math.max(r, g, b), min = Math.min(r, g, b);
        var h, s, l = (max + min) / 2;

        if(max == min){
            h = s = 0; // achromatic
        }else{
            var d = max - min;
            s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
            switch(max){
                case r: h = (g - b) / d + (g < b ? 6 : 0); break;
                case g: h = (b - r) / d + 2; break;
		case b: h = (r - g) / d + 4; break;
            }
            h /= 6;
        }

        return [h, s, l];
    }

function load() {
	var drawingCanvas = document.getElementById("cam");

	if (drawingCanvas.getContext) {
		var context = drawingCanvas.getContext("2d");
		context.drawImage(image,0,0,640,480,0,0,300,150);

        var data = context.getImageData(0, 0, 300, 150);

        var image = data.data;

        var rTotal = 0;
        var gTotal = 0;
        var bTotal = 0;

        var pixelCount = image.length / 4;

        for (var i = 0; i < image.length; i += 4) {
            var r = image[i + 0];
            var g = image[i + 1];
            var b = image[i + 2];
            var a = image[i + 3];

            rTotal += r;
            gTotal += g;
            bTotal += b;
        }

        var rAvg = rTotal / pixelCount;
        var gAvg = gTotal / pixelCount;
        var bAvg = bTotal / pixelCount;
		
		var hsl = rgbToHsl(rAvg, gAvg, bAvg);

        var l = hsl[2];

        if (camera.isDark && l >= 0.3) {
            camera.isDark = false;
            console.log("Not dark anymore", l);

            var requst_data = {
                "speech_text": "The lights are back on"
            };

	        $.ajax({
                type: "POST",
                url: robot.urls.speech,
                data: JSON.stringify(request_data),
                contentType: "application/json"
            });
        } else if (!camera.isDark && l < 0.3) {
            camera.isDark = true;
            console.log("It's dark!", l);

            var requst_data = {
                "speech_text": "The lights went out"
            };
	
	        $.ajax({
                type: "POST",
                url: robot.urls.speech,
                data: JSON.stringify(request_data),
                contentType: "application/json"
            });
        }
    }

}



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
