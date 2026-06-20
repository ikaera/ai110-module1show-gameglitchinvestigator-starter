# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used                                                       | Expected Behavior                           | Actual Behavior                                                                                                    | Console Error / Output |
| ---------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| 6 (secret #: 59)                                                 | "Go HIGHER!" hint                           | "Go LOWER!" hint shown                                                                                             | none                   |
| Change difficulty from normal (range 1-100, attempts: 8) to hard | Range should increase and attempts decrease | instead Range decreases, attempts decrease is normal (range 1-50, attempts: 5)                                     | none                   |
| Change difficulty from normal (range 1-100, attempts: 8) to easy | Range should decrease and attempts increase | Range decreases but attempts also decrease from 8 to 6 (range 1-20, attempts: 6)                                   | none                   |
| push New Game                                                    | start new game                              | "You already won. Start a new game to play again"- persists, history does not clear up and new game does not start | none                   |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
