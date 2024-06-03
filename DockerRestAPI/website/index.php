<html>
    <head>
        <title>CIS 322 REST-api demo: Control times</title>
    </head>

    <body>
        <h1>Control Times</h1>
        
        <h2>All Control Times</h2>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/listAll/json');
            $controls = json_decode($json);
            foreach ($controls as $control) {
                echo "<li>KM: $control->km, MI: $control->mi, Location: $control->location, Open: $control->open, Close: $control->close</li>";
            }
            ?>
        </ul>
        
        <h2>Open Times Only</h2>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/listOpenOnly/json');
            $controls = json_decode($json);
            foreach ($controls as $control) {
                echo "<li>KM: $control->km, Open: $control->open</li>";
            }
            ?>
        </ul>
        
        <h2>Close Times Only</h2>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/listCloseOnly/json');
            $controls = json_decode($json);
            foreach ($controls as $control) {
                echo "<li>KM: $control->km, Close: $control->close</li>";
            }
            ?>
        </ul>
    </body>
</html>
