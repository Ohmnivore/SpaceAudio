class Roles:
    custom = 32

def min_to_string(minutes):
    m, s = divmod(minutes, 60)
    h, m = divmod(m, 60)
    return "%d:%02d" % (m, s)

def filesize_to_string(filesize):
    return str(round(filesize / 1000000, 1)) + ' MB'
