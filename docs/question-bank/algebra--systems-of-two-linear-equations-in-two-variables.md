# Systems of two linear equations in two variables

[← Question bank index](README.md) · Algebra · 80 questions, easiest first

### 1. alg-elimination-sum-x

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

The solution to the system of equations $3x + y = 14$ and $x - y = 2$ is $(x, y)$. What is the value of $x$?

- **A.** $2$
- **B.** $4$
- **C.** $6$
- **D.** $8$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Adding the two equations eliminates y: 4x = 16, so x = 4. Substituting back, y = x - 2 = 2. Distractors: 2 is the value of y, not x; 6 is x + y; 8 is the product xy.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x+y=14</code><br><code>x-y=2</code>

Click the intersection: (4, 2). The x-coordinate is 4.

</details>

---

### 2. alg-sys-count-equal-slopes-zero

*Easy · Multiple choice · route: hand-primary · techniques: T2*

How many solutions $(x, y)$ does the system consisting of $y = 4x - 1$ and $y = 4x + 6$ have?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Both equations are in slope-intercept form. Each line has slope 4, but the y-intercepts are -1 and 6. Two distinct lines with the same slope are parallel and never meet, so the system has zero solutions. Distractors: 'Exactly one' is the count for lines with different slopes, but these slopes are equal; 'Exactly two' is never possible for two lines; 'Infinitely many' would require the same slope and the same intercept, but the intercepts differ.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=4x-1</code><br><code>y=4x+6</code>

Two parallel lines appear and never meet, even after zooming out, so there is no intersection point. Reading the slopes by hand is faster; use the graph only as a check.

</details>

---

### 3. alg-sys-drones-altitude-interpret-y

*Easy · Multiple choice · route: either · techniques: T2*

The equations $y = 20 + 3x$ and $y = 140 - 5x$ model the altitudes $y$, in meters, of drones A and B, respectively, $x$ seconds after a test begins. Their graphs in the $xy$-plane intersect at $(15, 65)$. Which statement is the best interpretation of 65 in this context?

- **A.** The drones are at the same altitude 65 seconds after the test begins.
- **B.** Both drones are at an altitude of 65 meters 15 seconds after the test begins.
- **C.** Drone B descends 65 meters during the first 15 seconds of the test.
- **D.** Drone A is 65 meters higher than drone B 15 seconds after the test begins.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The intersection point is a solution to both equations, so at $x = 15$ seconds both models give $y = 65$: $20 + 3(15) = 65$ and $140 - 5(15) = 65$. Since $y$ is altitude in meters, 65 is the altitude, in meters, that both drones share 15 seconds after the test begins. Distractors: 'same altitude 65 seconds after' reads 65 as the time, which is the other coordinate; 'descends 65 meters' treats the altitude as a change, but drone B descends $140 - 65 = 75$ meters; '65 meters higher' reads $y$ as a difference, but at the intersection the altitudes are equal.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=20+3x</code><br><code>y=140-5x</code>

Click the intersection: (15, 65). The x-coordinate is the time, in seconds, and the y-coordinate is the shared altitude, in meters.

</details>

---

### 4. alg-sys-elim-subtract-y

*Easy · Multiple choice · route: either · techniques: T2*

The ordered pair $(x, y)$ satisfies both $4x + 3y = 25$ and $4x - y = 1$. What is the value of $y$?

- **A.** $\frac{7}{4}$
- **B.** $6$
- **C.** $8$
- **D.** $12$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Both equations have the term 4x, so subtracting the second equation from the first eliminates x: (4x + 3y) - (4x - y) = 25 - 1, which yields 4y = 24, so y = 6. Therefore, the value of y is 6. Distractors: 7/4 is the value of x, the wrong variable; 8 divides 24 by 3, the y-coefficient in the first equation, instead of by 4; 12 treats 3y - (-y) as 2y, a sign slip that gives 2y = 24.

**Desmos** (not yet verified in Desmos). Type:<br><code>4x+3y=25</code><br><code>4x-y=1</code>

Click the intersection: (1.75, 6). The question asks for y, so the answer is 6. Subtracting the equations by hand is just as quick.

</details>

---

### 5. alg-sys-florist-bouquets-roses-spr

*Easy · Student-produced response · route: either · techniques: T2*

A florist puts 3 roses in each small bouquet and 7 in each large bouquet. The equation $3s + 7l = 156$ represents one day's roses, where $s$ and $l$ are the numbers of small and large bouquets. There were twice as many small bouquets as large ones. How many large bouquets were made?

**Answer:** 12

<details><summary>Solutions</summary>

**By hand.** It's given that $s = 2l$. Substituting into $3s + 7l = 156$ yields $6l + 7l = 156$, or $13l = 156$, so $l = 12$. Therefore, the florist made 12 large bouquets (and 24 small ones).

**Desmos** (not yet verified in Desmos). Type:<br><code>3x+7y=156</code><br><code>x=2y</code>

Use x for s and y for l. Click the intersection: (24, 12). The question asks for large bouquets, the y-coordinate, 12.

</details>

---

### 6. alg-sys-horizontal-line-intersection-x

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $y = 5$ and $y = 2x - 3$ intersect at the point $(x, y)$. What is the value of $x$?

- **A.** $1$
- **B.** $4$
- **C.** $5$
- **D.** $7$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** At the intersection point, both equations hold, so $2x - 3 = 5$. Adding 3 to both sides yields $2x = 8$, so $x = 4$. Therefore, the value of $x$ is 4. Distractors: 1 comes from subtracting 3 instead of adding it ($2x = 2$); 5 is the $y$-coordinate of the intersection point; 7 comes from substituting 5 for $x$ instead of for $y$.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5</code><br><code>y=2x-3</code>

Click the intersection: (4, 5). The question asks for the x-coordinate, 4.

</details>

---

### 7. alg-sys-intersection-standard-and-slope-form-x

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $2x + 5y = 1$ and $y = x - 4$ intersect at the point $(x, y)$. What is the value of $x$?

- **A.** $-\frac{19}{7}$
- **B.** $-1$
- **C.** $\frac{5}{7}$
- **D.** $3$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Substituting x - 4 for y in 2x + 5y = 1 yields 2x + 5(x - 4) = 1, or 7x - 20 = 1. Adding 20 to both sides yields 7x = 21, so x = 3. Therefore, the value of x is 3. Distractors: -19/7 results from substituting x + 4 instead of x - 4 (7x + 20 = 1); -1 is the y-coordinate of the intersection; 5/7 results from not distributing the 5, writing 2x + 5x - 4 = 1.

**Desmos** (not yet verified in Desmos). Type:<br><code>2x+5y=1</code><br><code>y=x-4</code>

Click the intersection: (3, -1). The question asks for the x-coordinate, 3.

</details>

---

### 8. alg-sys-pottery-studio-equal-cost-hours

*Easy · Multiple choice · route: either · techniques: T2*

Pottery studio A charges a fee of 18 dollars plus 6 dollars per hour of wheel time. Pottery studio B charges a fee of 30 dollars plus 4 dollars per hour of wheel time. For how many hours of wheel time do the two studios charge the same total amount?

- **A.** $1.2$
- **B.** $6$
- **C.** $12$
- **D.** $54$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Let h be the number of hours. Studio A charges 18 + 6h dollars and studio B charges 30 + 4h dollars. Setting the charges equal yields 18 + 6h = 30 + 4h, so 2h = 12 and h = 6. Therefore, the studios charge the same total for 6 hours. Distractors: 1.2 divides the difference in fees, 12, by the sum of the hourly rates, 10, instead of their difference; 12 is the difference in fees before dividing by 2; 54 is the equal total charge in dollars, not the number of hours.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=18+6x</code><br><code>y=30+4x</code>

Click the intersection: (6, 54). The question asks for the hours, the x-coordinate 6, not the cost 54.

</details>

---

### 9. alg-sys-soap-sales-interpret-constant

*Easy · Multiple choice · route: hand-primary · techniques: —*

A shop sells small bars of soap for 4 dollars each and large bars for 7 dollars each. The system $x + y = 50$ and $4x + 7y = 275$ represents one day of sales, where $x$ and $y$ are the numbers of small and large bars sold. Which of the following is the best interpretation of 275 in this context?

- **A.** The total revenue, in dollars, from all bars sold that day is 275.
- **B.** The total number of bars sold that day is 275.
- **C.** The revenue, in dollars, from large bars sold that day is 275.
- **D.** The number of large bars sold that day is 275.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that each small bar sells for 4 dollars and each large bar for 7 dollars, so 4x is the revenue from small bars and 7y is the revenue from large bars. Their sum, 4x + 7y, is the total revenue in dollars, and the equation sets it equal to 275. Therefore, 275 is the total revenue, in dollars, from all bars sold that day. Distractors: 'The total number of bars sold that day is 275' confuses the two equations, since x + y = 50 gives the number of bars; 'The revenue from large bars sold that day is 275' describes only the term 7y, not the whole sum; 'The number of large bars sold that day is 275' confuses the revenue with the count y. This is an interpretation item, so there is nothing to type into Desmos.

</details>

---

### 10. alg-sys-solution-given-find-coefficient-a

*Easy · Multiple choice · route: hand-primary · techniques: —*

The ordered pair $(2, -3)$ is a solution to the system of equations $ax + 3y = 5$ and $x - y = 5$, where $a$ is a constant. What is the value of $a$?

- **A.** $-2$
- **B.** $\frac{1}{3}$
- **C.** $7$
- **D.** $14$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that $(2, -3)$ satisfies $ax + 3y = 5$. Substituting $x = 2$ and $y = -3$ yields $2a - 9 = 5$, so $2a = 14$ and $a = 7$. Therefore, the value of $a$ is 7. Distractors: $-2$ comes from dropping the negative sign of $y$, which gives $2a + 9 = 5$; 1/3 comes from swapping the coordinates, which gives $-3a + 6 = 5$; 14 is $2a$, the value before dividing by 2.

</details>

---

### 11. alg-sys-substitute-linear-y-x-spr

*Easy · Student-produced response · route: desmos-primary · techniques: T2*

If $y = 4x - 9$ and $3x + 2y = 37$, what is the value of $x$?

**Answer:** 5

<details><summary>Solutions</summary>

**By hand.** Substituting 4x - 9 for y in 3x + 2y = 37 yields 3x + 2(4x - 9) = 37, or 3x + 8x - 18 = 37. Combining like terms yields 11x - 18 = 37, so 11x = 55 and x = 5. Therefore, the value of x is 5 (and y = 4(5) - 9 = 11).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=4x-9</code><br><code>3x+2y=37</code>

Click the intersection: (5, 11). Enter the x-coordinate, 5, not the y-coordinate.

</details>

---

### 12. alg-sys-sum-in-words-and-equation-x

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

The sum of $x$ and $y$ is 12, and $3x - y = 4$. What is the value of $x$?

- **A.** $4$
- **B.** $8$
- **C.** $12$
- **D.** $16$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The first condition is $x + y = 12$. Adding it to $3x - y = 4$ yields $4x = 16$, so $x = 4$. Therefore, the value of $x$ is 4. Distractors: 8 is the value of $y$; 12 is the given sum; 16 is $4x$, the value before dividing by 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y=12</code><br><code>3x-y=4</code>

Write the sentence as x + y = 12 and type both equations. Click the intersection: (4, 8). The question asks for x, 4.

</details>

---

### 13. alg-sys-which-ordered-pair-satisfies-both

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

Which ordered pair $(x, y)$ is a solution to the system of equations $2x + y = 7$ and $x - 3y = 7$?

- **A.** $(-1, 4)$
- **B.** $(1, -2)$
- **C.** $(3, 1)$
- **D.** $(4, -1)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A solution must satisfy both equations. For $(4, -1)$: $2(4) + (-1) = 7$ and $4 - 3(-1) = 7$, so both are true. Alternate approach: substituting $x = 7 + 3y$ into $2x + y = 7$ yields $14 + 7y = 7$, so $y = -1$ and $x = 4$. Therefore, the solution is $(4, -1)$. Distractors: $(-1, 4)$ swaps the coordinates of the solution; $(1, -2)$ satisfies only $x - 3y = 7$; $(3, 1)$ satisfies only $2x + y = 7$.

**Desmos** (not yet verified in Desmos). Type:<br><code>2x+y=7</code><br><code>x-3y=7</code>

Click the intersection: (4, -1). It matches choice D.

</details>

---

### 14. alg-system-substitution-y

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

The solution to the system of equations $y = 2x - 3$ and $x + y = 9$ is $(x, y)$. What is the value of $y$?

- **A.** $1$
- **B.** $2$
- **C.** $4$
- **D.** $5$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Substituting 2x - 3 for y in x + y = 9 yields x + 2x - 3 = 9, so 3x = 12 and x = 4. Then y = 2(4) - 3 = 5. Distractors: 4 is the value of x, not y; 2 results from a sign slip, x + 2x + 3 = 9, which gives x = 2; 1 is the y-value that slip produces, 2(2) - 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x-3</code><br><code>x+y=9</code>

Click the intersection: (4, 5). The question asks for y, so the answer is 5.

</details>

---

### 15. alg-system-sum-of-coordinates

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

The ordered pair $(x, y)$ is the solution to the system of equations $y = 2x + 1$ and $y = -3x + 16$. What is the value of $x + y$?

- **A.** $3$
- **B.** $7$
- **C.** $10$
- **D.** $21$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Since both equations give y, 2x + 1 = -3x + 16. Adding 3x to both sides and subtracting 1 from both sides yields 5x = 15, so x = 3. Substituting 3 for x in y = 2x + 1 yields y = 7. Therefore, x + y = 3 + 7 = 10. Distractors: 3 is x alone and 7 is y alone; 21 is the product xy rather than the sum.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x+1</code><br><code>y=-3x+16</code>

Click the intersection: (3, 7). The question asks for x + y, so add the coordinates: 3 + 7 = 10.

</details>

---

### 16. alg-decimal-system-difference

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

The system $0.3x + 0.5y = 5.1$ and $2x - 3y = -4$ has solution $(x, y)$. What is the value of $x - y$?

- **A.** $-1$
- **B.** $1$
- **C.** $7$
- **D.** $13$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Multiply the first equation by 10: 3x + 5y = 51. Double it: 6x + 10y = 102. Triple the second: 6x - 9y = -12. Subtract: 19y = 114, so y = 6 and x = 7. x - y = 1. Distractors: -1 is y - x, 7 is x alone, 13 is x + y.

**Desmos** (not yet verified in Desmos). Type:<br><code>0.3x+0.5y=5.1</code><br><code>2x-3y=-4</code>

Click the intersection: (7, 6). Then x - y = 1.

</details>

---

### 17. alg-fraction-coefficient-system-x-spr

*Medium · Student-produced response · route: desmos-primary · techniques: T2*

If $\frac{x}{2} + \frac{y}{3} = 5$ and $x - y = 3$, what is the value of $x$?

**Answer:** 36/5 (≈ 7.2)

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the first equation by 6 yields 3x + 2y = 30. From the second equation, y = x - 3. Substituting x - 3 for y yields 3x + 2(x - 3) = 30, which simplifies to 5x - 6 = 30. Adding 6 to both sides yields 5x = 36, so x = 36/5.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{x}{2}+\frac{y}{3}=5</code><br><code>x-y=3</code>

Click the intersection: (7.2, 4.2). The x-coordinate is 7.2; enter 7.2 or 36/5.

</details>

---

### 18. alg-fraction-slope-system-y

*Medium · Student-produced response · route: desmos-primary · techniques: T2*

The solution to the system of equations $y = \frac{1}{2}x - 4$ and $y = -\frac{3}{4}x + 1$ is $(x, y)$. What is the value of $y$?

**Answer:** -2

<details><summary>Solutions</summary>

**By hand.** Setting the two expressions for y equal yields 1/2 x - 4 = -3/4 x + 1. Adding 3/4 x to both sides yields 5/4 x - 4 = 1, so 5/4 x = 5 and x = 4. Substituting 4 for x in y = 1/2 x - 4 yields y = 2 - 4 = -2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{1}{2}x-4</code><br><code>y=-\frac{3}{4}x+1</code>

Click the intersection: (4, -2). The y-coordinate is -2; enter -2.

</details>

---

### 19. alg-hardware-bolts-containers

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

A hardware store sells bolts in boxes of 25 bolts and in bags of 8 bolts. A customer buys 14 of these containers, which hold 248 bolts in all. How many boxes of bolts does the customer buy?

- **A.** $6$
- **B.** $7$
- **C.** $8$
- **D.** $31$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let b be the number of boxes and g the number of bags. The customer buys 14 containers, so b + g = 14, and the containers hold 248 bolts, so 25b + 8g = 248. From the first equation, g = 14 - b. Substituting into the second equation yields 25b + 8(14 - b) = 248, which simplifies to 17b + 112 = 248, so 17b = 136 and b = 8. Distractors: 6 is the number of bags, not boxes; 7 assumes equal numbers of boxes and bags, but 25(7) + 8(7) = 231, not 248; 31 is 248 divided by 8, the count if every container were a bag.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y=14</code><br><code>25x+8y=248</code>

With x boxes and y bags, click the intersection: (8, 6). The number of boxes is x = 8.

</details>

---

### 20. alg-intersection-point-constants-sum

*Medium · Multiple choice · route: hand-primary · techniques: T4*

In the $xy$-plane, the graphs of $y = 3x + a$ and $y = -2x + b$, where $a$ and $b$ are constants, intersect at the point $(4, 9)$. What is the value of $a + b$?

- **A.** $-2$
- **B.** $4$
- **C.** $14$
- **D.** $20$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Since (4, 9) lies on both graphs, substituting 4 for x and 9 for y in each equation yields 9 = 12 + a, so a = -3, and 9 = -8 + b, so b = 17. Therefore, a + b = -3 + 17 = 14. Distractors: 20 comes from the sign error a = 12 - 9 = 3; -2 comes from the sign error b = 9 - 8 = 1; 4 comes from making both sign errors.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x+a</code><br><code>y=-2x+b</code><br><code>(4,9)</code>

Add sliders for a and b and drag each line until it passes through (4, 9): a = -3 and b = 17, so a + b = 14. Substituting the point by hand is faster.

</details>

---

### 21. alg-sys-add-equations-for-sum

*Medium · Multiple choice · route: hand-primary · techniques: T2*

If $5x + 2y = 31$ and $3x + 6y = 25$, what is the value of $x + y$?

- **A.** $\frac{4}{3}$
- **B.** $\frac{17}{3}$
- **C.** $7$
- **D.** $56$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Adding the two equations yields (5x + 3x) + (2y + 6y) = 31 + 25, or 8x + 8y = 56. Dividing both sides by 8 yields x + y = 7. Therefore, the value of x + y is 7 (the solution itself is x = 17/3, y = 4/3, which is not needed). Distractors: 4/3 is the value of y alone; 17/3 is the value of x alone; 56 is 8x + 8y, the intermediate sum before dividing by 8.

**Desmos** (not yet verified in Desmos). Type:<br><code>5x+2y=31</code><br><code>3x+6y=25</code>

Click the intersection: about (5.667, 1.333). Adding the coordinates gives 7. Adding the equations by hand is faster; Desmos is a check, and it shows decimals for both coordinates.

</details>

---

### 22. alg-sys-bike-shop-repairs-model

*Medium · Multiple choice · route: hand-primary · techniques: —*

At a bike shop, each tire repair takes 15 minutes and each brake repair takes 40 minutes. One day, the shop completed 22 of these repairs in a total of 8 hours. Which system of equations can be solved for $t$ and $b$, where $t$ is the number of tire repairs and $b$ is the number of brake repairs?

- **A.** $t + b = 8$ and $15t + 40b = 22$
- **B.** $t + b = 22$ and $15t + 40b = 8$
- **C.** $t + b = 22$ and $40t + 15b = 480$
- **D.** $t + b = 22$ and $15t + 40b = 480$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The shop completed 22 repairs, so $t + b = 22$. Tire repairs take $15t$ minutes and brake repairs take $40b$ minutes, and 8 hours is $8 \times 60 = 480$ minutes, so $15t + 40b = 480$. Therefore, the system is $t + b = 22$ and $15t + 40b = 480$ (its solution is 16 tire repairs and 6 brake repairs). Distractors: $t + b = 8$ and $15t + 40b = 22$ swaps the number of repairs and the time; $t + b = 22$ and $15t + 40b = 8$ mixes minutes and hours without converting; $t + b = 22$ and $40t + 15b = 480$ attaches each repair time to the wrong kind of repair.

</details>

---

### 23. alg-sys-bowling-equal-cost-fee-spr

*Medium · Student-produced response · route: either · techniques: T2, T4*

Bowling alley A charges a shoe-rental fee plus 6.00 dollars per game. Bowling alley B charges a shoe-rental fee of 4.50 dollars plus 7.50 dollars per game. For 5 games, the total costs at the two alleys are equal. What is the shoe-rental fee, in dollars, at alley A?

**Answer:** 12

<details><summary>Solutions</summary>

**By hand.** For 5 games, alley B charges $4.50 + 7.50(5) = 42.00$ dollars. If alley A's fee is $f$ dollars, it charges $f + 6.00(5) = f + 30$ dollars. Setting the costs equal yields $f + 30 = 42$, so $f = 12$. Therefore, alley A's shoe-rental fee is 12.00 dollars.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=f+6x</code><br><code>y=4.5+7.5x</code><br><code>x=5</code>

Add a slider for f and drag it until the first two lines meet on x = 5; that happens at f = 12, where the intersection is (5, 42). Computing B's cost for 5 games by hand is just as fast.

</details>

---

### 24. alg-sys-coffee-blend-pricier-beans

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

A roaster mixes beans that cost 12 dollars per kilogram with beans that cost 20 dollars per kilogram to make 40 kilograms of a blend worth 15 dollars per kilogram. How many kilograms of the 20-dollar beans are in the blend?

- **A.** $15$
- **B.** $20$
- **C.** $25$
- **D.** $30$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Let x and y be the kilograms of 12-dollar and 20-dollar beans. The total mass gives x + y = 40, and the total value gives 12x + 20y = 15(40) = 600. Multiplying the first equation by 12 yields 12x + 12y = 480; subtracting it from the second yields 8y = 120, so y = 15. Therefore, the blend has 15 kilograms of the 20-dollar beans. Distractors: 20 assumes equal amounts of each bean, which would give a price of 16 dollars per kilogram; 25 is x, the kilograms of 12-dollar beans; 30 solves 20y = 600 and ignores the 12-dollar beans.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y=40</code><br><code>12x+20y=15\cdot40</code>

Let x be the kilograms of 12-dollar beans and y the kilograms of 20-dollar beans. Click the intersection: (25, 15). The question asks for y, 15.

</details>

---

### 25. alg-sys-combine-for-five-x-plus-seven-y

*Medium · Multiple choice · route: hand-primary · techniques: T2*

If $4x + 5y = 23$ and $x + 2y = 8$, what is the value of $5x + 7y$?

- **A.** $3$
- **B.** $5$
- **C.** $15$
- **D.** $31$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The coefficients of $5x + 7y$ are the sums of the coefficients in the two equations: $4 + 1 = 5$ and $5 + 2 = 7$. Adding the equations yields $(4x + 5y) + (x + 2y) = 23 + 8$, or $5x + 7y = 31$. Alternate approach: substituting $x = 8 - 2y$ into the first equation yields $32 - 3y = 23$, so $y = 3$ and $x = 2$; then $5(2) + 7(3) = 31$. Therefore, the value of $5x + 7y$ is 31. Distractors: 3 is the value of $y$, an intermediate result; 5 is the value of $x + y$; 15 comes from subtracting the equations, which gives $3x + 3y = 15$, instead of adding them.

**Desmos** (not yet verified in Desmos). Type:<br><code>4x+5y=23</code><br><code>x+2y=8</code>

Click the intersection: (2, 3). Then 5(2) + 7(3) = 31. Adding the two equations by hand gives 5x + 7y in one step, so Desmos is slower and serves as a check.

</details>

---

### 26. alg-sys-decimal-coefficients-y-spr

*Medium · Student-produced response · route: desmos-primary · techniques: T2*

For the solution $(x, y)$ to the system of equations $0.4x + 1.5y = 7.3$ and $1.2x - 0.5y = 2.9$, what is the value of $y$?

**Answer:** 19/5 (≈ 3.8)

<details><summary>Solutions</summary>

**By hand.** Multiplying the first equation by 3 yields 1.2x + 4.5y = 21.9. Subtracting the second equation from this one eliminates x: 4.5y - (-0.5y) = 21.9 - 2.9, or 5y = 19, so y = 3.8. Therefore, the value of y is 3.8 (and x = 4).

**Desmos** (not yet verified in Desmos). Type:<br><code>0.4x+1.5y=7.3</code><br><code>1.2x-0.5y=2.9</code>

Click the intersection: (4, 3.8). Enter the y-coordinate, 3.8 (or 19/5).

</details>

---

### 27. alg-sys-difference-gives-2x-minus-y-spr

*Medium · Student-produced response · route: either · techniques: T2*

The system of equations $3x + y = 17$ and $x + 2y = 9$ has the solution $(x, y)$. What is the value of $2x - y$?

**Answer:** 8

<details><summary>Solutions</summary>

**By hand.** Subtracting the second equation from the first yields (3x - x) + (y - 2y) = 17 - 9, or 2x - y = 8. Therefore, the value of 2x - y is 8. Alternate approach: solving the system gives x = 5 and y = 2, and 2(5) - 2 = 8.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x+y=17</code><br><code>x+2y=9</code>

Click the intersection: (5, 2). Then 2x - y = 2(5) - 2 = 8. You can also type 2(5)-2 on a new line.

</details>

---

### 28. alg-sys-fraction-coefficients-x-minus-y

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

If $\frac{1}{3}x - \frac{1}{2}y = 1$ and $\frac{3}{4}x + \frac{1}{4}y = 5$, what is the value of $x - y$?

- **A.** $2$
- **B.** $4$
- **C.** $6$
- **D.** $8$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Multiplying the first equation by 6 yields 2x - 3y = 6, and multiplying the second by 4 yields 3x + y = 20. Multiplying 3x + y = 20 by 3 yields 9x + 3y = 60; adding this to 2x - 3y = 6 yields 11x = 66, so x = 6. Then y = 20 - 3(6) = 2. Therefore, x - y = 6 - 2 = 4. Distractors: 2 is the value of y alone; 6 is the value of x alone; 8 is x + y instead of x - y.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{1}{3}x-\frac{1}{2}y=1</code><br><code>\frac{3}{4}x+\frac{1}{4}y=5</code>

Click the intersection: (6, 2). Then x - y = 6 - 2 = 4.

</details>

---

### 29. alg-sys-fractions-both-sides-x-spr

*Medium · Student-produced response · route: desmos-primary · techniques: T2*

If $\frac{x - 1}{2} = \frac{y + 3}{4}$ and $\frac{x + 2y}{5} = \frac{x + 1}{4}$, what is the value of $x$?

**Answer:** 3

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the first equation by 4 yields $2(x - 1) = y + 3$, so $y = 2x - 5$. Multiplying both sides of the second equation by 20 yields $4(x + 2y) = 5(x + 1)$, or $4x + 8y = 5x + 5$, so $x = 8y - 5$. Substituting $y = 2x - 5$ yields $x = 16x - 45$, so $15x = 45$ and $x = 3$. Check: $y = 1$, and $\frac{3 - 1}{2} = \frac{1 + 3}{4} = 1$ and $\frac{3 + 2}{5} = \frac{3 + 1}{4} = 1$. Therefore, the value of $x$ is 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>(x-1)/2=(y+3)/4</code><br><code>(x+2y)/5=(x+1)/4</code>

Type each equation as written, with parentheses around every numerator. Click the intersection: (3, 1). The question asks for x, 3.

</details>

---

### 30. alg-sys-hiker-flat-uphill-distance

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

A hiker walks 5 kilometers per hour on flat ground and 3 kilometers per hour uphill. The equation $5f + 3u = 21$ models a 21-kilometer hike: $f$ hours on flat ground and $u$ hours uphill. The hiker spent 1 more hour on flat ground than uphill. How far, in kilometers, did the hiker walk uphill?

- **A.** $2$
- **B.** $3$
- **C.** $6$
- **D.** $15$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that $f = u + 1$. Substituting into $5f + 3u = 21$ yields $5(u + 1) + 3u = 21$, or $8u + 5 = 21$, so $u = 2$ hours. At 3 kilometers per hour, the uphill distance is $3(2) = 6$ kilometers. Therefore, the hiker walked 6 kilometers uphill. Distractors: 2 is the number of hours uphill, not the distance; 3 is the number of hours on flat ground; 15 is the distance on flat ground, $5(3)$.

**Desmos** (not yet verified in Desmos). Type:<br><code>5x+3y=21</code><br><code>x=y+1</code>

Use x for f and y for u. Click the intersection: (3, 2). That is 2 hours uphill, so the uphill distance is 3(2) = 6 kilometers.

</details>

---

### 31. alg-sys-ice-sculptures-equal-height

*Medium · Multiple choice · route: desmos-primary · techniques: T2, T9*

Ice sculpture A is 30 centimeters tall and melts so that its height decreases by 1.2 centimeters per hour. Ice sculpture B is 22 centimeters tall, and its height decreases by 0.8 centimeters per hour. When the sculptures are the same height, what is that height, in centimeters?

- **A.** $6$
- **B.** $8$
- **C.** $20$
- **D.** $25.2$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** After $t$ hours, sculpture A is $30 - 1.2t$ centimeters tall and sculpture B is $22 - 0.8t$ centimeters tall. Setting the heights equal yields $30 - 1.2t = 22 - 0.8t$, or $8 = 0.4t$, so $t = 20$. Substituting yields $30 - 1.2(20) = 6$. Therefore, the common height is 6 centimeters. Distractors: 8 is the starting difference in heights; 20 is the number of hours, not the height; 25.2 comes from adding the rates, $8 \div 2 = 4$ hours, as if the heights moved toward each other, and then evaluating $30 - 1.2(4)$.

**Desmos** (not yet verified in Desmos). Type:<br><code>a(x)=30-1.2x</code><br><code>b(x)=22-0.8x</code><br><code>a(20)</code>

Graph both height functions and click the intersection: (20, 6). The time is 20 hours, but the question asks for the height, 6. Typing a(20) confirms 6.

</details>

---

### 32. alg-sys-infinite-solutions-y-at-given-x

*Medium · Multiple choice · route: hand-primary · techniques: T2*

The system of equations $ax + 6y = 18$ and $2x + 3y = 9$, where $a$ is a constant, has infinitely many solutions. For one of the solutions $(x, y)$, $x = 3$. What is the value of $y$?

- **A.** $1$
- **B.** $2$
- **C.** $3$
- **D.** $4$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A system with infinitely many solutions has two equations with the same graph, so every solution satisfies $2x + 3y = 9$. Substituting $x = 3$ yields $6 + 3y = 9$, so $y = 1$. (The first equation is 2 times the second, so $a = 4$, but $a$ is not needed.) Therefore, the value of $y$ is 1. Distractors: 2 comes from assuming $a = 2$ and solving $2(3) + 6y = 18$; 3 is the given value of $x$; 4 is the value of $a$, not $y$.

**Desmos** (not yet verified in Desmos). Type:<br><code>2x+3y=9</code><br><code>x=3</code>

Every solution lies on the line 2x + 3y = 9, so graph it with x = 3 and click the intersection: (3, 1). Substituting by hand is faster; use the graph as a check.

</details>

---

### 33. alg-sys-line-through-intercepts-coordinate-sum

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the line with equation $3x + 4y = 20$ intersects the line through the points $(0, -2)$ and $(4, 0)$ at the point $(x, y)$. What is the value of $x + y$?

- **A.** $\frac{4}{5}$
- **B.** $\frac{24}{5}$
- **C.** $\frac{28}{5}$
- **D.** $\frac{32}{5}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The line through (0, -2) and (4, 0) has slope (0 - (-2))/(4 - 0) = 1/2 and y-intercept -2, so its equation is y = (1/2)x - 2. Substituting into 3x + 4y = 20 yields 3x + 2x - 8 = 20, so 5x = 28 and x = 28/5. Then y = (1/2)(28/5) - 2 = 4/5, and x + y = 32/5. Therefore, the value of x + y is 32/5. Distractors: 4/5 is y alone; 24/5 is x - y instead of x + y; 28/5 is x alone.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x+4y=20</code><br><code>y=\frac{1}{2}x-2</code>

The second line has slope (0 - (-2))/(4 - 0) = 1/2 and y-intercept -2. Click the intersection: (5.6, 0.8). Then x + y = 6.4, which is 32/5.

</details>

---

### 34. alg-sys-lines-described-standard-form

*Medium · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, line $p$ is the line with a slope of 3 and a $y$-intercept of $(0, -2)$, and line $q$ is the line through the points $(0, 4)$ and $(8, 0)$. Which system of equations has lines $p$ and $q$ as its graphs?

- **A.** $3x - y = -2$ and $x + 2y = 8$
- **B.** $3x - y = 2$ and $x + 2y = 8$
- **C.** $3x - y = 2$ and $2x + y = 4$
- **D.** $x - 3y = 2$ and $x + 2y = 8$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Line $p$ has slope 3 and $y$-intercept $(0, -2)$, so $y = 3x - 2$, which is equivalent to $3x - y = 2$. Line $q$ has slope $\frac{0 - 4}{8 - 0} = -\frac{1}{2}$ and $y$-intercept $(0, 4)$, so $y = -\frac{1}{2}x + 4$; multiplying by 2 and rearranging yields $x + 2y = 8$. Therefore, the system is $3x - y = 2$ and $x + 2y = 8$. Distractors: $3x - y = -2$ and $x + 2y = 8$ has the sign of line $p$'s intercept flipped (it is $y = 3x + 2$); $3x - y = 2$ and $2x + y = 4$ uses run over rise for line $q$'s slope, $-2$ instead of $-\frac{1}{2}$; $x - 3y = 2$ and $x + 2y = 8$ swaps the coefficients of line $p$, giving slope $\frac{1}{3}$.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x-2</code><br><code>y=-x/2+4</code><br><code>3x-y=2</code><br><code>x+2y=8</code>

Graph the two lines from the description first, then type the pair of equations from each choice and toggle them on and off. Only choice B lies exactly on top of both lines; zoom out to confirm.

</details>

---

### 35. alg-sys-no-solution-fraction-slope-a

*Medium · Multiple choice · route: hand-primary · techniques: T3*

The system of equations $y = -\frac{2}{5}x + 3$ and $ax + 5y = 10$, where $a$ is a constant, has no solution. What is the value of $a$?

- **A.** $-2$
- **B.** $-\frac{2}{5}$
- **C.** $\frac{2}{5}$
- **D.** $2$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A system of two linear equations has no solution when the lines are parallel and distinct. Solving ax + 5y = 10 for y yields y = -(a/5)x + 2, a line with slope -a/5 and y-intercept 2. The first line has slope -2/5 and y-intercept 3. Setting -a/5 = -2/5 yields a = 2, and the intercepts 2 and 3 differ, so the lines are parallel and distinct. Therefore, the value of a is 2. Distractors: -2 comes from a sign slip when solving for y, writing the slope as a/5; -2/5 is the slope of the first line, not the constant a; 2/5 sets a equal to the size of the slope and forgets that the slope is a divided by 5.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-\frac{2}{5}x+3</code><br><code>ax+5y=10</code>

Add a slider for a and drag it until the two lines are parallel; that happens at a = 2. Comparing slopes by hand is faster and exact, so use the slider only as a check.

</details>

---

### 36. alg-sys-nursery-shrubs-trees-model

*Medium · Multiple choice · route: hand-primary · techniques: —*

A plant nursery sold 87 shrubs and trees in one day. The number of shrubs sold was 12 more than twice the number of trees sold. If $s$ is the number of shrubs and $t$ is the number of trees sold, which system of equations models these facts?

- **A.** $s = 2t + 12$ and $s + t = 87$
- **B.** $t = 2s + 12$ and $s + t = 87$
- **C.** $s + 12 = 2t$ and $s + t = 87$
- **D.** $s = 2(t + 12)$ and $s + t = 87$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that 87 shrubs and trees were sold in all, so s + t = 87. Twice the number of trees is 2t, and 12 more than that is 2t + 12, which equals the number of shrubs, so s = 2t + 12. Therefore, the system is s = 2t + 12 and s + t = 87 (its solution is 62 shrubs and 25 trees). Distractors: t = 2s + 12 and s + t = 87 swaps the roles of shrubs and trees; s + 12 = 2t and s + t = 87 adds the 12 to the wrong side, making the shrubs 12 fewer than twice the trees; s = 2(t + 12) and s + t = 87 adds 12 before doubling, a grouping slip. Translating words into equations is faster by hand, so there is no Desmos route.

</details>

---

### 37. alg-sys-ratio-x-over-y-elimination

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

The solution to the system of equations $6x - 4y = 18$ and $3x + 5y = 30$ is $(x, y)$. What is the value of $\frac{x}{y}$?

- **A.** $\frac{3}{5}$
- **B.** $\frac{5}{3}$
- **C.** $2$
- **D.** $15$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Multiplying the second equation by 2 yields $6x + 10y = 60$. Subtracting the first equation yields $14y = 42$, so $y = 3$. Substituting into $3x + 5y = 30$ yields $3x = 15$, so $x = 5$. Therefore, $\frac{x}{y} = \frac{5}{3}$. Distractors: 3/5 is $\frac{y}{x}$, the ratio inverted; 2 is $x - y$; 15 is $xy$.

**Desmos** (not yet verified in Desmos). Type:<br><code>6x-4y=18</code><br><code>3x+5y=30</code>

Click the intersection: (5, 3). Divide the x-coordinate by the y-coordinate: 5/3.

</details>

---

### 38. alg-sys-two-clubs-members-table-weeks-spr

*Medium · Student-produced response · route: either · techniques: T2*

The membership of each of two clubs changes by the same number of members every week. At weeks 0, 3, and 6, club A had 54, 63, and 72 members, and club B had 102, 93, and 84 members. After how many weeks will the two clubs have the same number of members?

**Answer:** 8

<details><summary>Solutions</summary>

**By hand.** Club A gains (63 - 54)/3 = 3 members per week, so after w weeks it has 54 + 3w members. Club B changes by (93 - 102)/3 = -3 members per week, so it has 102 - 3w members. Setting 54 + 3w = 102 - 3w yields 6w = 48, so w = 8. Therefore, the clubs have the same number of members, 78, after 8 weeks.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=54+3x</code><br><code>y=102-3x</code>

First find each rule from the table: club A gains 3 members per week from 54, and club B loses 3 per week from 102. Click the intersection: (8, 78). Enter the number of weeks, 8, not the number of members.

</details>

---

### 39. alg-sys-two-tables-intersection-b

*Medium · Multiple choice · route: either · techniques: T2*

For the linear function $f$, a table gives $f(1) = 5$, $f(3) = 11$, and $f(6) = 20$. For the linear function $g$, a table gives $g(-1) = 24$, $g(2) = 18$, and $g(5) = 12$. In the $xy$-plane, the lines $y = f(x)$ and $y = g(x)$ cross at a single point. What is the $y$-coordinate of the crossing point?

- **A.** $4$
- **B.** $14$
- **C.** $22$
- **D.** $74$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The slope of f is (11 - 5)/(3 - 1) = 3, and f(1) = 5 gives f(x) = 3x + 2. The slope of g is (18 - 24)/(2 - (-1)) = -2, and g(2) = 18 gives g(x) = -2x + 22. Setting 3x + 2 = -2x + 22 yields 5x = 20, so the x-coordinate is 4 and the y-coordinate is f(4) = 3(4) + 2 = 14. Therefore, the y-coordinate of the point is 14. Distractors: 4 is the x-coordinate; 22 is the y-intercept of g, not the intersection; 74 comes from a sign slip that gives g a slope of 2, so g(x) = 2x + 26 and 3x + 2 = 2x + 26 yields x = 24 and y = 74.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x+2</code><br><code>y=-2x+22</code>

First find each rule from two table rows (slopes 3 and -2). Then click the intersection: (4, 14). The question asks for the y-coordinate, 14.

</details>

---

### 40. alg-sys-verbal-lines-point-slope-x

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, one line passes through the point $(1, 3)$ and has slope 2, and a second line has slope $-1$ and $y$-intercept $(0, 9)$. The two lines intersect at the point $(x, y)$. What is the value of $x$?

- **A.** $\frac{4}{3}$
- **B.** $2$
- **C.** $\frac{8}{3}$
- **D.** $\frac{19}{3}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The first line passes through (1, 3) with slope 2, so y - 3 = 2(x - 1), or y = 2x + 1. The second line is y = -x + 9. Setting 2x + 1 = -x + 9 yields 3x = 8, so x = 8/3. Therefore, the value of x is 8/3. Distractors: 4/3 results from a sign slip in point-slope form, y - 3 = 2(x + 1), which gives y = 2x + 5 and 3x = 4; 2 treats the point (1, 3) as if 3 were the y-intercept, giving y = 2x + 3 and 3x = 6; 19/3 is the y-coordinate of the intersection.

**Desmos** (not yet verified in Desmos). Type:<br><code>y-3=2(x-1)</code><br><code>y=-x+9</code>

Point-slope form can be typed directly. Click the intersection: about (2.667, 6.333). The x-coordinate is 2.667, which is 8/3; use the fraction toggle to confirm.

</details>

---

### 41. alg-sys-which-system-has-given-solution

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

Which system of equations has the solution $(-2, 3)$?

- **A.** $x + y = 1$ and $2x + 3y = 0$
- **B.** $x - y = -5$ and $2x + y = 1$
- **C.** $x - y = 1$ and $3x + 2y = 0$
- **D.** $x + y = 1$ and $3x + 2y = 0$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Substitute $x = -2$ and $y = 3$ into each equation of each system. In choice D, $-2 + 3 = 1$ and $3(-2) + 2(3) = 0$, so both equations are true. Therefore, the system $x + y = 1$ and $3x + 2y = 0$ has the solution $(-2, 3)$. Distractors: $x + y = 1$ and $2x + 3y = 0$ has the solution $(3, -2)$, the coordinates swapped; in $x - y = -5$ and $2x + y = 1$, only the first equation holds, since $2(-2) + 3 = -1$; in $x - y = 1$ and $3x + 2y = 0$, only the second equation holds, since $-2 - 3 = -5$.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y=1</code><br><code>3x+2y=0</code><br><code>(-2,3)</code>

Plot the point (-2, 3), then type the two equations of each choice in turn. Only in choice D do both lines pass through the point; their intersection is exactly (-2, 3).

</details>

---

### 42. alg-sys-x-described-in-words-sum

*Medium · Multiple choice · route: hand-primary · techniques: T2*

The value of $x$ is 4 less than 3 times the value of $y$, and $2x + 5y = 47$. What is the value of $x + y$?

- **A.** $5$
- **B.** $11$
- **C.** $16$
- **D.** $55$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The sentence gives $x = 3y - 4$. Substituting into $2x + 5y = 47$ yields $2(3y - 4) + 5y = 47$, or $11y - 8 = 47$. Adding 8 to both sides yields $11y = 55$, so $y = 5$ and $x = 3(5) - 4 = 11$. Therefore, the value of $x + y$ is 16. Distractors: 5 is the value of $y$ alone; 11 is the value of $x$ alone; 55 is $11y$, an intermediate result.

**Desmos** (not yet verified in Desmos). Type:<br><code>x=3y-4</code><br><code>2x+5y=47</code>

Translate the sentence to x = 3y - 4 and type both equations. Click the intersection: (11, 5), and add the coordinates: 16. Substitution by hand is just as quick.

</details>

---

### 43. alg-system-count-solutions-coincident

*Medium · Multiple choice · route: either · techniques: T2*

How many solutions does the system of equations $4x - 6y = 10$ and $-6x + 9y = -15$ have?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the first equation by -3/2 yields -6x + 9y = -15, which is exactly the second equation. The two equations describe the same line, so every solution of one is a solution of the other, and the system has infinitely many solutions. Equivalently, the ratios 4/(-6), (-6)/9 and 10/(-15) all equal -2/3. Distractors: 'Zero' would require equal slopes with different intercepts, but the intercepts agree as well; 'Exactly one' would require different slopes, but both lines have slope 2/3; 'Exactly two' is never possible for two lines, which share zero, one, or infinitely many points.

**Desmos** (not yet verified in Desmos). Type:<br><code>4x-6y=10</code><br><code>-6x+9y=-15</code>

Only one line appears, because the two graphs lie exactly on top of each other. Toggle one equation off and on to confirm. Coincident lines mean infinitely many solutions.

</details>

---

### 44. alg-system-product-xy

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

If $x = 2y + 1$ and $3x + 4y = 33$, what is the value of $xy$?

- **A.** $3$
- **B.** $7$
- **C.** $10$
- **D.** $21$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Substituting 2y + 1 for x in 3x + 4y = 33 yields 6y + 3 + 4y = 33, so 10y = 30 and y = 3. Then x = 2(3) + 1 = 7, and xy = 21. Distractors: 7 is x alone; 3 is y alone; 10 is x + y.

**Desmos** (not yet verified in Desmos). Type:<br><code>x=2y+1</code><br><code>3x+4y=33</code>

Click the intersection: (7, 3). Then xy = 7(3) = 21.

</details>

---

### 45. alg-theater-child-tickets

*Medium · Student-produced response · route: desmos-primary · techniques: T2*

A theater sold adult tickets for 12.00 dollars each and child tickets for 7.00 dollars each. For one showing, 380 tickets were sold for a total of 3,785.00 dollars. How many child tickets were sold for that showing?

**Answer:** 155

<details><summary>Solutions</summary>

**By hand.** Let a be the number of adult tickets and c the number of child tickets. Then a + c = 380 and 12a + 7c = 3,785. From the first equation, a = 380 - c. Substituting yields 12(380 - c) + 7c = 3,785, so 4,560 - 5c = 3,785, which gives 5c = 775 and c = 155. Therefore, 155 child tickets were sold.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y=380</code><br><code>12x+7y=3785</code>

Let x be the number of adult tickets and y the number of child tickets. Click the intersection: (225, 155). The child count is the y-coordinate, 155.

</details>

---

### 46. alg-woodworking-shop-system

*Medium · Multiple choice · route: hand-primary · techniques: —*

A woodworking shop builds stools and benches. Each stool uses 4 legs and 1 seat, and each bench uses 6 legs and 2 seats. The shop uses 94 legs and 27 seats in all. Which system of equations represents this situation, where $s$ is the number of stools and $b$ is the number of benches built?

- **A.** $4s + 6b = 94$ and $s + 2b = 27$
- **B.** $4s + 2b = 94$ and $6s + b = 27$
- **C.** $4s + 6b = 27$ and $s + 2b = 94$
- **D.** $6s + 4b = 94$ and $2s + b = 27$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Each stool uses 4 legs and each bench uses 6 legs, so s stools and b benches use 4s + 6b legs, which must equal 94. Each stool uses 1 seat and each bench uses 2 seats, so they use s + 2b seats, which must equal 27. The system is 4s + 6b = 94 and s + 2b = 27 (its solution is 13 stools and 7 benches). Distractors: 4s + 2b = 94 and 6s + b = 27 pairs each item's legs with the other item's seats; 4s + 6b = 27 and s + 2b = 94 swaps the two totals; 6s + 4b = 94 and 2s + b = 27 swaps the parts used by stools and benches.

</details>

---

### 47. alg-artist-prints-total-spr

*Hard · Student-produced response · route: either · techniques: T2*

An artist sells small prints for 15 dollars each and large prints for 40 dollars each. At a fair, the artist sold 3 times as many small prints as large prints and collected 1,020 dollars from these sales. How many prints did the artist sell in all?

**Answer:** 48

<details><summary>Solutions</summary>

**By hand.** Let s be the number of small prints and g the number of large prints sold. It's given that s = 3g and that 15s + 40g = 1,020. Substituting 3g for s yields 15(3g) + 40g = 1,020, which simplifies to 85g = 1,020, so g = 12. Then s = 3(12) = 36, and the total number of prints sold is 36 + 12 = 48.

**Desmos** (not yet verified in Desmos). Type:<br><code>x=3y</code><br><code>15x+40y=1020</code>

With x small prints and y large prints, click the intersection: (36, 12). The question asks for the total, 36 + 12 = 48.

</details>

---

### 48. alg-farm-stand-baskets-difference

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

At a farm stand, each basket of peaches weighs 8 kilograms and each basket of plums weighs 5 kilograms. A delivery of 21 baskets weighs 138 kilograms in all. How many more baskets of peaches than baskets of plums are in the delivery?

- **A.** $1$
- **B.** $10$
- **C.** $11$
- **D.** $21$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Let p be the number of baskets of peaches and q the number of baskets of plums. Then p + q = 21 and 8p + 5q = 138. Multiplying the first equation by 5 yields 5p + 5q = 105, and subtracting this from the second equation yields 3p = 33, so p = 11 and q = 21 - 11 = 10. The question asks for p - q = 11 - 10 = 1. Distractors: 11 is the number of baskets of peaches and 10 is the number of baskets of plums, each a wrong quantity; 21 is the total number of baskets.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y=21</code><br><code>8x+5y=138</code>

Click the intersection: (11, 10), meaning 11 baskets of peaches and 10 baskets of plums. The question asks for the difference, 11 - 10 = 1.

</details>

---

### 49. alg-infinite-solutions-c

*Hard · Multiple choice · route: hand-primary · techniques: T3*

The system of equations $6x - 10y = c$ and $-9x + 15y = 12$, where $c$ is a constant, has infinitely many solutions. What is the value of $c$?

- **A.** $-18$
- **B.** $-8$
- **C.** $8$
- **D.** $18$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Two linear equations have infinitely many solutions when one is a multiple of the other. Multiplying -9x + 15y = 12 by -2/3 yields 6x - 10y = -8, so c = -8. Distractors: 8 drops the sign of the multiplier; -18 and 18 use the multiplier -3/2 or 3/2 instead of its reciprocal -2/3.

**Desmos** (not yet verified in Desmos). Type:<br><code>6x-10y=c</code><br><code>-9x+15y=12</code>

Add a slider for c with step 1 and drag until the two lines coincide: c = -8. The ratio method by hand is faster and exact.

</details>

---

### 50. alg-no-solution-k

*Hard · Multiple choice · route: either · techniques: T3, T4*

In the system of equations $5x - ky = 8$ and $15x + 12y = 2$, $k$ is a constant. If the system has no solution, what is the value of $k$?

- **A.** $-4$
- **B.** $-\frac{4}{5}$
- **C.** $4$
- **D.** $36$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** No solution means equal slopes and different intercepts. Slopes match when 5/15 = -k/12, so -k = 4 and k = -4. Check the intercepts: 5x + 4y = 8 has y-intercept 2 while 15x + 12y = 2 has y-intercept 1/6, so the lines are parallel, not the same line. Distractors: 4 is the sign slip (-k = 4 read as k = 4), -4/5 drops the 5 from the ratio, using 1/15 = -k/12; 36 inverts the ratio and drops the sign, using 15/5 = k/12.

**Desmos** (not yet verified in Desmos). Type:<br><code>5x-ky=8</code><br><code>15x+12y=2</code>

Add a slider for k and set its step to 1. Drag until the lines are parallel with no intersection: k = -4. Hybrid: match the ratio 5/15 = -k/12 by hand, then confirm on the graph.

</details>

---

### 51. alg-parallel-unless-coincident-b

*Hard · Multiple choice · route: either · techniques: T3*

The system of equations $y = 2x + b$ and $4x - 2y = 7$, where $b$ is a constant, has at least one solution. What is the value of $b$?

- **A.** $-\frac{7}{2}$
- **B.** $-\frac{7}{4}$
- **C.** $\frac{7}{4}$
- **D.** $\frac{7}{2}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Solving 4x - 2y = 7 for y yields y = 2x - 7/2. Both lines have slope 2, so they are parallel, and a system of two parallel lines has a solution only when the lines are the same line. That requires the y-intercepts to agree: b = -7/2. Alternate approach: substituting 2x + b for y in 4x - 2y = 7 yields 4x - 4x - 2b = 7, so -2b = 7 and b = -7/2; for any other value of b the equation reads 0 = (nonzero number) and the system has no solution. Distractors: -7/4 divides 7 by -4 instead of -2; 7/2 and 7/4 result from sign errors in solving -2b = 7 or 4b = 7.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x+b</code><br><code>4x-2y=7</code>

Add a slider for b. The two lines are parallel for every value of b, so they share a point only when they coincide; drag b until the graphs overlap, at b = -3.5. Substituting by hand confirms the exact value.

</details>

---

### 52. alg-proportional-system-a-plus-b

*Hard · Multiple choice · route: either · techniques: T3*

The system of equations $3x - 4y = 10$ and $ax + by = 5$, where $a$ and $b$ are constants, has infinitely many solutions. What is the value of $a + b$?

- **A.** $-2$
- **B.** $-\frac{1}{2}$
- **C.** $\frac{1}{2}$
- **D.** $\frac{7}{2}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The system has infinitely many solutions when the second equation is a constant multiple of the first. The constants give the multiple: 5 = (1/2)(10). Therefore a = (1/2)(3) = 3/2 and b = (1/2)(-4) = -2, and a + b = 3/2 + (-2) = -1/2. Distractors: -2 scales by 2 instead of by 1/2 (a = 6, b = -8, a + b = -2); 7/2 drops the sign of b (3/2 + 2); 1/2 is the scale factor itself, not the sum a + b.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x-4y=10</code><br><code>ax+by=5</code>

Add sliders for a and b and drag until the lines coincide: a = 1.5 and b = -2, so a + b = -0.5. Two sliders are hard to tune; use the ratio 5/10 = 1/2 by hand and confirm on the graph.

</details>

---

### 53. alg-sum-difference-trick

*Hard · Student-produced response · route: hand-primary · techniques: T2*

If $7j + 2k = 61$ and $4j + 5k = 37$, what is the value of $7(j - k)$?

**Answer:** 56

<details><summary>Solutions</summary>

**By hand.** Subtract the second equation from the first: (7j - 4j) + (2k - 5k) = 61 - 37, so 3j - 3k = 24 and j - k = 8. Then 7(j - k) = 56. Solving for j and k separately (j = 77/9, k = 5/9) is unnecessary.

**Desmos** (not yet verified in Desmos). Type:<br><code>7x+2y=61</code><br><code>4x+5y=37</code><br><code>7(x-y)</code>

Desmos can only give the intersection, (8.556, 0.556), and then you still compute 7(8.556 - 0.556) = 56 with rounded values. Subtracting the equations by hand is faster and exact.

</details>

---

### 54. alg-sys-bagels-juices-combined-price

*Hard · Multiple choice · route: hand-primary · techniques: T2*

At a cafe, 3 bagels and 2 juices cost 13.50 dollars in total, and 5 bagels and 4 juices cost 24.50 dollars in total. All bagels have the same price, and all juices have the same price. What is the cost, in dollars, of 1 bagel and 1 juice together?

- **A.** $2.50$
- **B.** $3.00$
- **C.** $5.50$
- **D.** $11.00$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let b be the price of a bagel and j the price of a juice, in dollars. Then 3b + 2j = 13.50 and 5b + 4j = 24.50. Subtracting the first equation from the second yields 2b + 2j = 11.00, and dividing by 2 yields b + j = 5.50. Therefore, 1 bagel and 1 juice cost 5.50 dollars together. Distractors: 2.50 is the price of a bagel alone; 3.00 is the price of a juice alone; 11.00 is the cost of 2 bagels and 2 juices, the intermediate result before dividing by 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x+2y=13.5</code><br><code>5x+4y=24.5</code>

With x the bagel price and y the juice price, click the intersection: (2.5, 3). Add the coordinates to get 5.50. Subtracting the equations by hand gets there in one step, so Desmos is a check.

</details>

---

### 55. alg-sys-boat-current-speed

*Hard · Multiple choice · route: either · techniques: T2*

A boat travels 36 kilometers downstream in 2 hours and returns 36 kilometers upstream in 3 hours. Let $b$ be the boat's speed in still water and let $c$ be the speed of the current, both in kilometers per hour. What is the value of $c$?

- **A.** $3$
- **B.** $6$
- **C.** $12$
- **D.** $15$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Downstream the current adds to the boat's speed, so b + c = 36/2 = 18. Upstream it subtracts, so b - c = 36/3 = 12. Subtracting the second equation from the first yields 2c = 6, so c = 3. Therefore, the value of c is 3 (and b = 15). Distractors: 6 is 2c, the difference of the two speeds before dividing by 2; 12 is the upstream speed b - c; 15 is b, the boat's speed in still water.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y=18</code><br><code>x-y=12</code>

With x for b and y for c, the downstream speed is x + y = 36/2 and the upstream speed is x - y = 36/3. Click the intersection: (15, 3). The current is the y-coordinate, 3.

</details>

---

### 56. alg-sys-bridges-ages-future

*Hard · Multiple choice · route: either · techniques: T2*

Bridge A is 4 times as old as bridge B. In 12 years, bridge A will be 2.5 times as old as bridge B. How old, in years, is bridge A now?

- **A.** $12$
- **B.** $24$
- **C.** $48$
- **D.** $60$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let $a$ and $b$ be the current ages, in years, of bridges A and B. Then $a = 4b$, and in 12 years $a + 12 = 2.5(b + 12)$. Substituting $4b$ for $a$ yields $4b + 12 = 2.5b + 30$, or $1.5b = 18$, so $b = 12$ and $a = 48$. Check: in 12 years the ages are 60 and 24, and $60 = 2.5(24)$. Therefore, bridge A is 48 years old now. Distractors: 12 is bridge B's age; 24 is bridge B's age in 12 years; 60 is bridge A's age in 12 years, not now.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=4x</code><br><code>y+12=2.5(x+12)</code>

Use x for bridge B's age and y for bridge A's age now. Click the intersection: (12, 48). Bridge A's age is the y-coordinate, 48.

</details>

---

### 57. alg-sys-car-rental-six-dollars-less

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

To rent a car for a day, agency A charges 45 dollars plus 0.20 dollars per mile driven, and agency B charges 30 dollars plus 0.25 dollars per mile driven. For how many miles driven is agency A's charge 6 dollars less than agency B's charge?

- **A.** $120$
- **B.** $180$
- **C.** $300$
- **D.** $420$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** For m miles, agency A charges 45 + 0.20m dollars and agency B charges 30 + 0.25m dollars. A's charge is 6 dollars less than B's when (30 + 0.25m) - (45 + 0.20m) = 6, or 0.05m - 15 = 6. Adding 15 to both sides yields 0.05m = 21, so m = 420. Check: A charges 129.00 dollars and B charges 135.00 dollars. Therefore, the answer is 420 miles. Distractors: 120 drops the 15-dollar difference in fees and solves 0.05m = 6; 180 is where A's charge is 6 dollars more than B's (0.05m - 15 = -6); 300 is where the two charges are equal.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(30+0.25x)-(45+0.2x)</code><br><code>y=6</code>

The first line is B's charge minus A's charge. Zoom out and click where it meets y = 6: (420, 6). The answer is 420 miles.

</details>

---

### 58. alg-sys-courier-van-unloaded-type-b-spr

*Hard · Student-produced response · route: desmos-primary · techniques: T2*

A courier van starts a route with 900 kilograms of cargo. At each type A stop it unloads 60 kilograms, and at each type B stop it unloads 25 kilograms. After 20 stops, the van has 120 kilograms of cargo left. How many kilograms of cargo did the van unload at type B stops?

**Answer:** 300

<details><summary>Solutions</summary>

**By hand.** Let $a$ and $b$ be the numbers of type A and type B stops. Then $a + b = 20$, and the van unloaded $900 - 120 = 780$ kilograms, so $60a + 25b = 780$. Substituting $a = 20 - b$ yields $1200 - 60b + 25b = 780$, or $35b = 420$, so $b = 12$. At 25 kilograms per stop, the van unloaded $25(12) = 300$ kilograms at type B stops. Therefore, the answer is 300.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y=20</code><br><code>60x+25y=900-120</code>

Use x for type A stops and y for type B stops. Click the intersection: (8, 12). The question asks for kilograms unloaded at type B stops: 25(12) = 300.

</details>

---

### 59. alg-sys-cyclists-catch-up-distance-spr

*Hard · Student-produced response · route: desmos-primary · techniques: T2*

A cyclist leaves a trailhead riding at 18 kilometers per hour. Half an hour later, a second cyclist leaves the same trailhead on the same path riding at 24 kilometers per hour. How far, in kilometers, from the trailhead does the second cyclist catch up with the first?

**Answer:** 36

<details><summary>Solutions</summary>

**By hand.** Let t be the number of hours since the first cyclist left. The first cyclist's distance from the trailhead is d = 18t, and the second cyclist, who has ridden for t - 0.5 hours, is at d = 24(t - 0.5) = 24t - 12. Setting 18t = 24t - 12 yields 6t = 12, so t = 2, and d = 18(2) = 36. Therefore, the second cyclist catches up 36 kilometers from the trailhead.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=18x</code><br><code>y=24(x-0.5)</code>

Let x be the hours since the first cyclist left and y the distance in kilometers. Zoom out and click the intersection: (2, 36). The question asks for the distance, the y-coordinate 36, not the time 2.

</details>

---

### 60. alg-sys-decimal-equation-infinite-partner

*Hard · Multiple choice · route: either · techniques: T13*

One equation of a system of two linear equations is $0.4x - 1.2y = 2$. Which of the following could be the other equation if the system has infinitely many solutions?

- **A.** $2x - 6y = 10$
- **B.** $x - 3y = 2$
- **C.** $-x + 3y = 5$
- **D.** $3x - y = 15$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A system has infinitely many solutions when one equation is a constant multiple of the other. Multiplying 0.4x - 1.2y = 2 by 5 yields 2x - 6y = 10, so that choice describes the same line. Therefore, the other equation could be 2x - 6y = 10. Distractors: x - 3y = 2 scales the x- and y-coefficients by 2.5 but copies the constant 2 instead of scaling it to 5, so the lines are parallel and the system has no solution; -x + 3y = 5 is equivalent to x - 3y = -5, a sign slip on the constant that again gives parallel lines and no solution; 3x - y = 15 swaps the roles of the coefficients, giving a line with a different slope and exactly one solution.

**Desmos** (not yet verified in Desmos). Type:<br><code>0.4x-1.2y=2</code><br><code>2x-6y=10</code>

Type the given equation, then each choice in turn on the second line. Only 2x - 6y = 10 lands exactly on the given line (the graph shows a single line). The other choices give a parallel line or a crossing line.

</details>

---

### 61. alg-sys-exactly-one-solution-condition

*Hard · Multiple choice · route: hand-primary · techniques: —*

The system of equations $4x - 6y = 3$ and $6x + ky = c$, where $k$ and $c$ are constants, has exactly one solution. Which of the following must be true?

- **A.** $k \neq -9$
- **B.** $k = -9$
- **C.** $c \neq \frac{9}{2}$
- **D.** $c = \frac{9}{2}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A system of two linear equations has exactly one solution when the lines have different slopes, that is, when the x- and y-coefficients are not proportional. The coefficients are proportional when 6/4 = k/(-6), which yields k = -9. So the system has exactly one solution exactly when k is not -9, whatever the value of c. Therefore, k ≠ -9 must be true. Distractors: k = -9 makes the lines parallel, giving no solution or infinitely many; c ≠ 9/2 is what rules out infinitely many solutions when k = -9, but with k = -9 the system would then have no solution, and with k ≠ -9 the constant c can be anything; c = 9/2 is the constant that makes the lines identical when k = -9, and it is not required when the slopes differ. This item is pure reasoning about coefficients, so there is no Desmos route.

</details>

---

### 62. alg-sys-fractions-both-sides-x-minus-y

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

If $\frac{x + y}{2} = \frac{x - 5}{4}$ and $\frac{2x - y}{5} = \frac{y + 10}{3}$, what is the value of $x - y$?

- **A.** $-1$
- **B.** $1$
- **C.** $3$
- **D.** $7$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the first equation by 4 yields $2x + 2y = x - 5$, or $x + 2y = -5$. Multiplying both sides of the second equation by 15 yields $3(2x - y) = 5(y + 10)$, or $6x - 3y = 5y + 50$, which simplifies to $3x - 4y = 25$. Substituting $x = -5 - 2y$ yields $-15 - 10y = 25$, so $y = -4$ and $x = 3$. Therefore, $x - y = 3 - (-4) = 7$. Distractors: $-1$ is $x + y$; 1 comes from forgetting to multiply 10 by 5, which gives $3x - 4y = 5$ and the point $(-1, -2)$; 3 is the value of $x$ alone.

**Desmos** (not yet verified in Desmos). Type:<br><code>(x+y)/2=(x-5)/4</code><br><code>(2x-y)/5=(y+10)/3</code>

Type each equation as written, with parentheses around every numerator. Click the intersection: (3, -4). Then x - y = 3 - (-4) = 7.

</details>

---

### 63. alg-sys-functions-intersection-then-evaluate

*Hard · Multiple choice · route: desmos-primary · techniques: T9, T2*

Let $f(x) = 3x - 7$ and $g(x) = -\frac{1}{2}x + 7$, and let $a$ be the number for which $f(a) = g(a)$. What is the value of $f(2a)$?

- **A.** $3$
- **B.** $5$
- **C.** $10$
- **D.** $17$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that f(a) = g(a), so 3a - 7 = -(1/2)a + 7, which also makes (a, f(a)) the intersection of the two lines in the xy-plane. Adding (1/2)a + 7 to both sides yields (7/2)a = 14, so a = 4 and f(a) = f(4) = 5. Then f(2a) = f(8) = 3(8) - 7 = 17. Therefore, the value of f(2a) is 17. Distractors: 3 is g(8), evaluating the wrong function; 5 is f(a), stopping before doubling a; 10 is 2f(a), doubling the output instead of the input.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=3x-7</code><br><code>g(x)=-\frac{1}{2}x+7</code><br><code>f(2\cdot4)</code>

Graph both functions and click the intersection: (4, 5), so a = 4. Then type f(2\*4) on a new line; Desmos shows 17.

</details>

---

### 64. alg-sys-half-k-coefficient-no-solution-spr

*Hard · Student-produced response · route: hand-primary · techniques: T3*

The system of equations $\frac{k}{2}x - 3y = 4$ and $5x + 9y = 2$, where $k$ is a constant, has no solution. What is the value of $k$?

**Answer:** -10/3 (≈ -3.333)

<details><summary>Solutions</summary>

**By hand.** A system of two linear equations has no solution when the x- and y-coefficients are proportional but the constants are not. The y-coefficients give the ratio -3/9 = -1/3, so (k/2)/5 = -1/3, which yields k/2 = -5/3 and k = -10/3. The constants give 4/2 = 2, which differs from -1/3, so the lines are parallel and distinct rather than identical. Therefore, the value of k is -10/3.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{k}{2}x-3y=4</code><br><code>5x+9y=2</code>

Add a slider for k and drag it until the lines are parallel, near k = -3.33. The slider cannot land exactly on -10/3, so use the ratio method for the exact value and enter -10/3 (or -3.333).

</details>

---

### 65. alg-sys-infinite-shifted-constants-ab-spr

*Hard · Student-produced response · route: hand-primary · techniques: —*

The system of equations $(a - 1)x + 4y = 10$ and $3x + (b + 2)y = 15$, where $a$ and $b$ are constants, has infinitely many solutions. What is the value of $ab$?

**Answer:** 12

<details><summary>Solutions</summary>

**By hand.** A system of two linear equations has infinitely many solutions when one equation is a constant multiple of the other. Comparing the constants, the first equation is 10/15 = 2/3 times the second. So the x-coefficients satisfy a - 1 = (2/3)(3) = 2, which yields a = 3, and the y-coefficients satisfy 4 = (2/3)(b + 2), which yields b + 2 = 6, so b = 4. Therefore, ab = 3(4) = 12. Two unknown constants are slow to tune with sliders, so this item has no Desmos route; graphing 2x + 4y = 10 and 3x + 6y = 15 afterward confirms that the lines coincide.

</details>

---

### 66. alg-sys-infinite-solutions-product-mc

*Hard · Multiple choice · route: hand-primary · techniques: T3*

The system of equations $y = mx + 1$ and $4x - 6y = c$, where $m$ and $c$ are constants, has infinitely many solutions. What is the value of $mc$?

- **A.** $-9$
- **B.** $-6$
- **C.** $-4$
- **D.** $4$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A system has infinitely many solutions when both equations describe the same line. Solving $4x - 6y = c$ for $y$ yields $y = \frac{2}{3}x - \frac{c}{6}$. Matching this with $y = mx + 1$ gives $m = \frac{2}{3}$ and $-\frac{c}{6} = 1$, so $c = -6$. Therefore, $mc = \frac{2}{3}(-6) = -4$. Distractors: $-9$ uses the slope inverted, $m = \frac{3}{2}$; $-6$ is the value of $c$ alone; 4 comes from a sign error that gives $c = 6$.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=mx+1</code><br><code>4x-6y=c</code>

Two sliders are hard to tune by dragging. Rewrite 4x - 6y = c by hand as y = (2/3)x - c/6 first; then set m = 2/3 and drag c until the lines coincide at c = -6. The hand method is faster.

</details>

---

### 67. alg-sys-parallel-line-through-point

*Hard · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, line $\ell$ passes through the point $(2, 5)$. A system of two linear equations consisting of an equation of line $\ell$ and $3x - 4y = 12$ has no solution. Which of the following is an equation of line $\ell$?

- **A.** $4x + 3y = 23$
- **B.** $3x - 4y = 14$
- **C.** $3x - 4y = -14$
- **D.** $4x - 3y = -7$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A system with no solution consists of two parallel, distinct lines, so line l has the same slope as 3x - 4y = 12 and can be written 3x - 4y = C for a constant C. Substituting the point (2, 5) yields 3(2) - 4(5) = 6 - 20 = -14, so C = -14, which differs from 12. Therefore, an equation of line l is 3x - 4y = -14. Distractors: 4x + 3y = 23 passes through (2, 5) but is perpendicular to the given line, so the system has exactly one solution; 3x - 4y = 14 is parallel but drops the negative sign of -14, so it does not pass through (2, 5); 4x - 3y = -7 passes through (2, 5) but swaps the coefficients, giving the reciprocal slope 4/3 and exactly one solution.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x-4y=12</code><br><code>(2,5)</code><br><code>3x-4y=-14</code>

Type the given line and the point, then each choice in turn. Keep the choice that passes through (2, 5) and runs parallel to the given line without touching it: 3x - 4y = -14.

</details>

---

### 68. alg-sys-parameter-ratio-x-over-y

*Hard · Multiple choice · route: either · techniques: T4*

The system of equations $2x + 3y = 7k$ and $5x - y = 9k$, where $k$ is a nonzero constant, has the solution $(x, y)$. What is the value of $\frac{x}{y}$?

- **A.** $\frac{1}{2}$
- **B.** $\frac{7}{9}$
- **C.** $\frac{9}{7}$
- **D.** $2$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Multiplying the second equation by 3 yields $15x - 3y = 27k$. Adding this to the first equation yields $17x = 34k$, so $x = 2k$. Substituting into $5x - y = 9k$ yields $10k - y = 9k$, so $y = k$. Since $k \ne 0$, $\frac{x}{y} = \frac{2k}{k} = 2$. Therefore, the value of $\frac{x}{y}$ is 2. Distractors: 1/2 is $\frac{y}{x}$, the ratio inverted; 7/9 and 9/7 come from dividing the right-hand sides $7k$ and $9k$, as if the ratio of the constants gave the ratio of the variables.

**Desmos** (not yet verified in Desmos). Type:<br><code>2x+3y=7k</code><br><code>5x-y=9k</code>

Add a slider for k and set it to any nonzero value, such as k = 1: the intersection is (2, 1). Drag k to another value, such as 3: the intersection is (6, 3). The ratio x/y stays 2.

</details>

---

### 69. alg-sys-puppies-weight-weeks-units

*Hard · Multiple choice · route: either · techniques: T2*

Puppy A weighs 18 pounds and gains 2 pounds per week. Puppy B weighs 6 pounds and gains 0.5 pound per day. If both puppies keep gaining weight at these rates, after how many weeks will they weigh the same?

- **A.** $8$
- **B.** $12$
- **C.** $34$
- **D.** $56$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Puppy B gains $0.5 \times 7 = 3.5$ pounds per week. After $w$ weeks, puppy A weighs $18 + 2w$ pounds and puppy B weighs $6 + 3.5w$ pounds. Setting these equal yields $12 = 1.5w$, so $w = 8$. Without the conversion, $18 + 2w = 6 + 0.5w$ has a negative solution, a sign that the units do not match. Therefore, the puppies weigh the same after 8 weeks. Distractors: 12 is the starting difference in weight; 34 is the common weight, in pounds; 56 is the time in days, $8 \times 7$.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=18+2x</code><br><code>y=6+3.5x</code>

Convert puppy B's rate to pounds per week first: 0.5(7) = 3.5. With x in weeks, click the intersection: (8, 34). The question asks for weeks, 8.

</details>

---

### 70. alg-sys-scale-first-equation-seven-x-nine-y-spr

*Hard · Student-produced response · route: hand-primary · techniques: T2*

If $2x + 5y = 13$ and $3x - y = 4$, what is the value of $7x + 9y$?

**Answer:** 30

<details><summary>Solutions</summary>

**By hand.** Look for numbers $m$ and $n$ with $m(2x + 5y) + n(3x - y) = 7x + 9y$. Matching coefficients gives $2m + 3n = 7$ and $5m - n = 9$, so $m = 2$ and $n = 1$. Multiplying the first equation by 2 yields $4x + 10y = 26$, and adding the second equation yields $7x + 9y = 26 + 4 = 30$. Solving for $x$ and $y$ separately is possible but gives the fractions $x = \frac{33}{17}$ and $y = \frac{31}{17}$. Therefore, the value of $7x + 9y$ is 30.

**Desmos** (not yet verified in Desmos). Type:<br><code>2x+5y=13</code><br><code>3x-y=4</code><br><code>7(33/17)+9(31/17)</code>

The intersection shows rounded coordinates (1.941, 1.824), so 7x + 9y computed from them is only approximately 30. The exact solution is (33/17, 31/17); typing the third line confirms 30. Scaling and adding by hand is faster and exact.

</details>

---

### 71. alg-sys-slider-k-meet-on-x-axis

*Hard · Multiple choice · route: desmos-primary · techniques: T4, T13*

In the $xy$-plane, the graphs of $y = kx + 2$ and $3x - 2y = 8$, where $k$ is a constant, intersect at a point on the $x$-axis. What is the value of $k$?

- **A.** $-\frac{4}{3}$
- **B.** $-\frac{3}{4}$
- **C.** $\frac{3}{4}$
- **D.** $\frac{3}{2}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A point on the x-axis has y = 0. Substituting 0 for y in 3x - 2y = 8 yields 3x = 8, so the point is (8/3, 0). That point must also lie on y = kx + 2, so 0 = k(8/3) + 2, which yields (8/3)k = -2 and k = -3/4. Therefore, the value of k is -3/4. Distractors: -4/3 inverts the division at the last step, computing -(8/3)/2; 3/4 drops the sign when moving 2 across the equals sign; 3/2 is the slope of the second line, as if the lines had to be parallel.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=kx+2</code><br><code>3x-2y=8</code><br><code>k=-0.75</code>

Type the first two lines and add a slider for k. The second line crosses the x-axis at about (2.667, 0); drag k until the first line passes through that point too. To confirm exactly, set k to each choice (third line); only k = -0.75 makes all three meet on the x-axis.

</details>

---

### 72. alg-sys-solution-x-twice-y-coefficient-k

*Hard · Multiple choice · route: either · techniques: T3*

The system of equations $3x + ky = 26$ and $x - 4y = -2$, where $k$ is a constant, has a solution $(x, y)$ for which $x = 2y$. What is the value of $k$?

- **A.** $2$
- **B.** $\frac{23}{2}$
- **C.** $20$
- **D.** $44$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Only the second equation is free of $k$, so use it with the condition $x = 2y$. Substituting $2y$ for $x$ in $x - 4y = -2$ yields $-2y = -2$, so $y = 1$ and $x = 2$. Substituting $(2, 1)$ into $3x + ky = 26$ yields $6 + k = 26$, so $k = 20$. Therefore, the value of $k$ is 20. Distractors: 2 is the value of $x$, an intermediate result; 23/2 comes from swapping the coordinates and substituting $x = 1$ and $y = 2$, which gives $3 + 2k = 26$; 44 comes from using $y = 2x$ instead of $x = 2y$, which gives $x = \frac{2}{7}$ and $y = \frac{4}{7}$.

**Desmos** (not yet verified in Desmos). Type:<br><code>x-4y=-2</code><br><code>x=2y</code><br><code>3x+ky=26</code>

The first two lines meet at (2, 1). Add a slider for k and drag it until the third line passes through (2, 1); it does at k = 20. Confirm by substituting: 3(2) + 20(1) = 26.

</details>

---

### 73. alg-sys-swapped-slope-intercept-y-spr

*Hard · Student-produced response · route: either · techniques: T4*

In the $xy$-plane, the graphs of $y = ax + b$ and $y = bx + a$ intersect at the point $(x, y)$, where $a$ and $b$ are constants and $a \ne b$. If $a + b = 9$, what is the value of $y$?

**Answer:** 9

<details><summary>Solutions</summary>

**By hand.** At the intersection, $ax + b = bx + a$. Rearranging yields $ax - bx = a - b$, or $(a - b)x = a - b$. Since $a \ne b$, dividing by $a - b$ yields $x = 1$. Substituting $x = 1$ into $y = ax + b$ yields $y = a + b = 9$. Therefore, the value of $y$ is 9.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=ax+(9-a)</code><br><code>y=(9-a)x+a</code>

Use b = 9 - a so only one slider is needed. Add a slider for a and drag it to several values other than 4.5 (where the lines coincide). The intersection stays at (1, 9), so y = 9.

</details>

---

### 74. alg-sys-symmetric-coefficients-difference-of-squares

*Hard · Multiple choice · route: either · techniques: T2*

If $13x + 7y = 47$ and $7x + 13y = 13$, what is the value of $x^2 - y^2$?

- **A.** $3$
- **B.** $\frac{17}{3}$
- **C.** $17$
- **D.** $102$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Adding the equations yields 20x + 20y = 60, so x + y = 3. Subtracting the second equation from the first yields 6x - 6y = 34, so x - y = 17/3. Since x^2 - y^2 = (x + y)(x - y), the value is 3(17/3) = 17. Therefore, the value of x^2 - y^2 is 17. Distractors: 3 is x + y, an intermediate result; 17/3 is x - y, another intermediate result; 102 takes x - y as 34 by forgetting to divide 6x - 6y = 34 by 6, then multiplies by 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>13x+7y=47</code><br><code>7x+13y=13</code><br><code>\left(\frac{13}{3}\right)^2-\left(-\frac{4}{3}\right)^2</code>

Click the intersection: about (4.333, -1.333), which is (13/3, -4/3). Type the third line with those exact fractions to get 17; squaring the rounded decimals gives only an approximation.

</details>

---

### 75. alg-sys-three-constants-p-plus-r

*Hard · Multiple choice · route: hand-primary · techniques: —*

The ordered pair $(-1, 4)$ is the solution to the system of equations $px + qy = 10$ and $qx + ry = 13$, where $p$, $q$, and $r$ are constants. If $q$ is 1 more than $p$, what is the value of $p + r$?

- **A.** $5$
- **B.** $6$
- **C.** $7$
- **D.** $9$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting $x = -1$ and $y = 4$ into $px + qy = 10$ yields $-p + 4q = 10$. It's given that $q = p + 1$, so $-p + 4(p + 1) = 10$, or $3p + 4 = 10$, which gives $p = 2$ and $q = 3$. Substituting $x = -1$, $y = 4$ and $q = 3$ into $qx + ry = 13$ yields $-3 + 4r = 13$, so $r = 4$. Therefore, $p + r = 2 + 4 = 6$. Distractors: 5 is $p + q$; 7 is $q + r$; 9 is $p + q + r$, the sum of all three constants.

</details>

---

### 76. alg-sys-three-constants-solution-given-c-spr

*Hard · Student-produced response · route: hand-primary · techniques: —*

In the system of equations $ax + 3y = 19$ and $4x - by = c$, the solution is $(2, 5)$, where $a$, $b$, and $c$ are constants. If $b$ is twice $a$, what is the value of $c$?

**Answer:** -12

<details><summary>Solutions</summary>

**By hand.** It's given that $(2, 5)$ satisfies both equations. Substituting $x = 2$ and $y = 5$ into $ax + 3y = 19$ yields $2a + 15 = 19$, so $a = 2$. Since $b$ is twice $a$, $b = 4$. Substituting $x = 2$, $y = 5$ and $b = 4$ into $4x - by = c$ yields $c = 8 - 20 = -12$. Therefore, the value of $c$ is $-12$.

</details>

---

### 77. alg-system-k-on-line

*Hard · Student-produced response · route: hand-primary · techniques: T4, T2*

The system of equations $3x - 2y = 7$ and $5x + 4y = k$, where $k$ is a constant, has solution $(x, y)$. If $y = 2x$, what is the value of $k$?

**Answer:** -91

<details><summary>Solutions</summary>

**By hand.** Substituting 2x for y in 3x - 2y = 7 yields 3x - 4x = 7, so x = -7 and y = -14. Substituting these values into 5x + 4y = k yields k = 5(-7) + 4(-14) = -35 - 56 = -91.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x-2y=7</code><br><code>5x+4y=k</code><br><code>y=2x</code>

Add a slider for k and widen its range to about -100 to 100. Drag until all three lines meet at one point, (-7, -14): k = -91. Substituting y = 2x by hand is much faster.

</details>

---

### 78. alg-system-k-two-places-infinite

*Hard · Student-produced response · route: either · techniques: T3*

The system of equations $3x + ky = 11$ and $kx + 12y = 22$, where $k$ is a constant, has infinitely many solutions. What is the value of $k$?

**Answer:** 6

<details><summary>Solutions</summary>

**By hand.** Two linear equations have infinitely many solutions when one is a constant multiple of the other. Since 22 = 2(11), the second equation must be 2 times the first: 2(3) = k and 2k = 12, and both yield k = 6. Check: 2(3x + 6y) = 6x + 12y and 2(11) = 22. Note that k = -6 also makes the lines parallel, since 3(12) = k·k, but then -2 times the first equation is -6x - 12y = -22, not -6x + 12y = 22, so that system would have no solution.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x+ky=11</code><br><code>kx+12y=22</code>

Add a slider for k with step 1 and drag until the two lines lie on top of each other: k = 6. At k = -6 the lines are parallel but distinct. The ratio method by hand is as fast.

</details>

---

### 79. alg-tanks-equal-volume

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

Tank A contains 300 liters of water and is being filled at a rate of 12 liters per minute. Tank B contains 540 liters of water and is being drained at a rate of 8 liters per minute. When the two tanks contain the same amount of water, how many liters of water does each tank contain?

- **A.** $12$
- **B.** $396$
- **C.** $444$
- **D.** $636$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let t be the time in minutes. Tank A holds 300 + 12t liters and Tank B holds 540 - 8t liters. Setting them equal yields 300 + 12t = 540 - 8t, so 20t = 240 and t = 12. Each tank then holds 300 + 12(12) = 444 liters. Distractors: 12 is the time in minutes, not the amount of water; 396 uses 8 as the filling rate for Tank A (300 + 8(12)); 636 adds instead of subtracting for Tank B (540 + 8(12)).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=300+12x</code><br><code>y=540-8x</code>

Click the intersection: (12, 444). The question asks for the amount of water, the y-coordinate, 444 liters, not the time.

</details>

---

### 80. alg-which-equation-no-solution

*Hard · Multiple choice · route: either · techniques: T13, T2*

The equation $6x - 9y = 14$ is one of two equations in a system of linear equations. Which of the following could be the other equation if the system has no solution?

- **A.** $-4x + 6y = 11$
- **B.** $6x + 9y = 14$
- **C.** $9x - 6y = 14$
- **D.** $12x - 18y = 28$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** No solution means the same slope and a different intercept, so the x- and y-coefficients must be proportional but the constant must not be. 6x - 9y = 14 has slope 2/3. For -4x + 6y = 11: slope 4/6 = 2/3, and multiplying the given equation by -2/3 gives -4x + 6y = -28/3, not 11, so the lines are parallel and distinct. Distractors: 12x - 18y = 28 is exactly twice the given equation, so the system has infinitely many solutions; 9x - 6y = 14 swaps the coefficients and has slope 3/2, so the lines cross; 6x + 9y = 14 flips the sign on y and has slope -2/3, so the lines cross.

**Desmos** (not yet verified in Desmos). Type:<br><code>6x-9y=14</code><br><code>-4x+6y=11</code><br><code>6x+9y=14</code><br><code>9x-6y=14</code><br><code>12x-18y=28</code>

Graph the given line, then each choice. Three of the choices cross it or lie on top of it; only -4x + 6y = 11 is a separate parallel line (zoom out to be sure there is no crossing off screen). The ratio check by hand is about as fast.

</details>

---
