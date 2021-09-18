def format_br_currency( value ):

    s = "%.2f" % value
    s1 , s2  = s.split( "." )
    return "R$ " + s1 + "," + s2