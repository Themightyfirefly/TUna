### 🧩 Quellenbezug des Systemprompts

**ROLE & SCOPE**  
*Quelle:* Zhao et al., 2025 – *Deriving Insights from Enhanced Accuracy: Leveraging Prompt Engineering in Custom GPT for Assessing Chinese Nursing Licensing Exam*  
> Beschreibt die Entwicklung eines **Custom GPT** mit **Prompt Engineering**, **Retrieval-Augmented Generation (RAG)** und **semantic search**.  
> → Belegt, dass spezialisierte GPTs mit klar definiertem Zweck + RAG-Integration deutlich höhere Genauigkeit erreichen.  
> → Deshalb ist **TUna** strikt auf TU-Studienorganisation beschränkt.

---

**BEHAVIORAL IDENTITY**  
*Quelle:* Salewski et al., 2024 – *In-Context Impersonation Reveals Large Language Models’ Strengths and Biases*  
> Zeigt, dass Rollen-Prompts Verhalten, Stil und Bias signifikant beeinflussen.  
> → „Always speak as institutional assistant“ stellt Rollenstabilität und Neutralität sicher.

---

**CORE REASONING LOOP**  
*Quellen:* Li et al., 2024 – *Confidence Matters (Revisiting Intrinsic Self-Correction Capabilities of LLMs)* · Sun et al., 2024 – *Prompt Chaining vs Stepwise Prompt*  
> Li et al. führen das **If-or-Else (IoE)**-Prinzip ein, bei dem LLMs ihre eigene Sicherheit einschätzen und nur bei Unsicherheit revidieren → umgesetzt in Schritt 5.  
> Sun et al. zeigen, dass mehrstufiges Draft–Critique–Refine-Prompting bessere Resultate liefert → umgesetzt in Schritt 6.

---

**RESPONSE STRUCTURE**  
*Quelle:* Sun et al., 2024 – *Prompt Chaining / Refinement in Text Summarization*  
> Klare Phasenstruktur (Draft → Critique → Refine) und explizite Abschnitte (Short Answer, Steps, Details …) erhöhen Transparenz und Lesbarkeit.

---

**HALLUCINATION GUARD**  
*Quellen:* Tran Nhat et al., 2025 – *Kickoff Day 1: Prompt Engineering Basics & Chain-of-Verification* · Zhao et al., 2025  
> *Kickoff Day 1* betont Quellenprüfung, Fehleranalyse und Chain-of-Verification zur Reduktion von Halluzinationen.  
> *Zhao et al.* zeigen, dass Custom GPTs mit RAG-gestützter Wissensbasis weniger falsche Antworten produzieren.  
> → Regel: *„Never invent / state uncertainty.“*

---

**CRISIS MODE**  
*Quelle:* Tran Nhat et al., 2025 – *Kickoff Day 2: Ethical Prompting & Empathy in LLMs*  
> Beschreibt den Umgang mit emotional aufgeladenen oder krisenbezogenen Eingaben.  
> → Empathische, aber abgegrenzte Reaktionen entsprechen HCI-Ethikprinzipien (Empathie ohne Rollensprung).

---

**SECURITY & ETHICS**  
*Quelle:* Tran Nhat et al., 2025 – *Kickoff Day 2: Bias, Accountability & Transparency in AI Systems*  
> Betonung von Verantwortlichkeit und Transparenz im Prompt-Design.  
> → Regeln gegen Prompt-Injection und für DSGVO-Konformität folgen direkt den Lehrinhalten aus *Kickoff Day 2*.

---

**OUTPUT LANGUAGE**  
*Quelle:* Zhao et al., 2025 – *Deriving Insights from Enhanced Accuracy … (Custom GPT for Nursing Exam)*  
> Das Paper stellt den Einsatz von **semantic search und intent-basiertem Retrieval** zur Kontextanpassung vor.  
> → Die automatische Sprachspiegelung in TUna folgt diesem Prinzip der kontextsensitiven Antwortgenerierung.
