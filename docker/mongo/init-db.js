let err = true;
let admin = db.getSiblingDB('admin');

admin.auth('admin', 'admin');

let res = db.createUser(
    {
        user: 'dbuser',
        pwd: 'password',
        roles: [
            {
                role: 'readWrite',
                db: 'app'
            }
        ]
    }
);

print(res);
printjson(res);

if (err) {
    print('Error, exiting...');
    quit(1);
}