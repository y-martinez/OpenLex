# -*- coding: utf-8 -*-

db = DAL('sqlite://storage_new.sqlite')
from gluon.tools import *

auth = Auth(globals(),db)
auth.define_tables()
crud = Crud(globals(),db)

db.define_table('persona',
                Field('sexo',requires = IS_IN_SET({'F':'Femenino', 'M':'Masculino', 'J':'Persona Jurídica'},
                                                   zero=T('Elija persona jurídica o sexo'),
                                                   error_message='debe elegir persona jurídica o sexo persona física')),
                Field('apellido',required=True,label=T('Apellido o Razón Social')),
                Field('nombre',label=T('Nombre')),
                Field('domicilio',required=True,label=T('Domicilio')),
                Field('cuitcuil',required=True,label=T('CUIT/CUIL')),
                Field('fotografia','upload',requires = IS_EMPTY_OR(IS_IMAGE())),
                auth.signature,
               format='%(cuitcuil)s %(apellido)s,%(nombre)s')
db.persona.id.readable=db.persona.id.writable=False

db.define_table('fuero',
                Field('descripcion',required=True,label=T('Descripción')),
               format='%(descripcion)s')
db.fuero.id.readable=db.fuero.id.writable=False

db.define_table('instancia',
                Field('descripcion',required=True,label=T('Descripción')),
               format='%(descripcion)s')
db.instancia.id.readable=db.instancia.id.writable=False

db.define_table('juzgado',
                Field('descripcion',required=True,label=T('Descripción')),
                Field('fuero_id',db.fuero,label=T('Fuero')),
                Field('instancia_id',db.instancia,label=T('Instancia')),
                auth.signature)
db.juzgado.fuero_id.widget = SQLFORM.widgets.autocomplete(
     request, db.fuero.descripcion, id_field=db.fuero.id)
db.juzgado.instancia_id.widget = SQLFORM.widgets.autocomplete(
     request, db.instancia.descripcion, id_field=db.instancia.id)
db.juzgado.fuero_id.requires = IS_IN_DB(db,db.fuero.id,'%(descripcion)s')
db.juzgado.instancia_id.requires = IS_IN_DB(db,db.instancia.id,'%(descripcion)s')
db.juzgado.descripcion.requires = IS_NOT_IN_DB(db, 'juzgado.descripcion')
db.juzgado.id.readable=db.juzgado.id.writable=False

db.define_table('expediente',
                Field('numero',requires = IS_NOT_IN_DB(db, 'expediente.numero'),label=T('Nº de expediente')),
                Field('caratula',required=True, label=T('Carátula')),
                Field('juzgado_id',db.juzgado, label=T('Juzgado o Fiscalía de origen')),
                Field('inicio','date', label=T('Fecha inicio')),
                Field('final','date', label=T('Fecha fin')),
                auth.signature,
               format='%(numero)s %(caratula)s')
db.expediente.id.readable=db.expediente.id.writable=False
db.expediente.juzgado_id.widget = SQLFORM.widgets.autocomplete(
     request, db.juzgado.descripcion, id_field=db.juzgado.id)

db.define_table('movimiento',
                Field('expediente_id',db.expediente),
                Field('procesal',requires = IS_IN_SET({'P':'Procesal', 'E':'Extraprocesal'},
                                                   zero=None,
                                                   error_message='Seleccione estado del campo')),
                Field('titulo',required=True, label=T('Título')),
                Field('texto','text',label=T('Texto'),requires = IS_NOT_EMPTY()),
                Field('archivo','upload'),
                auth.signature,
               format='%(titulo)s')
db.movimiento.expediente_id.readable=db.movimiento.expediente_id.writable=False
db.movimiento.id.readable=db.movimiento.id.writable=False
db.movimiento._singular = T("Movimiento")
db.movimiento._plural = T("Movimientos")

db.define_table('agenda',
                Field('expediente_id',db.expediente),
                Field('vencimiento','datetime'),
                Field('titulo',required=True, label=T('Título')),
                Field('texto','text',label=T('Texto'),requires = IS_NOT_EMPTY()),
                auth.signature)
