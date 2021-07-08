class DataHelper:

    @staticmethod
    def str_to_bool(string):
        if string == 'True':
            return True
        elif string == 'False':
            return False
        else:
            raise ValueError
