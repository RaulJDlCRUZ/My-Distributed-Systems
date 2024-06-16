#!/usr/bin/make -f

all:

clean:
	$(RM) -r data/

run: app-workspace
	$(MAKE) run-node1 &
	sleep 1
	$(MAKE) run-node2

run-node1: data/db/registry data/db/node1/servers
	icegridnode --Ice.Config=node1.config

run-node2: data/db/node2/servers
	icegridnode --Ice.Config=node2.config

run-client:
	./Client.py --Ice.Config=locator.config printer

app-workspace: data/Printer
	cp Printer.ice Server.py data/Printer
	icepatch2calc data/Printer

data/%:
	mkdir -p $@
