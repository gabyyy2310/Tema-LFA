Acest proiect are ca scop validarea unor cuvinte pentru o expresie regulata (RegEx). Pentru aceasta, vom face urmatorii pasi:
-aplicam algoritmul SHUNTING-YARD pentru a transforma expresia regula in expresie de tip postfix
-aplicam algoritmul lui THOMPSON pentru a transforma expresia postfix intr-un NFA
-aplicam SUBSET CONSTRUCTION pentru a transforma NFA-ul in DFA
-facem verifcarea daac DFA-ul accepta un anume cuvant.
Combinand toate acestea, putem ajunge sa vedem daca un anumit cuvant e validat de o anumita expresie regulata.

Rularea programului se face imediat, apasand pur si simplu butonul Run.

Decizii luate in implementare:
-am ales sa inlocuiesc SD-ul stack cu o lista care simuleaza un stack (o lista la care append-uiam elemente, respectiv eliminam elemente de la final -> ca intr-o stiva)
-am combinat in aceeasi functie transformarea din lambda-NFA in DFA (pentru simplitate)
-am ales sa fac afisarea sub forma : [OK] Input: '{string}' -> Expected: {expected}, Got: {result} pentru a se vedea clar ce Test Case-uri nu au mers si a se putea remedia eventualele erori mai usor.

Probleme intampinate:
-cea mai mare problema a fost legata de asociativitatea la stanga in Shunting-Yard, deoarece aceasta crea probleme majore in expresii complicate. Am remediat problema adaugand o lista de asociativitate.
-citirea din fisier JSON: omiterea "encoding='utf-8" crease probleme initial

Afisarea rezultatelor compilarii se face in consola, nu in fisier.
