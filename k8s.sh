# #!/bin/bash

# # Script to generate Kubernetes Secret and Deployment YAMLs for each service in a Docker Compose file

# # Check if docker-compose.yaml file exists
# if [ ! -f "docker-compose.yaml" ]; then
#   echo "docker-compose.yaml file not found!"
#   exit 1
# fi

# # Extract service names
# services=$(yq e '.services | keys | .[]' docker-compose.yaml)

# # Loop through each service to generate secret and deployment
# for service in $services; do
#   # Initialize JSON object for Secret
#   secret_json="{\"apiVersion\": \"v1\",\"kind\": \"Secret\",\"metadata\": {\"name\": \"${service}-secret\"},\"type\": \"Opaque\",\"data\": {"

#   # Extract environment variables for the service
#   env_vars=$(yq e ".services.$service.environment | keys[]" docker-compose.yaml)

#   # Encode each environment variable in Base64 and append to secret_json
#   for key in $env_vars; do
#     value=$(yq e ".services.$service.environment.$key" docker-compose.yaml)
#     encoded_value=$(echo -n $value | base64)
#     secret_json="$secret_json\"$key\": \"$encoded_value\","
#   done

#   # Remove trailing comma and close JSON object
#   secret_json=${secret_json%,}
#   secret_json="$secret_json}}"

#   # Convert JSON to YAML and save to a file named after the service
#   echo $secret_json | yq e -P - > ${service}-secret.yaml
#   echo "Kubernetes Secret for $service has been generated in ${service}-secret.yaml"

#   # Initialize JSON object for Deployment
#   deployment_object= yq e
#   deployment_json="{\"apiVersion\": \"apps/v1\",\"kind\": \"Deployment\",\"metadata\": {\"name\": \"$service\"},\"spec\": {\"replicas\": 1,\"selector\": {\"matchLabels\": {\"app\": \"$service\"}},\"template\": {\"metadata\": {\"labels\": {\"app\": \"$service\"}},\"spec\": {\"containers\": [{\"name\": \"$service\",\"image\": \"$(yq e .services.$service.image docker-compose.yaml)\",\"ports\": [{\"containerPort\": $(yq e .services.$service.ports[0] docker-compose.yaml | cut -d ':' -f 1)}],\"envFrom\": [{\"secretRef\": {\"name\": \"${service}-secret\"}}]}]}}}}"

#   # Convert JSON to YAML and save to a file named after the service
#   echo $deployment_json | yq e -P - > ${service}-deployment.yaml
#   echo "Kubernetes Deployment for $service has been generated in ${service}-deployment.yaml"

# done

#!/bin/bash

# Initialize files to hold all secrets and deployments
echo '' > all-secrets.yaml
echo '' > all-deployments.yaml

# Extract service names
services=$(yq e '.services | keys | .[]' docker-compose.yaml)

# Loop through each service to generate secret and deployment
for service in $services; do
  # Initialize Kubernetes Secret YAML
  secret_yaml="apiVersion: v1\nkind: Secret\nmetadata:\n  name: ${service}-secret\ntype: Opaque\ndata:"
  echo "$secret_yaml"
  # Extract environment variables for the service
  # fix this line: Error: bad expression, please check expression syntax with yq r -h
  # env_vars=$(yq e -v '.services.$service.environment | keys[]' docker-compose.yaml)
  env_vars=$(yq '.services[$service].environment | keys[]' docker-compose.yaml)
  echo "$env_vars"
  echo "services.$service.environment | keys[]"
  echo yo
  echo < "$(yq e '.services[$service].environment | keys[]' docker-compose.yaml)"
  # Encode each environment variable in Base64 and append to secret_yaml
  for key in $env_vars; do
    value=$(yq e ".services.$service.environment.$key" docker-compose.yaml)
    echo $value
     # set value from enviorment variable value is empty
    if [ -z "$value" ]; then
      value=$(printenv $key)
    fi
    echo $key: $encoded_value
    encoded_value=$(echo -n $value | base64)
    secret_yaml="$secret_yaml\n  $key: $encoded_value"
  done

  # Append to all-secrets.yaml
  echo -e "$secret_yaml\n---" >> all-secrets.yaml

  # Initialize Kubernetes Deployment YAML
  deployment_yaml="apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: $service\nspec:\n  replicas: 1\n  selector:\n    matchLabels:\n      app: $service\n  template:\n    metadata:\n      labels:\n        app: $service\n    spec:\n      containers:\n      - name: $service\n        image: $(yq e .services.$service.image docker-compose.yaml)\n        ports:\n        - containerPort: $(yq e .services.$service.ports[0] docker-compose.yaml | cut -d ':' -f 1)\n        envFrom:\n        - secretRef:\n            name: ${service}-secret"

  # Append to all-deployments.yaml
  echo -e "$deployment_yaml\n---" >> all-deployments.yaml

done

echo "All Kubernetes Secrets have been generated in all-secrets.yaml"
echo "All Kubernetes Deployments have been generated in all-deployments.yaml"
