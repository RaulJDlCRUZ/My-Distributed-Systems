#!/usr/bin/make -f

NUM_FILEMANAGERS ?= 1
FILE ?= example.png
FILE_HASH ?= $(shell md5sum $(FILE) | cut -d' ' -f1)


start:
	$(MAKE) run-icestorm & $(MAKE) run-registry &
	sleep 1
	$(MAKE) run-filemanager &
	sleep 1
	$(MAKE) run-frontend

run-filemanager:
	mkdir -p storage
	./FileManager.py --Ice.Config=filemanager1.config

run-frontend:
	./Frontend.py --Ice.Config=frontend1.config $(NUM_FILEMANAGERS)

test-client:
	mkdir -p downloads
	./Client.py --Ice.Config=client.config --upload $(FILE)
	./Client.py --Ice.Config=client.config --list
	./Client.py --Ice.Config=client.config --download $(FILE_HASH)
	./Client.py --Ice.Config=client.config --remove $(FILE_HASH)
	./Client.py --Ice.Config=client.config --list

run-icestorm:
	mkdir -p IceStorm/
	icebox --Ice.Config=icebox.config

run-registry:
	mkdir -p data/db/registry
	icegridregistry --Ice.Config=registry.config

run-remove:
	./Client.py --Ice.Config=client.config --remove $(FILE_HASH)

clean:
	$(RM) -r downloads/ storage/ __pycache__/ URFS/
	$(RM) urfs_ice.py *.pyc

vclean: clean
	$(RM) -r IceStorm/ data/

# CUSTOM RULES
semi-clean:
	$(RM) -r downloads/ storage/ __pycache__/ URFS/
	$(RM) urfs_ice.py *.pyc
	$(RM) -r IceStorm/ data/
	slice2py urfs.ice