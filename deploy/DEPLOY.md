# Publicar o COBOL Tester na EC2

Guia completo para colocar a aplicacao web no ar em uma instancia EC2 (Amazon Linux 2023).

---

## Pre-requisitos (voce faz no Console AWS)

Estes passos sao de infraestrutura e so podem ser feitos por voce no console/CLI da AWS:

1. **Instancia EC2 ligada e acessivel**
   - Tipo sugerido: t3.small ou superior (o compilador COBOL usa CPU/memoria)
   - SO: Amazon Linux 2023
   - Anote o IP publico (ou Elastic IP)

2. **Security Group** com as portas liberadas (Inbound):
   | Tipo | Porta | Origem | Para que |
   |------|-------|--------|----------|
   | SSH  | 22    | seu IP / VPN | acesso administrativo |
   | Custom TCP | 5000 | seu IP / VPN / 0.0.0.0-0 | acessar a aplicacao |

   > Se preferir servir na porta 80, use um proxy (nginx) ou rode o gunicorn na 80 (requer permissao). O padrao aqui e 5000.

3. **Par de chaves (.pem)** na pasta `vmchaves/` (ex.: `poc-prodesp-kp.pem`).
   - No Windows, garanta permissao restrita da chave, senao o SSH recusa:
     ```powershell
     icacls vmchaves\poc-prodesp-kp.pem /inheritance:r /grant:r "$($env:USERNAME):(R)"
     ```

4. **Teste de conexao** (se der timeout, o problema e rede/Security Group/VPN, nao a app):
   ```powershell
   ssh -i vmchaves\poc-prodesp-kp.pem ec2-user@<IP-DA-EC2> "echo ok"
   ```

---

## Passo 1 - Deploy da aplicacao

Na pasta do projeto, rode (troque `<IP>`):

```powershell
ssh -i vmchaves\poc-prodesp-kp.pem ec2-user@<IP> "bash -s" < deploy\deploy-ec2.sh
```

O script `deploy-ec2.sh` faz na EC2:
- instala python3, pip, gcc, git
- instala o **GnuCOBOL** do sistema (ou compila do source se nao houver pacote)
- clona/atualiza o repositorio
- instala as dependencias de `requirements.txt` (inclui **gunicorn**)
- gera um **SECRET_KEY** fixo (para a sessao de login nao cair a cada restart)
- instala um **servico systemd** (`cobol-tester.service`) que sobe o **gunicorn**
  (modo producao) na porta 5000, habilitado para iniciar sozinho a cada boot
  da instancia (nohup nao sobrevive a reboot - por isso o servico existe)

---

## Passo 2 - Enviar os fontes COBOL (necessario para teste real)

Os fontes COBOL e os copybooks estao no `.gitignore` (vem de arquivos .7z grandes),
entao **nao chegam pelo git clone**. Sem eles, a app sobe mas roda em modo simulacao
(nao compila COBOL de verdade). Para habilitar o teste real, envie-os via scp:

```powershell
.\deploy\enviar-fontes.ps1 -Ip <IP>
```

Isso copia `fontes_convertidos/`, `cobol_build/copy/` e `PGM POC cob original/`.
Depois, reinicie o servidor (ver secao "Reiniciar").

---

## Passo 3 - Acessar

- URL: `http://<IP-DA-EC2>:5000`
- Login inicial: **admin / prodesp_2026** (o sistema exige troca de senha? Nao para o admin;
  usuarios novos criados por ele sim.)

> Recomendado: no primeiro acesso, entre como admin e crie os usuarios reais / troque a senha.

---

## Operacao

O servidor roda como servico systemd (`cobol-tester`) - sobe sozinho a cada
boot da instancia (nao depende de ninguem estar com uma sessao SSH aberta,
nem de rodar o deploy de novo apos um reboot).

**Ver o log:**
```bash
tail -f /tmp/cobol-tester.log
# ou, via journal do systemd:
sudo journalctl -u cobol-tester -f
```

**Status:**
```bash
sudo systemctl status cobol-tester
```

**Parar / iniciar:**
```bash
sudo systemctl stop cobol-tester
sudo systemctl start cobol-tester
```

**Reiniciar (apos git pull ou envio de fontes):**
```bash
cd ~/prodesp-cobol-tester && git pull
# se algum copybook compartilhado (cobol_build/copy/*.cpy) mudou, limpar o
# cache de compilacao para forcar recompilar com a versao nova:
rm -f cobol_build/*.so cobol_build/*.dll cobol_build/*_processed cobol_build/DRIVER-*
sudo systemctl restart cobol-tester
```

Ou simplesmente rode de novo o `deploy-ec2.sh` (ele reinstala o servico e reinicia sozinho).

---

## Notas importantes

- **GnuCOBOL no Linux:** o codigo agora detecta o compilador automaticamente -
  no Windows usa o pacote local; na EC2 usa o `cobc` do sistema. Modulos compilam
  para `.so` no Linux (em vez de `.dll`).
- **Persistencia de usuarios:** `data/users.json` fica so na EC2 (nao versionado).
  Se recriar a instancia, o admin inicial e recriado com a senha padrao.
- **IP publico:** se a instancia nao tem Elastic IP associado, um stop/start
  (nao um reboot simples) troca o IP publico - o servico sobe sozinho de
  qualquer forma, mas o endereco de acesso pode mudar. Para um IP fixo,
  aloque um Elastic IP no console AWS e associe a instancia.
- **Producao real:** para uso serio, considere tambem: nginx como proxy
  reverso, HTTPS (certificado), e um SECRET_KEY/senha admin vindos de
  variavel de ambiente segura (o servico systemd ja cobre o restart
  automatico).
- **Banco DB2:** a feature de execucao com banco depende dos artefatos ainda pendentes
  (ver docs/EMAIL_SOLICITACAO_PRODESP.md). A geracao de DDL/massa (aba Estrutura de Dados)
  funciona com o que ja existe.

---

## Solucao de problemas

| Sintoma | Causa provavel | Acao |
|---------|----------------|------|
| SSH timeout | Security Group / VPN / instancia parada | Verificar porta 22 e IP no console AWS |
| Abre local mas nao pela URL | Porta 5000 nao liberada | Liberar inbound 5000 no Security Group |
| "cobc indisponivel" no log | GnuCOBOL nao instalou | Rodar o passo 2 do script manualmente |
| Compila mas nao acha fonte | Fontes nao enviados | Rodar `enviar-fontes.ps1` |
| Sessao cai a cada restart | SECRET_KEY aleatorio | Conferir `.env.deploy` e exportar antes de subir |
