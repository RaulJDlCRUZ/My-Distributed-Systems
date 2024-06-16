#!/usr/bin/make -f
# -*- mode:makefile -*-

clean:
	$(RM) -r *~ proxy.out Math_ice.py Example/

run-server:
	./Server.py --Ice.Config=Server.config | tee proxy.out

run-client:
	./Client.py '$(shell head -1 proxy.out)' 3 TIMES 5

gen-src:
	slice2py Math.ice
