package web_interface;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;

public class Utilities {
			
	// HTML5 DOCTYPE
	public static final String DOCTYPE = "<!DOCTYPE html>";
	
	// CREATE THE HEAD
	public static String head(String title) {
		return(/*DOCTYPE +*/"<html><head>" +
				"<meta http-equiv='X-UA-Compatible' content='IE=9' />" +
				"<title>" + title + "</title>" +
				"<link rel='stylesheet' type='text/css' href='./css/font-awesome.min.css' />" +
				"<link rel='stylesheet' type='text/css' href='./css/bootstrap.css' />" +
				"<script src='./js/jquery.js'></script>" +
				"<script src='./js/bootstrap.js'></script>" +
				"<script src='./js/bootstrap-button.js'></script>" +
				"</head>");
	}
	
	public static String tab(String icon, int totalTabs, int currentTab, String id, String title, String content) {
		return("<div class='rotate' style='-webkit-transform:rotate(" + ((360 / totalTabs) * currentTab) + "deg);'>" +
				"<div class='tab btn btn-inverse dropdown' id='" + id + "' title='" + title + "' " + 
                		"data-toggle='dropdown'>" +
                		"<i class='" + icon + "'></i></div>");
	}
	
	  /** Read a parameter with the specified name, convert it to an int,
	      and return it. Return the designated default value if the parameter
	      doesn't exist or if it is an illegal integer format.
	  */
	  
	  public static int getIntParameter(HttpServletRequest request, String paramName, int defaultValue) {
	    String paramString = request.getParameter(paramName);
	    int paramValue;
	    try {
	      paramValue = Integer.parseInt(paramString);
	    } catch(NumberFormatException nfe) { // Handles null and bad format
	      paramValue = defaultValue;
	    }
	    return(paramValue);
	  }
	
	  public static String getCookieValue(Cookie[] cookies, String cookieName, String defaultValue) {
	    for(int i=0; i<cookies.length; i++) {
	      Cookie cookie = cookies[i];
	      if (cookieName.equals(cookie.getName()))
	        return(cookie.getValue());
	    }
	    return(defaultValue);
	  }

}