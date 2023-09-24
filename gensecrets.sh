#!/bin/bash

# # Script to generate Kubernetes Secret YAML from .env file

# # Check if .env file exists
# if [ ! -f "./next/.env" ]; then
#   echo ".env file not found!"
#   exit 1
# fi

# # Initialize Kubernetes Secret YAML
# secret_yaml="apiVersion: v1\nkind: Secret\nmetadata:\n  name: k8s-secret\ntype: Opaque\ndata:"

# # Read .env file and convert each line to Base64
# while read -r line || [ -n "$line" ]; do
#   key=$(echo $line | cut -d '=' -f 1)
#   value=$(echo $line | cut -d '=' -f 2-)
#   encoded_value=$(echo -n $value | base64)
#   secret_yaml="$secret_yaml\n  $key: $encoded_value"
# done < ./next/.env

# # Save to my-secret.yaml
# echo -e $secret_yaml > k8s-secret.yaml

# echo "Kubernetes Secret has been generated in k8s-secret.yaml"

# Script to generate Kubernetes Secret YAMLs for each service in a Docker Compose file

compose_file="docker-compose.yml"

# Check if $compose_file file exists
# if [ ! -f $compose_file ]; then
#   echo "$compose_file file not found!"
#   exit 1
# fi

# Extract service names
services=$(yq e '.services | keys | .[]' $compose_file)

# Loop through each service to generate secret
# Loop through each service to generate secret and deployment
for service in $services; do
  # Initialize Kubernetes Secret YAML
  secret_yaml="apiVersion: v1\nkind: Secret\nmetadata:\n  name: ${service}-secret\ntype: Opaque\ndata:"

  # Extract environment variables for the service
  env_vars=$(yq e ".services.$service.environment | keys[]" $compose_file)

  # Encode each environment variable in Base64 and append to secret_yaml
  for key in $env_vars; do
    value=$(yq e ".services.$service.environment.$key" $compose_file)
    # set value from enviorment variable value is empty
    if [ -z "$value" ]; then
      value=$(printenv $key)
    fi

    encoded_value=$(echo -n $value | base64)
    if [ -z "$encoded_value" ]; then
      encoded_value=$(echo -n $key | base64)
    fi
    secret_yaml="$secret_yaml\n  $key: $encoded_value "
  done

  # Save to a YAML file named after the service
  echo -e $secret_yaml > ${service}-secret.yaml
  echo "Kubernetes Secret for $service has been generated in ${service}-secret.yaml"

  # Initialize Kubernetes Deployment YAML
  deployment_yaml="apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: $service\nspec:\n  replicas: 1\n  selector:\n    matchLabels:\n      app: $service\n  template:\n    metadata:\n      labels:\n        app: $service\n    spec:\n      containers:\n      - name: $service\n        image: $(yq e .services.$service.image $compose_file)\n        ports:\n        - containerPort: $(yq e .services.$service.ports[0] $compose_file | cut -d ':' -f 1)\n        envFrom:\n        - secretRef:\n            name: ${service}-secret"

  # Save to a YAML file named after the service
  echo -e $deployment_yaml > ${service}-deployment.yaml
  echo "Kubernetes Deployment for $service has been generated in ${service}-deployment.yaml"
done
