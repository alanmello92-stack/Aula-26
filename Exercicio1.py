import mysql.connector
import pandas as pd
import matplotlib.pyplot as pyplot
from mysql.connector import Error

# 1) Cursos (ids gerados: 1, 2, 3)
cursos = [
    # (Nome_curso, Carga_horaria, Turno)
    ('Informática',    800,  'Manhã'),
    ('Administração',  1000, 'Noite'),
    ('Enfermagem',     1200, 'Tarde'),
]

# 2) Alunos (ids gerados: 1 a 10) — o último campo é o id_curso (FK)
# 1 = Informática, 2 = Administração, 3 = Enfermagem
alunos = [
    # (Nome, CPF, Nascimento, Matricula, ID_curso)
    ('Ana Souza',      '11122233344', '2005-03-14', 14357, 1),  # id 1
    ('Bruno Lima',     '22233344455', '2004-07-22', 98563, 1),  # id 2
    ('Carla Mendes',   '33344455566', '2003-11-05', 27643, 2),  # id 3
    ('Diego Ferreira', '44455566677', '2006-01-30', 36506, 3),  # id 4
    ('Joana Ribeiro',  '55566677788', '2005-04-21', 54194, 1),  # id 5
    ('Lucas Martins',  '66677788899', '2004-09-10', 54763, 1),  # id 6
    ('Mariana Costa',  '77788899900', '2003-12-02', 54371, 3),  # id 7
    ('Pedro Alves',    '88899900011', '2006-06-18', 45391, 2),  # id 8
    ('Rafaela Nunes',  '99900011122', '2005-08-25', 55123, 3),  # id 9
    ('Thiago Rocha',   '10120230344', '2004-02-14', 77623, 1),  # id 10
]

# 3) Disciplinas (ids gerados: 1 a 6) — o último campo é o id_curso (FK)
disciplinas = [
    # (Nome_disciplina, Carga_horaria, ID_curso)
    (1, 'Lógica de Programação', 80, 1),  # id 1
    (2, 'Banco de Dados',        60, 1),  # id 2
    (3, 'Gestão Financeira',     60, 2),  # id 3
    (4, 'Marketing',             40, 2),  # id 4
    (5, 'Anatomia',              80, 3),  # id 5
    (6, 'Farmacologia',          60, 3),  # id 6
]

# 4) Notas — cada aluno recebe nota nas disciplinas do seu curso
notas = [
    # (ID_nota, nota, data_avaliacao, ID_aluno, id_disciplina)
 # Ana Souza - Informática
    (1, 8.5, '2026-03-10', 1, 1),
    (2, 9.0, '2026-03-15', 1, 2),

    # Bruno Lima - Informática
    (3, 7.5, '2026-03-10', 2, 1),
    (4, 8.0, '2026-03-15', 2, 2),

    # Carla Mendes - Administração
    (5, 9.0, '2026-03-12', 3, 3),
    (6, 8.5, '2026-03-18', 3, 4),

    # Diego Ferreira - Enfermagem
    (7, 7.0, '2026-03-11', 4, 5),
    (8, 8.5, '2026-03-17', 4, 6),

    # Joana Ribeiro - Informática
    (9, 9.5, '2026-03-10', 5, 1),
    (10, 9.0, '2026-03-15', 5, 2),

    # Lucas Martins - Informática
    (11, 6.5, '2026-03-10', 6, 1),
    (12, 7.5, '2026-03-15', 6, 2),

    # Mariana Costa - Enfermagem
    (13, 8.0, '2026-03-11', 7, 5),
    (14, 9.0, '2026-03-17', 7, 6),

    # Pedro Alves - Administração
    (15, 7.5, '2026-03-12', 8, 3),
    (16, 8.0, '2026-03-18', 8, 4),

    # Rafaela Nunes - Enfermagem
    (17, 9.5, '2026-03-11', 9, 5),
    (18, 8.5, '2026-03-17', 9, 6),

    # Thiago Rocha - Informática
    (19, 8.0, '2026-03-10', 10, 1),
    (20, 7.0, '2026-03-15', 10, 2),
]

try:
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='escola' 
    )
    if conexao.is_connected():
        print("conectado com sucesso!")

        cursor = conexao.cursor()
        inserts= [
        ("cursos",
        "INSERT IGNORE INTO cursos (Nome_curso, Carga_horaria, Turno) "
        "VALUES (%s,%s,%s)",
        cursos),
        ("alunos",
        "INSERT IGNORE INTO alunos(Nome, CPF, Nascimento, Matricula, ID_curso) "
        "VALUES (%s, %s, %s, %s, %s)",
         alunos),
        ("disciplinas",
        "INSERT IGNORE INTO disciplinas (Nome_disciplina, Carga_horaria, ID_curso) "
        "VALUES (%s, %s, %s)",
        disciplinas),
        ("notas",
        "INSERT IGNORE INTO notas (ID_nota, nota, data_avaliacao, ID_aluno, id_disciplina) "
        "VALUES (%s, %s, %s, %s, %s)",
        notas),
        ]

        for tabela, sql, valores in inserts:
            cursor.executemany(sql, valores)
            conexao.commit()
            print(f"{tabela}: {cursor.rowcount} linha(s) inserida(s)")


        consulta = """
            SELECT a.ID_aluno, a.Nome, c.Nome_curso, c.Turno,
            d.Nome_disciplina, n.Nota, n.Data_avaliacao
            FROM notas n
            INNER JOIN alunos a ON n.ID_aluno = a.ID_aluno
            INNER JOIN disciplina d ON n.ID_disciplina = d.ID_disciplina
            INNER JOIN cursos      c ON a.ID_curso      = c.ID_curso
            ORDER BY c.Nome_curso, a.Nome, d.Nome_disciplina
            """
        
        cursor.execute(consulta)

        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        df["Nota"] = df["Nota"].astype(float)

        print("\nDataframe(Notas + Alunos + Disciplinas + Cursos):")
        print(df)


        df.to_csv("notas_alunos.csv", index=False, encoding="utf-8-sig")
        print("\nArquivo notas_alunos.CSV gerado!")

except Error as e:
    print(f"Erro ao conectar ou executar:{e}")

finally:
    if 'cursor' in locals():
        try:
            cursor.close()
        except Exception:
            pass
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
        print("Conexão encerrada.")

