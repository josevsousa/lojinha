# -*- coding: utf-8 -*-

@auth.requires_login()
def cadastrarClientes():
  	return dict(formCadastro=crud.create(db.clientes))

@auth.requires_login()
def listarClientes():
	clientes = db(db.clientes.id>0).select()
	#return dict(livros=livros)

	#virtaul fields
	class Virtual(object):
		def botoes(self):
			#admin
			if auth.has_membership('admin'):   #URL('clientes','deletar',args=[self.clientes.id])
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('clientes','select',args=[self.clientes.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('clientes','update',args=[self.clientes.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_id=self.clientes.id,_href='#',_class='btn btn-default fechar Jview btn-xs')),_class='btn-group JpositionA')
			#user qualquer
			else:
				bts = DIV(XML(A(SPAN(_class='glyphicon glyphicon-eye-open'),_href=URL('clientes','select',args=[self.clientes.id]),_class='btn btn-default f Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-pencil'),_href=URL('clientes','update',args=[self.clientes.id]),_class='btn btn-default Jview btn-xs')),XML(A(SPAN(_class='glyphicon glyphicon-remove'),_href='#',_class='btn btn-default Jview btn-xs',_disabled='disabled')),_class='btn-group JpositionA')
			return bts

	clientes.setvirtualfields(campos_virtual = Virtual())		
	
	return dict(formListar=clientes)



# ===================================================
#select
def select():
	table = db(db.clientes.id==request.args[0]).select()
	return dict(table=table)
#insert
def inserir():
	return dict(form=crud.create(db.clientes))
#update
def update():
	return dict(formUpdate=crud.update(db.clientes,request.args(0),_class="formEditar"))
#delete
@auth.requires_membership('admin')
def deletar():
	db(db.clientes.id == request.vars.cod).delete()
	return ''

# ===================================================