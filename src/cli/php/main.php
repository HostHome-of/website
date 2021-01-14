<?php
$args = $_SERVER["argv"];
function empezar($verbose) {
    if ($verbose) {
        echo "con verbose\n";
    }
    echo "empezando";
}

function ayuda() {
    echo "ayuda";
}

if (count($args) > 1) {
    if (count($args) == 3) {
        if ($args[1] == "empezar") {
            if ($args[2] == "-v" or $args[2] == "--verbose") {
                empezar(true);
                exit();
            } else {
                echo "Argumento invalido :: ". $args[2] ." :: Porfavor pon \"php hothome -h\"";
            }
        }
    } else if ($args[1] == "empezar") {
        empezar(false);
        exit();
    } else if ($args[1] == "-h" or $args[1] == "--help") {
        ayuda();
        exit();
    } else {
        echo "Porfavor mete un argumento.\nPuedes poner :: php hosthome -h";
        exit();
    }
} else {
    echo "Porfavor mete un argumento.\nPuedes poner :: php hosthome -h";
    exit();
}
