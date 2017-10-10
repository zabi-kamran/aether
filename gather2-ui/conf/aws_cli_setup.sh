# configure AWS cli and get secrets

# S3 secrets
configure_aws_cli () {
  mkdir -p ~/.aws
  envsubst < /code/conf/extras/aws_config.tmpl > ~/.aws/config
  export AWS_PROFILE=assume_role
  echo '# application environment variables' >> ~/.bashrc
  aws s3 cp --sse AES256 s3://ecs-secrets-prod/$PROJECT - >> ~/.bashrc
}

configure_aws_cli()