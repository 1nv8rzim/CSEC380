<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]>      <html class="no-js"> <!--<![endif]-->
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>HW 4 | Act 1 | Step 2</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Matomo -->
        <script>
        var _paq = window._paq = window._paq || [];
        /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
        _paq.push(['trackPageView']);
        _paq.push(['enableLinkTracking']);
        (function() {
            var u="//arch.student.rit.edu:8080/";
            _paq.push(['setTrackerUrl', u+'matomo.php']);
            _paq.push(['setSiteId', '1']);
            var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
            g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
        })();
        </script>
        <!-- End Matomo Code -->
    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="browsehappy">You are using an <strong>outdated</strong> browser. Please <a href="#">upgrade your browser</a> to improve your experience.</p>
        <![endif]-->
        <h1>
            Welcome to Max Fusco's Web HW 4, Act 1, Step 2
        </h1>

        <h2>
            Your Information:
        </h2>
        <?php
            if(isset($_SERVER['HTTP_REFERER'])){
                echo "Referer: " . $_SERVER['HTTP_REFERER'] . "<br>";
            } else {
                echo "Referer: no refer found <br>";
            }
            echo "IP: " . $_SERVER['REMOTE_ADDR'] . "<br>";
            echo "User Agent: " . $_SERVER['HTTP_USER_AGENT'] . "<br>";
        ?>

        <h3>
            Plugins
        </h3>

        <div id="plugins"></div>

        <script src="plugins.js" async defer></script>
    </body>
</html>