<?php
$file = "switch.json";
$jsonString = file_get_contents($file);

if (isset($_REQUEST['bname']))
{
    $data = json_decode($jsonString,true);
    $data[$_REQUEST['bname']] = $_REQUEST['bstatus'];
    $newJsonString = json_encode($data);
    file_put_contents('switch.json', $newJsonString);
}
echo $jsonString;

?>
