<html>
<head>
    <title>My shop</title>
</head>
<body>
    <h1>La liste des produits disponibles est :</h1>
    <ul>
        <?php
        $json = @file_get_contents('http://product-service:80/');
        if ($json !== false) {
            $obj = json_decode($json);
            $products = $obj->products;

            foreach ($products as $product) {
                echo "<li>$product</li>";
            }
        } else {
            echo "<li>Impossible de contacter le service API.</li>";
        }
        ?>
    </ul>
</body>
</html>
