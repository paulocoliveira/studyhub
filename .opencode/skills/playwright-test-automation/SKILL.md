---
name: playwright-test-automation
description: Orienta a criação, execução e investigação de testes E2E Playwright no StudyHub seguindo padrões de automação confiáveis.
---

# Objetivo

Transformar comportamentos relevantes do StudyHub em testes Playwright claros, executáveis, confiáveis e orientados por evidência.

# Antes de implementar

- entenda o comportamento esperado;
- identifique de onde essa expectativa vem;
- examine testes existentes antes de escolher estrutura ou padrões;
- observe a aplicação quando houver incerteza sobre elementos, fluxo ou comportamento;
- identifique pré-condições e dados necessários.

# Implementação

- mantenha cada teste focado em um comportamento relevante;
- prefira locators orientados ao usuário, como role, label e texto visível;
- use escopo quando existirem elementos semelhantes em diferentes regiões da página;
- evite seletores frágeis baseados em estrutura de DOM quando houver alternativa melhor;
- não use esperas arbitrárias como mecanismo de sincronização;
- use assertions que comprovem o comportamento, não apenas que uma ação foi executada;
- reutilize padrões existentes quando eles já resolverem o mesmo problema;
- mantenha o teste compreensível para outro QA;
- não coloque credenciais diretamente no código.

# Autenticação

Quando o teste exigir autenticação, use as variáveis de ambiente:

- `STUDYHUB_EMAIL`
- `STUDYHUB_PASSWORD`

Se elas não estiverem disponíveis, informe a limitação em vez de inventar credenciais.

# Execução

Depois de criar ou alterar um teste:

1. execute primeiro o menor escopo relevante;
2. observe o resultado real;
3. use erro, screenshot, trace ou error context quando forem úteis;
4. só conclua sucesso depois de uma execução bem-sucedida.

# Quando o teste falhar

Não tente imediatamente fazê-lo passar.

Determine primeiro qual destas hipóteses é mais consistente com as evidências:

- defeito da aplicação;
- expectativa incorreta;
- problema no próprio teste;
- dado inadequado;
- problema de ambiente.

Use novas evidências para reduzir a incerteza.

Não remova ou enfraqueça uma assertion relevante somente porque ela expõe uma falha.

# Princípio

**Execute antes de confiar. Investigue antes de corrigir.**
