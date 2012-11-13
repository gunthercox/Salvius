<!-- CLI CODE FROM http://sourceforge.net/p/olshell/code/4/tree/ -->
 <h2>CLI</h2>
		<form onload="init()" name="shell" onsubmit="return formSubmit();">
		<div id="container"> 
		<div id="top"></div>
		<div id="bottom">
		<div id="prompt"></div>
		<input id="promptinput" name="command" type="text" size='50' onkeyup="key(event)" tabindex="1">
		</div>
		</div> 
		</form>
        </div>
		</div>

<script type="text/javascript" language="JavaScript">
		var current_line = 0;
		var command_hist = new Array();
		var last = 0;
		
		var the_cwd;
		var the_prompt;
		var color = 'linux';
	
		function key(e) {
			if (!e) var e = window.event;
		
			if (e.keyCode == 38 && current_line < command_hist.length) {
				if (current_line == 0) {
					command_hist.unshift(document.shell.command.value);
					current_line++;
				}
				document.shell.command.value = command_hist[current_line];
				current_line++;
			}
			
			if (e.keyCode == 40 && current_line > 0) {
				current_line--;
				document.shell.command.value = command_hist[current_line];
			}
		}
		
		function init() {
			document.shell.setAttribute("autocomplete", "off");
			document.shell.command.focus();
			
			<?php 
				echo "the_cwd = '".getcwd()."';";
				
				$user=shell_exec("whoami");
				$host=explode(".", shell_exec("uname -n"));
				echo "the_prompt = '"."".rtrim($user).""."@"."".rtrim($host[0])."';";
			?>
			document.getElementById("prompt").innerHTML = the_prompt + ":" + the_cwd + "> ";
		}

		//---------------- AJAX stuff start ---------------------------
		function createRequestObject() {
			var ro;
			var browser = navigator.appName;
			if(browser == "Microsoft Internet Explorer"){
				ro = new ActiveXObject("Microsoft.XMLHTTP");
			}else{
				ro = new XMLHttpRequest();
			}
			return ro;
		}
		
		var http = createRequestObject();
		
		function sendRequest(option, command) {
			http.open('get', 'rpc.php?option=' + option + '&command=' + command + '&cwd=' + the_cwd);
			http.onreadystatechange = handleResponse;
			http.send(null);
		}
		
		function handleResponse() {
			if(http.readyState == 4){
				var response = http.responseText;
				var update = new Array();
		
				if(response.indexOf('|' != -1)) {
					update = response.split('|');
					switch (update[0]) {
						case 'command':
							if (update[2]) { //cwd (only if changed)
								the_cwd = update[2];
							}
							document.getElementById("top").innerHTML += "<pre>" + update[1] + "</pre>";
							document.getElementById("prompt").innerHTML = the_prompt + ":" + the_cwd + "> ";
							document.shell.command.value = "";
							document.shell.command.focus();
							document.shell.command.select();
							break;
						case 'prompt':
							the_prompt = update[1];
							break;		 
					}
				}
			}
		}
		
		function formSubmit () {
			document.getElementById("top").innerHTML += the_prompt + ":" + the_cwd + "> ";
			document.getElementById("top").innerHTML += document.shell.command.value;
			command_hist.unshift(document.shell.command.value);
			sendRequest('command', document.shell.command.value); 
			
			return false;
		}
		//---------------- AJAX stuff end ---------------------------
		
	</script>