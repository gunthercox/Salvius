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
	
	// CREATE TABS: TITLE | ICON | ID
	public static String[][] tab = {
		{"Head", "icon-eye-open", ""},
	    {"Settings", "icon-cog", ""},
	    {"Lights", "icon-lightbulb", ""},
	    {"Speech", "icon-volume-up", ""},
	    {"Write", "icon-pencil", ""},
	    {"Tools", "icon-wrench", ""},
	    {"Conversation", "icon-globe", ""},
	    {"Sensor readings", "icon-bar-chart", ""},
	    {"Power", "icon-off", ""}
	    };
    
	// ARRAY OF ARDUINO INPUT VALUES
	public static String[][] sensorData = {
		{"ID", "Sensor", "Value"},
		{"~1", "PIR", "51.5 W"},
		{"~2", "Light", "61.2 Lm"},
		{"A0", "Sound", "0.2 dB"}
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
				out.println(Robot_Head.tab);
			}
    		
			// OPERATING MODE
			if (i == 1) {					        
		        out.println(Control_Mode.tab);
			}

		    // LIGHTS
			if (i == 2) {
		        out.println(Robot_Lights.tab);
			}
			
			// TEXT TO SPEECH
			if (i == 3) {
				out.println("<ul class='dropdown-menu well tts' style='-webkit-transform:rotate(" + ((360 / tab.length) * (-i)) + "deg);'>" +
							"<div class='row'></div><div class='row span4'>" +
							"<input type='text' class='span3' placeholder='Enter text to speak'>");
				out.println(Utilities.mediaControler());
				out.println("</div></ul>");
			}
			
			// HAND-WRITING
			if (i == 4) {
				out.println("<ul class='dropdown-menu well txt' style='-webkit-transform:rotate(" + ((360 / tab.length) * (-i)) + "deg);'>" +
							"<div class='row span4'>" +
							"<input type='text' class='span3' placeholder='Enter text to write'>");
				out.println(Utilities.mediaControler());
				out.println("</div></ul>");
			}
			
			// SENSOR READINGS
			if (i == 7) {
				out.println("<ul class='dropdown-menu sensor' style='-webkit-transform:rotate(" + ((360 / tab.length) * (-i)) + "deg);'>");
				out.println(Utilities.table(sensorData));
				out.println("</ul>");
			}
			
		    // POWER
			if (i == 8) {
		        out.println(Power.tab);
			}
    					
    		out.println("</div>");
        	}
        
        // CAMERA FEED & EXPAND-ALL / COLLAPSE-ALL BUTTONS
		out.println("<img id='camera' src='./img/img.jpg' />" +
					"<div id='dot'></div>" +
					"<button class='toggle btn btn-primary icon-folder-close' id='toggle' data-toggle='button'></button>" +
					"</div>");
		
		out.println("<script>");
		
		out.println(Power.script);
					
		out.println("$('#camera').click(function(e) {" +
					"if ($('.rotate').hasClass('open')) {" +
					"$('#dot').addClass('dot icon-screenshot');" +
					"$('.dot').css({'top':e.pageY, 'left':e.pageX});" +
					"} else {" +
					"$('#dot').removeClass('dot icon-screenshot');" +
					"}" +
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
