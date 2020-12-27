API_HOST = {
    'local':{
        "test": "http://tests.local/wp-json/wc/v3/",
        'prod': "",
        'dev': ""
    },
    'ammps':{
        "test": "http://127.0.0.1/wp/wp-json/wc/v3/",
        'prod': "",
        'dev': ""
    }
}


WC_API_HOST = {
    "test": "http://tests.local/",
    'prod': "",
    'dev': ""
}


DB_HOST = {
    'local_machine': {
            "test":{
                'host':'localhost',
                'database':'local',
                'table_prefix':'wp_',
                'port':10005,
            },
            'prod':{},
            'dev':{}
    },
    'docker': {
            "test":{
                'host':'host.docker.internal',
                'database':'local',
                'table_prefix':'wp_',
                'port':3306,
            },
            'prod':{},
            'dev':{}
    }
}