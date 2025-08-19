import pickle 


api = 'gemini_api.pkl'

key = "You gemini API key here"


def load_model(api, key):
    f = open(api, 'wb')
    pickle.dump(key, f)
    f.close()

load_model(api, key)

