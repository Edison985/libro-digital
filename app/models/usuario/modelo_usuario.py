from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime



class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"
    usu_id: Optional[int] = Field(default=None, primary_key=True)
    usu_nombre: str = Field(max_length=50)
    usu_correo: str = Field(max_length=100, unique=True)
    usu_clave: str
    usu_verificado: bool = Field(default=False)
    usu_fecharegistro: datetime = Field(default_factory=datetime.utcnow)
    usu_idrol: Optional[int] = Field(default=None, foreign_key="rol.rol_id")

    rol: Optional["Rol"] = Relationship(back_populates="usuarios")

class UsuarioCreate(SQLModel):
    usu_nombre: str
    usu_correo: str
    usu_clave: str


class UsuarioUpdate(SQLModel):
    usu_nombre: Optional[str] = None
    usu_correo: Optional[str] = None
    usu_clave: Optional[str] = None


class UsuarioResponse(SQLModel):
    usu_id: int
    usu_nombre: str
    usu_correo: str
    usu_verificado: bool
    usu_fecharegistro: datetime
    usu_idrol: Optional[int]
    