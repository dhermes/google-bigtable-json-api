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
	    table_service.BigtableTableService
	mv bigtabletableadmin-v1.discovery bigtabletableadmin-v1.discovery.rest
	sed -i 's/{name}\/rename/{name}:rename/g' bigtabletableadmin-v1.discovery.rest
	sed -i 's/columnFamilies\/{name}/{name}/g' bigtabletableadmin-v1.discovery.rest
	mv operations-v1.discovery operations-v1.discovery.rest
	sed -i 's/{name}\/cancel/{name}:cancel/g' operations-v1.discovery.rest
	mv bigtableclusteradmin-v1.discovery bigtableclusteradmin-v1.discovery.rest
	sed -i 's/{name}\/undelete/{name}:undelete/g' bigtableclusteradmin-v1.discovery.rest

.PHONY: generate
