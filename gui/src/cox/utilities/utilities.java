package cox.utilities;

public class utilities {
			
	private final static String TITLE = "Interface";
	
	// CREATE THE HEAD
	public static String head() {
		return( "<meta http-equiv='X-UA-Compatible' content='IE=9' />" +
				"<title>" + TITLE + "</title>" +
				"<link rel='stylesheet' type='text/css' href='./css/font-awesome.min.css' />" +
				"<link rel='stylesheet' type='text/css' href='./css/bootstrap.css' />" +
				"<link rel='stylesheet' href='css/normalize.css' />" +
				"<link rel='stylesheet' href='css/foundation.css' />" +
				"<script src='js/foundation.min.js'></script>" +
				"<script src='js/foundation/foundation.alerts.js'></script>" +
				"<script src='js/vendor/jquery.js'></script>" +
				"<script src='js/vendor/zepto.js'></script>" +
				"<script src='js/vendor/custom.modernizr.js'></script>");
	}
	
	// CREATE TABS: TITLE | ICON
	public static String[][] tab = {
		{"Head", "icon-eye-open"},
	    {"Settings", "icon-cog"},
	    {"Lights", "icon-lightbulb"},
	    {"Speech", "icon-volume-up"},
	    {"Write", "icon-pencil"},
	    {"Tools", "icon-wrench"},
	    {"Conversation", "icon-globe"},
	    {"Sensor readings", "icon-bar-chart"},
	    {"Power", "icon-off"}
	    };
	
	// ARRAY OF ARDUINO INPUT VALUES
	public static String[][] sensorData = {
		{"ID", "Sensor", "Value"},
		{"~1", "PIR", "51.5 W"},
		{"~2", "Light", "61.2 Lm"},
		{"A0", "Sound", "0.2 dB"}
	};
	
	public static String[] tabular = new String[tab.length];
	
	// TABS
	public static String tab(String master_state, String minor_state, String icon, int totalTabs, int id, String title, String content) {
		
		String open = "";
		
		if ("1".equals(minor_state) || "1".equals(master_state)) { tabular[id] = "0"; open = "open"; } else { tabular[id] = "1"; open = " "; }
		
		return("<div class='rotate " + open + " t" + Integer.toString(id) + "'>" +
				"<button name='tab" + id + "' class='tab btn btn-inverse dropdown' title='" + title + "' " +
				"value='" + tabular[id] + "'" +
				"data-toggle='dropdown'>" +
				"<i class='" + icon + "'></i></button>");
	}
	
	// CREATE TABLE FROM 3D ARRAY
	public static String table(String data[][]) {
		StringBuffer sb = new StringBuffer();
		
		// CREATE TABLE HEAD
		sb.append("<table class='table table-striped'><thead><tr>");
		for (int i = 0; i < data[0].length; i++) {
			sb.append("<th>" + data[0][i] + "</th>");
		}
		sb.append("</tr></thead>");
		
		// CREATE TABLE BODY
		sb.append("<tbody>");
		for (int j = 1; j < data.length; j++) {

			sb.append("<tr>");
			
			for (int k = 0; k < data[j].length; k++) {
				sb.append("<td>" + data[j][k] + "</td>");
			}

			sb.append("</tr>");
			
		}
		
		sb.append("</tbody></table>");
		
		return sb.toString();	
	}

}
