var robot = new Robot();

var $camera = $('#cam');

$camera.networkCamera({
    'url': 'https://www.google.com/logos/doodles/2015/fourth-of-july-2015-5118459331477504.2-hp.jpg',
    //'ip': 'http://192.168.1.2/image/jpeg.cgi',
    'streaming': true
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

$('a[href="#health"]').on("shown.bs.tab", function(e) {
    robot.renderStatus();
});

$('.navbar [data-toggle="tab"]').on("show.bs.tab", function(e) {
    var href = $(this).attr("href");

    // Only stream the camera feed when the tab is shown
    if (href == "#interface") {
        $camera.networkCamera('stream');
    } else {
        $camera.networkCamera('pause');
    }
});

$(".js-toggle-mobile").click(function(e) {
    e.preventDefault();

    $(this).find(".fa").toggleClass("fa-spin");
    robot.mobile = !robot.mobile;
});

$("#write").click(function() {
    console.log("Write button not implemented");
});

$(".js-capture-photo").click(function() {
    robot.snapshot();
});

$(".js-terminate").click(function() {
    robot.terminate();
});

$(".error-list").on("click", ".js-dismiss", function() {
    $(this).parents(".alert").remove();
    robot.error();
});

$("js-dismiss-all").click(function() {
    $(".error-list .alert").remove();
    robot.error();
});

$("#say").click(function(e) {
    e.preventDefault();

    var value = $(".js-speech-text");

    var request_data = {
        "speech_text": value.val()
    };

    $.ajax({
        type: "POST",
        url: robot.urls.speech,
        data: JSON.stringify(request_data),
        contentType: "application/json"
    }).success(function(data) {
        value.val("");
    }).error(function(data) {
        robot.error("Failed to post data");
    });
});

$(".js-speech-text").keypress(function(e) {
    if(e.which == 13) {
        e.preventDefault();
        $("#say").click();
    }
});

$(".chat-input").keyup(function(e) {
    if (e.keyCode == 13) {
        var text = $(this).val();
        var indicator = $(this).parent().find(".fa");
        var session_log = $(".chat-log");
        robot.respond(text, session_log, indicator);
        $(this).val("").focus();
    }
});

$(".js-rotate-head").on("input change", function(e) {
    // Display the value of the slider
    var input = $(this);
    var value = parseInt(input.val());
    input.parent().find("output").text(value);
}).on("input change",  $.debounce(250, function(e) {

    var input = $(this);
    var value = parseInt(input.val());
    var previous_value = input.data("previous-value");
    var json_data = {
        "rotate": value
    };

    // Do not send a request if the value has not changed
    if (value != previous_value) {
        $.ajax({
            type: "PATCH",
            url: robot.urls["api_neck"],
            data: JSON.stringify(json_data),
            contentType: "application/json"
        });
    }

    input.data("previous-value", value);

}));

$(".js-angle-head").on("input change", function() {
    var input = $(this);
    var value = parseInt(input.val());

    // TODO: Send to api
});

$(".js-soundboard").on("click", "button", function() {
    var request_data = {
        "speech_text": $(this).text()
    };

    $.ajax({
        type: "POST",
        url: robot.urls.speech,
        data: JSON.stringify(request_data),
        contentType: "application/json"
    }).success(function(data) {
        value.val("");
    }).error(function(data) {
        robot.error("Failed to post data");
    });
});


///////////////////////////////////////////////////////


init();

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
