import pickle
def dump(obj, filename):
    try:
        with open(filename, 'wb') as write:
            pickle.dump(obj, write)
        return True
    except Exception as e:
        print(e)
        return False

def load(filename):
    try:
        with open(filename, 'rb') as read:
            ret = pickle.load(read)
    except Exception as e:
        raise e
    return ret
