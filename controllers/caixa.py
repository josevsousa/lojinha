# -*- coding: utf-8 -*-

@auth.requires_login()
def cliente():
	#existe sessão aberta?
	if not session.venda.codigo: #não
		session.venda.userDiv = UL(LI(STRONG('Nome : '),SPAN(''),_class="list-group-item"),LI(STRONG('Celular : '),SPAN(''),_class="list-group-item"),LI(STRONG('E-mail :'),SPAN(''),_class="list-group-item"),_class="list-group")
	else: #sim

		#mostra o div com os novos valores
		session.venda.userDiv = UL(
			LI(STRONG('Nome: '),SPAN(session.venda.nome,_id="nn"),_class="list-group-item"),
			LI(STRONG('Celular : '),SPAN(session.venda.celular),_class="list-group-item"),
			LI(STRONG('E-mail : '),SPAN(session.venda.email),_class="list-group-item"),_class="list-group")	
	return dict(codigo=session.venda.codigo)


@auth.requires_login()
def clientes_retorno():
    pattern = '%' + request.vars.itens + '%' #primeira letra maiusculo
    selecionado = [row for row in db(db.clientes.nome.like(pattern)).select()] #select no db
	#se a session nao existir criar ela

    if not session.venda.codigo:
		from random import*
		session.venda.codigo = randint(1000,10000000) 
	
		# response.flash = "Codigo da venda : %s"%session.vendaAtual_codigo  

    for s in selecionado:
    	session.venda.nome = s.nome
    	session.venda.celular = s.celular
    	session.venda.email = s.email
	
	# userDiv = UL(
	# 	LI(STRONG('Nome : '),SPAN(session.vendaAtual_nome,_id="nn"),_class="list-group-item"),
	# 	LI(STRONG('Celular : '),SPAN(session.vendaAtual_celuar),_class="list-group-item"),
	# 	LI(STRONG('E-mail : '),SPAN(session.vendaAtual_email),_class="list-group-item"),_class="list-group")

    return ''

@auth.requires_login()
def produto():
	return dict(tb=session.venda.itens)

@auth.requires_login()
def caixa():	
	listaCompras = session.venda.itens 
	return dict(l=listaCompras)

@auth.requires_login()
def addProdutoAjax():
	if not session.venda.sTotal:
	    session.venda.total = 0 


	codigo = request.vars.codigo
	produto = request.vars.produto
	qtde = request.vars.qtde

	#buscar valor do item
	valorItem = db(db.produtos.codigo_produto == codigo).select("preco_produto_lojinha")[0]._extra['preco_produto_lojinha']
	
  	valorTotal = int(qtde)*float(valorItem)
  	session.venda.sTotal = float(session.venda.sTotal)+float(valorTotal)
	# soma valorItem com a qtde
		
	itensVendaTable = session.venda.itens                              
	itensVendaTable.insert(0, TR(TD(codigo),TD(qtde),TD(produto),TD("R$ %.2f"%valorItem),TD("R$ %.2f"%valorTotal),TD(A(SPAN(_class="glyphicon glyphicon-remove"), _class="btn btn-default fechar Jview btn-xs", _href="#"),_class="btD")))
	session.venda.itens = itensVendaTable

	return ''

@auth.requires_login()
def delItemProduto():
    index = request.vars.delIndex
    index = index.split(";")
    session.venda.itens.__delitem__(int(index[0]))
    session.venda.sTotal = float(session.venda.sTotal) - float(index[1]) #subtração do valor dos itens

    return dict()

@auth.requires_login()
def fecharVenda():
	index = request.vars.transitory
	index = index.split(";")

	# dados a gravar no db
	codigoVenda = session.venda.codigo
	clienteEmail = session.venda.email
	tipoVenda = index[0]
	valorVenda = index[1]
	valorDesconto = index[2]
	vendedor = session.auth.user.email
	itensVenda = session.venda.itens

	if valorDesconto == '':
		valorDesconto = '0.00'
		pass

	#---- GUARDAR VENDA NO DB
	db.historicoVendas.insert(
		codigoVenda = codigoVenda,
		clienteEmail = clienteEmail,
		tipoVenda = tipoVenda,
		valorVenda = valorVenda,
		valorDesconto = valorDesconto,  
		vendedor = vendedor,
		itensVenda = itensVenda 
		)
	db.commit()
	
	viewDesc = "";
	if valorDesconto != "0.00":
		valorT = (float(valorVenda) + float(valorDesconto))
		viewDesc = "<h3><b>Total</b> : R$ %.2f - <b>Desconto</b> : <span>R$ %.2f</span></h3>"%(valorT, float(valorDesconto))
		
	# comprovante do email para impressao
	div = XML(
			"<div style='text-align:center;display:none' class='logoP'>"+
				"<img src='https://dl.dropboxusercontent.com/u/11469395/Nallu.paiva/logoPrint.png' width='95pt'><hr>" +
			"</div>"+
			"<h3>Recibo de compra Nallubaby ( codigo : %s )</h3><br>"%session.venda.codigo +		
		"<div id='retornoCliente'>" +
			"<ul class='list-group'>" +
				"<li class='list-group-item'><strong>Cliente: </strong><span id='nn'>%s</span></li>"%session.venda.nome +
				"<li class='list-group-item'><strong>Celular : </strong><span>%s</span></li>"%session.venda.celular +
				"<li class='list-group-item'><strong>E-mail : </strong><span>%s</span></li>"%session.venda.email +
			"</ul> "  +
		"</div>" +
			"<div class='table-responsive'>"+
				"<table class='table table-bordered'>"+
					"<thead>"+
						"<tr>"+
							"<th>Código</th>"+
							"<th>Qtde</th>"+
							"<th>Produto</th>"+
							"<th>Valor Unidade</th>"+
							"<th>Valor Total</th>"+
						"</tr>"+
					"</thead>"+
					"<tbody id='bodyPrint'>%s</tbody>"%itensVenda +
				"</table>"+
				"%s"%viewDesc +
				"<h3><b>SUB-TOTAL</b> = R$ %.2f  |  <b>Tipo pagamento</b> : %s </h3>"%(float(valorVenda), tipoVenda) + 
			"</div>"  +	
			"<hr>" +
			"<a href='cliente?menu=caixa' class='btn btn-default btVolt'>Voltar</a>" +
			"<a href='javascript:window.print()' class='btn btn-info btPrint'>imprimir</a>" 
			# "<nav>" +
			#   "<ul class='pager' style='%s'>"%'width:100px' +
			#     "<li class='previous'><a href='cliente?menu=caixa'><span aria-hidden='true'>&larr;</span> voltar</a></li> "+
			#   "</ul>" +
			# "</nav>"
		)
	
	# comprovante do email sem html
	itensNew = itensVenda
	itensNew = itensNew
	emailSimples = "|---------------- RECIBO DE COMPRA ----------------|\n"\
	" ### ESSE DISPOSITIVO NAO E POSSIVEL VISUALIZAR OS DADOS ###\n"\
	" ### Por gentileza visualize no seu email."


	# comprovante do email com html
	emailHTML = "<html><body>"\
		"<div class='gl'"\
			"<div style='text-align:center'>"\
				"<img src='https://dl.dropboxusercontent.com/u/11469395/Nallu.paiva/logoPrint.png' width='95pt'><hr>" \
			"</div>"\
			"<h3>Recibo de compra Nallubaby ( codigo : %s )</h3>" \
			"<div>"\
				"<table id='myT' style='width:%s'>"\
					"<thead>"\
						"<tr>"\
							"<th>Código</th>"\
							"<th>Qtde</th>"\
							"<th>Produto</th>"\
							"<th>Valor Unidade</th>"\
							"<th>Valor Total</th>"\
						"</tr>"\
					"</thead>"\
					"<tbody>%s</tbody>" \
				"</table>"\
				"%s" \
				"<h3><b>SUB-TOTAL</b> = R$ %.2f  |  <b>Tipo pagamento</b> : %s </h3>" \
			"</div><hr>" \
			"<h3>Muito Obrigado pela compra! Volte sempre."\
		"</div></body></html>"\
		"<style> .btD{display:none} </style>"%(session.venda.codigo,'100%',itensVenda,viewDesc,float(valorVenda),tipoVenda)	
		

	#---- ENVIAR COMPROVANTE AO CLIENTE
	if mail:
	    if mail.send(to=["%s"%session.venda.email],
	        subject='Recibo de compra Nallubaby Cod:',
	        # message= "Hello this is an email send from minerva.com from contact us form.\nName:"+ session.name+" \nEmail : " + session.email +"\nSubject : "+session.subject +"\nMessage : "+session.message+ ".\n "
	    	message=[emailSimples, emailHTML]
	    ):
	        response.flash = 'Recibo enviado por email ao cliente!.'
	    else:
	        response.flash = 'Problema ao enviars o email!'
	else:
	    response.flash = 'Unable to send the email : email parameters not defined'
	
	#---- LIMPAR STORAGE
	session.__delitem__('venda')

	return div		
	
@auth.requires_membership('admin')
def historico():
	return dict(formListar=db(db.historicoVendas.id>0).select())

def buscarVenda():
	#codigo de busca
	busca = request.vars.transitory
	venda = db(db.historicoVendas.codigoVenda == busca).select()


	# dados pego no db
	codigoVenda = busca
	tipoVenda = venda[0].tipoVenda
	valorVenda = venda[0].valorVenda	
	valorDesconto = venda[0].valorDesconto
	vendedor = venda[0].vendedor
	itensVenda =  venda[0].itensVenda

		
	viewDesc = "";
	if valorDesconto != "":
		valorT = (float(valorVenda) + float(valorDesconto))
		viewDesc = "<h3><b>Total</b> : R$ %.2f - <b>Desconto</b> : <span>R$ %.2f</span></h3>"%(valorT, float(valorDesconto))


	# comprovante do email para impressao
	div = XML(
		"<div class='animated fadeIn'>"
			"<div style='text-align:center;display:none' class='logoP'>"+
				"<img src='https://dl.dropboxusercontent.com/u/11469395/Nallu.paiva/logoPrint.png' width='95pt'><hr>" +
			"</div>"+
			"<h3>Recibo de compra Nallubaby ( codigo : %s )</h3><br>"%codigoVenda +		
		"<div id='retornoCliente'>" +
			"<ul class='list-group'>" +
				"<li class='list-group-item'><strong>Cliente: </strong><span id='nn'>Jose</span></li>" +
				"<li class='list-group-item'><strong>Celular : </strong><span>(55) 55555-5555</span></li>" +
				"<li class='list-group-item'><strong>E-mail : </strong><span>jose@gmail.com</span></li>" +
			"</ul> "  +
		"</div>" +
			"<div class='table-responsive'>"+
				"<table class='table table-bordered'>"+
					"<thead>"+
						"<tr>"+
							"<th>Código</th>"+
							"<th>Qtde</th>"+
							"<th>Produto</th>"+
							"<th>Valor Unidade</th>"+
							"<th>Valor Total</th>"+
						"</tr>"+
					"</thead>"+
					"<tbody id='bodyPrint'>%s</tbody>"%itensVenda +
				"</table>"+
				"%s"%viewDesc +
				"<h3><b>SUB-TOTAL</b> = R$ %.2f  |  <b>Tipo pagamento</b> : %s </h3>"%(float(valorVenda), tipoVenda) + 
			"</div>"  +	
			"<hr>" +
			"<a href='historico?menu=caixa' class='btn btn-default btVolt'>Voltar</a>" +
			"<a href='javascript:window.print()' class='btn btn-info btPrint'>imprimir</a>" +
			"</div>"
			# "<nav>" +
			#   "<ul class='pager' style='%s'>"%'width:100px' +
			#     "<li class='previous'><a href='cliente?menu=caixa'><span aria-hidden='true'>&larr;</span> voltar</a></li> "+
			#   "</ul>" +
			# "</nav>"

		)
	return div	


def cancelarVenda():	
	#---- LIMPAR STORAGE
	session.__delitem__('venda')
	return ''


def excluirVendaRegistrada():
    #db(db.historicoVendas.codigoVenda == request.vars.transitory).delete()
    db(db.historicoVendas.codigoVenda == request.vars.transitory).update(deletado=True)
    return ''