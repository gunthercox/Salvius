<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1"%>
<%@ page import="java.io.File" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<% out.print(com.Utilities.head()); %>
</head>
<body><form method="post" action="">

<%-- DIRECTORY PATH AND LISTING VARIABLES --%>
<% String path = "."; File folder = new File(path); File[] listOfFiles = folder.listFiles(); %>

<%-- SESSION VARIABLES --%>
<% String view = request.getParameter("viewmode"); session.setAttribute("view", view); %>
<% String toggle = request.getParameter("togglemode"); session.setAttribute("toggle", toggle); %>

<%-- INITIALIZE SESSION VARIABLES IF NULL OR NECESSARY --%>
<% if (view == null) { session.setAttribute("view", "1"); } %>
<% if (toggle == null) { session.setAttribute("toggle", "0"); } %>

<%-- SESSION VARIABLE OUTPUT --%>
view: <%=session.getAttribute( "view" )%><br />
toggle: <%=session.getAttribute( "toggle" )%><br />

<div class='circle' id='camera'>

<%-- SELECT LAYOUT BASED ON SESSION VARIABLE --%>
<% if ("3".equals(view)) {
    	
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
} else if ("2".equals(view)) {
	
	// CURRENTLY NO ACTION
	
// APPS VIEW
} else {
     
// CREATE THE PRIMARY TAB RING
for (int i = 0; i < com.Beans.tab.length; i++) {
     	
	// GIVE THE TAB AN ID NUMBER
    com.Beans.tab[i][2] = Integer.toString(i);
    
	out.print(com.Utilities.tab(com.Beans.tab[i][1], com.Beans.tab.length, i, com.Beans.tab[i][2], com.Beans.tab[i][0], ""));
 		
// THIS WILL BECOME A CASE SELECT OR ( FOR X IN TAB )

// HEAD CONTROL
if (i == 0) {
	out.print(com.Robot_Head.tab);
}
 		
// OPERATING MODE
if (i == 1) {					        
	out.print(com.Control_Mode.tab);
}

   // LIGHTS
if (i == 2) {
	out.print(com.Robot_Lights.tab);
}

// TEXT TO SPEECH
if (i == 3) {
	out.print("<ul class='dropdown-menu well tts' style='-webkit-transform:rotate(" + ((360 / com.Beans.tab.length) * (-i)) + "deg);'>" +
	"<div class='row span4'>" +
	"<input type='text' name='box-speech' class='span3' placeholder='Enter text to speak'>" +
	"<button type='submit' class='icon-play'></button>" +
	"<button type='submit' class='icon-pause'></button>" +
	"<button type='submit' class='icon-stop'></button>" +
	"</div></ul>");
}

// HAND-WRITING
if (i == 4) {
	out.print("<ul class='dropdown-menu well txt' style='-webkit-transform:rotate(" + ((360 / com.Beans.tab.length) * (-i)) + "deg);'>" +
	"<div class='row span4'>" +
	"<input type='text' name='box-writing' class='span3' placeholder='Enter text to write'>" +
	"<button type='submit' class='icon-play'></button>" +
	"<button type='submit' class='icon-pause'></button>" +
	"<button type='submit' class='icon-stop'></button>" +
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
	out.print(com.Power.tab);
}
 		
out.print("</div>");

	}

} %>

<script>
<% out.print(com.Power.script); %>

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
		<button id="toggle" type="submit" name=togglemode value="<% if ("1".equals(toggle)) { out.print("0"); } else { out.print("1"); } %>" class="btn<% if ("1".equals(toggle)) { out.print(" btn-success icon-folder-open"); } else { out.print(" btn-primary icon-folder-close"); } %>"></button>
		<div class="btn-group">
			<button type="submit" name=viewmode value=1 class="btn btn-primary icon-dashboard <% if ("1".equals(view)) { out.print("active"); } %>"></button>
			<button type="submit" name=viewmode value=2 class="btn btn-primary icon-list-alt <% if ("2".equals(view)) { out.print("active"); } %>"></button>
			<button type="submit" name=viewmode value=3 class="btn btn-primary icon-sitemap <% if ("3".equals(view)) { out.print("active"); } %>"></button>
		</div>

	</div>
	
</div>

</form></body></html>
