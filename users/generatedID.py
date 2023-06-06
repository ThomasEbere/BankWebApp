import random, string


class UserId:
    @staticmethod
    def generaterandom():
        x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        return x
