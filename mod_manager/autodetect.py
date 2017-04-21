import socket

# XXX: UNSTABLE!!!

# Experimental module for detecting packages from a live server
# Reverse-engineered by observing UDP traffic between Factorio client and server
# It was actually quite fun :D


FACTORIO_PORT = 34197

def detect_server_packages(addr):
    """Returns a list of (name, version) tuples."""

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1.0) # seconds

    try:
        s.sendto(bytes([
            0x02,               # packet type (CONN_START)
            0xa3, 0x1c,         # ???
            0xa3, 0x1c,         # ???
            0x00, 0x0e, 0x16,   # version??
            0xfe, 0x62,         # build??
            0x26, 0xc1, 0xfd, 0xcf
        ]), (addr, FACTORIO_PORT))
    except socket.gaierror:
        raise ConnectionRefusedError

    while True:
        try:
            data = s.recv(512)
        except socket.timeout:
            raise BrokenPipeError
        break

    assert data[0] == 0x03 # packet type (CONN_START_RESP)
    copy_to_next = list(data[-8:])

    s.sendto(bytes([
        0x04,                   # packet type (CONN_INIT)
        0xa4, 0x1c              # ???
        ]+copy_to_next+[
        0xbc, 0x60, 0x89, 0x44, # ???

        # username
        # filled this with null bytes, and it's still working
        0x08, # len=8
        0x00, 0x00, 0x00, 0x00, # 0000 # <- letters 0-3
        0x00, 0x00, 0x00, 0x00, # 0000 # <- letters 4-7

        # padding bytes?
        0x00, 0x00, 0x00, 0x00, # 0000
        0x00, 0x00, 0x00, 0x00, # 0000
        0x00, 0x00, 0x00, 0x00, # 0000

        0x01, 0x00, 0x00, 0x00, # u32: mod table entry count = 1

        # 0. entry
        0x04, # len=4
        0x62, 0x61, 0x73, 0x65, # "base"

        0x00, 0x0e, 0x16, 0x11, # ???
        0xee, 0xe2, 0x2e        # ???

    ]), (addr, FACTORIO_PORT))


    data = bytes()
    while True:
        try:
            d = s.recv(1024)
        except socket.timeout:
            raise BrokenPipeError
        if data:
            assert d[0] == 0xc5 # packet type: CONN_JOIN
            # coninuation packages have 4
            d = d[4:]
        data += d
        if len(d) < 511:
            break
    s.close()

    if data[0] != 0x45:
        return {} # vanilla

    # not vanilla, mod match error
    FIXED_STR = b"Active mods configuration doesn't match"
    assert FIXED_STR in data

    ptr = data.find(FIXED_STR)+len(FIXED_STR)

    # set pt to the start of the username list
    ptr = ptr+6


    # step over username array

    # collect usernames just for fun
    usernames = []
    usernames.append(data[ptr+1:ptr+int(data[ptr])+1].decode())

    ptr = ptr + int(data[ptr]) + 1
    while data[ptr] != 0xff:
        usernames.append(data[ptr+1:ptr+int(data[ptr])+1].decode())
        ptr = ptr + int(data[ptr]) + 1

    ptr += 1 # step over the list terminator

    # Just for fun, for now
    # print("Usernames:")
    # print(usernames)

    ptr += 4 # step over, but over what???

    mod_arr_len = int("".join([hex(x)[2:] for x in list(data[ptr:ptr+4])[::-1]]), 16)

    ptr += 12

    mods = []
    for _ in range(mod_arr_len-1):
        if data[ptr] == 0xff: # alternate end-of-list marker
            break
        mod_name = data[ptr+1:ptr+int(data[ptr])+1].decode()
        ptr = ptr + int(data[ptr]) + 1
        mod_version = ".".join([str(int(x)) for x in data[ptr:ptr+3]])
        assert mod_version.count(".") == 2
        ptr += 3

        mods.append((mod_name, mod_version))

        # step over, but over what??
        ptr += 4

    assert len(mods) == len(set([m[0] for m in mods])), "Duplicate mods"

    return mods
