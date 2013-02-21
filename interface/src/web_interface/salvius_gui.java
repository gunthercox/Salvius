package web_interface;

import java.awt.MouseInfo;
import java.awt.Point;
import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/home")
public class salvius_gui extends HttpServlet {
	private static final long serialVersionUID = 1L;
	
	// CREATE TABS: TITLE | ICON | ID
	public static String[][] tab = {
		{"Head", "icon-eye-open", ""},
	    {"Settings", "icon-cog", ""},
	    {"Lights", "icon-lightbulb", ""},
	    {"Speech", "icon-volume-up", ""},
	    {"Write", "icon-pencil", ""},
	    {"Science", "icon-beaker", ""},
	    {"Signal", "icon-signal", ""},
	    {"Sensor readings", "icon-bar-chart", ""},
	    {"Power", "icon-off", ""}
	    };
    
    public salvius_gui() {
        super();
    }

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		// SPEECH OUTPUT
		//Voice robotVoice = new Voice("kevin16");
		//robotVoice.say("testing 1 2 3");
		
		// GET HEADERS
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        
        out.println(Utilities.head("Interface") +
        		"<body><div class='circle'>");
        
        // CREATE THE PRIMARY TAB RING
        for (int i = 0; i < tab.length; i++) {
        	
        	// GIVE THE TAB AN ID NUMBER
        	tab[i][2] = Integer.toString(i);
        	
    		out.println(Utilities.tab(tab[i][1], tab.length, i, tab[i][2], tab[i][0], ""));
    		
			// THIS WILL BECOME A CASE SELECT
			// OR, --> FOR X IN TAB <--
	
			// HEAD CONTROL
			if (i == 0) {
				// OVERLAY HEAD NAVIGATION ON CAMERA IMAGE
				out.println("<ul class='dropdown-menu' role='menu'>" +
				"<p class='text-center'>Click a point on the view screen to center it.</p></ul>");
			}
    		
			// OPERATING MODE
			if (i == 1) {					        
		        out.println("<ul class='dropdown-menu' role='menu'>" +
		        			"<div class='btn-group btn-group-vertical' data-toggle='buttons-radio'>" +
		        			"<button type='button' class='btn btn-action'>Atonomus</button>" +
		        			"<button type='button' class='btn btn-success'>Assisted</button>" +
		        			"<button type='button' class='btn btn-warning active'>Teleoperated</button>" +
		        			"</div></ul>");
			}

		    // LIGHTS
			if (i == 2) {
		        out.println("<ul class='dropdown-menu' role='menu'>" +
		        			"<div class='btn-group' data-toggle='buttons-checkbox'>" +
		        			"<button type='button' class='btn btn-large btn-danger'>IR</button>" +
		        			"<button type='button' class='btn btn-large btn-inverse'>UV</button>" +
		        			"</div></ul>");
			}
			
			// TEXT TO SPEECH
			if (i == 3) {
				out.println("<ul class='dropdown-menu tts' style='-webkit-transform:rotate(" + ((360 / tab.length) * (-i)) + "deg);'>" +
							"<div class='well well-small'>" +
							"<input type='text' placeholder='Enter text...'>" +
							"</div></ul>");
			}
			
			// HAND-WRITING
			if (i == 4) {
				out.println("<ul class='dropdown-menu txt' style='-webkit-transform:rotate(" + ((360 / tab.length) * (-i)) + "deg);'>" +
							"<div class='well well-small'>" +
							"<input type='text' placeholder='Enter text...'>" +
							"</div></ul>");
			}
			
			// SENSOR READINGS
			if (i == 7) {
				out.println("<ul class='dropdown-menu sensor' style='-webkit-transform:rotate(" + ((360 / tab.length) * (-i)) + "deg);'>" +
							"<table class='table table-striped'>" +
				            "<thead>" +
				            "<tr><th>ID</th><th>Sensor</th><th>Value</th></tr></thead>" +
				            "<tbody>" +
				            "<tr><td>~1</td><td>PIR</td><td>51.5 W</td></tr>" +
				            "<tr><td>~2</td><td>Light</td><td>61.2 Lm</td></tr>" +
				            "<tr><td>A0</td><td>Sound</td><td>0.2 dB</td></tr>" +
				            "</tbody></table></ul>");
			}
			
		    // POWER
			if (i == 8) {
		        out.println("<ul class='dropdown-menu' role='menu'>" +
		        			"<div class='btn-group' data-toggle='buttons-radio'>" +
		        			"<button type='button' class='btn btn-large active'>" +
		        			"<i class='icon-circle'></i></button>" +
		        			"<button type='button' class='btn btn-large'><i class='icon-circle-blank'></i></button>" +
		        			"</div>" +
		        			"<p class='text-center'>Battery: " + "33.05%" + "</p>" +
		        			"</ul>");
			}
    					
    		out.println("</div>");
        	}
        
        // CAMERA FEED & EXPAND-ALL / COLLAPSE-ALL BUTTONS
		out.println("<h2 class='text-center' id='coordinates'>0, 0</h2>" +
					"<img id='camera' src='./img/img.jpg' />" +
	        		"<button class='toggle btn btn-primary icon-folder-close' id='toggle' data-toggle='button'></button>" +
	        		
					"</div>");
		
		out.println("<script>" +
		
					"$('.camera').click(function() {" +
					"return confirm('" + "" + "');" +
					"});" +
					
					"$('.toggle').each(function() {" +
					"$(this).click(function() {" +
					"$(this).toggleClass('btn-success icon-folder-open');" +
					"if ($('.rotate').hasClass('open')) {" +
					"$('.rotate').removeClass('open');" +
					"} else {" +
					"$('.rotate').addClass('open');" +
					"}" +
					"});" +
					"});" +
					
					"$('.tab').click(function() {" +
					"if ($(this).parent('div').hasClass('open')) {" +
					"$(this).parent('div').removeClass('open');" +
					"} else {" +
					"$(this).parent('div').addClass('open');" +
					"}" +
					"});" +
					
					"jQuery(document).ready(function() {" +
					   "$('#camera').click(function(e){" +
					   "$('#coordinates').html(e.pageX +', '+ e.pageY);" +
					   "});" + 
					"});" +
					
					"</script>");
		
        out.println("</body></html>");
        
		// CLOSE STREAM
        out.close();
	}

    public void doPost(HttpServletRequest request, HttpServletResponse response)
    throws IOException, ServletException {
        doGet(request, response);
    }
}
