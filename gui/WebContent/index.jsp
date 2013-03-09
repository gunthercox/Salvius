<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" %>
<%@ page import="java.io.File" %>

<%-- DIRECTORY PATH AND LISTING VARIABLES --%>
<% String path = "."; File folder = new File(path); File[] listOfFiles = folder.listFiles(); %>

<%-- SESSION VARIABLES --%>
<% ServletContext servletContext = getServletContext(); %>
<% Object view = "1"; %>
<% Object toggle = "0"; %>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<% out.print(com.Utilities.head()); %>

<%-- DYNAMICALLY GENERATE CSS --%>
<style>
<% for (int i = 0; i < com.Beans.tab.length; i++) {
	out.println(".t" + i + "{-webkit-transform:rotate(" + ((360 / com.Beans.tab.length) * i) + "deg);}");
	
	// SET VARIABLES FOR EACH TAB AS CLOSED (0)
	if (com.Beans.tabular[i] == null) {
	com.Beans.tabular[i] = "0";
	}
	servletContext.setAttribute("tab" + i, com.Beans.tabular[i]);
	
	String tabname = "tab" + i;
	if (request.getParameter(tabname) != null) {
		com.Beans.tabular[i] = request.getParameter(tabname); servletContext.setAttribute(tabname, com.Beans.tabular[i]);
	}
	
} %>
</style>

</head>
<body><form method="post" action="">

<%-- SET SESSION VARIABLES AND DEFAULTS --%>
<%
if (request.getParameter("viewmode") != null) {
	view = request.getParameter("viewmode"); servletContext.setAttribute("vmode", view);
}

if (request.getParameter("togglemode") != null) {
	toggle = request.getParameter("togglemode"); servletContext.setAttribute("tmode", toggle);
}
%>

<%-- SESSION VARIABLE OUTPUT --%>
view: <%= servletContext.getAttribute("vmode") %><br />
toggle: <%= servletContext.getAttribute("tmode") %><br />
<% for (int i = 0; i < com.Beans.tab.length; i++) {
out.println("tab" + i + ": " + servletContext.getAttribute("tab" + i) + "<br />");
} %>

<div class='circle' id='camera'>

<%-- SELECT LAYOUT BASED ON SESSION VARIABLE --%>
<% if ("3".equals(servletContext.getAttribute("vmode"))) {
    	
	for (int i = 0; i < listOfFiles.length; i++) {
		out.print("<div class='rotate' style='-webkit-transform:rotate(" + ((360 / listOfFiles.length) * i) + "deg);'>");
	
		// ITEM IS FILE
		if (listOfFiles[i].isFile()) {
			out.print("<div class='dir btn btn-inverse dropdown' id='" + i + "' data-toggle='dropdown' style='margin-left:-40px!important'>" +
			"<i class='icon-file'></i><br />" + listOfFiles[i].getName() + "</div>");
		} 
	
		// ITEM IS FOLDER
		else {
			out.print("<div class='dir tab btn btn-inverse dropdown' id='" + i + "data-toggle='dropdown' style='margin-left:-40px!important'>" +
			"<i class='icon-folder-close-alt'></i><br />" + listOfFiles[i].getName() + "</div>");
		}
		
	out.print("</div>");
}
    	
// CLI VIEW
} else if ("2".equals(servletContext.getAttribute("vmode"))) {
	
	// CURRENTLY NO ACTION
	
// APPS VIEW
} else {
     
// CREATE THE PRIMARY TAB RING
for (int i = 0; i < com.Beans.tab.length; i++) {
	
	out.print(com.Utilities.tab((String)servletContext.getAttribute("tmode"), (String)servletContext.getAttribute("tab" + i), com.Beans.tab[i][1], com.Beans.tab.length, i, com.Beans.tab[i][0], ""));
	
// THIS WILL BECOME A CASE SELECT OR ( FOR X IN TAB )

// HEAD CONTROL
if (i == 0) {
	out.print("<ul class='dropdown-menu' role='menu'>" +
			"<p class='text-center'>Select a point on the view screen to center it.</p></ul>");
}
 		
// OPERATING MODE
if (i == 1) {					        
	out.print("<ul class='dropdown-menu' role='menu'>" +
			"<div class='btn-group btn-group-vertical' data-toggle='buttons-radio'>" +
			"<button type='button' class='btn btn-action'>Atonomus</button>" +
			"<button type='button' class='btn btn-success'>Assisted</button>" +
			"<button type='button' class='btn btn-warning active'>Teleoperated</button>" +
			"</div></ul>");
}

// LIGHTS
if (i == 2) {
	out.print("<ul class='dropdown-menu' role='menu'>" +
			"<div class='btn-group' data-toggle='buttons-checkbox'>" +
			"<button type='button' class='btn btn-large btn-danger'>IR</button>" +
			"<button type='button' class='btn btn-large btn-inverse'>UV</button>" +
			"</div></ul>");
}

// TEXT TO SPEECH
if (i == 3) {
	out.print("<ul class='dropdown-menu well tts' style='-webkit-transform:rotate(" + ((360 / com.Beans.tab.length) * (-i)) + "deg);'>" +
	"<div class='row span4'>" +
	"<input type='text' name='box-speech' class='span3' placeholder='Enter text to speak'>" +
	"<button class='icon-play'></button>" +
	"<button class='icon-pause'></button>" +
	"<button class='icon-stop'></button>" +
	"</div></ul>");
}

// HAND-WRITING
if (i == 4) {
	out.print("<ul class='dropdown-menu well txt' style='-webkit-transform:rotate(" + ((360 / com.Beans.tab.length) * (-i)) + "deg);'>" +
	"<div class='row span4'>" +
	"<input type='text' name='box-writing' class='span3' placeholder='Enter text to write'>" +
	"<button class='icon-play'></button>" +
	"<button class='icon-pause'></button>" +
	"<button class='icon-stop'></button>" +
	"</div></ul>");
}

// SENSOR READINGS
if (i == 7) {
	out.print("<ul class='dropdown-menu sensor' style='-webkit-transform:rotate(" + ((360 / com.Beans.tab.length) * (-i)) + "deg);'>");
	out.print(com.Utilities.table(com.Beans.sensorData));
	out.print("</ul>");
}

   // POWER
if (i == 8) {
	out.print("<ul class='dropdown-menu' role='menu'>" +
			"<div class='btn-group' data-toggle='buttons-radio'>" +
			"<button type='button' class='btn btn-large active'>" +
			"<i class='icon-circle'></i></button>" +
			"<button type='button' id='off' class='btn btn-large'><i class='icon-circle-blank'></i></button>" +
			"</div>" +
			"<p class='text-center'>Battery: " + "33.05%" + "</p>" +
			"</ul>");
}
 		
out.print("</div>");

	}

} %>

<script>

$('#off').click(function() {
	return confirm('Are you sure you want to deactivate the robot?');
});

$('#toggle').each(function() {
	$(this).click(function() {
		if ($('.rotate').hasClass('open')) {
		$('.rotate').removeClass('open');
		} else {
		$('.rotate').addClass('open');
		}
	});
});
			
$('#camera').click(function(e) {
if ($('.rotate').hasClass('open')) {
	$('#dot').addClass('dot icon-screenshot');
	$('.dot').css({'top':e.pageY, 'left':e.pageX});
} else {
	$('#dot').removeClass('dot icon-screenshot');
	}
});
		
$('.tab').click(function() {
	if ($(this).parent('div').hasClass('open')) {
	$(this).parent('div').removeClass('open');
	} else {
	$(this).parent('div').addClass('open');
	}
});

</script>

<%-- CAMERA FEED & CONTROL BUTTONS --%>
<div id="dot"></div>
	<div class="btn-bar btn-toolbar">
		<button id="toggle" name=togglemode value="<% if ("1".equals(servletContext.getAttribute("tmode"))) { out.print("0"); } else { out.print("1"); } %>" class="btn<% if ("1".equals(servletContext.getAttribute("tmode"))) { out.print(" btn-success icon-folder-open"); } else { out.print(" btn-primary icon-folder-close"); } %>"></button>
		<div class="btn-group">
			<button name=viewmode value=1 class="btn btn-primary icon-dashboard <% if ("1".equals(servletContext.getAttribute("vmode"))) { out.print("active"); } %>"></button>
			<button name=viewmode value=2 class="btn btn-primary icon-list-alt <% if ("2".equals(servletContext.getAttribute("vmode"))) { out.print("active"); } %>"></button>
			<button name=viewmode value=3 class="btn btn-primary icon-sitemap <% if ("3".equals(servletContext.getAttribute("vmode"))) { out.print("active"); } %>"></button>
		</div>

	</div>
	
</div>

</form></body></html>
