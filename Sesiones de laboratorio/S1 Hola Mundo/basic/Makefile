#!/usr/bin/make -f
# -*- mode:makefile -*-

clean:
	$(RM) -r *~ proxy.out Printer_ice.py Example/

run-server:
	./Server.py --Ice.Config=Server.config | tee proxy.out

run-client:
	./Client.py '$(shell head -1 proxy.out)'

gen-src:
	slice2py Printer.ice
