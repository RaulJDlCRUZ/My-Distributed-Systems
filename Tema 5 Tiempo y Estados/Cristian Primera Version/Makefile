#!/usr/bin/make -f
# -*- mode:makefile -*-

clean:
	$(RM) -r *~ proxy.out Cristian_ice.py Cristian/

run-server:
	./Server.py --Ice.Config=Server.config | tee proxy.out

run-cristian:
	./Cristian.py '$(shell head -1 proxy.out)'

gen-src:
	slice2py Cristian.ice
