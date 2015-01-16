# -*- coding: utf-8 -*-

class Enum( object ):
    def __init__( self, **kwargs ):
        self.attrs = kwargs
        for key, value in kwargs.iteritems():
            setattr( self, key, key )

    def __iter__(self):
        return self.attrs.iteritems()


class DigitEnum( Enum ):
    def __init__(self, **kwargs ):
        self.attrs = dict( kwargs.itervalues() )

        for key, pair in kwargs.iteritems():
            setattr( self, key, pair[ 0 ] )
