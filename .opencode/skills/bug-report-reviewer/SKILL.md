---
name: bug-report-reviewer
description: Use esta skill ao revisar um bug report antes de triagem, compartilhamento com o time ou criação de um ticket. Avalie clareza, evidência, comportamento esperado, informações ausentes e severidade sem inventar dados.
---

# Objetivo

Ajudar a revisar a qualidade de um bug report antes de tratá-lo como um defeito confirmado.

# Como trabalhar

1. Identifique qual comportamento foi observado e qual problema está sendo alegado.
2. Separe o que está explicitamente informado do que está sendo assumido.
3. Verifique se o comportamento esperado está claro.
4. Se houver PRD, requisito ou outra fonte confiável disponível e isso for necessário, consulte somente o contexto relevante para verificar o comportamento esperado.
5. Identifique informações ausentes que dificultam reproduzir, entender ou avaliar o problema.
6. Avalie se severity ou prioridade estão justificadas pelo impacto descrito.
7. Quando não houver evidência suficiente, faça perguntas específicas em vez de completar as lacunas.

# Regras

- Não assuma que um comportamento inesperado para o usuário é necessariamente um bug.
- Não invente steps, dados, ambiente, comportamento esperado ou impacto.
- Não transforme uma suposição em fato.
- Quando existir evidência de requisito, deixe claro o que ela sustenta.
- Questione severity quando não houver impacto suficiente para justificá-la.
- Prefira poucas perguntas específicas a uma checklist genérica.
- Não gere casos de teste, a menos que isso seja solicitado.

# O que observar no bug report

Considere, quando aplicável:

- título;
- comportamento observado;
- comportamento esperado;
- passos para reprodução;
- dados ou estado necessários;
- ambiente;
- frequência/reprodutibilidade;
- impacto;
- evidências;
- relação com requisito conhecido;
- severity/prioridade.

Nem todos os bugs precisam de todos esses campos.

# Resultado esperado

## 1. Entendimento do relato

Resuma em poucas linhas o que o bug report está alegando.

## 2. O que está claro

Liste somente informações sustentadas pelo relato ou por evidência consultada.

## 3. Lacunas ou assumptions

Mostre o que está ausente, ambíguo ou sendo assumido.

## 4. Comportamento esperado / requisito

Informe se existe evidência suficiente para considerar o comportamento contrário ao esperado.

Se não houver, diga que ainda não é possível concluir.

## 5. Severity

Avalie se a severity informada parece sustentada pelo impacto conhecido.

## 6. Perguntas para avançar

Faça somente as perguntas que realmente ajudariam a decidir ou reproduzir o problema.

## 7. Próximo passo recomendado

Indique se o relato parece:

- pronto para seguir;
- precisar de mais informação;
- poder representar comportamento esperado;
- ou exigir validação de produto/requisito antes de ser tratado como bug.
