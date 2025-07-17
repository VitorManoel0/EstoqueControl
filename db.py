# Configurar o engine e criar as tabelas
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from persistence.data_definition import metadata
import time


def create_database_engine():
    """
    Cria o engine do banco de dados tentando diferentes configurações do Supabase
    """

    # Configurações para tentar (pooling primeiro, depois conexão direta)
    connection_configs = [
        {
            "url": os.environ.get('DATABASE_URL'),
            "description": "Conexão via DATABASE_URL (pooling)"
        },
        {
            "url": os.environ.get('DIRECT_URL'),
            "description": "Conexão via DIRECT_URL (conexão direta)"
        }
    ]

    # Filtra URLs que não são None
    connection_configs = [config for config in connection_configs if config["url"]]

    if not connection_configs:
        raise ValueError("Nem DATABASE_URL nem DIRECT_URL foram definidas nas variáveis de ambiente")

    engine_config = {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 3600,
        "echo": False
    }

    for config in connection_configs:
        try:
            print(f"Tentando conectar: {config['description']}")

            engine = create_engine(config["url"], **engine_config)

            # Testa a conexão usando text() para SQLAlchemy 2.0+
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                test_result = result.fetchone()
                if test_result[0] == 1:
                    print(f"✅ Conexão bem-sucedida: {config['description']}")
                    return engine

        except OperationalError as e:
            print(f"❌ Falha na conexão: {config['description']}")
            print(f"Erro: {e}")
            continue
        except Exception as e:
            print(f"❌ Erro inesperado: {config['description']}")
            print(f"Erro: {e}")
            continue

    raise Exception("Não foi possível conectar ao banco de dados com nenhuma configuração")


def create_tables_with_retry(engine, max_retries=3):
    """
    Cria as tabelas com tentativas de retry
    """
    for attempt in range(max_retries):
        try:
            print(f"Tentativa {attempt + 1} de criar tabelas...")
            metadata.create_all(engine)
            print("✅ Tabelas criadas com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar tabelas (tentativa {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print("Aguardando 2 segundos antes da próxima tentativa...")
                time.sleep(2)
                return None
            else:
                print("Esgotadas as tentativas de criar tabelas")
                raise
    return None

engine = None
SessionLocal = None

try:
    engine = create_database_engine()

    create_tables_with_retry(engine)

    # Configurar o sessionmaker para criar sessões
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print("🎉 Configuração do banco de dados concluída com sucesso!")

except Exception as e:
    print(f"💥 Erro fatal na configuração do banco: {e}")
    print("\n🔍 Possíveis soluções:")
    print("1. Verifique se o projeto Supabase está ativo no dashboard")
    print("2. Confirme se a senha está correta na variável de ambiente")
    print("3. Verifique as configurações de rede/firewall")
    print("4. Tente habilitar conexões diretas no Supabase")
    print("5. Defina as variáveis DATABASE_URL e/ou DIRECT_URL")
    raise

def get_db():
    """
    Dependência para obter uma sessão do banco de dados.
    """
    if SessionLocal is None:
        raise Exception("Banco de dados não foi inicializado corretamente")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
