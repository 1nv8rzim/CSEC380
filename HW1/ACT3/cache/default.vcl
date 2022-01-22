vcl 4.1;

backend default {
    .host = "loadbalancer";
    .port = "80";
}