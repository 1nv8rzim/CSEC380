window.onload = () => {
    var pluginArray = navigator.plugins;
    var pluginHTML = "<ul>";;
    
    for (const plugin of pluginArray) {
        pluginHTML += "<li>" + plugin.name + "</li> <br>";
    }
    pluginHTML += "</ul>";
    document.getElementById('plugins').innerHTML = pluginHTML;
}