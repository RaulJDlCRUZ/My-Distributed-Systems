import grpc
import factorial_checker_pb2
import factorial_checker_pb2_grpc


def fact(n):
    return 1 if (n == 1 or n == 0) else n * fact(n - 1)


if __name__ == '__main__':
    server = '192.168.8.224'
    port = int(4080)
    channel = grpc.insecure_channel(f'{server}:{port}')
    stub = factorial_checker_pb2_grpc.FactorialCheckerStub(channel)
    message = factorial_checker_pb2.NumberRequest(email='raul.jimenez8')
    response = stub.RequestRandomNumber(message)
    # print(response)
    mi_factorial = fact(int(response.number))
    # print(mi_factorial)

    messageii = factorial_checker_pb2.CheckRequest(
        email='raul.jimenez8', factorial=mi_factorial)
    responseii = stub.CheckFactorial(messageii)
    print(responseii)
