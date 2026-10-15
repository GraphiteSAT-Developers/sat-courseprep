# Probability and conditional probability

[← Question bank index](README.md) · Problem-Solving and Data Analysis · 20 questions, easiest first

### 1. psda-bulb-shipment-expected-defective

*Easy · Multiple choice · route: hand-primary · techniques: —*

A hardware store estimates that the probability that a randomly selected light bulb in a shipment is defective is 0.04. Based on this estimate, how many of the 1,250 bulbs in the shipment are expected to be defective?

- **A.** $5$
- **B.** $50$
- **C.** $500$
- **D.** $1200$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** It's given that the probability a bulb is defective is 0.04. The expected number of defective bulbs is the probability times the number of bulbs: 0.04(1,250) = 50. Therefore, 50 bulbs are expected to be defective. Distractors: 5 uses 0.004 (0.4%) instead of 0.04; 500 uses 0.4 (40%); 1200 is the expected number of bulbs that are not defective, 1,250 - 50.

</details>

---

### 2. psda-fair-food-ride-joint

*Easy · Multiple choice · route: hand-primary · techniques: —*

A two-way table classifies 300 people at a fair by whether each bought food and whether each bought a ride ticket: food and ride ticket, 120; food only, 70; ride ticket only, 50; neither, 60. What is the probability that a person chosen at random from this group bought both?

- **A.** $\frac{2}{5}$
- **B.** $\frac{17}{30}$
- **C.** $\frac{19}{30}$
- **D.** $\frac{12}{17}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that 120 of the 300 people bought both food and a ride ticket. The probability is 120/300 = 2/5. Therefore, the probability is 2/5. Distractors: 17/30 is the probability of buying a ride ticket, (120 + 50)/300; 19/30 is the probability of buying food, (120 + 70)/300; 12/17 is the probability of buying food given a ride ticket, 120/170.

</details>

---

### 3. psda-parking-lot-van

*Easy · Multiple choice · route: hand-primary · techniques: T11*

There are 40 vehicles in a store's parking lot. Of these, 14 are trucks, 18 are sedans, and the rest are vans. If one of the 40 vehicles is selected at random, what is the probability that the selected vehicle is a van?

- **A.** $\frac{1}{5}$
- **B.** $\frac{7}{20}$
- **C.** $\frac{9}{20}$
- **D.** $\frac{4}{5}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The number of vans is 40 - 14 - 18 = 8. The probability of selecting a van is the number of vans divided by the total number of vehicles, 8/40 = 1/5. Distractors: 7/20 is the probability of a truck (14/40); 9/20 is the probability of a sedan (18/40); 4/5 is the probability of not selecting a van (32/40).

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{40-14-18}{40}</code>

The line shows 0.2; the fraction toggle gives 1/5. Counting the vans by hand is faster.

</details>

---

### 4. psda-prob-red-cards-letter

*Easy · Multiple choice · route: hand-primary · techniques: —*

Each of 90 cards is either red or blue, and each card shows either a letter or a digit. Of the 40 red cards, 15 show a letter. What is the probability that a red card chosen at random shows a letter?

- **A.** $\frac{1}{6}$
- **B.** $\frac{3}{8}$
- **C.** $\frac{4}{9}$
- **D.** $\frac{5}{8}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** It's given that the card is selected from the 40 red cards, so 40 is the denominator. Of these, 15 show a letter, so the probability is 15/40 = 3/8. Distractors: 1/6 uses all 90 cards as the denominator, 15/90; 4/9 is the probability that a card is red, 40/90; 5/8 is the probability that a red card shows a digit, 25/40.

</details>

---

### 5. psda-tokens-not-red

*Easy · Multiple choice · route: hand-primary · techniques: T11*

A box contains 50 tokens. Of these, 12 are red, 18 are blue, and the rest are green. One token is selected from the box at random. What is the probability that the selected token is not red?

- **A.** $\frac{6}{25}$
- **B.** $\frac{9}{25}$
- **C.** $\frac{2}{5}$
- **D.** $\frac{19}{25}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that 12 of the 50 tokens are red, so 50 - 12 = 38 tokens are not red. The probability of selecting a token that is not red is 38/50 = 19/25. Distractors: 6/25 is the probability that the token is red, 12/50; 9/25 is the probability that it is blue, 18/50; 2/5 is the probability that it is green, 20/50, which answers 'not red and not blue' rather than 'not red'.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{50-12}{50}</code>

The line shows 0.76; the fraction toggle gives 19/25. The complement is quicker in the head than in the calculator.

</details>

---

### 6. psda-bean-plants-soil-given-flowered

*Medium · Multiple choice · route: either · techniques: T11*

A two-way table classifies 250 bean plants by soil type and whether each flowered: soil A and flowered, 84; soil A and did not flower, 36; soil B and flowered, 78; soil B and did not flower, 52. If a plant that flowered is selected at random, what is the probability that it was grown in soil B?

- **A.** $\frac{39}{125}$
- **B.** $\frac{13}{27}$
- **C.** $\frac{13}{25}$
- **D.** $\frac{3}{5}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The selection is made only from plants that flowered, and 84 + 78 = 162 plants flowered. Of these, 78 were grown in soil B, so the probability is 78/162 = 13/27. Therefore, the probability is 13/27. Distractors: 3/5 reverses the condition, the probability that a soil B plant flowered, 78/130; 39/125 uses all 250 plants as the denominator, 78/250; 13/25 is the probability that a plant was grown in soil B, 130/250, ignoring the condition.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{78}{84+78}</code>

The line shows 0.4814...; the fraction toggle gives 13/27. The work is choosing the denominator: only the plants that flowered.

</details>

---

### 7. psda-club-members-given-probability

*Medium · Student-produced response · route: either · techniques: T9, T11*

A club has only junior members and senior members. The club has 24 junior members. If one member of the club is selected at random, the probability that the member is a senior member is $\frac{5}{8}$. How many members does the club have?

**Answer:** 64

<details><summary>Solutions</summary>

**By hand.** It's given that the probability of selecting a senior member is 5/8, so the probability of selecting a junior member is 1 - 5/8 = 3/8. The 24 junior members are therefore 3/8 of the club: (3/8)n = 24, so n = 24 · 8/3 = 64. Dividing 24 by 5/8 (38.4) or treating 24 as the number of seniors are the common slips.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{24}{1-\frac{5}{8}}</code>

The line shows 64. The setup, that the juniors are the other 3/8 of the club, is the work.

</details>

---

### 8. psda-conditional-table

*Medium · Multiple choice · route: hand-primary · techniques: T11*

A survey asked 240 students in grades 11 and 12 whether they prefer online or in-person study sessions. Of the 120 grade 11 students, 54 prefer online sessions. Of the 120 grade 12 students, 72 prefer online sessions. If a student who prefers online sessions is chosen at random, what is the probability that the student is in grade 12?

- **A.** $\frac{3}{10}$
- **B.** $\frac{21}{40}$
- **C.** $\frac{4}{7}$
- **D.** $\frac{3}{5}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Condition on preferring online: 54 + 72 = 126 students. Of those, 72 are in grade 12, so the probability is 72/126 = 4/7. Distractors: 3/10 is 72/240 (whole survey as denominator), 3/5 is 72/120 (conditioning on grade 12 instead), 21/40 is 126/240 (P(online)).

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{72}{54+72}</code>

The fraction toggle shows 4/7. The work is reading the table; the calculator only reduces the fraction.

</details>

---

### 9. psda-household-pets-at-least-two

*Medium · Multiple choice · route: hand-primary · techniques: —*

A survey of 50 households recorded the number of pets in each: 0 pets, 14 households; 1 pet, 18 households; 2 pets, 11 households; 3 pets, 7 households. For a household chosen at random from those surveyed, what is the probability of at least 2 pets?

- **A.** $\frac{9}{25}$
- **B.** $\frac{1}{2}$
- **C.** $\frac{16}{25}$
- **D.** $\frac{18}{25}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** At least 2 pets means 2 pets or 3 pets, so 11 + 7 = 18 households qualify. The probability is 18/50 = 9/25. Therefore, the probability is 9/25. Distractors: 1/2 is 18/36, dividing by only the households that have pets; 16/25 is 32/50, the probability of fewer than 2 pets; 18/25 is 36/50, the probability of at least 1 pet.

</details>

---

### 10. psda-inspection-truck-given-failed

*Medium · Student-produced response · route: either · techniques: T11*

A two-way table classifies the 360 vehicles inspected at a station in one week by type and result: car and passed, 198; car and failed, 42; truck and passed, 84; truck and failed, 36. One of the vehicles that failed is chosen at random. What is the probability that this vehicle is a truck?

**Answer:** 6/13 (≈ 0.4615)

<details><summary>Solutions</summary>

**By hand.** The selection is made only from the vehicles that failed, and 42 + 36 = 78 vehicles failed. Of these, 36 are trucks, so the probability is 36/78 = 6/13. Therefore, the probability is 6/13. Using all 360 vehicles (36/360 = 1/10) or all 120 trucks (36/120 = 3/10, the probability that a truck failed) are the common slips.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{36}{42+36}</code>

The line shows 0.4615...; enter 6/13 (fraction toggle) or the full-width decimal .4615 or 0.461. A short decimal such as 0.46 is marked wrong.

</details>

---

### 11. psda-tiles-with-replacement-both-blue

*Medium · Multiple choice · route: hand-primary · techniques: T11*

A bag contains 30 tiles, and 12 of the tiles are blue. A tile is drawn at random, its color is noted, and it is put back in the bag. A second tile is then drawn at random. What is the probability that both tiles drawn are blue?

- **A.** $\frac{22}{145}$
- **B.** $\frac{4}{25}$
- **C.** $\frac{2}{5}$
- **D.** $\frac{4}{5}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Each draw is made from all 30 tiles, because the first tile is put back, so the probability of blue is 12/30 = 2/5 on each draw and the draws are independent. The probability that both are blue is (2/5)(2/5) = 4/25. Therefore, the probability is 4/25. Distractors: 22/145 is (12/30)(11/29), the probability without replacement; 2/5 is the probability for a single draw; 4/5 adds the two probabilities instead of multiplying them.

**Desmos** (not yet verified in Desmos). Type:<br><code>\left(\frac{12}{30}\right)^2</code>

The line shows 0.16; the fraction toggle gives 4/25. Multiplying 2/5 by 2/5 by hand is faster; use Desmos only as a check.

</details>

---

### 12. psda-workshop-book-conditional

*Medium · Multiple choice · route: either · techniques: T11*

Of 150 people at a workshop, 90 were first-time attendees. Of the 40 people who bought a book, 28 were first-time attendees. If one of the people who did not buy a book is selected at random, what is the probability that this person was a first-time attendee?

- **A.** $\frac{31}{75}$
- **B.** $\frac{31}{55}$
- **C.** $\frac{31}{45}$
- **D.** $\frac{7}{10}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Build the two-way table. The number of people who did not buy a book is 150 - 40 = 110. Of the 90 first-time attendees, 28 bought a book, so 90 - 28 = 62 did not. Conditioning on not buying a book, the probability of a first-time attendee is 62/110 = 31/55. Distractors: 31/75 uses all 150 people as the denominator, 62/150; 31/45 conditions the other way, the probability that a first-time attendee did not buy a book, 62/90; 7/10 is the probability that a book buyer was a first-time attendee, 28/40.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{90-28}{150-40}</code>

The line shows about 0.5636; the fraction toggle gives 31/55. Filling in the two-way table (62 first-time attendees among the 110 who did not buy a book) is the work.

</details>

---

### 13. psda-commuters-transit-conditional

*Hard · Multiple choice · route: either · techniques: T11*

Each of 200 commuters either drives or takes transit. Of the 120 who drive, 45 commute more than 30 minutes. Of all 200 commuters, 95 commute more than 30 minutes. What is the probability that a randomly chosen commuter who takes transit has a commute of 30 minutes or less?

- **A.** $\frac{3}{20}$
- **B.** $\frac{2}{7}$
- **C.** $\frac{3}{8}$
- **D.** $\frac{5}{8}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Fill in the two-way table. There are 200 - 120 = 80 transit commuters. Of the 95 commuters over 30 minutes, 45 drive, so 95 - 45 = 50 take transit. The transit commuters at 30 minutes or less number 80 - 50 = 30. Conditioning on taking transit, the probability is 30/80 = 3/8. Distractors: 5/8 is the probability that a transit commuter commutes more than 30 minutes (50/80); 3/20 uses all 200 commuters as the denominator (30/200); 2/7 conditions the other way, the probability that a commuter at 30 minutes or less takes transit (30/105).

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{80-(95-45)}{80}</code>

The line shows 0.375; the fraction toggle gives 3/8. The work is filling in the two-way table: 80 transit commuters, 50 of them over 30 minutes.

</details>

---

### 14. psda-display-bin-red-apples

*Hard · Student-produced response · route: either · techniques: T11*

A store's display bin holds 18 green apples and some red apples. After 6 more red apples are added to the bin, the probability that an apple selected at random from the bin is green is $\frac{3}{8}$. How many red apples were in the bin before the 6 were added?

**Answer:** 24

<details><summary>Solutions</summary>

**By hand.** It's given that after the 6 red apples are added, the 18 green apples are 3/8 of the bin. If T is the new total, (3/8)T = 18, so T = 18 · 8/3 = 48. The bin then holds 48 - 18 = 30 red apples, so before the 6 were added it held 30 - 6 = 24 red apples. Therefore, the answer is 24. Answering 30 gives the red apples after the 6 were added, and answering 48 gives the total, not the red apples.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{18}{\frac{3}{8}}-18-6</code>

The line shows 24. The setup is the work: 18 is 3/8 of the new total, then remove the green apples and the 6 added red ones.

</details>

---

### 15. psda-game-club-neither

*Hard · Multiple choice · route: hand-primary · techniques: T11*

Of the 80 members of a game club, 30 play chess, 25 play checkers, and 10 play both chess and checkers. What is the probability that a randomly chosen member of the club plays neither chess nor checkers?

- **A.** $\frac{3}{16}$
- **B.** $\frac{5}{16}$
- **C.** $\frac{7}{16}$
- **D.** $\frac{9}{16}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The 10 members who play both are counted in the 30 and in the 25, so the number who play at least one game is 30 + 25 - 10 = 45. The number who play neither is 80 - 45 = 35, and the probability is 35/80 = 7/16. Therefore, the probability is 7/16. Distractors: 5/16 is (80 - 30 - 25)/80, forgetting to add back the 10 counted twice; 3/16 is (80 - 30 - 25 - 10)/80, subtracting the overlap a third time; 9/16 is 45/80, the probability of playing at least one game.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{80-(30+25-10)}{80}</code>

The line shows 0.4375; the fraction toggle gives 7/16. Desmos is slower than the count by hand and only helps once the overlap is handled; use it as a check.

</details>

---

### 16. psda-prob-museum-audio-no-tour

*Hard · Multiple choice · route: either · techniques: T11*

Of the 300 visitors to a museum one day, 180 took a guided tour and 110 rented an audio guide; 65 visitors did both. What is the probability that a randomly chosen visitor who did not take a guided tour rented an audio guide?

- **A.** $\frac{3}{20}$
- **B.** $\frac{11}{30}$
- **C.** $\frac{3}{8}$
- **D.** $\frac{9}{22}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Build the two-way table. The number of visitors who did not take a guided tour is 300 - 180 = 120. Of the 110 who rented an audio guide, 65 also took a tour, so 110 - 65 = 45 rented an audio guide without a tour. Conditioning on not taking a tour, the probability is 45/120 = 3/8. Distractors: 3/20 uses all 300 visitors as the denominator, 45/300; 11/30 is the probability that any visitor rented an audio guide, 110/300, ignoring the condition; 9/22 conditions the other way, the probability that an audio-guide renter did not take a tour, 45/110.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{110-65}{300-180}</code>

The line shows 0.375; the fraction toggle gives 3/8. The work is filling in the two-way table: 120 visitors without a tour, 45 of whom rented an audio guide.

</details>

---

### 17. psda-prob-seed-varieties-not-sprouted

*Hard · Student-produced response · route: hand-primary · techniques: —*

A garden club planted 90 seeds: 50 of variety A and 40 of variety B. Of the variety A seeds, 40 sprouted. If one of the seeds that sprouted is selected at random, the probability that it is variety A is $\frac{5}{8}$. How many of the variety B seeds did not sprout?

**Answer:** 16

<details><summary>Solutions</summary>

**By hand.** It's given that the 40 sprouted variety A seeds are 5/8 of all sprouted seeds, so the number of sprouted seeds s satisfies (5/8)s = 40, and s = 64. The number of sprouted variety B seeds is 64 - 40 = 24. Since there are 40 variety B seeds, 40 - 24 = 16 did not sprout. Therefore, 16 variety B seeds did not sprout. Common slips: 24 is the number of variety B seeds that sprouted; 10 is the number of variety A seeds that did not sprout; 26 is the total number of seeds that did not sprout, 90 - 64.

</details>

---

### 18. psda-prob-shelter-young-cats

*Hard · Multiple choice · route: either · techniques: T11*

An animal shelter has 120 animals, 45 of them cats and the rest dogs. Of the dogs, 40% are under one year old. If an animal under one year old is selected at random, the probability that it is a dog is $\frac{3}{5}$. What is the probability that a randomly selected cat is under one year old?

- **A.** $\frac{2}{3}$
- **B.** $\frac{4}{9}$
- **C.** $\frac{2}{5}$
- **D.** $\frac{1}{6}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** There are 120 - 45 = 75 dogs, and 40% of them, 0.4(75) = 30, are under one year old. It's given that these 30 dogs are 3/5 of all animals under one year old, so that total u satisfies (3/5)u = 30, and u = 50. Then 50 - 30 = 20 cats are under one year old, and the probability that a randomly selected cat is under one year old is 20/45 = 4/9. Distractors: 2/3 divides the 30 young dogs by the 45 cats; 2/5 is the probability that an animal under one year old is a cat, 20/50, which conditions on age instead of on being a cat; 1/6 uses all 120 animals as the denominator, 20/120.

**Desmos** (not yet verified in Desmos). Type:<br><code>d=0.4(120-45)</code><br><code>u=\frac{d}{\frac{3}{5}}</code><br><code>\frac{u-d}{45}</code>

The lines show d = 30, u = 50 and 0.4444...; the fraction toggle gives 4/9. The setup (30 young dogs are 3/5 of all young animals) is the work.

</details>

---

### 19. psda-spanish-art-given-art

*Hard · Multiple choice · route: either · techniques: T11*

Of 400 students at a school, 60% take Spanish. Of the students who take Spanish, 25% take art, and of the students who do not take Spanish, 40% take art. What is the probability that a student chosen at random from those who take art also takes Spanish?

- **A.** $\frac{1}{4}$
- **B.** $\frac{31}{100}$
- **C.** $\frac{15}{31}$
- **D.** $\frac{3}{5}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that 60% of 400, or 240 students, take Spanish, so 160 do not. Of the 240, 25% take art: 0.25(240) = 60. Of the 160, 40% take art: 0.4(160) = 64. So 60 + 64 = 124 students take art, and 60 of them take Spanish. The probability is 60/124 = 15/31. Therefore, the probability is 15/31. Distractors: 1/4 is the probability that a Spanish student takes art, the reverse condition; 31/100 is the probability that a student takes art, 124/400; 3/5 is the probability that a student takes Spanish, ignoring the condition.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{0.25(240)}{0.25(240)+0.4(160)}</code>

The line shows 0.4838...; the fraction toggle gives 15/31. The work is the two counts: 240 take Spanish and 160 do not.

</details>

---

### 20. psda-two-lines-defective-source

*Hard · Multiple choice · route: either · techniques: T11*

Last month, production line A made 3,000 items, of which 4% were defective, and production line B made 5,000 items, of which 1.5% were defective. Among the defective items, what is the probability that a randomly chosen one came from line A?

- **A.** $\frac{39}{1600}$
- **B.** $\frac{3}{8}$
- **C.** $\frac{5}{13}$
- **D.** $\frac{8}{13}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Line A made 0.04(3,000) = 120 defective items and line B made 0.015(5,000) = 75, so there are 120 + 75 = 195 defective items. The probability that a defective item came from line A is 120/195 = 8/13. Therefore, the probability is 8/13. Distractors: 3/8 is 3,000/8,000, the share of all items made by line A, ignoring the condition; 5/13 is 75/195, the probability for line B; 39/1600 is 195/8,000, the probability that any item is defective.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{0.04(3000)}{0.04(3000)+0.015(5000)}</code>

The line shows 0.6153...; the fraction toggle gives 8/13. The work is converting each percent to a count of defective items first.

</details>

---
