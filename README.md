# Trabalho de Algoritmos para IA - Labirinto

# Nomes:
- Ernesto Terra dos Santos
- Gabriel Fonseca

## **Algoritmo de Dijkstra vs. Algoritmo de Força Bruta**

### **Objetivo:**
O objetivo deste trabalho é comparar dois algoritmos de busca em grafos: o Algoritmo de Dijkstra e o Algoritmo de Força Bruta, aplicados a um labirinto. O labirinto é representado como uma grade onde cada célula pode ser um espaço livre ou uma parede. O algoritmo deve encontrar o caminho mais curto entre um ponto inicial e um ponto final.



# Comparação Entre o Algoritmo de Dijkstra e o Algoritmo de Força Bruta

## **Algoritmo de Dijkstra:**

- **Visão Geral:**
  - O algoritmo de Dijkstra é um algoritmo de busca em grafos usado para encontrar o caminho mais curto entre um nó inicial e um nó destino. É uma abordagem mais eficiente em comparação aos algoritmos de força bruta, especialmente quando lidamos com grafos ponderados ou labirintos grandes. Embora no caso de labirintos o problema possa ser tratado como um grafo não ponderado, onde cada movimento tem o mesmo custo, o Dijkstra ainda traz melhorias significativas.

- **Complexidade de Tempo:**
  - A complexidade de tempo do algoritmo de Dijkstra é **O((V + E) log V)**, onde `V` é o número de vértices (células no labirinto) e `E` é o número de arestas (movimentos possíveis).
  - O uso de uma fila de prioridade (min-heap) acelera o algoritmo consideravelmente em comparação com uma abordagem ingênua.

- **Complexidade de Espaço:**
  - **O(V)** para armazenar distâncias, nós visitados e a fila de prioridade.
  - Para labirintos maiores, esse uso de memória é gerenciável e escala melhor do que os métodos de força bruta.

- **Vantagens:**
  1. **Eficiência:** O algoritmo de Dijkstra garante o caminho mais curto e é mais rápido, especialmente em labirintos grandes e complexos. Ele explora eficientemente os caminhos de menor custo primeiro.
  2. **Escalabilidade:** À medida que o tamanho do labirinto aumenta, o desempenho do Dijkstra melhora significativamente em comparação com a força bruta.
  3. **Solução Ótima:** O Dijkstra sempre encontra o caminho mais curto, tornando-o mais confiável do que a força bruta.

- **Desvantagens:**
  1. **Complexidade:** É mais complexo de implementar em comparação com a força bruta, especialmente com o uso de filas de prioridade.
  2. **Sobrecarga:** Embora o algoritmo seja eficiente, a fila de prioridade e a memória extra para o rastreamento de distâncias e nós anteriores introduzem uma sobrecarga.

---

## **Algoritmo de Força Bruta:**

- **Visão Geral:**
  - O método de força bruta geralmente explora todos os caminhos possíveis do ponto de partida até o ponto de destino, verificando cada possibilidade sem otimização. Isso resulta na verificação de todos os caminhos possíveis no labirinto.

- **Complexidade de Tempo:**
  - A complexidade de tempo é **O(2^N)** para busca exaustiva, onde `N` é o número de posições ou movimentos possíveis. Isso torna o algoritmo exponencialmente lento, especialmente para labirintos grandes.
  - O método de força bruta pode explorar caminhos que não levam ao destino, desperdiçando tempo em rotas não ótimas.

- **Complexidade de Espaço:**
  - **O(N)** para armazenar os caminhos possíveis e explorá-los, mas o uso de memória é geralmente gerenciável em labirintos menores.

- **Vantagens:**
  1. **Simplicidade:** O algoritmo de força bruta é fácil de implementar. Não envolve estruturas de dados complicadas.
  2. **Sem Assumções:** Não exige suposições sobre a estrutura do labirinto (por exemplo, não assume arestas não ponderadas).

- **Desvantagens:**
  1. **Ineficácia:** À medida que o tamanho do labirinto aumenta, o método de força bruta se torna altamente ineficiente, verificando todos os caminhos possíveis, mesmo os que são claramente subótimos.
  2. **Impraticabilidade em Labirintos Grandes:** Para labirintos grandes, torna-se praticamente inutilizável devido ao crescimento exponencial da complexidade de tempo.
  3. **Não Garante a Solução Ótima:** Diferente do Dijkstra, a força bruta não garante o caminho mais curto, a menos que todos os caminhos sejam verificados, e ainda assim, de maneira ineficiente.

---

## **Resumo da Comparação:**

| Métrica             | Algoritmo de Dijkstra                      | Algoritmo de Força Bruta                   |
|---------------------|-------------------------------------------|-------------------------------------------|
| **Complexidade de Tempo** | **O((V + E) log V)**                    | **O(2^N)** (crescimento exponencial)      |
| **Complexidade de Espaço** | **O(V)**                                | **O(N)**                                  |
| **Eficiência**      | Muito eficiente, especialmente em labirintos grandes. | Lento, impraticável para labirintos grandes. |
| **Otimização**      | Sempre encontra o caminho mais curto.    | Pode não encontrar o caminho mais curto ou levar muito tempo para encontrar. |
| **Simplicidade**    | Mais complexo devido ao uso de filas de prioridade e rastreamento de distâncias. | Simples de implementar com loops básicos. |
| **Escalabilidade**  | Escala bem com o tamanho do labirinto.    | Não escala bem com o aumento do tamanho do labirinto. |
| **Caso de Uso**     | Melhor para labirintos grandes ou quando a optimalidade é necessária. | Adequado para labirintos pequenos ou quando uma solução exaustiva é aceitável. |

---

## **Conclusão:**

- **O Algoritmo de Dijkstra** é muito superior ao **Algoritmo de Força Bruta** em termos de eficiência, escalabilidade e otimização. Ele garante o caminho mais curto e se sai muito melhor em labirintos maiores devido à sua complexidade de tempo mais eficiente.
- **A Força Bruta** é útil para problemas pequenos ou como uma ferramenta de ensino, mas para qualquer coisa além de uma grade pequena, o método de Dijkstra é a escolha óbvia. À medida que o tamanho do labirinto aumenta, a força bruta se torna impraticável devido à sua complexidade de tempo exponencial.
