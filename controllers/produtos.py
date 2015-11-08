# coding: utf8
@auth.requires_membership('admin')
def cadastrarProdutos():
	menu = 'produtos'
	return dict(formCadastro=crud.create(db.produtos))


def listarProdutos___():
	menu = 'produtos'
	return dict(formListar=crud.select(db.produtos, db.produtos.id>0)) #db.books.id>0,['id','titulo']

@auth.requires_login()
def listarProdutos():
	produtos = db(db.produtos.id>0).select()
	#return dict(livros=livros)

	#virtaul fields
	class Virtual(object):
		def botoes(self):
			#admin
			if auth.has_membership('admin'):   #URL('produtos','deletar',args=[self.produtos.id])
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('produtos','select',args=[self.produtos.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('produtos','update',args=[self.produtos.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default fechar Jview btn-xs')),_class='btn-group JpositionA')
			#user qualquer
			else:
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('produtos','select',args=[self.produtos.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),_class='btn-group JpositionA')
			return bts

		# def img(self): 
		# 	img =  IMG(_src=URL('default','download',args='1026'), _id='imgMin')
		# 	# img =  IMG(_src=URL('static','/images/logo-lojinha.png'), _id='imgMin')
		# 	return img

	produtos.setvirtualfields(campos_virtual = Virtual())		

	return dict(formListar=produtos)

# ============== select insert update ==============
def selectCrud():
	todos = crud.select(db.produtos, db.produtos.id == request.args(0),['codigo_produto','nome_produto','preco_produto_lojinha','dataGravado'])
	return dict(form=todos)
#select
def select():
	table = db(db.produtos.id==request.args[0]).select()
	return dict(table=table)
#insert
@auth.requires_membership('admin')
def inserir():
	return dict()
	#return dict(form=crud.create(db.produtos))
#update
@auth.requires_membership('admin')
def update():
	return dict(form=crud.update(db.produtos,request.args(0)))
#delete
def deletar():
	print request.vars.cod
	db(db.produtos.codigo_produto == request.vars.cod).delete()
	return ''


# ===================================================


#@auth.requires_membership('admin')
def listarProdutoss():
    grid = SQLFORM.grid(db.produtos)
    return dict(formListar=grid)

