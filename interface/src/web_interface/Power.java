package web_interface;

public class Power {

	// TAB CONTENT HTML
	public static String tab = "<ul class='dropdown-menu' role='menu'>" +
								"<div class='btn-group' data-toggle='buttons-radio'>" +
								"<button type='button' class='btn btn-large active'>" +
								"<i class='icon-circle'></i></button>" +
								"<button type='button' id='off' class='btn btn-large'><i class='icon-circle-blank'></i></button>" +
								"</div>" +
								"<p class='text-center'>Battery: " + "33.05%" + "</p>" +
								"</ul>";

	// TAB EVENT JQUERY
	public static String script = "$('#off').click(function() {" +
								"return confirm('Are you sure you want to deactivate the robot?');" +
								"});";
	
}
