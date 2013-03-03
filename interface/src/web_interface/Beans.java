package web_interface;

public class Beans {
  
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
}