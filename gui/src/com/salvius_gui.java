package com;

import java.io.IOException;

import javax.servlet.ServletContext;
import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/servlet")
public class salvius_gui extends HttpServlet {
	private static final long serialVersionUID = 1L;
	
    public salvius_gui() {
        super();
    }

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		/* You can save variables in ServletContext by using setAttribute method.
		 * Also, you can get the actual value by using getAttribute. */
        ServletContext servletContext = getServletContext();
        Object someAttribute = servletContext.getAttribute("someAttribute");
        System.out.println("someAttribute: " + someAttribute);
        
        servletContext.setAttribute("someAttribute", "Hello world!");
	}

    public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        doGet(request, response);
    }
    
    /* you can use a Listener to ServletContext, so you can execute some code when the
     * application starts (is deployed correctly) to initialize the attributes on the
     * ServletContext) and when it finish (before its undeployed). */
    public final class MyAppListener implements ServletContextListener {
        public void contextInitialized(ServletContextEvent event) {
            System.out.println("Application gets started.");
            ServletContext servletContext = event.getServletContext();
            servletContext.setAttribute("someAttribute", "Hello world!");
        }

        public void contextDestroyed(ServletContextEvent event) {
            System.out.println("Application has finished.");
        }
    }
}
