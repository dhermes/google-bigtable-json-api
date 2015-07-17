from gcloud_bigtable._generated import bigtable_cluster_service_messages_pb2

import generate_python


with open('generated_sample.py', 'wb') as FILE_OBJ:
    generate_python.format_python_file(
        bigtable_cluster_service_messages_pb2.DESCRIPTOR,
        FILE_OBJ, indent_space=4)
