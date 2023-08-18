import os


class Test_operation():
    def Local_ip(self, ip_address):
        print(__name__)
        print(__name__ == "__main__")
        return ip_address

    def Local_hostname(self, hostname):
        print(__name__)
        print(__name__ == "__main__")
        return hostname

    def operation(self, statement):
        info = os.popen(statement)
        print(__name__)
        print(__name__ == "__main__")
        return info.read()

    def test_mat(self, add_number):
        print(__name__)
        print(__name__ == "__main__")
        return add_number + 1
