<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1"%>
<%@ page import="java.io.File" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<% out.print(web_interface.Utilities.head()); %>
</head>
<body><form method="post" action="">

<%-- DIRECTORY PATH AND LISTING VARIABLES --%>
<% String path = "."; File folder = new File(path); File[] listOfFiles = folder.listFiles(); %>

<%-- SESSION VARIABLES --%>
<% String view = request.getParameter( "viewmode" ); session.setAttribute( "view", view ); %>
<% String toggle = request.getParameter( "togglemode" ); session.setAttribute( "toggle", toggle ); %>

<%-- INITIALIZE SESSION VARIABLES IF NULL OR NECESSARY --%>
<% int tog = 0;
try {
	
	// TRY TO CONVERT THE TOGGLE STRING TO AN INTEGER
	tog = Integer.parseInt(toggle);
	
  } catch (NumberFormatException e) {
	  
	// IF TOGGLE STRING IS NULL SET IT TO ZERO
    tog = 0;
} %>

<% int val = 0;
try {
	
	// TRY TO CONVERT THE VIEW STRING TO AN INTEGER
	val = Integer.parseInt(view);
	
  } catch (NumberFormatException e) {
	  
	// IF VIEW STRING IS NULL SET IT TO ZERO
    val = 0;
} %>

<%-- SESSION VARIABLE OUTPUT --%>
view: <%= session.getAttribute( "view" ) %><br />
toggle: <%= session.getAttribute( "toggle" ) %><br />

<div class='circle' id='camera'>

<%-- SELECT LAYOUT BASED ON SESSION VARIABLE --%>
<% if (val == 3) {
    	
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
} else if (val == 2) {
	
	// CURRENTLY NO ACTION
	
// APPS VIEW
} else {
     
// CREATE THE PRIMARY TAB RING
for (int i = 0; i < web_interface.Beans.tab.length; i++) {
     	
	// GIVE THE TAB AN ID NUMBER
    web_interface.Beans.tab[i][2] = Integer.toString(i);
    
	out.print(web_interface.Utilities.tab(web_interface.Beans.tab[i][1], web_interface.Beans.tab.length, i, web_interface.Beans.tab[i][2], web_interface.Beans.tab[i][0], ""));
 		
// THIS WILL BECOME A CASE SELECT OR ( FOR X IN TAB )

// HEAD CONTROL
if (i == 0) {
	out.print(web_interface.Robot_Head.tab);
}
 		
// OPERATING MODE
if (i == 1) {					        
	out.print(web_interface.Control_Mode.tab);
}

   // LIGHTS
if (i == 2) {
	out.print(web_interface.Robot_Lights.tab);
}

// TEXT TO SPEECH
if (i == 3) {
	out.print("<ul class='dropdown-menu well tts' style='-webkit-transform:rotate(" + ((360 / web_interface.Beans.tab.length) * (-i)) + "deg);'>" +
	"<div class='row span4'>" +
	"<input type='text' name='box-speech' class='span3' placeholder='Enter text to speak'>" +
	"<button type='submit' class='icon-play'></button>" +
	"<button type='submit' class='icon-pause'></button>" +
	"<button type='submit' class='icon-stop'></button>" +
	"</div></ul>");
}

// HAND-WRITING
if (i == 4) {
	out.print("<ul class='dropdown-menu well txt' style='-webkit-transform:rotate(" + ((360 / web_interface.Beans.tab.length) * (-i)) + "deg);'>" +
	"<div class='row span4'>" +
	"<input type='text' name='box-writing' class='span3' placeholder='Enter text to write'>" +
	"<button type='submit' class='icon-play'></button>" +
	"<button type='submit' class='icon-pause'></button>" +
	"<button type='submit' class='icon-stop'></button>" +
	"</div></ul>");
}

// SENSOR READINGS
if (i == 7) {
	out.print("<ul class='dropdown-menu sensor' style='-webkit-transform:rotate(" + ((360 / web_interface.Beans.tab.length) * (-i)) + "deg);'>");
	out.print(web_interface.Utilities.table(web_interface.Beans.sensorData));
	out.print("</ul>");
}

   // POWER
if (i == 8) {
	out.print(web_interface.Power.tab);
}
 		
out.print("</div>");
	}
}
      
%>

<script>
<% out.print(web_interface.Power.script); %>

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
		<button id="toggle" type="submit" name=togglemode value="<% if (tog == 0) { out.print("1"); } else { out.print("0"); } %>" class="btn<% if (tog == 0) { out.print(" btn-success icon-folder-open"); } else { out.print(" btn-primary icon-folder-close"); } %>"></button>
		<div class="btn-group">
			<button type="submit" name=viewmode value=1 class="btn btn-primary icon-dashboard <% if (val == 1) { out.print("active"); } %>"></button>
			<button type="submit" name=viewmode value=2 class="btn btn-primary icon-list-alt <% if (val == 2) { out.print("active"); } %>"></button>
			<button type="submit" name=viewmode value=3 class="btn btn-primary icon-sitemap <% if (val == 3) { out.print("active"); } %>"></button>
		</div>

	</div>
	
</div>

</form></body></html>
