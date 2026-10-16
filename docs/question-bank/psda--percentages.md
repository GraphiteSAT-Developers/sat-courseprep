# Percentages

[← Question bank index](README.md) · Problem-Solving and Data Analysis · 23 questions, easiest first

### 1. psda-jacket-sale-price

*Easy · Multiple choice · route: hand-primary · techniques: T9*

The regular price of a jacket is 80.00 dollars. The jacket is on sale for 35% off the regular price. What is the sale price, in dollars, of the jacket?

- **A.** $28.00$
- **B.** $45.00$
- **C.** $52.00$
- **D.** $108.00$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A discount of 35% leaves 100% - 35% = 65% of the regular price, so the sale price is 0.65 · 80.00 = 52.00 dollars. Alternate approach: the discount is 0.35 · 80 = 28 dollars, and 80 - 28 = 52. Distractors: 28.00 is the amount of the discount, not the sale price; 45.00 subtracts 35 dollars instead of 35%; 108.00 increases the price by 35% instead of decreasing it.

**Desmos** (not yet verified in Desmos). Type:<br><code>80\cdot0.65</code>

The line shows 52. Desmos is only the arithmetic; 35% off means paying 65%, which is the step to get right.

</details>

---

### 2. psda-orchard-young-apple-percent

*Easy · Multiple choice · route: hand-primary · techniques: T9*

An orchard has 400 trees: 240 are apple trees and the rest are pear trees. Of the apple trees, 60 are less than 5 years old. What percent of all the trees in the orchard are apple trees less than 5 years old?

- **A.** $60\%$
- **B.** $40\%$
- **C.** $25\%$
- **D.** $15\%$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that the orchard has 400 trees in all and that 60 of them are apple trees less than 5 years old. As a percent of all the trees, this is 60/400 · 100 = 15. Therefore, 15% of the trees are apple trees less than 5 years old. Distractors: 60% is the share of all trees that are apple trees (240/400); 40% is the share that are pear trees (160/400); 25% is 60 as a percent of the 240 apple trees, which uses the part of the breakdown instead of the whole orchard.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{60}{400}\cdot100</code>

The line shows 15. Dividing by hand is just as fast; use Desmos only to check the arithmetic, and make sure the denominator is all 400 trees.

</details>

---

### 3. psda-percent-of-number

*Easy · Multiple choice · route: hand-primary · techniques: T9*

What number is 35% of 840?

- **A.** $29.4$
- **B.** $294$
- **C.** $546$
- **D.** $2,400$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** 35% of a number is 0.35 times the number. Multiplying yields 0.35 · 840 = 294. Therefore, 294 is 35% of 840. Distractors: 29.4 uses 0.035 instead of 0.35; 546 is 65% of 840, the part that remains after taking 35%; 2,400 divides 840 by 0.35 instead of multiplying.

**Desmos** (not yet verified in Desmos). Type:<br><code>0.35\cdot840</code>

The line shows 294. One multiplication by hand (10% is 84, so 35% is 3.5 · 84) is as fast.

</details>

---

### 4. psda-scale-reading-percent-error

*Easy · Student-produced response · route: either · techniques: T9, T11*

A kitchen scale shows a mass of 494 grams for an object whose actual mass is 520 grams. The reading is $p\%$ less than the actual mass. What is the value of $p$?

**Answer:** 5

<details><summary>Solutions</summary>

**By hand.** It's given that the actual mass is 520 grams and the reading is 494 grams, so the reading is 520 − 494 = 26 grams too low. A percent less than the actual mass is measured against the actual mass: 26/520 = 0.05, which is 5%. Therefore, p = 5.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{520-494}{520}\cdot100</code>

The line shows 5. Enter 5. Divide by the actual mass, 520; dividing by the reading, 494, gives about 5.263, which is the wrong base.

</details>

---

### 5. psda-a-b-c-percent-chain

*Medium · Student-produced response · route: hand-primary · techniques: —*

The value of $a$ is 40% of $b$, and $b$ is 150% of $c$, where $a$, $b$, and $c$ are positive constants. If $a$ is $p\%$ of $c$, what is the value of $p$?

**Answer:** 60

<details><summary>Solutions</summary>

**By hand.** It's given that a = 0.40b and b = 1.50c. Substituting 1.50c for b in the first equation yields a = 0.40(1.50c) = 0.60c. Therefore, a is 60% of c, and p = 60. Adding the percents (190) or multiplying 40 by 150 without converting either to a decimal are the common slips.

</details>

---

### 6. psda-grain-drying-original

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

During drying, a batch of grain lost 12% of its mass. After drying, the grain had a mass of 2,640 kilograms. What was the mass, in kilograms, of the grain before drying?

- **A.** $2,323.2$
- **B.** $2,956.8$
- **C.** $3,000$
- **D.** $22,000$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that the grain lost 12% of its mass, so the remaining mass is 100% − 12% = 88% of the original mass m. Therefore, 0.88m = 2,640, and dividing both sides by 0.88 yields m = 3,000. The grain had a mass of 3,000 kilograms before drying. Distractors: 2956.8 adds 12% of 2,640 to 2,640, taking the percent of the wrong base; 2323.2 takes 12% off 2,640 a second time; 22,000 divides 2,640 by 0.12, treating 2,640 as the mass lost.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=0.88x</code><br><code>y=2640</code>

Click the intersection (zoom out; it is near x = 3000) and read x = 3000.

</details>

---

### 7. psda-helmet-price-before-tax

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

The total cost of a helmet, including a 6% sales tax, is 63.60 dollars. What is the cost, in dollars, of the helmet before tax?

- **A.** $57.60$
- **B.** $59.78$
- **C.** $60.00$
- **D.** $67.42$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let x be the cost, in dollars, before tax. Adding a 6% tax multiplies the cost by 1.06, so 1.06x = 63.60. Dividing both sides by 1.06 yields x = 60. Therefore, the helmet costs 60.00 dollars before tax. Distractors: 57.60 subtracts 6 dollars instead of 6%; 59.78 takes 6% off the total (63.60 · 0.94), but the tax is 6% of the pre-tax cost, not of the total; 67.42 adds another 6% to the total (63.60 · 1.06).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=1.06x</code><br><code>y=63.6</code>

Zoom out until the two graphs meet near x = 60, click the intersection and read x = 60, so the cost before tax is 60.00 dollars.

</details>

---

### 8. psda-machine-value-depreciation

*Medium · Multiple choice · route: desmos-primary · techniques: T9*

A machine was bought for 18,000.00 dollars. Each year, its value decreases by 10% of its value at the start of that year. What is the value, in dollars, of the machine 3 years after it was bought?

- **A.** $4,878$
- **B.** $12,600$
- **C.** $13,122$
- **D.** $14,580$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Each year the value is multiplied by 1 − 0.10 = 0.9, so after 3 years the value is 18,000(0.9)^3 = 18,000 · 0.729 = 13,122. Therefore, the machine is worth 13,122.00 dollars. Distractors: 4,878.00 is the total amount of value lost (18,000 − 13,122), not the value; 12,600.00 takes 10% of the original value each year (a 30% drop); 14,580.00 is the value after 2 years.

**Desmos** (not yet verified in Desmos). Type:<br><code>18000(0.9)^3</code>

The line shows 13122, so the value is 13,122.00 dollars. Use the growth factor 0.9 with the exponent 3.

</details>

---

### 9. psda-notebook-price-revenue

*Medium · Student-produced response · route: either · techniques: T9*

A store raised the price of a notebook by 25%. After the increase, the number of notebooks the store sold each week decreased by 16%. The weekly revenue from notebooks, the price times the number sold, increased by $p\%$. What is the value of $p$?

**Answer:** 5

<details><summary>Solutions</summary>

**By hand.** Revenue is price times number sold, so its growth factor is the product of the two growth factors: 1.25 · (1 − 0.16) = 1.25 · 0.84 = 1.05. A growth factor of 1.05 is a 5% increase. Therefore, p = 5. Subtracting the percents (25 − 16 = 9) is the common error.

**Desmos** (not yet verified in Desmos). Type:<br><code>(1.25\cdot0.84-1)\cdot100</code>

The line shows 5. Enter 5.

</details>

---

### 10. psda-percent-of-percent-music-art

*Medium · Student-produced response · route: either · techniques: T9, T11*

At a certain school, 45% of the students take a music class. Of the students who take a music class, 60% also take an art class. If $p\%$ of all the students at the school take both a music class and an art class, what is the value of $p$?

**Answer:** 27

<details><summary>Solutions</summary>

**By hand.** It's given that 45% of the students take music and that 60% of those students also take art. The students who take both are 60% of 45% of all students, which is 0.60 · 0.45 = 0.27, or 27% of all students. Therefore, p = 27. Adding the percents (105) or subtracting them (15) ignores that the 60% applies only to the music students.

**Desmos** (not yet verified in Desmos). Type:<br><code>0.45\cdot0.60\cdot100</code>

The line shows 27. Enter 27, not 0.27: the question asks for p where p% is the share.

</details>

---

### 11. psda-percent-return

*Medium · Multiple choice · route: either · techniques: T1*

A quantity is increased by 30% and the result is then decreased by $p\%$. The final amount is 91% of the original quantity. What is the value of $p$?

- **A.** $9$
- **B.** $21$
- **C.** $30$
- **D.** $39$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** 1.3(1 - p/100) = 0.91, so 1 - p/100 = 0.7 and p = 30. Distractors: 9 is 100 - 91, 39 is 130 - 91 (subtracting percentage points), 21 is 30 - 9.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=1.3\left(1-\frac{x}{100}\right)</code><br><code>y=0.91</code>

Click the intersection: x = 30.

</details>

---

### 12. psda-pond-fish-three-year-chain

*Medium · Multiple choice · route: either · techniques: T9*

The number of fish in a pond increased by 20% during the first year, decreased by 25% during the second year, and increased by 10% during the third year. The number of fish at the end of the third year was what percent of the number at the start of the first year?

- **A.** $90\%$
- **B.** $99\%$
- **C.** $101\%$
- **D.** $105\%$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Each percent change multiplies the number of fish by a growth factor: an increase of 20% by 1.20, a decrease of 25% by 0.75, and an increase of 10% by 1.10. The product is 1.20 · 0.75 · 1.10 = 0.99. Therefore, the final number is 99% of the starting number. Distractors: 90% stops after the second year (1.20 · 0.75); 101% treats the 1% change as an increase; 105% adds the percents (20 − 25 + 10 = 5) instead of multiplying the growth factors.

**Desmos** (not yet verified in Desmos). Type:<br><code>1.2\cdot0.75\cdot1.1</code>

The line shows 0.99, so the final number is 99% of the starting number. Type the three growth factors, not the percents.

</details>

---

### 13. psda-scooter-fleet-percent-increase

*Medium · Multiple choice · route: hand-primary · techniques: T9*

The number of rental scooters in a city's fleet increased by 150% from 2020 to 2024. The fleet had 1,500 scooters in 2024. How many scooters did the fleet have in 2020?

- **A.** $600$
- **B.** $750$
- **C.** $1,000$
- **D.** $2,250$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** An increase of 150% means the 2024 number is 100% + 150% = 250% of the 2020 number, so the growth factor is 2.5. If n is the 2020 number, then 2.5n = 1,500, and dividing both sides by 2.5 yields n = 600. Therefore, the fleet had 600 scooters in 2020. Distractors: 1,000 divides 1,500 by 1.5, reading 'increased by 150%' as 'is 150% of'; 750 divides by 2, treating the increase as a doubling; 2,250 multiplies 1,500 by 1.5, applying the increase in the wrong direction.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{1500}{1+1.5}</code>

The line shows 600. Recognizing that a 150% increase is a growth factor of 2.5 is the whole problem; the division is quick by hand.

</details>

---

### 14. psda-chess-club-girls

*Hard · Multiple choice · route: hand-primary · techniques: T1*

Each of the 1,000 students at a school is a boy or a girl. Of the boys, 30% are in the chess club, and of the girls, 45% are in the chess club. Overall, 36% of the students are in the chess club. How many girls are at the school?

- **A.** $400$
- **B.** $500$
- **C.** $600$
- **D.** $640$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that 36% of the 1,000 students, or 360 students, are in the club. Let g be the number of girls, so there are 1,000 − g boys. The club members number 0.3(1,000 − g) + 0.45g = 300 + 0.15g. Setting 300 + 0.15g = 360 yields 0.15g = 60, so g = 400. Therefore, there are 400 girls at the school. Distractors: 600 is the number of boys; 500 assumes equal numbers of boys and girls; 640 is the number of students not in the club (1,000 − 360).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=0.3(1000-x)+0.45x</code><br><code>y=360</code>

Here x is the number of girls. Click the intersection and read x = 400. Writing the one equation by hand is about as fast, so Desmos is a check.

</details>

---

### 15. psda-deposit-two-year-rate

*Hard · Multiple choice · route: desmos-primary · techniques: T1, T13*

A deposit of 5,000.00 dollars is placed in an account. At the end of each year, the balance increases by $r\%$, where $r$ is a positive constant. After 2 years, with no other deposits or withdrawals, the balance is 5,832.00 dollars. What is the value of $r$?

- **A.** $8$
- **B.** $8.32$
- **C.** $16.64$
- **D.** $108$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Each year the balance is multiplied by 1 + r/100, so after 2 years 5,000(1 + r/100)^2 = 5,832. Dividing by 5,000 yields (1 + r/100)^2 = 1.1664, and since r is positive, 1 + r/100 = 1.08. Therefore, r = 8. Distractors: 8.32 splits the total gain of 16.64% evenly over the 2 years, ignoring that the second year's increase applies to a larger balance; 16.64 is the total percent increase over 2 years; 108 is the yearly growth factor written as a percent.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5000(1+x/100)^2</code><br><code>y=5832</code><br><code>5000(1.08)^2</code>

The curve meets y = 5832 at x = 8 and at x = −208; r is positive, so take 8. To check choices instead, the third line shows 5832 for r = 8.

</details>

---

### 16. psda-double-increase-44

*Hard · Student-produced response · route: either · techniques: T1*

The price of a certain item was increased by $p\%$, and then the new price was increased by $p\%$ again. The final price was 44% greater than the original price. What is the value of $p$?

**Answer:** 20

<details><summary>Solutions</summary>

**By hand.** It's given that the price is increased by p% twice, so the original price is multiplied by the growth factor 1 + p/100 two times, and the final price is 1.44 times the original. Therefore, (1 + p/100)^2 = 1.44. Since an increase makes 1 + p/100 positive, 1 + p/100 = 1.2, which yields p = 20. A common slip is 22, which splits the 44% into two equal additive increases and ignores the compounding.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left(1+\frac{x}{100}\right)^2</code><br><code>y=1.44</code>

Click the intersection with positive x and read x = 20. The other intersection, x = −220, is not an increase.

</details>

---

### 17. psda-markup-discount-profit-p

*Hard · Multiple choice · route: desmos-primary · techniques: T9, T13*

A store sets the regular price of a certain item 60% above the item's wholesale cost. During a sale, the regular price is reduced by $p\%$, and the store still sells the item for 20% more than the wholesale cost. What is the value of $p$?

- **A.** $20$
- **B.** $25$
- **C.** $37.5$
- **D.** $40$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Let the wholesale cost be c. A regular price 60% above cost is 1.6c, and a sale price 20% above cost is 1.2c. Reducing 1.6c by p% gives 1.6c(1 - p/100), so 1.6c(1 - p/100) = 1.2c. Dividing both sides by 1.6c yields 1 - p/100 = 0.75, so p/100 = 0.25 and p = 25. Distractors: 40 subtracts the percents, 60% - 20%, as if percent changes added; 37.5 reduces the regular price all the way back to cost, 0.6/1.6; 20 repeats the profit percent as the discount.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(p)=1.6\left(1-\frac{p}{100}\right)</code><br><code>f(20)</code><br><code>f(25)</code><br><code>f(37.5)</code><br><code>f(40)</code>

Let the wholesale cost be 1, so f(p) is the sale price as a fraction of the cost. Only f(25) shows 1.2, the price that is 20% above cost; f(20) shows 1.28, f(37.5) shows 1, and f(40) shows 0.96.

</details>

---

### 18. psda-mixing-saline

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

A chemist has a saline solution that is 12% salt by volume and another that is 40% salt by volume. How many milliliters of the 40% solution must be combined with some of the 12% solution to produce 350 milliliters of a solution that is 28% salt by volume?

- **A.** $150$
- **B.** $175$
- **C.** $200$
- **D.** $245$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let y be the amount of 40% solution; then 350 - y is the 12% amount. Salt: 0.12(350 - y) + 0.40y = 0.28(350) = 98, so 42 + 0.28y = 98 and y = 200. Distractors: 150 is the amount of the 12% solution (read the wrong coordinate); 245 is 0.7 · 350, treating 28/40 as the fraction needed; 175 assumes equal parts.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y=350</code><br><code>0.12x+0.4y=0.28\cdot350</code>

Let x be milliliters of the 12% solution and y of the 40%. Click the intersection: (150, 200). The question asks for the 40% solution, so the answer is y = 200.

</details>

---

### 19. psda-monthly-sales-successive

*Hard · Multiple choice · route: desmos-primary · techniques: T9*

A store sold 2,500 units of a product in January. Sales in February were 8% lower than in January, and sales in March were 15% higher than in February. March sales were $p\%$ higher than January sales. What is the value of $p$?

- **A.** $5.8$
- **B.** $7$
- **C.** $23$
- **D.** $105.8$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that February sales were 8% lower than January's, so February sales were 0.92 · 2,500 = 2,300 units, and that March sales were 15% higher than February's, so March sales were 1.15 · 2,300 = 2,645 units. The increase from January is 2,645 − 2,500 = 145, and 145/2,500 = 0.058, or 5.8%. Therefore, p = 5.8. Alternate approach: the combined growth factor is 0.92 · 1.15 = 1.058. Distractors: 7 subtracts the percents (15 − 8), ignoring that the 15% applies to the smaller February total; 23 adds them; 105.8 reports March sales as a percent of January sales instead of the percent increase.

**Desmos** (not yet verified in Desmos). Type:<br><code>m=2500\cdot0.92\cdot1.15</code><br><code>\frac{m-2500}{2500}\cdot100</code>

The first line shows 2645 (March sales); the second shows 5.8.

</details>

---

### 20. psda-recycling-households-p

*Hard · Multiple choice · route: desmos-primary · techniques: T9*

In 2020, 40% of the 2,500 households in a town recycled. In 2024, 50% of the 2,800 households in the town recycled. The number of households that recycled was $p\%$ greater in 2024 than in 2020. What is the value of $p$?

- **A.** $10$
- **B.** $25$
- **C.** $40$
- **D.** $140$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that 40% of 2,500 households recycled in 2020, which is 0.4 · 2,500 = 1,000 households, and 50% of 2,800 households recycled in 2024, which is 0.5 · 2,800 = 1,400 households. The increase is 1,400 − 1,000 = 400, and 400/1,000 = 0.40, so the number grew by 40%. Therefore, p = 40. Distractors: 10 is the change in percentage points (50 − 40); 25 is the percent change in the recycling rate (10/40), which ignores the growth in the number of households; 140 is the 2024 count as a percent of the 2020 count, not the percent increase.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{0.5\cdot2800-0.4\cdot2500}{0.4\cdot2500}\cdot100</code>

The line shows 40. Type the counts, not the rates: the change in households divided by the 2020 count, times 100.

</details>

---

### 21. psda-rug-prices-chain-difference

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

At a store, the price of rug A is 30% greater than the price of rug B, and the price of rug B is 20% less than the price of rug C. Rug A costs 2.40 dollars more than rug C. What is the price, in dollars, of rug C?

- **A.** $24.00$
- **B.** $40.00$
- **C.** $60.00$
- **D.** $62.40$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let c be the price, in dollars, of rug C. Then rug B costs 0.8c and rug A costs 1.3(0.8c) = 1.04c, so rug A costs 4% more than rug C. It's given that 1.04c − c = 2.40, so 0.04c = 2.40 and c = 60. Therefore, rug C costs 60.00 dollars. Distractors: 24.00 treats rug A as 10% more than rug C (30% − 20%); 40.00 multiplies the percents (0.30 · 0.20 = 0.06) instead of the growth factors; 62.40 is the price of rug A.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=1.3\cdot0.8x-x</code><br><code>y=2.4</code>

x is the price of rug C. Zoom out until the line meets y = 2.4 near x = 60, click the intersection and read x = 60.

</details>

---

### 22. psda-store-hardcover-fiction-share

*Hard · Multiple choice · route: hand-primary · techniques: T9*

Of the books in a store, 40% are fiction and the rest are nonfiction. Of the fiction books, 30% are hardcover, and of the nonfiction books, 60% are hardcover. If $p\%$ of the hardcover books in the store are fiction, what is the value of $p$?

- **A.** $12$
- **B.** $25$
- **C.** $30$
- **D.** $48$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Suppose the store has 100 books. Then 40 are fiction, and 30% of 40 = 12 are fiction hardcovers; 60 are nonfiction, and 60% of 60 = 36 are nonfiction hardcovers. There are 12 + 36 = 48 hardcover books, and 12/48 = 0.25 of them are fiction. Therefore, p = 25. Distractors: 12 is the fiction hardcovers as a percent of all books; 30 is the percent of fiction books that are hardcover, the reverse of what is asked; 48 is the percent of all books that are hardcover.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{0.4\cdot0.3}{0.4\cdot0.3+0.6\cdot0.6}\cdot100</code>

The line shows 25. Setting up the fraction is the real work; Desmos only does the arithmetic, so the hand route is about as fast.

</details>

---

### 23. psda-tax-tip-original-cost

*Hard · Multiple choice · route: desmos-primary · techniques: T9*

The cost of a meal before tax is $m$ dollars. A sales tax of 8% of the cost is added, and then a tip of 20% of the after-tax amount is added. If the total paid is 64.80 dollars, what is the value of $m$?

- **A.** $50.00$
- **B.** $50.63$
- **C.** $54.00$
- **D.** $60.00$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A tax of 8% multiplies the cost by the growth factor 1.08, giving 1.08m. A tip of 20% of that amount multiplies by 1.20, giving 1.20 · 1.08m = 1.296m. It's given that this total is 64.80, so m = 64.80/1.296 = 50.00. Distractors: 50.63 adds the percents and divides by 1.28, as if the tip were 20% of the pre-tax cost; 54.00 removes only the tip (64.80/1.20); 60.00 removes only the tax (64.80/1.08).

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{64.80}{1.08\cdot1.20}</code>

The line shows 50. Each percent increase is a growth factor, so the total is m times 1.08 times 1.20; divide the total by both factors.

</details>

---
