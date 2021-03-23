#!/usr/bin/env bash
set -u
mongo -- "$MONGO_INITDB_DATABASE" <<EOF
    var rootUser = '$MONGO_INITDB_ROOT_USERNAME';
    var rootPassword = '$MONGO_INITDB_ROOT_PASSWORD';

    var admin = db.getSiblingDB('admin');

    admin.auth(rootUser, rootPassword);

    var user = '$MONGO_USERNAME';
    var passwd = '$MONGO_PASSWORD' || user;

    var app = db.getSiblingDB('app');

    app.createUser({
        user: user,
        pwd: passwd,
        roles: [
            {role: 'readWrite', db: '$MONGO_DB'}
        ]
    });
EOF
