def import_file(file):
    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        yield line
    f.close()

