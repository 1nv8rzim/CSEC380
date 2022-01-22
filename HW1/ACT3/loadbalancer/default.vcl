vcl 4.1;

import directors;

backend web {
    .host = "webserver";
    .port = "80";
}

backend web_alt {
    .host = "webserver_alt";
    .port = "80";
}

sub vcl_init {
    new balancer = directors.round_robin();
    balancer.add_backend(web);
    balancer.add_backend(web_alt);
}

sub vcl_recv {
    set req.backend_hint = balancer.backend();
}