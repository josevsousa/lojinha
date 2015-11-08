# navAbas = UL(
# 	LI(A('Cliente',_href="#home", _toggle="tab"),_class="active",_role="presentation"),
# 	LI(A('Cliente',_href="#profile", _toggle="tab", _data-toggle="tab"),_role="presentation")
# 	,_class="nav nav-tabs",_role="tablist")

# if not session.sTotalRow:
# 	session.sTotalRow = 0

# venda = session
if not session.venda:
	session.venda = Storage()
	session.venda.sTotal = 0

if not session.venda.itens:
    session.venda.itens = DIV()  

