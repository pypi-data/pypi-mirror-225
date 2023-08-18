def get_provider_info():
    return {
        'package-name': 'ursactl',
        'name': 'Ursa Frontier',
        'description': 'Provides access to Ursa Frontier SaaS Platform datasets and data generation pipelines.',
        'connection-types': [
            {
                'connection-type': 'ursa_frontier_platform',
                'hook-class-name': 'ursactl.airflow_provider.hooks.UrsaCtlHook'
            }
        ]
    }
