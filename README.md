# Tema 2 LFA – RegEx Validator

**Autor:** Pirvulescu Gabriela

## 📝 Descriere generală

Acest proiect are ca scop să rezolve problema verificării încadrării unui anumit cuvânt în limbajul generat de o expresie regulată (RegEx).

Codul prezentat realizează următoarele ("compunerea" lor ducând la rezolvarea problemei noastre):

1. Transformă o expresie regulată (RegEx) în formă postfixată (RPN) folosind algoritmul **Shunting Yard**.
2. Construiește un **NFA** (automat finit nedeterminist), pornind de la forma postfixată, folosind algoritmul **Thompson**.
3. Convertește NFA-ul într-un **DFA** (automat finit determinist) folosind algoritmul de **Subset Construction (Powerset Construction)**.
4. Verifică dacă un șir de caractere este acceptat de DFA.

Testele sunt încărcate automat dintr-un fișier JSON și evaluate. Afișarea se face în consolă după simpla rulare (**RUN**) a programului. Pentru fiecare sub test case, se va arăta **OK** dacă sub-testul funcționează și **FAIL** altfel.

---

## 📁 Structura proiectului

regex-matcher/
│

├── main.py         ✅ Codul Python de validare a unui string într-o expresie regulată

├── tests.json      ✅ Test cases

└── README.md       ✅ Documentația


 
---

## 🔍 Algoritmi utilizați

### 1. `Shunting_Yard()` – Convertire unei expresii regulate în postfix
- Forma postfixată reprezintă o scriere de expresii în care opetaorii se pun mereu după termenii asupra cărora se aplică (spre exemplu, a.b (concatenarea) ar deveni ab.)
- Algoritmul transformă expresia regulată în formă postfixată.
- Inițial, adaugă concatenări explicite (`.`) între simboluri adiacente (deoarece în fișsierele de test concatenarea a.b e scrisă mereu ab, iar în algoritmul nostru avem nevoie de toate simbolurile explicit).
- Se espectă precedența operatorilor: `*`, `+`, `?`, `.`, `|` (pentru aceasta s-a folosit dicționarul operators), dar și asocitivitatea (dicționarul associativity)
- se utilizează o stivă (în cazul nostru, o listă ce simulează o stivă) în care se vor păstra simbolurile și se vor deschide și închide parantezele. Ținând cont de precedență, se vor adăuga operatorii la postfix. Fiecare caracter ce nu e operator se adaugă la postfix atunci când e întâlnit.

### 2. `thompson()` – Construirea unui NFA pornind de la o expresie în forma postfixată
- Aplică **algoritmul Thompson** pentru a construi un automat finit nedeterminist (NFA).
- Se creează o stivă (listă) care va stoca componentele lambda-NFA-ului (fragmentele intermediare) și se parcurge fiecare caracter al expresiei în notare postfix.
- Pentru fiecare simbol de tip operator întâlnit se simulează automate corespunzătoare care se vor adăuga la stivă. Se fac operațiile corespunzătoare pe aceste NFA-uri conform simbolurilor.
- E important că șirul e în formă postfixată - altfel nu am fi putut urma un algoritm similar. Ordinea din forma postfixată ajută la construcția în ordinea corectă a NFA-urilor noastre.
- Avem și o funcție care transformă NFA-ul dat sub forma de mai sus într-un NFA în forma uzuală cu care lucrăm noi.

### 3. `nfa_to_dfa()` – Subset Construction
- Transformă NFA-ul într-un DFA:
  - NFA-ul nostru din algoritmul Thompson este de fapt un lambda-NFA, dar asta nu influențează aplicabilitatea Subset Construction-ului (în continuare îi vom zice simplu, NFA)
  - Stările din DFA vor fi mulțimi de stări din NFA
  - Pentru fiecare mulțime de stări obținută la un anumit moment, ne uităm pentru fiecare literă în ce stări putem ajunge cu acea literă din stările din mulțimea respectivă. Dacă din mulțimea A se ajunge cu litera u la mulțimea B, tragem muchie cu u în DFA de la A la B.
  - starea inițială este lambda-închiderea stării inițiale din NFA (stările în care putem ajunge doar prin lambda-mișcări, pornind din starea inițială din NFA) - în varianta pentru NFA simplu (nu lambda-NFA) starea inițială ar fi pur și simplu mulțimea formată din starea inițială a NFA-ului.
  - Stările finale din DFA vor fi toate seturile care conțin stări finale din NFA.

### 4. `dfa_acceptance_check()` – Validarea șirurilor pentru un automat finit determinist
- Pornind de la simbolul de start, vedem dacă putem ajunge la stare finală urmând simbolurile dintr-un șir dat.
- Dacă se ajunge la None sau la un simbol ce nu e în alfabet, șirul nu va fi acceptat.
- Returnează `True` dacă șirul este acceptat, `False` în caz contrar.

---

## ✅ Testare automată

### Fișier JSON (`tests.json`)
Conține o listă de teste de forma:

```json
[
  {
    "name": "Test 1",
    "regex": "a(bc)*",
    "test_strings": [
      {"input": "abc", "expected": true},
      {"input": "a", "expected": true},
      {"input": "abcbc", "expected": true},
      {"input": "aaa", "expected": false}
    ]
  },
  {
    "name": "Test 2",
    "regex": "a*",
    "test_strings": [
      {"input": "a", "expected": true},
      {"input": "aaaa", "expected": true},
      {"input": "aa", "expected": true},
      {"input": "ba", "expected": false}
    ]
  }
]
