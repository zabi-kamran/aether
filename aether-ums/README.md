# WIP: multitenancy on Aether via UMS

**NOTE**: This describes how to set up UMS with Aether for local development. The UMS integration is a work in progress and is not yet suitable for a production deployment. 

To run aether locally with UMS, we first need to clone the ums repo and build an image from the correct branch:

```bash
cd /tmp
git clone git@github.com:eHealthAfrica/ums.git
cd /tmp/ums
git fetch origin
git checkout feat/rest-api
docker-compose build ums
```

This will build an image `ums_ums` which is referenced in the docker-compose file
in the aether repo.

Now we can start the aether environment as usual:

```bash
./scripts/generate-docker-compose-credentials.sh > .env
dcp up -d db
docker-compose up
```

For the following commands, you need to have both `requests` and `dotenv` installed.
To install them, do:

```
pip install requests
pip install dotenv
```

To create example projects for Aether, run:

```bash
python3 ./scripts/ums/create_projects.py
```

`UMS_ADMIN_USERNAME` and `UMS_ADMIN_PASSWORD` should match the corresponding environment variables in `docker-compose-base.yml`.

To create example users for Aether, run:

```bash
python3 ./scripts/ums/create_projects.py
```

At this point, you should be able to log in to any Aether module using the credentials in `./scripts/ums/create_projects.py`.

TODO: list examples.
