


class BibleGateway:


    # 1.4.7
    def getClass(string:str) -> str:
        array = string.split('.', 2)

        assert len(array) == 3, 'string must '