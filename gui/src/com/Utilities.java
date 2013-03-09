package com;

public class Utilities {
			
	private final static String TITLE = "Interface";
	
	// CREATE THE HEAD
	public static String head() {
		return( "<meta http-equiv='X-UA-Compatible' content='IE=9' />" +
				"<title>" + TITLE + "</title>" +
				"<link rel='stylesheet' type='text/css' href='./css/font-awesome.min.css' />" +
				"<link rel='stylesheet' type='text/css' href='./css/bootstrap.css' />" +
				"<script src='./js/jquery.js'></script>");
	}
	
	// TABS
	public static String tab(String state, String icon, int totalTabs, int currentTab, String id, String title, String content) {
		
		String open = "";
		
		if ("1".equals(state)) { 
			
			// SET A VARIABLE
			open = "open";
			
		} else {
			open = "";
		}
		
		return("<div class='rotate " + open + "' style='-webkit-transform:rotate(" + ((360 / totalTabs) * currentTab) + "deg);'>" +
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

}