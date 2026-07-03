#!/usr/bin/env python3
"""
Suite de Testes Expandida - Sistema COBOL Legado Prodesp
Executa testes para todos os programas disponíveis
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import sys
sys.path.insert(0, '.')

from executor_cobol import ExecutorCOBOL
try:
    from executor_cobol import ValidadorPlaca
except ImportError:
    # Se não está em executor_cobol, importar de runner.py
    import importlib.util
    spec = importlib.util.spec_from_file_location("runner", "runner.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    ValidadorPlaca = runner.ValidadorPlaca

@dataclass
class TestResult:
    """Resultado de um teste"""
    test_id: str
    nome: str
    programa: str
    categoria: str
    status: str  # PASS, FAIL, SKIP, ERROR
    entrada: str
    saida_esperada: str
    saida_obtida: str
    tempo_ms: float
    mensagem: str = ""

class TestSuiteExpanded:
    """Suite de testes expandida para todos os programas COBOL"""

    def __init__(self, programas_selecionados: List[str] = None):
        # Usar diretório atual para funcionar em qualquer lugar (local ou Render)
        base_dir = Path(__file__).parent
        self.executor = ExecutorCOBOL(str(base_dir))
        self.resultados: List[TestResult] = []
        self.tempo_inicio = None
        self.programas = self._descobrir_programas()
        self.programas_selecionados = programas_selecionados  # None = todos

    def _descobrir_programas(self) -> Dict:
        """Descobre todos os programas COBOL disponíveis"""
        # Usar caminho relativo para funcionar em qualquer lugar (local ou Render)
        codigo_dir = Path(__file__).parent / "PGM POC cob original"

        # Fallback para caminho absoluto (compatibilidade com código antigo)
        if not codigo_dir.exists():
            codigo_dir = Path("PGM POC cob original")

        programas = {}

        # Agrupar por tipo de programa
        for arquivo in codigo_dir.glob("*.C74"):
            nome = arquivo.stem

            # Classificar por padrão
            if "GAA" in nome:
                tipo = "GAA"
                descricao = "Gestão Arquivo Automotivo"
            elif "GEV" in nome:
                tipo = "GEV"
                descricao = "Gestão Empadronização Veicular"
            elif "GAT" in nome:
                tipo = "GAT"
                descricao = "Gestão Autoridades"
            else:
                tipo = "OUTRO"
                descricao = "Outro"

            if tipo not in programas:
                programas[tipo] = []

            programas[tipo].append({
                "nome": nome,
                "arquivo": arquivo.name,
                "descricao": descricao,
                "caminho": str(arquivo),
            })

        return programas

    def executar_todos(self) -> Dict:
        """Executa testes para todos os programas"""
        print("\n" + "=" * 80)
        print("[*] INICIANDO SUITE DE TESTES EXPANDIDA - SISTEMA COBOL PRODESP")
        print("=" * 80)
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Programas encontrados: {self._contar_programas()}")
        print("")

        self.tempo_inicio = time.time()

        # Executar testes por tipo de programa
        self._testes_validador_placa()  # PF-GAA-L004
        self._testes_outros_programas()  # Outros programas

        tempo_total = time.time() - self.tempo_inicio

        # Gerar relatório
        relatorio = self._gerar_relatorio(tempo_total)
        return relatorio

    def _contar_programas(self) -> int:
        """Conta total de programas"""
        total = 0
        for tipo, progs in self.programas.items():
            total += len(progs)
        return total

    def get_programas_disponiveis(self) -> Dict:
        """Retorna lista de programas disponíveis para teste"""
        resultado = {}
        for tipo, progs in self.programas.items():
            resultado[tipo] = [
                {
                    "nome": p["nome"],
                    "arquivo": p["arquivo"],
                    "descricao": p["descricao"],
                }
                for p in progs
            ]
        return resultado

    def _testes_validador_placa(self):
        """Testes unitários do validador de placas (PF-GAA-L004)"""
        print("[INICIANDO] Testes do Validador de Placas (PF-GAA-L004)")
        print("-" * 80)

        casos_teste = [
            ("TC-001", "AAA0A00", 11, "Mercosul - Sao Paulo"),
            ("TC-002", "ABC1234", 11, "Mercosul - Sao Paulo"),
            ("TC-003", "JWD0A00", 11, "Mercosul - Sao Paulo (ultima faixa)"),
            ("TC-004", "XYZ1234", 12, "Mercosul - Outros Estados"),
            ("TC-005", "MNO5678", 12, "Mercosul - Outros Estados"),
            ("TC-006", "SP1234", 21, "Antiga - Sao Paulo (SP)"),
            ("TC-007", "RJ1234", 22, "Antiga - Outros Estados"),
            ("TC-008", "MG2468", 22, "Antiga - Outros Estados (MG)"),
            ("TC-009", "AB12C34", 33, "2 letras - Carros"),
            ("TC-010", "XY9876", 33, "2 letras - Carros"),
            ("TC-020", "", 0, "Placa vazia"),
            ("TC-021", "   ", 0, "Placa com espacos"),
            ("TC-030", "ABC-1234", 0, "Com hifen"),
            ("TC-031", "ABC 1234", 0, "Com espaco no meio"),
            ("TC-032", "ABC.1234", 0, "Com ponto"),
            ("TC-033", "ABC@1234", 0, "Com @ (especial)"),
            ("TC-034", "ABC/1234", 0, "Com barra"),
        ]

        for test_id, entrada, saida_esperada, descricao in casos_teste:
            tempo_inicio = time.time()

            validador = ValidadorPlaca()
            resultado = validador.validar(entrada)

            tempo_ms = (time.time() - tempo_inicio) * 1000
            saida_obtida = resultado.codigo

            status = "PASS" if saida_obtida == saida_esperada else "FAIL"

            test_result = TestResult(
                test_id=test_id,
                nome=descricao,
                programa="PF-GAA-L004",
                categoria="Validador",
                status=status,
                entrada=entrada if entrada else "(vazio)",
                saida_esperada=str(saida_esperada),
                saida_obtida=str(saida_obtida),
                tempo_ms=tempo_ms,
                mensagem=resultado.descricao,
            )

            self.resultados.append(test_result)

            simbolo = "[OK]" if status == "PASS" else "[XX]"
            print(f"{simbolo} {test_id}: {entrada:10} -> {saida_obtida:3} (esperado {saida_esperada:3})")

        print()

    def _testes_outros_programas(self):
        """Testes genéricos para outros programas"""
        print("[INICIANDO] Testes de Disponibilidade - Outros Programas")
        print("-" * 80)

        # Testar se os arquivos existem
        contador = 0
        for tipo, programas in self.programas.items():
            if tipo == "GAA":  # Já testamos GAA-L004
                continue

            for prog_info in programas:
                # Se há seleção, verificar se este programa está selecionado
                if self.programas_selecionados and prog_info["nome"] not in self.programas_selecionados:
                    continue
                contador += 1
                prog_nome = prog_info["nome"]

                try:
                    caminho = Path(prog_info["caminho"])
                    arquivo_existe = caminho.exists()

                    if arquivo_existe:
                        # Ler primeiras linhas para validar
                        with open(caminho, 'r', encoding='latin-1', errors='ignore') as f:
                            conteudo = f.read(500)
                            tem_programa_id = "PROGRAM-ID" in conteudo or "IDENTIFICATION" in conteudo

                        status = "PASS" if tem_programa_id else "FAIL"
                        mensagem = "Arquivo COBOL válido" if tem_programa_id else "Arquivo inválido"
                    else:
                        status = "FAIL"
                        mensagem = "Arquivo não encontrado"

                    test_result = TestResult(
                        test_id=f"SYS-{contador:03d}",
                        nome=prog_nome,
                        programa=prog_nome,
                        categoria=tipo,
                        status=status,
                        entrada="N/A",
                        saida_esperada="Disponível",
                        saida_obtida="OK" if status == "PASS" else "Erro",
                        tempo_ms=0.1,
                        mensagem=mensagem,
                    )

                    self.resultados.append(test_result)

                    simbolo = "[OK]" if status == "PASS" else "[XX]"
                    print(f"{simbolo} {prog_nome:30} {mensagem}")

                except Exception as e:
                    test_result = TestResult(
                        test_id=f"SYS-{contador:03d}",
                        nome=prog_nome,
                        programa=prog_nome,
                        categoria=tipo,
                        status="ERROR",
                        entrada="N/A",
                        saida_esperada="Disponível",
                        saida_obtida="Erro",
                        tempo_ms=0.1,
                        mensagem=str(e)[:50],
                    )

                    self.resultados.append(test_result)
                    print(f"[ER] {prog_nome:30} Erro: {str(e)[:40]}")

        print()

    def _gerar_relatorio(self, tempo_total: float) -> Dict:
        """Gera relatório consolidado"""

        # Contar resultados
        total = len(self.resultados)
        passed = sum(1 for r in self.resultados if r.status == "PASS")
        failed = sum(1 for r in self.resultados if r.status == "FAIL")
        errored = sum(1 for r in self.resultados if r.status == "ERROR")

        taxa_sucesso = (passed / total * 100) if total > 0 else 0

        # Imprimir relatório
        print("=" * 80)
        print("RELATORIO DE TESTES EXPANDIDO")
        print("=" * 80)
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duracao: {tempo_total:.2f} segundos")
        print(f"Programas testados: {self._contar_programas()}")
        print("")

        print("RESUMO EXECUTIVO:")
        print(f"  Total de Testes: {total}")
        print(f"  Passaram:        {passed} ({passed/total*100:.1f}%)")
        print(f"  Falharam:        {failed} ({failed/total*100:.1f}%)")
        print(f"  Erros:           {errored} ({errored/total*100:.1f}%)")
        print(f"  Taxa de Sucesso: {taxa_sucesso:.1f}%")
        print("")

        # Resultado por categoria/programa
        categorias = {}
        for resultado in self.resultados:
            cat = resultado.categoria
            if cat not in categorias:
                categorias[cat] = {"total": 0, "pass": 0, "fail": 0, "error": 0}
            categorias[cat]["total"] += 1
            if resultado.status == "PASS":
                categorias[cat]["pass"] += 1
            elif resultado.status == "FAIL":
                categorias[cat]["fail"] += 1
            else:
                categorias[cat]["error"] += 1

        print("RESULTADOS POR CATEGORIA:")
        for cat in sorted(categorias.keys()):
            stats = categorias[cat]
            pct = stats["pass"] / stats["total"] * 100 if stats["total"] > 0 else 0
            print(f"  {cat:25} {stats['pass']}/{stats['total']} ({pct:5.1f}%)")
        print("")

        # Testes que falharam
        falhados = [r for r in self.resultados if r.status != "PASS"]
        if falhados:
            print("TESTES QUE FALHARAM:")
            for resultado in falhados[:10]:  # Mostrar apenas os primeiros 10
                print(f"  [{resultado.test_id}] {resultado.programa:20} {resultado.nome}")
            if len(falhados) > 10:
                print(f"  ... e mais {len(falhados) - 10} testes")
            print("")

        # Recomendacoes
        print("RECOMENDACOES:")
        if taxa_sucesso == 100:
            print("  [OK] Todos os testes passaram! Sistema pronto para deploy.")
        elif taxa_sucesso >= 95:
            print("  [AVISO] Taxa de sucesso > 95%. Revisar testes que falharam.")
        elif taxa_sucesso >= 80:
            print("  [CRITICO] Taxa de sucesso < 95%. Corrigir erros antes de deploy.")
        else:
            print("  [CRITICO] Taxa de sucesso < 80%. Nao recomendado para deploy.")

        print("")
        print("=" * 80)

        return {
            "data": datetime.now().isoformat(),
            "duracao": tempo_total,
            "total": total,
            "passed": passed,
            "failed": failed,
            "errored": errored,
            "taxa_sucesso": taxa_sucesso,
            "programas_testados": self._contar_programas(),
            "resultados": [asdict(r) for r in self.resultados],
        }

    def salvar_relatorio(self, relatorio: Dict, formato: str = "json"):
        """Salva relatório em arquivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if formato == "json":
            arquivo = f"TEST_RESULTS_EXPANDED_{timestamp}.json"
            with open(arquivo, "w") as f:
                json.dump(relatorio, f, indent=2)
            print(f"\nRelatorio JSON salvo em: {arquivo}")


def main():
    """Função principal"""

    # Executar testes
    suite = TestSuiteExpanded()

    try:
        relatorio = suite.executar_todos()
        suite.salvar_relatorio(relatorio)

        # Exit code
        if relatorio["taxa_sucesso"] >= 95:
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n[!] Testes interrompidos pelo usuario")
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERRO] Erro ao executar testes: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
