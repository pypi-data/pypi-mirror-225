#!/usr/bin/env python3

import cgi
import re, json, yaml
from os import environ, pardir, path
import sys, os, datetime

from bycon import *

"""podmd

* <https://progenetix.org/beacon/cohorts/>

podmd"""

################################################################################
################################################################################
################################################################################

def main():

    try:
        datasets()
    except Exception:
        print_text_response(traceback.format_exc(), byc["env"], 302)

################################################################################

def collections():

    try:
        datasets()
    except Exception:
        print_text_response(traceback.format_exc(), byc["env"], 302)
    
################################################################################

def datasets():

    initialize_bycon_service(byc)
    r, e = instantiate_response_and_error(byc, "beaconCollectionsResponse")
    response_meta_set_info_defaults(r, byc)
    
    __get_history_depth(byc)
    dbstats = datasets_update_latest_stats(byc)

    parse_filters(byc)
    parse_variants(byc)

    if "beaconResultsetsResponse" in byc["response_entity"]["response_schema"]:
        create_empty_beacon_response(byc)
        response_add_received_request_summary_parameters(byc)
        run_result_sets_beacon(byc)
        query_results_save_handovers(byc)
    else:
        create_empty_beacon_response(byc)
        response_add_received_request_summary_parameters(byc)
        populate_service_response( byc, dbstats )

        byc["service_response"]["response"]["collections"] = byc["service_response"]["response"].pop("results", None)
        byc["service_response"]["response"].pop("result_sets", None)
        for i, d_s in enumerate(byc["service_response"]["response"]["collections"]):
            # TODO: remove verifier hack
            for t in ["createDateTime", "updateDateTime"]:
                d = str(d_s[t])
                try:
                    if re.match(r'^\d\d\d\d\-\d\d\-\d\d$', d):
                        byc["service_response"]["response"]["collections"][i].update({t:d+"T00:00:00+00:00"})
                except:
                    pass

    cgi_print_response( byc, 200 )

################################################################################

def __get_history_depth(byc):

    if "statsNumber" in byc["form_data"]:
        s_n = byc["form_data"]["statsNumber"]
        try:
            s_n = int(s_n)
        except:
            pass
        if type(s_n) == int:
            if s_n > 0:
                byc.update({"stats_number": s_n})

################################################################################
################################################################################

if __name__ == '__main__':
    main()
