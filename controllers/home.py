# coding: utf8
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
      """       
    if session.auth:
        x = session.auth.user
        y = SQLFORM.grid(db.auth_user,user_signature=False)
        v = db(db.produtos.id==241).select('preco_produto_lojinha')
        z = "%s"%v

    else:
        x = "nao ta logado"    
    return locals()

#===== CRUD ========
#insert
def inserir():
	return dict(form=crud.create(db.books))
#update
def alterar():
	return dict(form=crud.update(db.produtos,request.args(0)))
#select
def listar():
	return dict(form=crud.select(db.books, db.books.id>0)) #db.books.id>0,['id','titulo']
#delete
def deletar():
	return dict(form=crud.delete(db.produtos, request.args(0)))
#search
def buscar():
	return dict(form=crud.search(db.books))
#=== FIM DO CRUD ===
