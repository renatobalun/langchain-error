zapocinjemo sa Langchain

langchain je jos jedan lib za izgradnu ai agenata.

1. proci kroz dokumentaciju: https://docs.langchain.com/oss/python/langchain/overview
- proci sve iz dokumentacije za Core components
- sve je vrlo bitno i potrebn je znati koje su mogucnosti
- vrlo bitna stvar kod Langchain je sto svaki korak ima svoj state koji mozemo dohvatiti ili updejtati
- tako mozemo imati long-term memory

2. proci kroz langgraph dokumentaciju, bitni izvori:
- https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph
- https://docs.langchain.com/oss/python/langgraph/workflows-agents


---------------

Zadatak: AI Error Analysis System
Cilj: Implementirati AI agenta koji automatski analizira greške iz production sistema i predlaže rješenja.

Šta je već gotovo
✅ Error Generator Service (port 8001) - šalje greške svakih 60 sekundi
✅ Webhook Receiver Service (port 8000) - prima greške
✅ 8 različitih tipova grešaka sa detaljnim kontekstom (stack trace, metrics, context)

Šta treba napraviti
1. iskoristi fast_api_erroring_app i napraviti jednu skriptu koja pokrece i stranu koja salje error i stranu koja prima error,
tako da se netrebaju pokretati te dvije app zasebno nego se pokrene jedna skripta koja pokrene dvije app

2. AI Analiza Greške (Step 1)

Receiver app kada dobije error se zapocinje analiza sa Langchain/Langgraph
Analizira se slijedece:
- Šta je uzrok greške
- Koliki je impact
- Urgentnost (critical/high/medium/low)
- Root cause analysis

Output: strukturiran JSON sa analizom

3. AI generiranje rješenja (Step 2)

Trebamo generirati:
- Konkretne code fixeve (Python kod)
- Configuration promjene
- Deployment korake
- Rollback plan

Output: executable kod + dokumentacija

4. Storage & History (Step 3)
Sačuvati sve analize u bazu (PostgreSQL)
