#!/usr/bin/env python3
"""
Executor de Programas COBOL Legado - Prodesp
Permite compilar e executar programas COBOL sem instalar compilador completo
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ResultadoValidacao:
    """Resultado da validação de placa"""
    placa: str
    valida: bool
    codigo: int
    descricao: str

class ValidadorPlaca:
    """Validador de placas veiculares (PF-GAA-L004)"""

    def __init__(self):
        self.codigos = {
            0: "Invalida",
            11: "Mercosul - Sao Paulo",
            12: "Mercosul - Outros estados",
            21: "Antiga - Sao Paulo",
            22: "Antiga - Outros estados",
            33: "2 letras - Carros",
            34: "2 letras - Motos",
        }

    def validar(self, placa: str) -> ResultadoValidacao:
        """Valida uma placa veicular"""
        placa_orig = placa or ""
        placa = placa_orig.strip().upper()

        # Validacao 1: Vazio ou nulo
        if not placa:
            return ResultadoValidacao(
                placa=placa_orig,
                valida=False,
                codigo=0,
                descricao=self.codigos[0]
            )

        # Validacao 2: Caracteres especiais nao sao permitidos
        for c in placa:
            if not c.isalnum():
                return ResultadoValidacao(
                    placa=placa_orig,
                    valida=False,
                    codigo=0,
                    descricao=self.codigos[0]
                )

        # Validacao 3: Deve ter pelo menos 4 caracteres
        if len(placa) < 4:
            return ResultadoValidacao(
                placa=placa_orig,
                valida=False,
                codigo=0,
                descricao=self.codigos[0]
            )

        # Validacao 4: Deve ter no maximo 10 caracteres
        if len(placa) > 10:
            return ResultadoValidacao(
                placa=placa_orig,
                valida=False,
                codigo=0,
                descricao=self.codigos[0]
            )

        try:
            faixa = placa[0:2]
            faixa_3 = placa[2] if len(placa) > 2 else " "
            milhar = placa[3] if len(placa) > 3 else " "
            serie = placa[4] if len(placa) > 4 else " "
            dezena = placa[5:7] if len(placa) >= 7 else placa[5:] if len(placa) > 5 else ""

            # Validacoes basicas
            if not faixa.isalpha():
                return ResultadoValidacao(
                    placa=placa_orig,
                    valida=False,
                    codigo=0,
                    descricao=self.codigos[0]
                )

            if not milhar.isdigit():
                return ResultadoValidacao(
                    placa=placa_orig,
                    valida=False,
                    codigo=0,
                    descricao=self.codigos[0]
                )

            if dezena and not dezena.replace(" ", "").isdigit():
                return ResultadoValidacao(
                    placa=placa_orig,
                    valida=False,
                    codigo=0,
                    descricao=self.codigos[0]
                )

            if not (serie.isdigit() or serie.isalpha()):
                return ResultadoValidacao(
                    placa=placa_orig,
                    valida=False,
                    codigo=0,
                    descricao=self.codigos[0]
                )

            # Logica de validacao
            if faixa_3.isdigit():
                if not dezena or dezena.strip() == "":
                    codigo = 34
                else:
                    codigo = 33
            else:
                ranges_outros = [
                    ("BFA", "GKI"),
                    ("QSN", "QSZ"),
                    ("SSR", "SWZ"),
                    ("TIO", "TMJ"),
                    ("UDA", "UGV"),
                    ("UOG", "USB"),
                ]

                eh_outro_estado = any(inicio <= faixa <= fim for inicio, fim in ranges_outros)

                if eh_outro_estado:
                    codigo = 22 if serie.isdigit() else 12
                else:
                    codigo = 21 if serie.isdigit() else 11

            return ResultadoValidacao(
                placa=placa_orig,
                valida=True,
                codigo=codigo,
                descricao=self.codigos[codigo]
            )

        except Exception:
            return ResultadoValidacao(
                placa=placa_orig,
                valida=False,
                codigo=0,
                descricao=self.codigos[0]
            )

class ExecutorCOBOL:
    """Executor de programas COBOL"""

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.programas = {}
        self.bibliotecas = {}
        self._carregar_metadados()

    def _carregar_metadados(self):
        """Carrega metadados dos programas COBOL"""

        # Metadados dos programas principais
        self.programas = {
            "PF-GAA-L004": {
                "tipo": "VALIDADOR",
                "descricao": "Validador de placas veiculares",
                "entrada": "Placa (ate 10 caracteres)",
                "saida": "Codigo de validacao (0-34)",
                "funcao": self._validador_placas,
            },
            "PF-GAA-B100-DB": {
                "tipo": "PROCESSADOR_BD",
                "descricao": "Processador de banco de dados",
                "entrada": "Arquivo de dados",
                "saida": "Registros processados",
                "funcao": None,  # Nao implementado em simulacao
            },
            "PF-GEV-T005-DB": {
                "tipo": "TABELA",
                "descricao": "Tabela de empadronizacao veicular",
                "entrada": "ID do veiculo",
                "saida": "Dados do veiculo",
                "funcao": None,
            },
        }

    def listar_programas(self) -> str:
        """Lista todos os programas disponiveis"""
        output = []
        output.append("=" * 70)
        output.append("PROGRAMAS DISPONIVEIS - EXECUTOR COBOL LEGADO")
        output.append("=" * 70)
        output.append("")

        # Programas implementados
        output.append("[IMPLEMENTADOS] (Prontos para usar)")
        for prog_id, info in self.programas.items():
            if info.get("funcao"):
                output.append(f"  [OK] {prog_id}")
                output.append(f"       Tipo: {info['tipo']}")
                output.append(f"       Desc: {info['descricao']}")
                output.append("")

        # Listar arquivos COBOL disponiveis
        cobol_dir = self.base_dir / "PGM POC cob original"
        if cobol_dir.exists():
            programas_disponiveis = list(cobol_dir.glob("*.C74"))
            output.append(f"[DISPONIVEIS NO DISCO] ({len(programas_disponiveis)} programas)")
            for prog in sorted(programas_disponiveis)[:10]:
                output.append(f"  - {prog.name} ({prog.stat().st_size / 1024:.1f} KB)")
            if len(programas_disponiveis) > 10:
                output.append(f"  ... e mais {len(programas_disponiveis) - 10}")

        return "\n".join(output)

    def _validador_placas(self, placa: str) -> Dict:
        """
        Valida uma placa veicular (simulacao de PF-GAA-L004)

        Logica baseada no codigo COBOL original:
        - Placa: 2 letras (FAIXA) + 1 char (FAIXA-3) + 1 char (MILHAR) + 1 char (SERIE) + 2 chars (DEZENA)

        Se FAIXA-3 eh numerico: placa de 2 letras (codigo 33 ou 34)
        Se SERIE eh numerico: placa antiga (codigo 21 ou 22)
        Se SERIE eh alfabetico: placa Mercosul (codigo 11 ou 12)
        """

        placa_orig = placa or ""
        placa = placa_orig.strip().upper()

        # Codigos de retorno
        codigos = {
            0: "Invalida",
            11: "Mercosul - Sao Paulo",
            12: "Mercosul - Outros estados",
            21: "Antiga - Sao Paulo",
            22: "Antiga - Outros estados",
            33: "2 letras - Carros",
            34: "2 letras - Motos",
        }

        # Validacao 1: Vazio ou nulo
        if not placa:
            return {"codigo": 0, "descricao": codigos[0], "valida": False}

        # Validacao 2: Caracteres especiais nao sao permitidos
        for c in placa:
            if not c.isalnum():
                return {"codigo": 0, "descricao": codigos[0], "valida": False}

        # Validacao 3: Deve ter pelo menos 4 caracteres (XX99 minimo)
        if len(placa) < 4:
            return {"codigo": 0, "descricao": codigos[0], "valida": False}

        # Validacao 4: Deve ter no maximo 10 caracteres
        if len(placa) > 10:
            return {"codigo": 0, "descricao": codigos[0], "valida": False}

        try:
            # Estrutura da placa segundo COBOL:
            # Pos 1-2: FAIXA (2 letras)
            # Pos 3: FAIXA-3
            # Pos 4: MILHAR
            # Pos 5: SERIE
            # Pos 6-7: DEZENA (2 chars)

            faixa = placa[0:2]
            faixa_3 = placa[2] if len(placa) > 2 else " "
            milhar = placa[3] if len(placa) > 3 else " "
            serie = placa[4] if len(placa) > 4 else " "
            dezena = placa[5:7] if len(placa) >= 7 else placa[5:] if len(placa) > 5 else ""

            # Validacao: Primeiros 2 devem ser letras
            if not faixa.isalpha():
                return {"codigo": 0, "descricao": codigos[0], "valida": False}

            # Validacao: MILHAR e DEZENA devem ser numericos
            if not milhar.isdigit():
                return {"codigo": 0, "descricao": codigos[0], "valida": False}

            if dezena and not dezena.replace(" ", "").isdigit():
                return {"codigo": 0, "descricao": codigos[0], "valida": False}

            # Validacao: SERIE deve ser numerico OU alfabetico
            if not (serie.isdigit() or serie.isalpha()):
                return {"codigo": 0, "descricao": codigos[0], "valida": False}

            # Validacao: FAIXA deve ser alfabetica
            if not faixa.isalpha():
                return {"codigo": 0, "descricao": codigos[0], "valida": False}

            # ===== LOGICA PRINCIPAL (COBOL PF-GAA-L004) =====

            # PASSO 1: Se FAIXA-3 eh numerico -> placa de 2 letras
            if faixa_3.isdigit():
                # Se DEZENA eh vazio -> codigo 34 (motos)
                # Senao -> codigo 33 (carros)
                if not dezena or dezena.strip() == "":
                    return {
                        "codigo": 34,
                        "descricao": codigos[34],
                        "valida": True,
                    }
                else:
                    return {
                        "codigo": 33,
                        "descricao": codigos[33],
                        "valida": True,
                    }

            # PASSO 2: Se FAIXA-3 eh alfabetico
            # Verificar ranges de SP vs Outros estados
            ranges_outros = [
                ("BFA", "GKI"),
                ("QSN", "QSZ"),
                ("SSR", "SWZ"),
                ("TIO", "TMJ"),
                ("UDA", "UGV"),
                ("UOG", "USB"),
            ]

            eh_outro_estado = False
            for inicio, fim in ranges_outros:
                if inicio <= faixa <= fim:
                    eh_outro_estado = True
                    break

            if eh_outro_estado:
                # Placa de outro estado
                if serie.isdigit():
                    return {
                        "codigo": 22,
                        "descricao": codigos[22],
                        "valida": True,
                    }
                else:
                    return {
                        "codigo": 12,
                        "descricao": codigos[12],
                        "valida": True,
                    }
            else:
                # Placa de Sao Paulo
                if serie.isdigit():
                    return {
                        "codigo": 21,
                        "descricao": codigos[21],
                        "valida": True,
                    }
                else:
                    return {
                        "codigo": 11,
                        "descricao": codigos[11],
                        "valida": True,
                    }

        except Exception as e:
            pass

        # Default: invalida
        return {"codigo": 0, "descricao": codigos[0], "valida": False}

    def executar_programa(self, prog_id: str, *args) -> Dict:
        """Executa um programa COBOL"""

        if prog_id not in self.programas:
            return {
                "status": "ERRO",
                "mensagem": f"Programa '{prog_id}' nao encontrado",
            }

        info = self.programas[prog_id]

        if not info.get("funcao"):
            return {
                "status": "INDISPONIVEL",
                "mensagem": f"Programa '{prog_id}' nao implementado em simulacao",
                "descricao": info["descricao"],
            }

        try:
            resultado = info["funcao"](*args)
            resultado["status"] = "SUCESSO"
            return resultado
        except Exception as e:
            return {
                "status": "ERRO",
                "mensagem": str(e),
            }

    def compilar_programa(self, programa: str) -> Dict:
        """Simula compilacao de um programa (sem compilador real)"""

        prog_path = self.base_dir / "PGM POC cob original" / programa

        if not prog_path.exists():
            return {
                "status": "ERRO",
                "mensagem": f"Arquivo nao encontrado: {programa}",
            }

        # Simulacao de compilacao
        return {
            "status": "SIMULACAO",
            "mensagem": "Compilacao simulada (compilador real nao disponivel)",
            "arquivo": programa,
            "tamanho": prog_path.stat().st_size,
            "instrucoes": f"""
Para compilar este programa com GnuCOBOL:

1. Instale GnuCOBOL:
   Windows: https://sourceforge.net/projects/gnucobol/files/
   Linux: apt-get install gnucobol
   macOS: brew install gnu-cobol

2. Compile:
   cobc -x "{programa}" -o prog.exe

3. Execute:
   ./prog.exe
""",
        }


def main():
    """Funcao principal"""

    print("\n" + "=" * 70)
    print("[*] EXECUTOR DE PROGRAMAS COBOL LEGADO - PRODESP")
    print("=" * 70)
    print("")

    # Usar diretório atual para funcionar em qualquer lugar
    base_dir = Path(__file__).parent
    executor = ExecutorCOBOL(str(base_dir))

    # Menu
    if len(sys.argv) < 2:
        print("USO: python executor_cobol.py [COMANDO] [ARGS]")
        print("")
        print("COMANDOS:")
        print("  listar              - Listar programas disponiveis")
        print("  validar PLACA       - Validar placa veicular")
        print("  executar PROG [ARGS]- Executar programa")
        print("")
        print("EXEMPLOS:")
        print("  python executor_cobol.py listar")
        print("  python executor_cobol.py validar AAA0A00")
        print("  python executor_cobol.py validar ABC1234")
        print("  python executor_cobol.py executar PF-GAA-L004 ABC1234")
        print("")
        return

    comando = sys.argv[1].lower()

    if comando == "listar":
        print(executor.listar_programas())

    elif comando == "validar":
        if len(sys.argv) < 3:
            print("[ERRO] Faltou informar a placa")
            print("Uso: python executor_cobol.py validar PLACA")
            return

        placa = sys.argv[2]
        resultado = executor.executar_programa("PF-GAA-L004", placa)

        print(f"\nPlaca: {placa}")
        print(f"Status: {resultado.get('status')}")
        print(f"Codigo: {resultado.get('codigo')}")
        print(f"Descricao: {resultado.get('descricao')}")
        print(f"Valida: {resultado.get('valida')}")

    elif comando == "executar":
        if len(sys.argv) < 3:
            print("[ERRO] Faltou informar o programa")
            print("Uso: python executor_cobol.py executar PROGRAMA [ARGS]")
            return

        prog = sys.argv[2]
        args = sys.argv[3:] if len(sys.argv) > 3 else []

        resultado = executor.executar_programa(prog, *args)

        print(f"\nPrograma: {prog}")
        print(f"Status: {resultado.get('status')}")

        for chave, valor in resultado.items():
            if chave != "status":
                print(f"{chave}: {valor}")

    else:
        print(f"[ERRO] Comando desconhecido: {comando}")
        print("Use: python executor_cobol.py --help")

    print("")


if __name__ == "__main__":
    main()
