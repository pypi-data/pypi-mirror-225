import os


class Test_operation():
    def Local_ip(self, ip_address):
        return ip_address

    def Local_hostname(self, hostname):
        return hostname

    def operation(self, statement):
        info = os.popen(statement)
        return info.read()

    def test_mat(self, add_number):
        return add_number + 1


if __name__ != "__main__":
    Test_operation