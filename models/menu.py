# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

# response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
#                   _class="navbar-brand",_href="http://www.web2py.com/",
#                   _id="web2py-logo")

response.logo = IMG(_src=URL('static','images/logo-lojinha.png'),_class="navbar-brand", _id="logo-lojinha")

response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

# response.menu = [
#     (T('Home'), False, URL('home', 'index'), [])
# ]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller


    # useful links to internal and external resources
    # response.menu += [
    response.menu = [
         
          (T('Caixa'),False, None, [
            (T('Caixa'), False, URL('caixa', 'cliente?menu=caixa'), []),
            (T('historico'), False, URL('caixa', 'historico?menu=caixa'), [])
          ]),
          (T('Clientes'), False, URL('clientes', 'listarClientes?menu=clientes'), []),
          (T('Produtos'), False, URL('produtos', 'listarProdutos?menu=produtos'), [])

          # (T('Produtos'), False, None, [
          #   (T('Listar Produtos'), False, URL('produtos', 'listarProdutos'), []),
          #   (T('Cadastro Produtos'), False, URL('produtos', 'cadastrarProdutos'), [])
          # ])
        ]

if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
