package web_interface;

import java.io.IOException;
import java.io.File;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class salvius_directories
 */
@WebServlet("/ftp")
public class salvius_directories extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public salvius_directories() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		// PREVENT PAGE FROM BEING CACHED
		response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
		response.setHeader("Pragma", "no-cache");
		response.setDateHeader("Expires", 0);
		
		// ROOT DIRECTORY PATH
		String path = ".";
		
		File folder = new File(path);
		File[] listOfFiles = folder.listFiles();
		
		// GET HEADERS
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        
        out.print(Utilities.head("Interface") +
        		"<body><div class='circle'>");
		

		 
		for (int i = 0; i < listOfFiles.length; i++) {
			
			out.print("<div class='rotate' style='-webkit-transform:rotate(" + ((360 / listOfFiles.length) * i) + "deg);'>");
			
			// ITEM IS FILE
			if (listOfFiles[i].isFile()) {
				out.print("<div class='dir btn btn-inverse dropdown' id='" + i + "' data-toggle='dropdown'>" +
						"<i class='icon-file'></i><br />" + listOfFiles[i].getName() + "</div>");
			} 
			
			// ITEM IS FOLDER
			else {
				out.print("<div class='dir tab btn btn-inverse dropdown' id='" + i + "data-toggle='dropdown'>" +
						"<i class='icon-folder-close-alt'></i><br />" + listOfFiles[i].getName() + "</div>");
			}
			
			out.print("</div>");
		}
		
        // CAMERA FEED & EXPAND-ALL / COLLAPSE-ALL BUTTONS
		out.print("<img id='camera' src='./img/img.jpg' />" +
				"<div id='dot'></div>" +
				"<div class='btn-bar btn-toolbar'>" +
				"<button class='btn btn-primary icon-folder-close' id='toggle' data-toggle='button'></button>" +
				"<div class='btn-group' data-toggle='buttons-radio'>" +
		  			"<button type='button' class='btn btn-primary active'>GUI</button>" +
		  			"<button type='button' class='btn btn-primary'>CLI</button>" +
		  			"<button href='http://localhost/interface/ftp' type='button' class='btn btn-primary'>FTP</button>" +
				"</div></div></div>");
		
		out.print("</div></body></html>");
	}


	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
	}

}
