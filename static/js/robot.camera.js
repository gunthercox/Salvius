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
