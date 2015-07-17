# Google BigTable API - JSON Interface

This project will take the `.proto` definitions for the
three BigTable services and convert them to `protorpc`
message classes.

After doing so, will use these message classes to
define a [Google Cloud Endpoints][1] service, which will in
turn generate a REST discovery document for the APIs.

[1]: https://cloud.google.com/appengine/docs/python/endpoints/
