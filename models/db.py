# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager, Crud, Mail, Storage

mail = Mail()
auth = Auth(db)
service = Service()
plugins = PluginManager()
crud = Crud(db)


## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email: 'logging' or
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'mail.seusite.com.br:587'
mail.settings.sender = 'user'
mail.settings.login = 'senha'


## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


## configura a data
# from datetime import datetime
# codigoVenda =  str(datetime.now()).replace('-','').replace(':','').replace('.','').replace(' ','')
# datetime.now().day
# datetime.now().hour
# datetime.now().minute
# datetime.now().second





#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


#tabela produtos
db.define_table('produtos',
                Field('codigo_produto', requires = IS_NOT_EMPTY(error_message="Codigo obrigatório"), label="Código"), #unique = nao repetir
                Field('nome_produto', requires = IS_NOT_EMPTY(error_message="Nome obrigatório"), label="Nome" ),
                Field('preco_produto_lojinha','double', label="R$"),
                Field('dataGravado','datetime', default=request.now, label="Data", writable=False),
                Field('foto_produto','upload', label="Foto"),
                migrate ='produtos.table'   
            )
db.produtos.codigo_produto.requires = IS_NOT_IN_DB(db, db.produtos.codigo_produto, error_message = 'Esse código já existe')


# db.define_table('autoCompletProdutos',
#                 Field('nome_produto'),
#                 Field('codigo_produto'),
#                 migrate = 'autoCompletProdutos.table'
#     )
# db.autoCompletProdutos.nome_produto.widget = SQLFORM.widgets.autocomplete(request, db.produtos.nome_produto, limitby=(0,5), min_length=2)




OPERADORA = ('TIM','OI','VIVO','CLARO','FIXO','NENHUMA')

# db.define_table('clientes',
#                 Field('nome',label='Nome'), #unique nao deixa o dado repetir no banco
#                 Field('celular', label='Cel..'),
#                 Field('operadora'),
#                 Field('email',label='E-mail'),
#                 Field('dataGravado','datetime'),
#                 Field('foto_cliente','upload', label='Foto'),
#                 migrate = "clientes.table"
#             )
db.define_table('clientes',
                Field('nome',label='Nome', requires = IS_NOT_EMPTY(error_message="O nome é obrigatório")), #unique nao deixa o dado repetir no banco
                Field('celular', label='Cel..'),
                Field('operadora',requires = IS_IN_SET(OPERADORA,error_message="Operadora obrigatório")),
                Field('email',label='E-mail', requires = IS_EMAIL(error_message='Invalido email!')),
                Field('dataGravado','datetime', default=request.now, label="Data", writable=False),
                Field('foto_cliente','upload', label='Foto'),
                migrate = "clientes.table"
            )
# validação clientes
db.clientes.celular.requires = IS_NOT_IN_DB(db, db.clientes.celular, error_message = 'Celular inválido')


db.define_table('historicoVendas',
        Field('codigoVenda', label='Código'),
        Field('clienteEmail'),
        Field('tipoVenda'),
        Field('valorVenda','double'),
        Field('valorDesconto','double'),
        Field('vendedor'),
        Field('itensVenda'), 
        Field('dataVenda','datetime', default=request.now),
        Field('deletado','boolean', default=False),
        migrate = "historioVendas.table"
    ) 
