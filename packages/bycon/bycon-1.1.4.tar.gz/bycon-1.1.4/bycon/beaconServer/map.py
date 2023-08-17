#!/usr/bin/env python3

from os import path, pardir
import sys

from bycon import *

"""podmd

podmd"""

################################################################################
################################################################################
################################################################################

def main():

    try:
        map()
    except Exception:
        print_text_response(traceback.format_exc(), byc["env"], 302)
    
################################################################################

def map():

    r, e = instantiate_response_and_error(byc, "beaconMapResponse")
    response_meta_set_info_defaults(r, byc)

    m_f = get_schema_file_path(byc, "beaconMap")
    beaconMap = load_yaml_empty_fallback( m_f )

    r.update( {"response": beaconMap } )
    byc.update({"service_response": r, "error_response": e })

    cgi_print_response( byc, 200 )

################################################################################
################################################################################
################################################################################

if __name__ == '__main__':
    main()
