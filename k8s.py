import yaml
import base64

# Load docker-compose.yaml
with open('docker-compose.yaml', 'r') as f:
    docker_compose = yaml.safe_load(f)

# Initialize lists to hold all secrets and deployments
all_secrets = []
all_deployments = []

# Loop through each service to generate secret and deployment
for service, config in docker_compose['services'].items():
    # Initialize dict for Secret
    secret_dict = {
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {'name': f'{service}-secret'},
        'type': 'Opaque',
        'data': {}
    }

    # Extract and encode environment variables
    for key, value in config.get('environment', {}).items():
        encoded_value = base64.b64encode(value.encode()).decode()
        secret_dict['data'][key] = encoded_value

    all_secrets.append(secret_dict)

    # Initialize dict for Deployment
    deployment_dict = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {'name': service},
        'spec': {
            'replicas': 1,
            'selector': {'matchLabels': {'app': service}},
            'template': {
                'metadata': {'labels': {'app': service}},
                'spec': {
                    'containers': [
                        {
                            'name': service,
                            'image': config.get('image', ''),
                            'ports': [{'containerPort': int(config.get('ports', ['8080'])[0].split(':')[0])}],
                            'envFrom': [{'secretRef': {'name': f'{service}-secret'}}]
                        }
                    ]
                }
            }
        }
    }

    all_deployments.append(deployment_dict)

# Save all secrets to a single YAML file
with open('all-secrets.yaml', 'w') as f:
    yaml.dump_all(all_secrets, f)

print('All Kubernetes Secrets have been generated in all-secrets.yaml')

# Save all deployments to a single YAML file
with open('all-deployments.yaml', 'w') as f:
    yaml.dump_all(all_deployments, f)

print('All Kubernetes Deployments have been generated in all-deployments.yaml')
