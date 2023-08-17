"""Regex dictionary for the EDI message, contains pattern and validation method"""
edifact_regexes = {
    "header": {
        "messagenumber": {
            "pattern": r"BGM\+\d+\+([\d:]+)\+",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "messagedate": {
            "pattern": r"DTM\+137:([^:]+)",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "buyerid": {
            "pattern": r"(?<=NAD\+BY\+)([^:]+)",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "buyerreference": {
            "pattern": r"(?<=NAD\+SU\+)([^:]+)",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "deliveryaddressID": {
            "pattern": r"(?<=NAD\+DP\+)([^:]+)",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "deliverypartyaddress": {
            "pattern": r"(?<=NAD\+DP\+\d{13}::)[0-9]\+\+(.*?)'",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        }
    },
    "lines": {
        "currency": {
            "pattern": r"CUX\+2:([A-Z]{3}):",
            "validator": {
                "__class__": "Str",
                "maxlen":3,
            }
        },
        "lineitemnr": {
            "pattern": r"LIN\+(\d+)\+\+",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "barcode": {
            "pattern": r"LIN.[a-z0-9]*\+\+([0-9]*)",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "fedas": {
            "pattern": r"PIA.[a-z0-9]*\+(\d+).GD",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "quantity": {
            "pattern": r"PIA.[a-z0-9]*\+(\d+).ST",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "itemNr": {
            "pattern": r"PIA.[a-z0-9]*\+(\d+).SA",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "itemcolor": {
            "pattern": r"(?<=IMD\+C\+35\+)\d+",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "itemsize": {
            "pattern": r"(?<=IMD\+C\+98\+).[a-z0-9]*",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "deliverydate": {
            "pattern": r"(?<=DTM\+2:)\d{8}",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "grossprice": {
            "pattern": r"(?<=PRI\+AAB:)(\d*.\d*)?",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        },
        "netprice": {
            "pattern": r"(?<=PRI\+NTP:)(\d*.\d*)?",
            "validator": {
                "__class__": "Str",
                "maxlen":100,
            }
        }
    }
}
