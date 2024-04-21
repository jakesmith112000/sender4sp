import random

def safe_log(log):
    name = int(random.randint(0,1000000000000) * random.randint(100,10000000) / random.randint(1,1000))
    open("logs/{}.txt".format(name),"w+").write(log)
    return name
def load_log(name:str):
    return open(f"logs/{name}.txt","r").read()