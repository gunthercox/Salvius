package web_interface;

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
	
	// CREATE TABS: TITLE | ICON | ID | HTML
	public static String[][] tab = {
		{"Head", "icon-move", "X" , ""},
	    {"Settings", "icon-cog", "X", ""},
	    {"Lights", "icon-lightbulb", "X", ""},
	    {"Speech", "icon-volume-up", "X", ""},
	    {"Write", "icon-pencil", "X", ""},
	    {"Science", "icon-beaker", "X", ""},
	    {"Eye", "icon-eye-open", "X", ""},
	    {"Something", "icon-book", "X", ""},
	    {"Mode", "icon-off", "X", ""}
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
        
        out.println("<html><head><meta http-equiv='X-UA-Compatible' content='IE=9' /><title>Interface</title></head>" +
				"<link rel='stylesheet' type='text/css' href='./css/gui.css' />" +
        		"<link rel='stylesheet' type='text/css' href='./css/font-awesome.min.css' />" +
        		"<link rel='stylesheet' type='text/css' href='./css/bootstrap.css' />" +
        		"<body>"+        		
        		"<div class='circle'>");
        
        for (int i = 0; i < tab.length; i++) {
        	
        	// GIVE THE TAB AN ID NUMBER
        	tab[i][2] = Integer.toString(i);
        	
        	//To keep URLs intact, use the data-target attribute instead of href="#".
        	
        	// CREATE THE PRIMARY TAB RING
    		out.println("<div class='rotate' style='-webkit-transform:rotate(" + ((360 / tab.length) * i) + "deg);'>" +
                		"<div class='tab btn dropdown' id='" + tab[i][2] + "' title='" + tab[i][0] + "' " + 
                		"data-toggle='dropdown'>" +
                		"<i class='" + tab[i][1] + "'></i></div>" +
                		"<ul class='dropdown-menu' role='menu' aria-labelledby='dLabel'>");
    		
					    // LIGHTS
						if (i == 2) {
					        out.println("<div class='btn-group' data-toggle='buttons-checkbox'>" +
					        			"<button type='button' class='btn btn-danger'>IR</button>" +
					        			"<button type='button' class='btn btn-inverse'>UV</button>" +
					        			"</div>");
						}
    					
    					// OPERATING MODE
						if (i == 1) {					        
					        out.println("<div class='btn-group btn-group-vertical' data-toggle='buttons-radio'>" +
					        			"<button type='button' class='btn btn-action'>Atonomus</button>" +
					        			"<button type='button' class='btn btn-success'>Assisted</button>" +
					        			"<button type='button' class='btn btn-warning'>Teleoperated</button>" +
					        			"</div>");
    					}
    					
    		out.println("</ul>" +
                		"</div>");
        	}
        
        // CAMERA CIRCLE & EXPAND-ALL / COLLAPSE-ALL BUTTONS
		out.println("<div class='camera'></div>" +
	        		"<button class='toggle btn btn-danger icon-plus' id='toggle'></button>" +
	        		
					"</div>");
		
		out.println("<script src='./js/jquery.js'></script>" +
					"<script src='./js/bootstrap.js'></script>" +
					"<script src='./js/bootstrap-button.js'></script>");
		
		out.println("<script>" +
					
					"$('.toggle').each(function() {" +
					"$(this).click(function() {" +
					"$(this).toggleClass('btn-danger icon-minus', 'btn-success icon-plus');" +
					"if ($('.rotate').hasClass('open')) {" +
					"$('.rotate').removeClass('open');" +
					"}" +
					"else {" +
					"$('.rotate').addClass('open');" +
					"}" +
					"});" +
					"});" +
					
					"$(document).ready(function() {" +
					"});" +
					
					"</script>");
		
        out.println("</body></html>");
			
	}

    public void doPost(HttpServletRequest request, HttpServletResponse response)
    throws IOException, ServletException {
        doGet(request, response);
    }
}
