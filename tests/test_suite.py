#!/usr/bin/env python3
"""
Suite de Testes Automatizados - Sistema COBOL Legado Prodesp
Executa testes unitarios, integracao e regressao
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
sys.path.insert(0, str(Path(__file__).parent.parent))
from app.executor_cobol import ExecutorCOBOL

@dataclass
class TestResult:
    """Resultado de um teste"""
    test_id: str
    nome: str
    categoria: str
    status: str  # PASS, FAIL, SKIP, ERROR
    entrada: str
    saida_esperada: str
    saida_obtida: str
    tempo_ms: float
    mensagem: str = ""

class TestSuite:
    """Suite de testes para COBOL"""

    def __init__(self):
        # Usar diretório atual para funcionar em qualquer lugar (local ou Render)
        base_dir = Path(__file__).parent
        self.executor = ExecutorCOBOL(str(base_dir))
        self.resultados: List[TestResult] = []
        self.tempo_inicio = None

    def executar_todos(self) -> Dict:
        """Executa toda a suite de testes"""
        print("\n" + "=" * 80)
        print("[*] INICIANDO SUITE DE TESTES - SISTEMA COBOL PRODESP")
        print("=" * 80)
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")

        self.tempo_inicio = time.time()

        # Executar grupos de testes
        self._testes_validador_placa()
        self._testes_casos_limite()
        self._testes_caracteres_especiais()
        self._testes_performance()

        tempo_total = time.time() - self.tempo_inicio

        # Gerar relatorio
        relatorio = self._gerar_relatorio(tempo_total)
        return relatorio

    def _testes_validador_placa(self):
        """Testes unitarios do validador de placas"""
        print("[INICIANDO] Testes do Validador de Placas (PF-GAA-L004)")
        print("-" * 80)

        casos_teste = [
            # ID, Entrada, Saida Esperada, Descricao
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
        ]

        for test_id, entrada, saida_esperada, descricao in casos_teste:
            tempo_inicio = time.time()
            resultado = self.executor.executar_programa("PF-GAA-L004", entrada)
            tempo_ms = (time.time() - tempo_inicio) * 1000

            saida_obtida = resultado.get("codigo", -1)
            status = "PASS" if saida_obtida == saida_esperada else "FAIL"

            test_result = TestResult(
                test_id=test_id,
                nome=descricao,
                categoria="Validador",
                status=status,
                entrada=entrada,
                saida_esperada=str(saida_esperada),
                saida_obtida=str(saida_obtida),
                tempo_ms=tempo_ms,
                mensagem=resultado.get("descricao", ""),
            )

            self.resultados.append(test_result)

            simbolo = "[OK]" if status == "PASS" else "[XX]"
            print(f"{simbolo} {test_id}: {entrada:10} -> {saida_obtida:3} (esperado {saida_esperada:3})")

        print()

    def _testes_casos_limite(self):
        """Testes de casos limite e bordas"""
        print("[INICIANDO] Testes de Casos Limite")
        print("-" * 80)

        casos_teste = [
            ("TC-020", "", 0, "Placa vazia"),
            ("TC-021", "   ", 0, "Placa com espacos"),
            ("TC-022", "123456", 0, "Apenas numeros"),
            ("TC-023", "ABCDEF", 0, "Apenas letras"),
            ("TC-024", None, 0, "Valor nulo"),
        ]

        for test_id, entrada, saida_esperada, descricao in casos_teste:
            if entrada is None:
                print(f"[-] {test_id}: {descricao} (SKIP)")
                continue

            tempo_inicio = time.time()
            try:
                resultado = self.executor.executar_programa("PF-GAA-L004", entrada)
                saida_obtida = resultado.get("codigo", -1)
                tempo_ms = (time.time() - tempo_inicio) * 1000

                status = "PASS" if saida_obtida == saida_esperada else "FAIL"

                test_result = TestResult(
                    test_id=test_id,
                    nome=descricao,
                    categoria="Casos Limite",
                    status=status,
                    entrada=repr(entrada),
                    saida_esperada=str(saida_esperada),
                    saida_obtida=str(saida_obtida),
                    tempo_ms=tempo_ms,
                )

                self.resultados.append(test_result)

                simbolo = "[OK]" if status == "PASS" else "[XX]"
                print(f"{simbolo} {test_id}: {repr(entrada):20} -> {saida_obtida:3}")

            except Exception as e:
                tempo_ms = (time.time() - tempo_inicio) * 1000
                test_result = TestResult(
                    test_id=test_id,
                    nome=descricao,
                    categoria="Casos Limite",
                    status="ERROR",
                    entrada=repr(entrada),
                    saida_esperada=str(saida_esperada),
                    saida_obtida="ERRO",
                    tempo_ms=tempo_ms,
                    mensagem=str(e),
                )
                self.resultados.append(test_result)
                print(f"[ER] {test_id}: ERRO - {str(e)[:50]}")

        print()

    def _testes_caracteres_especiais(self):
        """Testes com caracteres especiais"""
        print("[INICIANDO] Testes com Caracteres Especiais")
        print("-" * 80)

        casos_teste = [
            ("TC-030", "ABC-1234", 0, "Com hifen"),
            ("TC-031", "ABC 1234", 0, "Com espaco no meio"),
            ("TC-032", "ABC.1234", 0, "Com ponto"),
            ("TC-033", "ABC@1234", 0, "Com @ (especial)"),
            ("TC-034", "ABC/1234", 0, "Com barra"),
        ]

        for test_id, entrada, saida_esperada, descricao in casos_teste:
            tempo_inicio = time.time()
            resultado = self.executor.executar_programa("PF-GAA-L004", entrada)
            saida_obtida = resultado.get("codigo", -1)
            tempo_ms = (time.time() - tempo_inicio) * 1000

            status = "PASS" if saida_obtida == saida_esperada else "FAIL"

            test_result = TestResult(
                test_id=test_id,
                nome=descricao,
                categoria="Caracteres Especiais",
                status=status,
                entrada=entrada,
                saida_esperada=str(saida_esperada),
                saida_obtida=str(saida_obtida),
                tempo_ms=tempo_ms,
            )

            self.resultados.append(test_result)

            simbolo = "[OK]" if status == "PASS" else "[XX]"
            print(f"{simbolo} {test_id}: {entrada:15} -> {saida_obtida:3}")

        print()

    def _testes_performance(self):
        """Testes de performance"""
        print("[INICIANDO] Testes de Performance")
        print("-" * 80)

        # Teste de velocidade com 100 chamadas
        entradas = ["AAA0A00", "ABC1234", "SP1234", "AB12C34", ""]
        tempo_total = 0

        print("Executando 100 validacoes...")
        for i in range(100):
            entrada = entradas[i % len(entradas)]
            tempo_inicio = time.time()
            self.executor.executar_programa("PF-GAA-L004", entrada)
            tempo_total += time.time() - tempo_inicio

        tempo_medio = (tempo_total / 100) * 1000  # em ms
        throughput = 1000 / tempo_medio  # validacoes por segundo

        status = "PASS" if tempo_medio < 100 else "FAIL"

        test_result = TestResult(
            test_id="TC-100",
            nome="Performance: 100 validacoes",
            categoria="Performance",
            status=status,
            entrada="100 x mixed",
            saida_esperada="< 100ms por chamada",
            saida_obtida=f"{tempo_medio:.2f}ms",
            tempo_ms=tempo_total * 1000,
            mensagem=f"{throughput:.0f} validacoes/segundo",
        )

        self.resultados.append(test_result)

        print(f"Tempo medio: {tempo_medio:.2f}ms")
        print(f"Throughput: {throughput:.0f} validacoes/segundo")
        print(f"Status: {status}")
        print()

    def _gerar_relatorio(self, tempo_total: float) -> Dict:
        """Gera relatorio consolidado"""

        # Contar resultados
        total = len(self.resultados)
        passed = sum(1 for r in self.resultados if r.status == "PASS")
        failed = sum(1 for r in self.resultados if r.status == "FAIL")
        errored = sum(1 for r in self.resultados if r.status == "ERROR")
        skipped = sum(1 for r in self.resultados if r.status == "SKIP")

        taxa_sucesso = (passed / total * 100) if total > 0 else 0

        # Imprimir relatorio
        print("=" * 80)
        print("RELATORIO DE TESTES")
        print("=" * 80)
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duracao: {tempo_total:.2f} segundos")
        print("")

        print("RESUMO EXECUTIVO:")
        print(f"  Total de Testes: {total}")
        print(f"  Passaram:        {passed} ({passed/total*100:.1f}%)")
        print(f"  Falharam:        {failed} ({failed/total*100:.1f}%)")
        print(f"  Erros:           {errored} ({errored/total*100:.1f}%)")
        print(f"  Pulados:         {skipped}")
        print(f"  Taxa de Sucesso: {taxa_sucesso:.1f}%")
        print("")

        # Resultado por categoria
        categorias = {}
        for resultado in self.resultados:
            cat = resultado.categoria
            if cat not in categorias:
                categorias[cat] = {"total": 0, "pass": 0, "fail": 0}
            categorias[cat]["total"] += 1
            if resultado.status == "PASS":
                categorias[cat]["pass"] += 1
            else:
                categorias[cat]["fail"] += 1

        print("RESULTADOS POR CATEGORIA:")
        for cat, stats in categorias.items():
            pct = stats["pass"] / stats["total"] * 100 if stats["total"] > 0 else 0
            print(f"  {cat:25} {stats['pass']}/{stats['total']} ({pct:5.1f}%)")
        print("")

        # Testes que falharam
        falhados = [r for r in self.resultados if r.status != "PASS"]
        if falhados:
            print("TESTES QUE FALHARAM:")
            for resultado in falhados:
                print(f"  [{resultado.test_id}] {resultado.nome}")
                print(f"    Entrada:   {resultado.entrada}")
                print(f"    Esperado:  {resultado.saida_esperada}")
                print(f"    Obtido:    {resultado.saida_obtida}")
                if resultado.mensagem:
                    print(f"    Mensagem:  {resultado.mensagem}")
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
            "resultados": [asdict(r) for r in self.resultados],
        }

    def salvar_relatorio(self, relatorio: Dict, formato: str = "json"):
        """Salva relatorio em arquivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if formato == "json":
            arquivo = f"TEST_RESULTS_{timestamp}.json"
            with open(arquivo, "w") as f:
                json.dump(relatorio, f, indent=2)
            print(f"\nRelatorio JSON salvo em: {arquivo}")

        elif formato == "txt":
            arquivo = f"TEST_RESULTS_{timestamp}.txt"
            with open(arquivo, "w") as f:
                f.write("RELATORIO DE TESTES - SISTEMA COBOL PRODESP\n")
                f.write("=" * 80 + "\n")
                f.write(f"Data: {relatorio['data']}\n")
                f.write(f"Duracao: {relatorio['duracao']:.2f}s\n")
                f.write(f"Taxa de Sucesso: {relatorio['taxa_sucesso']:.1f}%\n")
                f.write("=" * 80 + "\n\n")

                for resultado in relatorio["resultados"]:
                    f.write(f"[{resultado['status']}] {resultado['test_id']}: {resultado['nome']}\n")
                    f.write(f"  Entrada: {resultado['entrada']}\n")
                    f.write(f"  Esperado: {resultado['saida_esperada']}\n")
                    f.write(f"  Obtido: {resultado['saida_obtida']}\n")
                    f.write(f"  Tempo: {resultado['tempo_ms']:.2f}ms\n\n")

            print(f"\nRelatorio TXT salvo em: {arquivo}")


def main():
    """Funcao principal"""

    # Parse argumentos
    teste_type = "todos"
    relatorio_format = "json"

    if len(sys.argv) > 1:
        if sys.argv[1] == "--test" and len(sys.argv) > 2:
            teste_type = sys.argv[2]
        if sys.argv[1] == "--report" and len(sys.argv) > 2:
            relatorio_format = sys.argv[2]

    # Executar testes
    suite = TestSuite()

    try:
        relatorio = suite.executar_todos()
        suite.salvar_relatorio(relatorio, relatorio_format)

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
        sys.exit(2)


if __name__ == "__main__":
    main()
