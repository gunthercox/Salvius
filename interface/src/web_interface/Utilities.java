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
	
	public static String circle() {
		return( "<div id='dot'></div>" +
				"<div class='btn-bar btn-toolbar'>" +
				"<button class='btn btn-primary icon-folder-close' id='toggle' data-toggle='button'></button>" +
				"<div class='btn-group' data-toggle='buttons-radio'>" +
					"<a href='gui?param1=1'>" +
		  			"<button type='button' class='btn btn-primary icon-dashboard active'></button></a>" +
		  			"<a href='gui?param1=2'>" +
		  			"<button type='button' class='btn btn-primary icon-list-alt'></button></a>" +
		  			"<a href='gui?param1=3'>" +
		  			"<button href='http://localhost/interface/ftp' type='button' class='btn btn-primary icon-sitemap'></button></a>" +
				"</div></div></div>");
	}
	
	// CREATE MEDIA BUTTON CONTROLS
	public static String tab(String icon, int totalTabs, int currentTab, String id, String title, String content) {
		return("<div class='rotate' style='-webkit-transform:rotate(" + ((360 / totalTabs) * currentTab) + "deg);'>" +
				"<div class='tab btn btn-inverse dropdown' id='" + id + "' title='" + title + "' " + 
				"data-toggle='dropdown'>" +
				"<i class='" + icon + "'></i></div>");
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
	
	public static String mediaControler() {
		return("<button class='icon-play'></button><button class='icon-pause'></button><button class='icon-stop'></button>");
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