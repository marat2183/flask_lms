#!/usr/bin/env bash
set -eu
mongo -- "$MONGO_DB" <<EOF
    var rootUser = '$MONGO_INITDB_ROOT_USERNAME';
    var rootPassword = '$MONGO_INITDB_ROOT_PASSWORD';
    var admin = db.getSiblingDB('admin');
    admin.auth(rootUser, rootPassword);

    var user = '$MONGO_USERNAME';
    var passwd = '${MONGO_PASSWORD-}' || user;
    db.createUser({user: user, pwd: passwd, roles: ["readWrite"]});
EOF

if [ $? -eq 0 ]; then
    echo "User $MONGO_USERNAME with password $MONGO_PASSWORD added to $MONGO_DB"
else
    echo '[ERROR] Failed adding user to database, aborting..' 1>&2
fi
