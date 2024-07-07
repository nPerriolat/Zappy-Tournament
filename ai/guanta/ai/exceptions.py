#!/usr/bin/env python3

class Dead(Exception):
    pass

class ConnectionRefused(Exception):
    pass

class BroadcastReceived(Exception):
    pass

class BroadcastDeny(Exception):
    pass

class Forked(Exception):
    pass
