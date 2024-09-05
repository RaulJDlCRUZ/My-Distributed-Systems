#!/usr/bin/make -f
# -*- mode:makefile -*-

clean:
	$(RM) -r *~ proxy.out Math_ice.py Example/

run-third:
	./Third_One.py --Ice.Config=Third.config | tee proxy_2.out

run-server:
	./Server.py '$(shell head -1 proxy_2.out)' --Ice.Config=Server.config | tee proxy.out

run-client:
	./Client.py '$(shell head -1 proxy.out)' 3 TIMES 5

gen-src:
	slice2py Math.ice
	slice2py Printer.ice
