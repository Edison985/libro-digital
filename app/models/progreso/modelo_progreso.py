from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ProgresoLectura(SQLModel, table=True):
    pro_id: Optional[int] = Field(default=None, primary_key=True)
    pro_idusuario: Optional[int] = Field(default=None, foreign_key="usuario.usu_id")
    pro_idlibro: Optional[int] = Field(default=None, foreign_key="libro.lib_id")
    pro_pagina_actual: Optional[int] = None
    pro_porcentaje: Optional[float] = None
    pro_ultimo_acceso: datetime = Field(default_factory=datetime.utcnow)