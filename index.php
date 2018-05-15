<?php include_once "header.php"; ?>

    <div class="container" style="margin-top:100px;">
        <div class="row">
            <textarea id="text-input" name="text-input" style="display:none;">
<?php 
$mdname = 'index';
if (isset($_GET['md']) && $_GET['md'] != ''){
    $mdname = $_GET['md'];
}
$mdnamearg = $mdname;
$mdname = str_replace(".html","",$mdname);
$args = explode("_",$mdname);

if (count($args) >= 2){
    $mdname = $args[0].'/'.$mdname;
}
$data = @file_get_contents("./markdown/".$mdname.".md");
if ($data)
    echo $data;
else{
    echo "#Sorry！".$mdnamearg.".html not found！";
}
?>
            </textarea>
            <div id="markdown-preview" class="mkfont"> </div>
            
            
        </div>
    </div>

    <?php include_once "footer.php"; ?>

<?php 
//var_dump($_GET); /
?>
