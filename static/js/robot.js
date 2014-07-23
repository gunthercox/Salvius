function Robot() {

    var self = this;

    this.error = function handleError(error) {
        var error = error || "";

        if (error != "") {
            var template = $('<li class="message">' + error +
            '<span class="js-dismiss close"></span></li>');
            $(".error-list").append(template);
        }

        // Change indicator led based on error count
        var errorCount = $(".error-list").find("li").length;
        if (errorCount > 0) {
            $(".warning.led").removeClass("green").addClass("red");
        } else {
            $(".warning.led").removeClass("red").addClass("green");
        }
    }

    this.terminate = function terminate() {
        var request = new XMLHttpRequest();
        request.open("POST", "/api/terminate/", true);
        request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
        request.send({});
    }

}

var robot = new Robot();

// SETTINGS
var camera_ip = "192.168.1.2";
var arduino_ip = "192.168.1.177";

$(".camera_ip").val(camera_ip);
$(".arduino_ip").val(arduino_ip);

var cameraImage = ["http://", camera_ip, "/image.jpg"].join("");
var arduinoJson = ["http://", arduino_ip].join("");

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
	newImg.src = cameraImage;
}

function imageLoaded() {
	var context = $("#cam")[0].getContext('2d');
	context.drawImage(newImg,0,0,640,480,0,0,300,150);
	setTimeout("imageUpdate()", imageUpdateMs);
}
	
$.ajax({ 
    type: "GET", 
    url: arduinoJson, 
    data: { get_param: "value" }, 
    dataType: 'json',
    success: function (data) {
        $.each(data, function(index, element) {
            $(".sensorValues").append("<tr><td>" + index + "</td><td>" + element + "</td></tr>");
        });
        $(".filter").removeClass("hide");
    }
}).error(function() {
    robot.error("Arduino api is unavailable.");
});

$(".js-terminate").click(function() {
    robot.terminate();
});

$(".panel").on("click", ".js-dismiss", function() {
    $(this).parents(".panel").addClass("hide");
});

$(".error-list").on("click", ".js-dismiss", function() {
    $(this).parents("li").remove();
    robot.error();
});

$(".js-dismiss-all").click(function() {
    $(".error-list li").remove();
    robot.error();
});

$('a[href="#warnings"]').click(function() {
    $(".warnings").toggleClass("hide");
});

$('a[href="#shutdown"]').click(function() {
    $(".shutdown").removeClass("hide");
});

$('a[href="#configuration"]').click(function() {
    $("#configuration").removeClass("hide");
});

$("#post").click(function() {
    var key = $("#key").val();
    var value = $("#value").val();
    var str = [key, value].join("=");
    $.ajax({
        type: "POST",
        url: "http://" + arduino_ip,
        data: str,
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        success: function(data) {
            $("#key").val("");
            $("#value").val("");
            //TODO: UPDATE TABLE IF NEEDED WHEN POSTING Dx
            // if key in table table.key.val(key)
        }
    }).error(function(data) {
        robot.error("Failure to post data.");
    });
});

$("#say").click(function() {
    var key = "say";
    var value = $("#value").val();
    var str = [key, value].join("=");
    $.ajax({
        type: "POST",
        url: "http://"+arduino_ip,
        data: str,
        contentType: "application/x-www-form-urlencoded; charset=utf-8"
    }).success(function(data) {
        $("#key").val("");
        $("#value").val("");
    }).error(function(data) {
        robot.error("Failure to post data");
    });
});

$("#write").click(function() {
    console.log("Write button not implemented");
});

var timer = {};

timer.rotationDelay = 0;
timer.rotationReset = 0;
timer.angleDelay = 0;
timer.angleReset = 0;

$(".js-rotate-head").on("input change", function() {
    var input = $(this);
    var value = input.val();
    value = parseInt(value);

    clearTimeout(timer.rotationReset);

    function zero() {

        if (timer.rotationReset) {
            clearTimeout(timer.rotationReset);
        }

        timer.rotationReset = setTimeout(function() {
            if (value > 0) {
                value -= 1;
                input.val(value);
                zero();
            }

            if (value < 0) {
                value += 1;
                input.val(value);
                zero();
            }
        }, 100);
    }

    if (timer.rotationDelay) {
        clearTimeout(timer.rotationDelay);
    }

    timer.rotationDelay = setTimeout(zero, 1000);
});

$(".js-angle-head").on("input change", function() {
    var input = $(this);
    var value = input.val();
    value = parseInt(value);

    clearTimeout(timer.angleReset);

    function zero() {

        if (timer.angleReset) {
            clearTimeout(timer.angleReset);
        }

        timer.angleReset = setTimeout(function() {
            if (value > 0) {
                value -= 1;
                input.val(value);
                zero();
            }

            if (value < 0) {
                value += 1;
                input.val(value);
                zero();
            }
        }, 100);
    }

    if (timer.angleDelay) {
        clearTimeout(timer.angleDelay);
    }

    timer.angleDelay = setTimeout(zero, 1000);
});

