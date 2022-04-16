<?php
$time = time();
$x = 100;
for ($i = 0; $i <= $x; $i++) {
  echo substr(md5($time - $i),0,22);
  echo "\n";
}
?> 