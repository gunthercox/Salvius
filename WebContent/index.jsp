<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" %>
<%@ page import="java.io.File" %>
<%@ page import="cox.utilities. * " %>

<%-- DIRECTORY PATH AND LISTING VARIABLES --%>
<% String path = "C:/"; File folder = new File(path); File[] listOfFiles = folder.listFiles(); %>

<%-- SESSION VARIABLES --%>
<% ServletContext servletContext = getServletContext(); %>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<% out.print(utilities.head()); %>

<%-- DYNAMICALLY GENERATE CSS --%>
<style>
<% for (int i = 0; i < utilities.tab.length; i++) {
	out.println(".t" + i + "{-webkit-transform:rotate(" + ((360 / utilities.tab.length) * i) + "deg);}");
	
	// SET VARIABLES FOR EACH TAB AS CLOSED (0)
	if (utilities.tabular[i] == null) {
		utilities.tabular[i] = "0";
	}
	
	if (request.getParameter("tab" + i) != null) {
		servletContext.setAttribute("tab" + Integer.toString(i), request.getParameter("tab" + Integer.toString(i)));
		utilities.tabular[i] = (String)servletContext.getAttribute("tab" + Integer.toString(i));
	}
	
} %>
</style>

<%-- GET SESSION VARIABLE VALUES FROMTHE PAGE --%>
<%
if (request.getParameter("viewmode") != null) { servletContext.setAttribute("vmode", request.getParameter("viewmode")); }
if (request.getParameter("togglemode") != null) { servletContext.setAttribute("tmode", request.getParameter("togglemode")); }

for (int j = 0; j < utilities.tabular.length; j++) {
	if (request.getParameter("tab" + Integer.toString(j)) == null) {
		// causes only one tab to show at a time and variable not to save
		servletContext.setAttribute("tab" + Integer.toString(j), "0");
	} else {
		servletContext.setAttribute("tab" + Integer.toString(j), request.getParameter("tab" + Integer.toString(j)));
	}
}

if (servletContext.getAttribute("vmode") == null) { servletContext.setAttribute("vmode", "1"); }
if (servletContext.getAttribute("tmode") == null) { servletContext.setAttribute("tmode", "0"); }

%>

</head>
<body><form method="post" action="">

<nav class="top-bar">
<div class="top-bar-section">
	<ul class="left">
		<li><button class="button <% if ("1".equals(servletContext.getAttribute("tmode"))) { out.print("pending"); } %>" name=togglemode value="<% if ("1".equals(servletContext.getAttribute("tmode"))) { out.print("0"); } else { out.print("1"); } %>" >
			<i class="icon-2x <% if ("1".equals(servletContext.getAttribute("tmode"))) { out.print(" icon-folder-open"); } else { out.print(" icon-folder-close"); } %>"></i>
		</button></li>
	</ul>
</div>
<div class="top-bar-section">
	<ul>
		<li><button name=viewmode value=1 class="button <% if ("1".equals(servletContext.getAttribute("vmode"))) { out.print("success"); } %>">
			<i class="icon-dashboard icon-2x"></i>
		</button></li>
		<li><button name=viewmode value=2 class="button <% if ("2".equals(servletContext.getAttribute("vmode"))) { out.print("success"); } %>">
			<i class="icon-list-alt icon-2x"></i>
		</button></li>
		<li><button name=viewmode value=3 class="button <% if ("3".equals(servletContext.getAttribute("vmode"))) { out.print("success"); } %>">
			<i class="icon-sitemap icon-2x"></i>
		</button></li>
	</ul>
</div>
</nav>

<div class="wrapper">

<%-- DISPLAY ALERTS AND MESSAGES --%>
<div>
<% if ("1".equals(servletContext.getAttribute("vmode"))) { %>

	<% if ("1".equals(servletContext.getAttribute("tab0"))) { %>
	<div class="alert-box primary"><b>Camera:</b> Select a point on the view screen to center it.<a href="" class="close">&times;</a></div>
	<% } %>
	
	<% if ("1".equals(servletContext.getAttribute("tab8"))) { %>
		<div class="alert-box primary"><b>Battery:</b> 33.05% remaining,<a href="" class="close">&times;</a></div>
	<% } %>
	
<% } %>
</div>

<%-- ################ SELECT LAYOUT BASED ON SESSION VARIABLE ################ --%>
<% if ("3".equals(servletContext.getAttribute("vmode"))) {
    	
	for (int i = 0; i < listOfFiles.length; i++) {
		out.print("<button class='button' id='" + i + "'>");
		
		// ITEM IS FILE
		if (listOfFiles[i].isFile()) {
			out.print("<i class='icon-file icon-2x'></i><br />" + listOfFiles[i].getName());
		} 
	
		// ITEM IS FOLDER
		else {
			out.print("<i class='icon-folder-close-alt icon-2x'></i><br />" + listOfFiles[i].getName());
		}
		
	out.print("</button>");
}
    	
/* ################ CLI VIEW ################ */
} else if ("2".equals(servletContext.getAttribute("vmode"))) {
	
	out.print("<div class='cli'>");
	
	// SESSION VARIABLE OUTPUT (FOR DEVELOPMENT PURPOSES)
	out.print("view: " + servletContext.getAttribute("vmode") + "<br />");
	out.print("toggle: " + servletContext.getAttribute("tmode") + "<br />");
	for (int i = 0; i < utilities.tab.length; i++) {
		out.print("tab" + i + ": " + servletContext.getAttribute("tab" + i) + "<br />");
	}
	
	out.print("</div>");
	
/* ################ APPS VIEW ################ */
} else {
	
	out.print("<div class='circle' id='camera'></div>");
     
// CREATE THE PRIMARY TAB RING
for (int i = 0; i < utilities.tab.length; i++) {
	
	out.print(utilities.tab((String)servletContext.getAttribute("tmode"), (String)servletContext.getAttribute("tab" + i), utilities.tab[i][1],utilities.tab.length, i, utilities.tab[i][0], ""));
	
// THIS WILL BECOME A CASE SELECT OR ( FOR X IN TAB )

// HEAD CONTROL
if (i == 0) {}
 		
// OPERATING MODE
if (i == 1) {					        
	out.print("<ul class='dropdown-menu'>" +
			"<div class='button-group button-group-vertical'>" +
			"<button type='button' class='button action'>Atonomus</button>" +
			"<button type='button' class='button success'>Assisted</button>" +
			"<button type='button' class='button alert active'>Teleoperated</button>" +
			"</div></ul>");
}

// LIGHTS
if (i == 2) {
	out.print("<div class='dropdown-menu'><div class='button-bar'>" +
			"<ul class='button-group'>" +
			"<li><button type='button' class='button alert'>IR</button></li>" +
			"<li><button type='button' class='button secondary'>UV</button></li>" +
			"</ul></div></div>");
}

// TEXT TO SPEECH
if (i == 3) {
	out.print("<ul class='dropdown-menu well tts' style='-webkit-transform:rotate(" + ((360 / utilities.tab.length) * (-i)) + "deg);'>" +
	"<div class='row span4'>" +
	"<input type='text' name='box-speech' class='span3' placeholder='Enter text to speak'>" +
	"<button class='icon-play'></button>" +
	"<button class='icon-pause'></button>" +
	"<button class='icon-stop'></button>" +
	"</div></ul>");
}

// HAND-WRITING
if (i == 4) {
	out.print("<ul class='dropdown-menu well txt' style='-webkit-transform:rotate(" + ((360 / utilities.tab.length) * (-i)) + "deg);'>" +
	"<div class='row span4'>" +
	"<input type='text' name='box-writing' class='span3' placeholder='Enter text to write'>" +
	"<button class='icon-play'></button>" +
	"<button class='icon-pause'></button>" +
	"<button class='icon-stop'></button>" +
	"</div></ul>");
}

// SENSOR READINGS
if (i == 7) {
	out.print("<ul class='dropdown-menu sensor' style='-webkit-transform:rotate(" + ((360 / utilities.tab.length) * (-i)) + "deg);'>");
	out.print(utilities.table(utilities.sensorData));
	out.print("</ul>");
}

   // POWER
if (i == 8) {
	out.print("<ul class='dropdown-menu'>" +
			"<div class='button-group'>" +
			"<button type='button' class='button active'>" +
			"<i class='icon-circle'></i></button>" +
			"<button type='button' id='off' class='button'><i class='icon-circle-blank'></i></button>" +
			"</div>" +
			"</ul>");
}
 		
out.print("</div>");

	}

} %>
</div>

</form></body></html>
