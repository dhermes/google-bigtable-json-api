GOOGLE_CLOUD_SDK=$(HOME)/google-cloud-sdk

help:
	@echo 'Makefile for a google-bigtable-json-api         '
	@echo '                                                '
	@echo '   make generate   Generates REST discovery doc.'

generate:
	$(GOOGLE_CLOUD_SDK)/platform/google_appengine/endpointscfg.py \
	    get_discovery_doc --format rest \
	    operations_service.Operations \
	    cluster_service.BigtableClusterService \
	    data_service.BigtableService \
	    table_service.BigtableTableService
	mv bigtabletableadmin-v1.discovery bigtabletableadmin-v1.discovery.rest
	sed -i 's/{name}\/rename/{name}:rename/g' bigtabletableadmin-v1.discovery.rest
	sed -i 's/columnFamilies\/{name}/{name}/g' bigtabletableadmin-v1.discovery.rest
	mv operations-v1.discovery operations-v1.discovery.rest
	sed -i 's/{name}\/cancel/{name}:cancel/g' operations-v1.discovery.rest
	mv bigtableclusteradmin-v1.discovery bigtableclusteradmin-v1.discovery.rest
	sed -i 's/{name}\/undelete/{name}:undelete/g' bigtableclusteradmin-v1.discovery.rest
	mv bigtable-v1.discovery bigtable-v1.discovery.rest
	sed -i 's/{table_name}\/rows\/read/{table_name}\/rows:read/g' bigtable-v1.discovery.rest
	sed -i 's/{table_name}\/rows\/sampleKeys/{table_name}\/rows:sampleKeys/g' bigtable-v1.discovery.rest
	sed -i 's/{table_name}\/rows\/{row_key}\/mutate/{table_name}\/rows\/{row_key}:mutate/g' bigtable-v1.discovery.rest
	sed -i 's/{table_name}\/rows\/{row_key}\/checkAndMutate/{table_name}\/rows\/{row_key}:checkAndMutate/g' bigtable-v1.discovery.rest
	sed -i 's/{table_name}\/rows\/{row_key}\/readModifyWrite/{table_name}\/rows\/{row_key}:readModifyWrite/g' bigtable-v1.discovery.rest

.PHONY: generate help
