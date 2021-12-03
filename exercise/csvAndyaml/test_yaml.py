import yaml

with open("test.yaml", "r") as f:
    read_f = yaml.load(f.read(), Loader=yaml.Loader)
    print("read_f: ", read_f)