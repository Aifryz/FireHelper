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

  /* create encoded polyline from the points */
  require_once('PolylineEncoder.php');
  $PolyEnc   = new PolylineEncoder($points);
  $EncString = $PolyEnc->dpEncode();
  return $EncString['Points'];

}
/* set some options */
$MapLat    = $_GET["lat"]; // latitude for map and circle center
$MapLng    = $_GET["lng"]; // longitude as above
$MapRadius = 0.36;         // the radius of our circle (in Kilometres)
$MapFill   = 'E85F0E';    // fill colour of our circle
$MapBorder = '91A93A';    // border colour of our circle
$MapWidth  = 640;         // map image width (max 640px)
$MapHeight = 480;         // map image heigt (max 640px)
$m1 =  $_GET["mark1"]; 
$m2 =  $_GET["mark2"];
$m3 =  $_GET["mark3"]; 
$x  = $_GET['x'];
$y  = $_GET['y'];
$p = 0;
$EncString3 = array();
foreach ($x as &$value)
{
    $EncString3[p] = GMapCircle($x[p], $y[p], $MapRadius);
    $p = p + 1;
}
$url;
for ($i = 0; $i < $p; $i++)
{
    $url += '&path=fillcolor:0x'.$MapFill.'33%7Ccolor:0x'.$MapBorder.'00%7Cenc:'.$EncString3[i];
}

$EncString2 = GMapCircle($x[1], $y[1], $MapRadius);
$EncString = GMapCircle($MapLat,$MapLng, $MapRadius);
$MapAPI = 'http://maps.google.com.au/maps/api/staticmap?';
$MapURL = $MapAPI.'center='.$MapLat.','.$MapLng.'&size='.$MapWidth.'x'.$MapHeight.'&maptype=roadmap&path=fillcolor:0x'.$MapFill.'33%7Ccolor:0x'.$MapBorder.'00%7Cenc:'.$EncString.'&sensor=false&zoom=13&markers='.$m1.','.$m2.$m3.$url;
echo $MapURL;?>

