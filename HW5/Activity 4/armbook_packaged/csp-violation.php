<?php 
include_once("common.php");
$contents = file_get_contents('php://input');
if($stmt = $mysqli->prepare("INSERT INTO csp (violation) VALUES (?)")){
    if($stmt->bind_param("s",$contents)){
        if(!$stmt->execute()){
            die("Error - Issue executing prepared statement: " . mysqli_error($mysqli));
        }
    }else{
            die("Error - Issue binding prepared statement: " . mysqli_error($mysqli));
       }
    if($stmt->close()){
            
    }else{
            die("Error - Failed to close prepared statement" . mysqli_error($mysqli));
    }

}else{
    die("Error - Issue preparing statement: " . mysqli_error($mysqli));
}
?>