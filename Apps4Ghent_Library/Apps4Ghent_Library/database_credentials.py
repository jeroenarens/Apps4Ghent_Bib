# Database credentials
_MONGODB_USER = 'mongouser'
_MONGODB_PASSWD = 'password'
_MONGODB_HOST = 'localhost'
_MONGODB_NAME = 'apps4ghent'

# Connection string without any authentication
_MONGODB_DATABASE_HOST = 'mongodb://%s/%s' % (_MONGODB_HOST, _MONGODB_NAME)

# Connection string with user/pass authentication
#_MONGODB_DATABASE_HOST = 'mongodb://%s:%s@%s/%s' % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)
