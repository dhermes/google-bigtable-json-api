help:
	@echo 'Makefile for a google-bigtable-json-api         '
	@echo '                                                '
	@echo '   make generate   Generates REST discovery doc.'

generate:
	$(HOME)/google-cloud-sdk/platform/google_appengine/endpointscfg.py \
	    get_discovery_doc --format rest \
	    table_service.BigtableTableService
	mv bigtabletableadmin-v1.discovery bigtabletableadmin-v1.discovery.rest
	sed -i 's/{name}\/rename/{name}:rename/g' bigtabletableadmin-v1.discovery.rest
	sed -i 's/columnFamilies\/{name}/{name}/g' bigtabletableadmin-v1.discovery.rest

.PHONY: generate
