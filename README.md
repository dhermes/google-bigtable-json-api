# Google BigTable API - JSON Interface

This project will take the `.proto` definitions for the
three BigTable services and convert them to `protorpc`
message classes.

After doing so, will use these message classes to
define a [Google Cloud Endpoints][1] service, which will in
turn generate a REST discovery document for the APIs.

We use a modified version of [`protorpc.generate_python`] to
generate files from `google.protobuf.descriptor.FileDescriptor`
objects.

[1]: https://cloud.google.com/appengine/docs/python/endpoints/
[2]: https://github.com/google/protorpc/blob/master/protorpc/generate_python.py
