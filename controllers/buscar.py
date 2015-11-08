# -*- coding: utf-8 -*-

def index():
	form = crud.search(db.historicoVendas)
	return dict(form=form)
