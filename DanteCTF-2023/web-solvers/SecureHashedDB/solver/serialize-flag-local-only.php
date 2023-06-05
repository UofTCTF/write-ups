<?php
class MD5DBEngine {
    private $HashString = "";
    private $objArray = array();

    public function __construct($HashString, Visualizer $visualizer) {
        $this->HashString = $HashString;
        $this->objArray['obj'] = $visualizer;
    }
}

class Visualizer {
    private $locationFile = "/srv/app/dbs/hashes.db";
}
$visualizer = new Visualizer();

$obj = new MD5DBEngine("useless", $visualizer);
echo base64_encode(serialize($obj));

?>
