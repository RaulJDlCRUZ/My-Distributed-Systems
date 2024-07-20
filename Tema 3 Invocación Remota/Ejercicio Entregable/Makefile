#

STUBS = factorial_checker_pb2.py factorial_checker_pb2_grpc.py

all: $(STUBS)

%_pb2.py: %.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $<


clean:
	$(RM) *~ $(STUBS)
	$(RM) -r __pycache__