var Robot = Robot || {};

Robot.settings = {};

Robot.loading = $('<div class="center"><i class="fa fa-spinner fa-spin"></i> Loading...</div>');

Robot.timers = {
    "rotationDelay": 0,
    "rotationReset": 0,
    "angleDelay": 0,
    "angleReset": 0
};

Robot.error = function error(error) {
    var error = error || "";

    if (error != "") {
        var template = $('<div class="alert alert-warning">' + error +
        '<span class="js-dismiss close"></span></div>');
        $(".error-list").append(template);
    }

    // Change indicator led based on error count
    var errorCount = $(".error-list").find(".alert").length;
    if (errorCount > 0) {
        $(".js-warning").addClass("warning");
    } else {
        $(".js-warning").removeClass("warning");
    }
}

Robot.snapshot = function snapshot() {
    var check = confirm("Save camera image?");
    if (check == true) {
        window.open(Robot.settings.camera_image_url, "_blank");
    }
}

Robot.terminate = function terminate() {
    var message = "WARNING: Emergency shutdown operation will deactivate all systems on the robot."
    var request = new XMLHttpRequest();
    if (confirm(message)) {
        request.open("POST", "/api/terminate/", true);
        request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
        request.send({});
    }
}

Robot.loadSensorData = function loadSensorData() {
    $.ajax({ 
        type: "GET", 
        url: Robot.settings.arduino_ip, 
        data: { get_param: "value" }, 
        dataType: 'json'
    }).success(function(data) {
        $.each(data, function(index, element) {
            $(".sensorValues").append("<tr><td>" + index + "</td><td>" + element + "</td></tr>");
        });
        $(".filter").removeClass("hide");
    }).error(function() {
        Robot.error("Arduino api is unavailable");
    });
}

Robot.renderLimbControl = function renderLimbControl(container, limb) {

    $(container).html("");

    var template = $('<li class="list-group-item"></li>');

    var renderable_types = ["elbow", "shoulder", "wrist", "hip", "knee", "ankle"];
    for (var section in limb) {
        if ($.inArray(section, renderable_types) > -1) {

            var row = template.clone();

            console.log(section, limb[section].joint_type);

            var control = $('<div><label></label><input type="number" min="0" max="100"></div>');
            control.find("label").text(section);
            control.find("input").val(limb[section].angle);
            control.find("input").data("url", limb[section].href);
            row.append(control);

            $(container).append(row);
        }
    }

    control.on("input", "input", function() {
        var value = $(this).val();
        value = { "angle": value };
        var data = $(this).data();

        $.ajax({
            type: "PATCH",
            url: data.url,
            data: JSON.stringify(value),
            contentType: "application/json"
        }).error(function() {
            Robot.error("Unable to update limb field");
        });
    });
}

var armClassList = [".js-arm-control-left", ".js-arm-control-right"];
for (var i = 0; i < armClassList.length; i++) {
    var loading = Robot.loading.clone();
    $(armClassList[i]).append(loading);
}
var legClassList = [".js-leg-control-left", ".js-leg-control-right"];
for (var i = 0; i < legClassList.length; i++) {
    var loading = Robot.loading.clone();
    $(legClassList[i]).append(loading);
}

$.ajax({
    type: "GET",
    url: "/api/robot/body/arms/"
}).success(function(data) {

    console.log(data);

    for (var i = 0; i < data.arms.length; i++) {
        var arm = data.arms[i];
        Robot.renderLimbControl(armClassList[i], arm);
    }
}).error(function() {
    Robot.error("Unable to load arm data");
});

$.ajax({
    type: "GET",
    url: "/api/robot/body/legs/"
}).success(function(data) {
    for (var i = 0; i < data.legs.length; i++) {
        var leg = data.legs[i];
        Robot.renderLimbControl(legClassList[i], leg);
    }
}).error(function() {
    Robot.error("Unable to load leg data");
});

$.ajax({
    type: "GET",
    url: "/api/settings/"
}).success(function(data) {
    Robot.settings.camera_image_url = data.camera_image_url;
    Robot.settings.arduino_ip = data.arduino_ip;

    $(".js-camera-url").val(Robot.settings.camera_image_url);
    $(".js-arduino-url").val(Robot.settings.arduino_ip);
    Robot.loadSensorData();
}).error(function() {
    Robot.error("Unable to load settings");
});

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
	newImg.src = Robot.settings.camera_image_url;
}

function imageLoaded() {
	var context = $("#cam")[0].getContext('2d');
	context.drawImage(newImg,0,0,640,480,0,0,300,150);
	setTimeout("imageUpdate()", imageUpdateMs);
}

$(".js-terminate").click(function() {
    Robot.terminate();
});

$(".error-list").on("click", ".js-dismiss", function() {
    $(this).parents(".alert").remove();
    Robot.error();
});

$(".js-dismiss-all").click(function() {
    $(".error-list .alert").remove();
    Robot.error();
});

$("#post").click(function() {
    var key = $("#key").val();
    var value = $("#value").val();
    var str = [key, value].join("=");
    $.ajax({
        type: "POST",
        url: "http://" + arduino_ip,
        data: str,
        contentType: "application/x-www-form-urlencoded; charset=utf-8"
    }).success(function(data) {
        $("#key").val("");
        $("#value").val("");
        //TODO: UPDATE TABLE IF NEEDED WHEN POSTING Dx
        // if key in table table.key.val(key)
    }).error(function(data) {
        Robot.error("Failure to post data.");
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
        Robot.error("Failure to post data");
    });
});

$("#write").click(function() {
    console.log("Write button not implemented");
});

$(".js-capture-photo").click(function() {
    Robot.snapshot();
});

$(".js-listen").click(function() {
    $(this).toggleClass("btn-default btn-success");
    // TODO
});

$(".tabs").on("click", ".tab-title", function(event) {
    event.preventDefault();
    event.stopPropagation();

    $(this).siblings().removeClass("active");
    $(this).addClass("active");

    var id = $(this).find("a").attr("href");
    $(id).siblings().removeClass("active");
    $(id).addClass("active");
});

$(".js-rotate-head").on("input change", function() {
    var input = $(this);
    var value = input.val();
    value = parseInt(value);

    clearTimeout(Robot.timers.rotationReset);

    function zero() {

        if (Robot.timers.rotationReset) {
            clearTimeout(Robot.timers.rotationReset);
        }

        Robot.timers.rotationReset = setTimeout(function() {
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

    if (Robot.timers.rotationDelay) {
        clearTimeout(Robot.timers.rotationDelay);
    }

    Robot.timers.rotationDelay = setTimeout(zero, 1000);
});

$(".js-angle-head").on("input change", function() {
    var input = $(this);
    var value = input.val();
    value = parseInt(value);

    clearTimeout(Robot.timers.angleReset);

    function zero() {

        if (Robot.timers.angleReset) {
            clearTimeout(Robot.timers.angleReset);
        }

        Robot.timers.angleReset = setTimeout(function() {
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

    if (Robot.timers.angleDelay) {
        clearTimeout(Robot.timers.angleDelay);
    }

    Robot.timers.angleDelay = setTimeout(zero, 1000);
});

$(".js-camera-url").on("change", function() {
    Robot.settings.camera_image_url = $(this).val();
    $.ajax({
        type: "PUT",
        url: "/api/settings/",
        data: JSON.stringify(Robot.settings),
        contentType: "application/json"
    }).error(function() {
        Robot.error("Error updating settings");
    });
});

$(".js-arduino-url").on("change", function() {
    Robot.settings.arduino_ip = $(this).val();
    $.ajax({
        type: "PUT",
        url: "/api/settings/",
        data: JSON.stringify(Robot.settings),
        contentType: "application/json"
    }).error(function() {
        Robot.error("Error updating settings");
    });
});
