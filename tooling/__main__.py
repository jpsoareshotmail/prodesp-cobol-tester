"""
CLI da ferramenta de geracao automatica de estrutura de dados.

Uso (a partir da raiz do projeto):

  # Gerar DDL + massa de todas as tabelas
  py -m tooling gerar --programas fontes_convertidos/Convertidos \
                       --copybooks cobol_build/copy \
                       --out saida_estrutura --massa 10

  # Ver DDL de um unico copybook
  py -m tooling ddl --copybook "entregas/.../MAPA_COFI04.cpy" --tabela COFI04DS

  # Gerar massa de um unico copybook
  py -m tooling massa --copybook "entregas/.../MAPA_COFI04.cpy" --tabela COFI04DS --linhas 5
"""
import argparse
import sys
from pathlib import Path


def cmd_gerar(args):
    from tooling.orchestrator import gerar_tudo
    copybooks = args.copybooks or []
    res = gerar_tudo(args.programas, copybooks, args.out, n_massa=args.massa)
    print(f"Tabelas processadas : {res['tabelas']}")
    print(f"Campos de copybook  : {res['campos_copybook']}")
    print(f"Arquivos gerados em : {res['out']}")
    print("  - schema.sql (DDL)")
    print("  - massa.sql  (INSERTs)")
    print("  - relatorio.md (cobertura fiel x inferido)")


def cmd_ddl(args):
    from tooling.ddl_generator import gerar_ddl_de_arquivo
    print(gerar_ddl_de_arquivo(args.copybook, table_name=args.tabela, schema=args.schema))


def cmd_massa(args):
    from tooling.data_generator import gerar_de_arquivo
    print(gerar_de_arquivo(args.copybook, table_name=args.tabela, n=args.linhas, schema=args.schema))


def main(argv=None):
    p = argparse.ArgumentParser(prog='tooling', description='Gerador de DDL e massa a partir de COBOL + copybooks')
    sub = p.add_subparsers(dest='cmd', required=True)

    g = sub.add_parser('gerar', help='Gera DDL + massa de todas as tabelas')
    g.add_argument('--programas', required=True, help='pasta dos programas COBOL convertidos')
    g.add_argument('--copybooks', action='append', help='pasta(s) de copybooks (pode repetir)')
    g.add_argument('--out', default='saida_estrutura', help='pasta de saida')
    g.add_argument('--massa', type=int, default=10, help='linhas de massa por tabela')
    g.set_defaults(func=cmd_gerar)

    d = sub.add_parser('ddl', help='DDL de um copybook')
    d.add_argument('--copybook', required=True)
    d.add_argument('--tabela', default=None)
    d.add_argument('--schema', default=None)
    d.set_defaults(func=cmd_ddl)

    m = sub.add_parser('massa', help='massa de um copybook')
    m.add_argument('--copybook', required=True)
    m.add_argument('--tabela', default=None)
    m.add_argument('--schema', default=None)
    m.add_argument('--linhas', type=int, default=10)
    m.set_defaults(func=cmd_massa)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    sys.exit(main())
