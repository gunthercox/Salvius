/* CANVIS CODE FROM http://dwdii.github.io/2011/10/23/Using-HTML5-Canvas-tag-for-Simple-Video-Animation.html
Known issue: http://stackoverflow.com/questions/13674835/canvas-tainted-by-cross-origin-data */
var imageUpdateMs = 1;
var count = 0;
var newImg;

setTimeout("imageUpdate()", imageUpdateMs);

function imageUpdate() {
	document.getElementById("txt").innerHTML = count++;

	newImg = new Image();
	newImg.Id = "cam" + count;
	newImg.Name = newImg.Id;
	newImg.onload = imageLoaded;
	newImg.src = robot.urls.camera_image_url;
}

function imageLoaded() {
	var context = $("#cam")[0].getContext('2d');
	context.drawImage(newImg,0,0,640,480,0,0,300,150);
	setTimeout("imageUpdate()", imageUpdateMs);
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
    document.getElementById("doEvent").innerHTML = "Not supported on your device or browser.  Sorry."
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
