# Configurar o engine e criar as tabelas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from persistence.data_definition import metadata

DATABASE_URL = 'sqlite:///mydatabase.db'  # Troque 'sqlite' pelo SGBD de sua preferência
engine = create_engine(DATABASE_URL)

# Criar todas as tabelas no banco de dados
metadata.create_all(engine)

print("Tabelas criadas com sucesso!")

# Configurar o sessionmaker para criar sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Função para obter uma nova sessão
def get_db():
    """
    Dependência para obter uma sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
