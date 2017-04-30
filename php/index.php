<?php
function GMapCircle($Lat,$Lng,$Rad,$Detail=8)
{
  $R    = 6371;
  $pi   = pi();
  $Lat  = ($Lat * $pi) / 180;
  $Lng  = ($Lng * $pi) / 180;
  $d    = $Rad / $R;
  $points = array();
  $i = 0;
  for($i = 0; $i <= 360; $i+=$Detail):
    $brng = $i * $pi / 180;
    $pLat = asin(sin($Lat)*cos($d) + cos($Lat)*sin($d)*cos($brng));
    $pLng = (($Lng + atan2(sin($brng)*sin($d)*cos($Lat), cos($d)-sin($Lat)*sin($pLat))) * 180) / $pi;
    $pLat = ($pLat * 180) /$pi;
    $points[] = array($pLat,$pLng);
  endfor;

  require_once('PolylineEncoder.php');
  $PolyEnc   = new PolylineEncoder($points);
  $EncString = $PolyEnc->dpEncode();
  return $EncString['Points'];

}

$MapLat    = $_GET["lat"];
$MapLng    = $_GET["lng"]; 
$MapRadius = 0.36;      
$MapFill   = 'E85F0E';  
$MapBorder = '91A93A';    
$MapWidth  = 640;         
$MapHeight = 480;         
$m1 =  $_GET["mark1"]; 
$m2 =  $_GET["mark2"];
$m3 =  $_GET["mark3"]; 
$x  = $_GET['x'];
$y  = $_GET['y'];
$EncString3 = array();
$c = 0;
foreach($x as $value)
{
    $EncString3[$c] = GMapCircle($x[$c], $y[$c], $MapRadius);
    $c = $c + 1;
}
$url = '';

for ($i = 0; $i <$c; $i++)
{
    $url .= '&path=fillcolor:0x'.$MapFill.'33%7Ccolor:0x'.$MapBorder.'00%7Cenc:'.$EncString3[$i];
}

$EncString = GMapCircle($MapLat,$MapLng, $MapRadius);
$MapAPI = 'http://maps.google.com.au/maps/api/staticmap?';
$MapURL = $MapAPI.'center='.$MapLat.','.$MapLng.'&size='.$MapWidth.'x'.$MapHeight.'&maptype=roadmap&path=fillcolor:0x'.$MapFill.'33%7Ccolor:0x'.$MapBorder.'00%7Cenc:'.$EncString.'&sensor=false&zoom=13&markers='.$m1.','.$m2.$m3.$url;
echo $MapURL;?>
