<?php
header('Refresh: .001');
?>

<html>
<head>
<cfheader name="cache-control" value="no-cache, no-store, must-revalidate">
<cfheader name="pragma" value="no-cache">
<cfheader name="expires" value="#getHttpTimeString(now())#">
<meta http-equiv="cache-control" content="no-cache">
<meta http-equiv="expires" content="<cfoutput>#getHttpTimeString(now())#</cfoutput>">
<meta http-equiv="pragma" content="no-cache">
<script language="JavaScript">
<!--

var sURL = unescape(window.location.pathname);

function doLoad()
{
    // the timeout value should be the same as in the "refresh" meta-tag
    setTimeout( "refresh()", 1000 );
}

function refresh()
{
    //  This version of the refresh function will cause a new
    //  entry in the visitor's history.  It is provided for
    //  those browsers that only support JavaScript 1.0.
    //
    window.location.href = sURL;
}
//-->
</script>

<script language="JavaScript1.1">
<!--
function refresh()
{
    //  This version does NOT cause an entry in the browser's
    //  page view history.  Most browsers will always retrieve
    //  the document from the web-server whether it is already
    //  in the browsers page-cache or not.
    //
    window.location.replace( sURL );
}
//-->
</script>

<script language="JavaScript1.2">
<!--
function refresh()
{
    //  This version of the refresh function will be invoked
    //  in browsers that support JavaScript version 1.2
    //  The argument to the location.reload function determines
    //  if the browser should retrieve the document from the
    //  web-server.  We need to cause the JavaScript block in
    //  the document body to be re-evaluated.
    //  If we needed to pull the document from the web-server
    //  again (such as where the document contents change
    //  dynamically) we would pass the argument as 'true'.
    //  
    window.location.reload( false );
}
//-->
</script>
</head>

<!-- Use the "onload" event to start the refresh process -->
</head>
<body onload="doLoad()">
<img id="refreshThis" src="../images/cam1.jpg" width="100" height="100"/><br />
<img id="refreshThis" src="../images/cam2.jpg" width="100" height="100"/>
</body>
</html>

