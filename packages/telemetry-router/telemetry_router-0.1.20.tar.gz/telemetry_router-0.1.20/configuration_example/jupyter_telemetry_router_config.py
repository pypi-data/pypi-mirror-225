# This file should be saved into one of the config directories provided by `jupyter --path`.

c.TelemetryRouterApp.exporters = [
    {
        'type': 'console',
        'id': 'ConsoleExporter',
    },
    {
        'type': 'file',
        'id': 'FileExporter',
        'path': 'log',
    },
    {
        'type': 'remote',
        'id': 'S3Exporter',
        'url': 'https://telemetry.mentoracademy.org/telemetry-edtech-labs-si-umich-edu/dev/test-telemetry',
        'env': ['WORKSPACE_ID']
    },
    {
        'type': 'remote',
        'id': 'MongoDBExporter',
        'url': 'https://68ltdi5iij.execute-api.us-east-1.amazonaws.com/mongo',
        'params': {
            'mongo_cluster': 'mengyanclustertest.6b83fsy.mongodb.net',
            'mongo_db': 'telemetry',
            'mongo_collection': 'dev'
        }
    },
]