
function isIp(str) {
    // var regex = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    var regex = /^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:[0-9]{1,4})?$/; // xxx.xxx.xxx.xxx[:PORT]
    return regex.test(str);
}

function getBaseDomain(url) {
    if(!url) {
        url = window.location.href;
    }
    url = url.replace("\\", "/");
    var pos = url.indexOf("://");
    if (pos >= 0) {
        url = url.substr(pos + 3);
    }
    var host = url.split("/")[0]; 
    if(isIp(host)) {
        return host; // IP - 127.0.0.1[:8080]
    } else {
        var domain = "";
        var matches = host.match(/(\w+\.\w+)(:[0-9]{1,4})?$/); // DOMAIN URL - g.org[:80] 
        if(!!matches) {
            domain = matches[0];
        }
        return domain;
    }
}

function validURL(url) {
    var strRegex = "^((https|http|file):\/\/)?"
                 + "(((([0-9]|1[0-9]{2}|[1-9][0-9]|2[0-4][0-9]|25[0-5])[.]{1}){3}([0-9]|1[0-9]{2}|[1-9][0-9]|2[0-4][0-9]|25[0-5]))" //IP URL - 199.194.52.184
                 + "|"
                 + "([0-9a-zA-Z\u4E00-\u9FA5\uF900-\uFA2D-]+[.]{1})+[a-zA-Z-]+)" //DOMAIN URL - www.google.com
                 + "(:[0-9]{1,4})?" //PORT - :80
                 + "((/?)|(/[0-9a-z_!~*\'().;?:@&=+$,%#-]+)+/?)$";
    var regex = new RegExp(strRegex);
    // console.log(regex.test(url));
    return regex.test(url);
}
