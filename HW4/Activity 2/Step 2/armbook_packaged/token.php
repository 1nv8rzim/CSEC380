<?php
if($_SESSION["token"] !== $_GET["token"]){
		die("Invalid token");
}
?>