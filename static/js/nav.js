$(".toggle-speech").on("click", function() {
    var className = "speech-menu-open";

    if ($("body").hasClass(className)) {
        $("body").removeAttr("class")
    } else {
        $("body").addClass(className);
    }

    var attr = $("body").attr("class");

    if (typeof attr !== typeof undefined && attr !== false) {
        var classList = attr.split(/\s+/);

        if (classList.length > 1) {
            $("body").removeAttr("class");
            $("body").addClass(className);
        }
    }
});

$(".toggle-writing").on("click", function() {
    var className = "writing-menu-open";

    if ($("body").hasClass(className)) {
        $("body").removeAttr("class")
    } else {
        $("body").addClass(className);
    }

    var attr = $("body").attr("class");

    if (typeof attr !== typeof undefined && attr !== false) {
        var classList = attr.split(/\s+/);

        if (classList.length > 1) {
            $("body").removeAttr("class");
            $("body").addClass(className);
        }
    }
});

$(".toggle-sensors").on("click", function() {
    var className = "sensor-menu-open";

    if ($("body").hasClass(className)) {
        $("body").removeAttr("class")
    } else {
        $("body").addClass(className);
    }

    var attr = $("body").attr("class");

    if (typeof attr !== typeof undefined && attr !== false) {
        var classList = attr.split(/\s+/);

        if (classList.length > 1) {
            $("body").removeAttr("class");
            $("body").addClass(className);
        }
    }
});

$(".toggle-configuration").on("click", function() {
    var className = "configuration-menu-open";

    if ($("body").hasClass(className)) {
        $("body").removeAttr("class")
    } else {
        $("body").addClass(className);
    }

    var attr = $("body").attr("class");

    if (typeof attr !== typeof undefined && attr !== false) {
        var classList = attr.split(/\s+/);

        if (classList.length > 1) {
            $("body").removeAttr("class");
            $("body").addClass(className);
        }
    }
});

$(".toggle-shutdown").on("click", function() {
    var className = "shutdown-menu-open";

    if ($("body").hasClass(className)) {
        $("body").removeAttr("class")
    } else {
        $("body").addClass(className);
    }

    var attr = $("body").attr("class");

    if (typeof attr !== typeof undefined && attr !== false) {
        var classList = attr.split(/\s+/);

        if (classList.length > 1) {
            $("body").removeAttr("class");
            $("body").addClass(className);
        }
    }
});

$(".toggle-slide-left").on("click", function() {
    var className = "sml-open";

    if ($("body").hasClass(className)) {
        $("body").removeAttr("class")
    } else {
        $("body").addClass(className);
    }

    var attr = $("body").attr("class");

    if (typeof attr !== typeof undefined && attr !== false) {
        var classList = attr.split(/\s+/);

        if (classList.length > 1) {
            $("body").removeAttr("class");
            $("body").addClass(className);
        }
    }
});

$(".js-close").click(function() {
    $("body").removeAttr("class");
});
