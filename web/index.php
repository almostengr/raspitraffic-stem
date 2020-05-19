<!DOCTYPE html>
<html>
<head>
<title>RaspiTraffic Control Panel</title>
<meta name="copyright" content="Kenny Robinson, @almostengr" />
<meta name="author" content="Kenny Robinson, @almostengr" />
<meta name="robots" content="noindex,nofollow" />
<meta name="language" content="English" />
<style type="text/css">
body{
	font-family: Arial;
	font-size: 10pt;
}

p#error {
	background-color: #c00;
	color: #fff;
	padding: 5px;
}

p#success {
	background-color: #82FA58;
	color: #000;
	padding: 5px;
}
</style>
</head>
<body>

<h1>RaspiTraffic Control Panel</h1>

<?php
// only peform these actions if the form has been submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST') {

	// get the program to run from the from
	$fileactionpath = "/tmp/traffic.txt";
	$filedisplaypath = "/tmp/traffic_display.txt";
	$pseudofilepath = "/tmp/traffic_pseudo.txt";

	// update the file with program to run
	$fileaction = file_put_contents($fileactionpath, $_POST['action']);
	$now = date("F j, Y, g:i:s a");

	if ($fileaction === FALSE || $filedisplay === FALSE) {
		// throw error if not able to write to the file
		echo "<p id='error'>$now Error when attempting to save the request.</p>";
	}
	else{
		// show success message if able to write to the file
		echo "<p id='success'>$now Submitted request.</p>";
	} // end if else

	if ($_POST['action'] == "pseudocode") {
	// only perform the below if pseudocode option has been selected
		$file2 = file_put_contents($pseudofilepath, $_POST['pseudocode']);
		if ($file2 === FALSE) {
		// display error if not able to open file
			echo "<p id='error'>Error when attempting to open file.</p>";
		}
	} // end if else
}
?>

<form method="post" action="index.php">
<p>
<strong>Select Action</strong><br />
<select name="action">
	<optgroup label="Run Signals">
		<option value="ustraffic" <?php $_POST['action']=="ustraffic" ? print 'selected="selected"' : false; ?>>US Traffic</option>
		<option value="ustrafficflasher" <?php $_POST['action']=="ustrafficflasher" ? print 'selected="selected"' : false; ?>>US Traffic with flasher</option>
		<option value="uktraffic" <?php $_POST['action']=="uktraffic" ? print 'selected="selected"' : false; ?>>UK Traffic</option>
		<option value="uktrafficflasher" <?php $_POST['action']=="uktrafficflasher" ? print 'selected="selected"' : false; ?>>UK Traffic with flasher</option>
		<option value="russiatraffic" <?php $_POST['action']=="russiatraffic" ? print 'selected="selected"' : false; ?>>Russia Traffic</option>
		<option value="russiatrafficflasher" <?php $_POST['action']=="russiatraffic" ? print 'selected="selected"' : false; ?>>Russia Traffic with flasher</option>
	</optgroup>
	<optgroup label="Steady On/Off">
		<option value="all_on" <?php $_POST['action']=="all_on" ? print 'selected="selected"' : false; ?>>All On</option>
		<option value="redon" <?php $_POST['action']=="redon" ? print 'selected="selected"' : false; ?>>Red On</option>
		<option value="redyellowon" <?php $_POST['action']=="redyellowon" ? print 'selected="selected"' : false; ?>>Red/Yellow On</option>
		<option value="yellowon" <?php $_POST['action']=="yellowon" ? print 'selected="selected"' : false; ?>>Yellow On</option>
		<option value="yellowgreenon" <?php $_POST['action']=="yellowgreenon" ? print 'selected="selected"' : false ?>>Yellow/Green On</option>
		<option value="greenon" <?php $_POST['action']=="greenon" ? print 'selected="selected"' : false; ?>>Green On</option>
		<option value="greenredon" <?php $_POST['action']=="greenredon" ? print 'selected="selected"' : false; ?>>Green/Red On</option>
		<option value="all_off" <?php $_POST['action']=="all_off" ? print 'selected="selected"' : false; ?>>All Off</option>
	</optgroup>
	<optgroup label="Games">
		<option value="redlightgreenlight" <?php $_POST['action']=="redlightgreenlight" ? print 'selected="selected"' : false; ?>>Red Light Green Light</option>
		<option value="redlightgreenlight2" <?php $_POST['action']=="redlightgreenlight2" ? print 'selected="selected"' : false; ?>>Red Light Green Light, with Yellow</option>
	</optgroup>
	<optgroup label="Flashers">
		<option value="flashred" <?php $_POST['action']=="flashred" ? print 'selected="selected"' : false; ?>>Flash Red</option>
		<option value="flashyel" <?php $_POST['action']=="flashyel" ? print 'selected="selected"' : false; ?>>Flash Yellow</option>
		<option value="flashgrn" <?php $_POST['action']=="flashgrn" ? print 'selected="selected"' : false; ?>>Flash Green</option>
		<option value="partymode4" <?php $_POST['action']=="partymode4" ? print 'selected="selected"' : false; ?>>Party Mode, Slow</option>
		<option value="partymode" <?php $_POST['action']=="partymode" ? print 'selected="selected"' : false; ?>>Party Mode</option>
		<option value="partymode2" <?php $_POST['action']=="partymode2" ? print 'selected="selected"' : false; ?>>Party Mode, Fast</option>
		<option value="partymode3" <?php $_POST['action']=="partymode3" ? print 'selected="selected"' : false; ?>>Party Mode, Faster</option>
	</optgroup>
	<optgroup label="Other">
		<option value="pseudocode" <?php $_POST['action']=="pseudocode" ? print 'selected="selected"' : false; ?>>Pseudocode</option>
	</optgroup>
	<optgroup label="Raspberry Pi Options">
		<option value="restart" <?php $_POST['action']=="restart" ? print 'selected="selected"' : false; ?>>Restart</option>
		<option value="shutdown" <?php $_POST['action']=="shutdown" ? print 'selected="selected"' : false; ?>>Shut Down</option>
	</optgroup>
</select>
</p>

<strong>Pseudocode Commands</strong><br />
<textarea name="pseudocode" cols="50" rows="4">
<?php $_POST['action']=="pseudocode" ? print $_POST["pseudocode"] : false; ?>
</textarea>
</p>

<p><input type="submit" name="submit" value="Submit" /></p>
</form>

<!-- pseudocode command input box -->
<p>Pseudocode Commands</p>
<ul>
<li><strong>red</strong> Turn on the red light</li>
<li><strong>yellow</strong> Turn on the yellow light</li>
<li><strong>green</strong> Turn on the green light</li>
<li><strong>repeat</strong> Repeat the loop. Has to be last line in the in order to repeat</li>
<li><strong>wait time</strong> Wait before doing the next command. "Time" is the number of seconds to wait</li>
<li><strong>off</strong> Turn off all the lights</li>
</ul>

<!-- FOOTER -- FOOTER -- FOOTER -->
<p style="text-align: center;">
Copyright &copy; 2017-<?php echo date("Y"); ?> @almostengr |
<a href="index.php">Home</a> |
<a href="https://github.com/almostengr/raspitraffic-stem" target="_blank">GitHub Repo</a>
</p>

</body>
</html>

