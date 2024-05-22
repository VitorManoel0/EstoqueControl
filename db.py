# Configurar o engine e criar as tabelas
from sqlalchemy import create_engine

from persistence.data_definition import metadata

DATABASE_URL = 'sqlite:///mydatabase.db'  # Troque 'sqlite' pelo SGBD de sua preferência
engine = create_engine(DATABASE_URL)

# Criar todas as tabelas no banco de dados
metadata.create_all(engine)

print("Tabelas criadas com sucesso!")