# Linear equations in two variables

[← Question bank index](README.md) · Algebra · 60 questions, easiest first

### 1. alg-dye-scarves-blankets-substitution

*Easy · Multiple choice · route: desmos-primary · techniques: T1*

A textile shop uses all of its 50 liters of dye on scarves and blankets. The equation $0.4s + 0.65b = 50$ represents this situation, where $s$ is the number of scarves dyed and $b$ is the number of blankets dyed. If 60 scarves are dyed, how many blankets are dyed?

- **A.** $16.9$
- **B.** $26$
- **C.** $27.5$
- **D.** $40$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Substituting 60 for $s$ yields $0.4(60) + 0.65b = 50$, or $24 + 0.65b = 50$. Subtracting 24 from both sides yields $0.65b = 26$, so $b = 40$. Therefore, 40 blankets are dyed. Distractors: 16.9 multiplies the remaining 26 liters by 0.65 instead of dividing; 26 is the number of liters left for blankets, an intermediate result; 27.5 swaps the two coefficients, using 0.65 liter per scarf and 0.4 liter per blanket.

**Desmos** (not yet verified in Desmos). Type:<br><code>0.4x+0.65y=50</code><br><code>x=60</code>

Here x is the number of scarves and y the number of blankets. Click the intersection of the two lines: (60, 40).

</details>

---

### 2. alg-horizontal-vertical-intersection-point

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $y = -9$ and $x = 4$ are lines. At which point do the two lines intersect?

- **A.** $(-9, 4)$
- **B.** $(-4, -9)$
- **C.** $(0, -9)$
- **D.** $(4, -9)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Every point on the graph of $x = 4$ has $x$-coordinate 4, and every point on the graph of $y = -9$ has $y$-coordinate $-9$. The only point on both lines is $(4, -9)$. Therefore, the lines intersect at $(4, -9)$. Distractors: $(-9, 4)$ swaps the coordinates; $(-4, -9)$ has a sign error in the $x$-coordinate; $(0, -9)$ is where the graph of $y = -9$ crosses the $y$-axis, which is not on the graph of $x = 4$.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-9</code><br><code>x=4</code>

Click the point where the horizontal and vertical lines cross: (4, -9).

</details>

---

### 3. alg-hostel-pillows-term-meaning

*Easy · Multiple choice · route: hand-primary · techniques: —*

A hostel spends exactly 180.00 dollars on pillows and towels. The equation $12p + 5t = 180$ represents this purchase, where $p$ is the number of pillows and $t$ is the number of towels. Which statement is the best interpretation of $12p$ in this context?

- **A.** The number of pillows bought.
- **B.** The price, in dollars, of one pillow.
- **C.** The total amount, in dollars, spent on towels.
- **D.** The total amount, in dollars, spent on pillows.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that the purchase totals 180 dollars and that p is the number of pillows. Each term on the left side is an amount of money, so 12 is the price, in dollars, of one pillow, and 12p is the price of one pillow times the number of pillows. Therefore, 12p is the total amount, in dollars, spent on pillows. Distractors: 'the number of pillows bought' describes p alone, not 12p; 'the price of one pillow' describes the coefficient 12; 'the total amount spent on towels' describes the other term, 5t.

</details>

---

### 4. alg-origin-line-missing-x-coordinate

*Easy · Multiple choice · route: either · techniques: T1*

In the $xy$-plane, a line passes through the origin and the point $(8, 6)$. The point $(k, 15)$ also lies on the line, where $k$ is a constant. What is the value of $k$?

- **A.** $11.25$
- **B.** $17$
- **C.** $20$
- **D.** $120$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A line through the origin represents a proportional relationship, so $\frac{y}{x}$ is the same for every point on it other than the origin. It follows that $\frac{15}{k} = \frac{6}{8}$, so $6k = 120$ and $k = 20$. Therefore, the value of $k$ is 20. Distractors: 11.25 is $15 \cdot \frac{6}{8}$, which uses the ratio upside down; 17 adds the difference $15 - 6 = 9$ to 8 instead of scaling; 120 is $15 \cdot 8$ before dividing by 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{6}{8}x</code><br><code>y=15</code>

Click the intersection of the two lines: (20, 15). The value of k is 20. Setting up the proportion by hand is about as fast.

</details>

---

### 5. alg-point-on-line-5x-3y-17

*Easy · Multiple choice · route: desmos-primary · techniques: T13*

In the $xy$-plane, which point lies on the graph of $5x - 3y = 17$?

- **A.** $(1, 4)$
- **B.** $(2, 9)$
- **C.** $(4, -1)$
- **D.** $(4, 1)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A point lies on the graph exactly when its coordinates satisfy the equation. Substituting 4 for x and 1 for y yields 5(4) - 3(1) = 20 - 3 = 17, so (4, 1) lies on the graph. Distractors: (1, 4) swaps the coordinates of the key, and 5(1) - 3(4) = -7; (4, -1) comes from a sign slip with -3y, and 5(4) - 3(-1) = 23; (2, 9) comes from solving for y with a sign error, y = (5x + 17)/3, and 5(2) - 3(9) = -17.

**Desmos** (not yet verified in Desmos). Type:<br><code>5x-3y=17</code><br><code>(1,4)</code><br><code>(2,9)</code><br><code>(4,-1)</code><br><code>(4,1)</code>

Graph the line and plot the four points; only (4, 1) sits on the line. Click it to confirm the label.

</details>

---

### 6. alg-point-on-standard-line-k

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the point $(4, k)$ lies on the graph of $2x + 3y = 23$, where $k$ is a constant. What is the value of $k$?

- **A.** $-5$
- **B.** $5$
- **C.** $\frac{31}{3}$
- **D.** $15$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since the point (4, k) lies on the graph, substituting 4 for x and k for y in 2x + 3y = 23 yields 2(4) + 3k = 23, so 8 + 3k = 23. Subtracting 8 from both sides yields 3k = 15, so k = 5. Distractors: -5 results from a sign error, 8 - 23 = -15; 31/3 results from adding 8 instead of subtracting it; 15 stops at 3k = 15 without dividing by 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>2x+3y=23</code><br><code>x=4</code>

Click the intersection of the line and the vertical line x = 4: (4, 5). The y-coordinate, 5, is k.

</details>

---

### 7. alg-slope-from-two-intercepts

*Easy · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, a line has an $x$-intercept at $(6, 0)$ and a $y$-intercept at $(0, -4)$. What is the slope of the line?

- **A.** $-\frac{3}{2}$
- **B.** $-\frac{2}{3}$
- **C.** $\frac{2}{3}$
- **D.** $\frac{3}{2}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The intercepts are the points (6, 0) and (0, -4). The slope is the change in y divided by the change in x: (0 - (-4))/(6 - 0) = 4/6 = 2/3. Therefore, the slope is 2/3. Distractors: 3/2 divides the change in x by the change in y; -2/3 subtracts the y-values in one order and the x-values in the other, (-4 - 0)/(6 - 0); -3/2 makes both errors.

**Desmos** (not yet verified in Desmos). Type:<br><code>(6,0)</code><br><code>(0,-4)</code><br><code>y=\frac{2}{3}x-4</code>

Every choice gives a line y = mx - 4 through (0, -4). Type y = mx - 4 with each choice for m; only m = 2/3 also passes through (6, 0). The slope formula by hand is as fast.

</details>

---

### 8. alg-slope-standard-form-7x-2y

*Easy · Multiple choice · route: hand-primary · techniques: —*

In the $xy$-plane, what is the slope of the graph of $7x + 2y = 9$?

- **A.** $-\frac{7}{2}$
- **B.** $-\frac{2}{7}$
- **C.** $\frac{2}{7}$
- **D.** $\frac{7}{2}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Solving the given equation for y puts it in slope-intercept form. Subtracting 7x from both sides yields 2y = -7x + 9, and dividing both sides by 2 yields y = -7/2 x + 9/2. Therefore, the slope of the graph is -7/2. Equivalently, a line Ax + By = C has slope -A/B = -7/2. Distractors: -2/7 inverts the ratio, -B/A; 7/2 drops the negative sign that comes from moving 7x to the other side; 2/7 makes both errors.

</details>

---

### 9. alg-slope-two-points

*Easy · Multiple choice · route: hand-primary · techniques: —*

In the $xy$-plane, a line passes through the points $(2, 7)$ and $(6, -1)$. What is the slope of the line?

- **A.** $-2$
- **B.** $-\frac{1}{2}$
- **C.** $\frac{1}{2}$
- **D.** $2$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The slope of a line through two points is the change in y divided by the change in x: (-1 - 7)/(6 - 2) = -8/4 = -2. Distractors: 2 drops the sign by taking the two differences in opposite orders; -1/2 divides the change in x by the change in y; 1/2 makes both errors.

</details>

---

### 10. alg-snack-stand-pretzels

*Easy · Multiple choice · route: hand-primary · techniques: —*

A snack stand sells pretzels for 3.00 dollars each and lemonades for 2.00 dollars each. The equation $3p + 2q = 96$ represents one day's sales, where $p$ is the number of pretzels and $q$ is the number of lemonades sold. If 12 lemonades were sold that day, how many pretzels were sold?

- **A.** $24$
- **B.** $28$
- **C.** $30$
- **D.** $32$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Substituting 12 for q in 3p + 2q = 96 yields 3p + 24 = 96. Subtracting 24 from both sides yields 3p = 72, so p = 24. Distractors: 30 results from substituting 12 for p instead of q (36 + 2q = 96); 32 ignores the lemonade sales (96/3); 28 subtracts 12 instead of 2(12) from 96 before dividing by 3.

</details>

---

### 11. alg-standard-form-y-intercept

*Easy · Multiple choice · route: hand-primary · techniques: —*

In the $xy$-plane, the graph of $3x - 5y = 30$ crosses the $y$-axis at the point $(0, y)$. What is the value of $y$?

- **A.** $-6$
- **B.** $6$
- **C.** $10$
- **D.** $30$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The y-intercept of a graph in the xy-plane is the point where x = 0. Substituting 0 for x in 3x - 5y = 30 yields -5y = 30, so y = -6. Therefore, the y-intercept is (0, -6). Distractors: 6 drops the negative sign when dividing 30 by -5; 10 is the x-coordinate of the x-intercept (y = 0 gives 3x = 30); 30 reads the constant term as the intercept without dividing by the coefficient of y.

</details>

---

### 12. alg-vertical-line-shared-x-equation

*Easy · Multiple choice · route: hand-primary · techniques: —*

In the $xy$-plane, a line passes through the points $(-3, 2)$ and $(-3, 9)$. Which equation represents the line?

- **A.** $x = -3$
- **B.** $y = -3$
- **C.** $y = 2$
- **D.** $y = 9$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that both points have an $x$-coordinate of $-3$. A line on which every point has the same $x$-coordinate is a vertical line, and its equation has the form $x = a$. Therefore, the line is represented by $x = -3$. Distractors: $y = -3$ writes the shared $x$-coordinate as a $y$-value; $y = 2$ is the horizontal line through the first point; $y = 9$ is the horizontal line through the second point.

</details>

---

### 13. alg-x-intercept-slope-intercept-form

*Easy · Student-produced response · route: either · techniques: T1*

In the $xy$-plane, the graph of $y = -4x + 10$ is a line. What is the $x$-coordinate of the point where this line crosses the $x$-axis?

**Answer:** 5/2 (≈ 2.5)

<details><summary>Solutions</summary>

**By hand.** A line crosses the x-axis where y = 0. Substituting 0 for y yields 0 = -4x + 10, so 4x = 10 and x = 10/4 = 5/2. Therefore, the line crosses the x-axis at x = 5/2, or 2.5.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-4x+10</code>

Click the gray point where the line crosses the x-axis: (2.5, 0). Enter 2.5 or 5/2. Setting y = 0 by hand is just as fast.

</details>

---

### 14. alg-catering-trays-verbal-rate-equation

*Medium · Multiple choice · route: either · techniques: T13*

A catering shop spends its whole budget on $x$ trays of salad and $y$ trays of pasta. For every 3 more salad trays it buys, it can buy 2 fewer pasta trays. One such order is 6 salad trays and 20 pasta trays. Which equation represents this situation?

- **A.** $2x - 3y = -48$
- **B.** $2x + 3y = 58$
- **C.** $2x + 3y = 72$
- **D.** $3x + 2y = 58$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Buying 3 more salad trays means buying 2 fewer pasta trays, so the slope of $y$ with respect to $x$ is $-\frac{2}{3}$. Through $(6, 20)$ the line is $y - 20 = -\frac{2}{3}(x - 6)$. Multiplying by 3 yields $3y - 60 = -2x + 12$, or $2x + 3y = 72$. Therefore, the situation is represented by $2x + 3y = 72$. Distractors: $2x - 3y = -48$ uses the slope $\frac{2}{3}$, a sign error; $2x + 3y = 58$ substitutes the order with $x$ and $y$ swapped, $2(20) + 3(6)$; $3x + 2y = 58$ inverts the rate to a slope of $-\frac{3}{2}$.

**Desmos** (not yet verified in Desmos). Type:<br><code>(6,20)</code><br><code>(9,18)</code><br><code>2x-3y=-48</code><br><code>2x+3y=58</code><br><code>2x+3y=72</code><br><code>3x+2y=58</code>

The order (9, 18) is 3 more salad trays and 2 fewer pasta trays than (6, 20). Type each choice in turn and keep the one whose line passes through both plotted points: 2x + 3y = 72.

</details>

---

### 15. alg-club-hoodies-keychains-tradeoff

*Medium · Multiple choice · route: hand-primary · techniques: —*

A club sells keychains for 8.00 dollars and hoodies for 20.00 dollars. Sales that meet its goal exactly satisfy $8k + 20h = 960$, where $k$ is the number of keychains and $h$ is the number of hoodies. If the club sells 4 more hoodies, how many fewer keychains must it sell to meet the goal exactly?

- **A.** $1.6$
- **B.** $4$
- **C.** $10$
- **D.** $80$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Selling 4 more hoodies adds 4(20) = 80 dollars. For the total to stay at 960 dollars, the keychain sales must drop by 80 dollars, which is 80/8 = 10 keychains. Equivalently, 8(k - 10) + 20(h + 4) = 8k + 20h - 80 + 80 = 960. Therefore, the club must sell 10 fewer keychains. Distractors: 80 is the dollar amount of the change, not a number of keychains; 4 assumes one keychain is traded for each hoodie; 1.6 multiplies 4 by the inverted ratio 8/20.

</details>

---

### 16. alg-horizontal-line-constant-y-crossing

*Medium · Multiple choice · route: either · techniques: T1*

In the $xy$-plane, the graph of $(2k - 6)x + (k + 1)y = 20$, where $k$ is a constant, is a horizontal line. At what value of $y$ does the graph cross the $y$-axis?

- **A.** $-10$
- **B.** $3$
- **C.** $5$
- **D.** $20$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A horizontal line has slope 0, so the coefficient of $x$ must be 0: $2k - 6 = 0$, so $k = 3$. The equation becomes $0x + 4y = 20$, or $y = 5$. Therefore, the graph crosses the $y$-axis at $y = 5$. Distractors: $-10$ comes from solving $2k - 6 = 0$ as $k = -3$, a sign error that makes the equation $-2y = 20$; $3$ is the value of $k$, an intermediate result; $20$ ignores the coefficient $k + 1$ of $y$.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x-6</code><br><code>(2\cdot3-6)x+(3+1)y=20</code>

In the first line x stands for k: its x-intercept, 3, is the k that makes the x-coefficient zero. The second line is the graph with k = 3; it is the horizontal line y = 5. Solving 2k - 6 = 0 by hand is about as fast.

</details>

---

### 17. alg-intercepts-triangle-area

*Medium · Multiple choice · route: either · techniques: T1*

In the $xy$-plane, the graph of $5x + 2y = 20$ and the two coordinate axes form a triangle. What is the area, in square units, of the triangle?

- **A.** $10$
- **B.** $14$
- **C.** $20$
- **D.** $40$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Substituting 0 for y yields 5x = 20, so the x-intercept is (4, 0). Substituting 0 for x yields 2y = 20, so the y-intercept is (0, 10). The triangle is a right triangle with legs 4 and 10 along the axes, so its area is (1/2)(4)(10) = 20. Distractors: 40 omits the factor 1/2; 14 adds the two intercepts, 4 + 10; 10 reports the y-intercept instead of the area.

**Desmos** (not yet verified in Desmos). Type:<br><code>5x+2y=20</code>

Click the two gray intercept points, (4, 0) and (0, 10). The legs of the right triangle are 4 and 10, so the area is (1/2)(4)(10) = 20. Finding the intercepts by hand is as fast.

</details>

---

### 18. alg-kiln-time-equation

*Medium · Multiple choice · route: hand-primary · techniques: —*

A ceramics studio reserves exactly 18 hours of kiln time for a class. Firing a small piece uses 0.25 hour of kiln time, and firing a large piece uses 0.75 hour. Which equation represents this situation, where $a$ is the number of small pieces and $b$ is the number of large pieces fired?

- **A.** $a + b = 18$
- **B.** $0.25a + 0.75b = 18$
- **C.** $0.75a + 0.25b = 18$
- **D.** $(0.25 + 0.75)(a + b) = 18$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Each small piece uses 0.25 hour, so a small pieces use 0.25a hours; each large piece uses 0.75 hour, so b large pieces use 0.75b hours. The total must equal the 18 hours reserved, so 0.25a + 0.75b = 18. Distractors: a + b = 18 counts pieces instead of hours; 0.75a + 0.25b = 18 swaps the firing times of small and large pieces; (0.25 + 0.75)(a + b) = 18 multiplies the total number of pieces by the sum of the two times, as if every piece used 1 hour.

</details>

---

### 19. alg-line-point-slope-equation

*Medium · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, a line has a slope of $-2$ and passes through the point $(6, 1)$. Which equation represents this line?

- **A.** $y = -2x - 11$
- **B.** $y = -2x + 1$
- **C.** $y = -2x + 13$
- **D.** $y = 2x - 11$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A line with slope -2 has an equation of the form y = -2x + b. Substituting the point (6, 1) yields 1 = -12 + b, so b = 13 and the equation is y = -2x + 13. Distractors: y = -2x + 1 uses the y-coordinate of the given point as the y-intercept; y = -2x - 11 makes a sign error when solving 1 = -12 + b; y = 2x - 11 drops the sign of the slope and then fits the point.

**Desmos** (not yet verified in Desmos). Type:<br><code>(6,1)</code><br><code>y=-2x+13</code>

Plot the point, then graph each choice; only y = -2x + 13 passes through (6, 1) while falling from left to right. Checking the point by hand is as fast.

</details>

---

### 20. alg-moving-boxes-table-equation

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

A moving truck is loaded exactly to its weight limit with $x$ light boxes and $y$ heavy boxes. Three combinations that reach the limit exactly are $(x, y) = (0, 12)$, $(6, 8)$, and $(15, 2)$. Which equation represents the relationship between $x$ and $y$?

- **A.** $2x + 3y = 12$
- **B.** $2x + 3y = 36$
- **C.** $2x - 3y = -36$
- **D.** $3x + 2y = 36$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The slope between (0, 12) and (6, 8) is (8 - 12)/(6 - 0) = -2/3, and (15, 2) gives (2 - 8)/(15 - 6) = -2/3 as well, so the points lie on one line with y-intercept 12: y = -2/3 x + 12. Multiplying by 3 yields 3y = -2x + 36, so 2x + 3y = 36. Distractors: 2x + 3y = 12 uses the y-intercept 12 as the constant without multiplying it by 3; 2x - 3y = -36 has a positive slope and fits only (0, 12); 3x + 2y = 36 swaps the coefficients of x and y.

**Desmos** (not yet verified in Desmos). Type:<br><code>(0,12)</code><br><code>(6,8)</code><br><code>(15,2)</code><br><code>2x+3y=36</code>

Plot the three points, then type each choice; only 2x + 3y = 36 passes through all three.

</details>

---

### 21. alg-parallel-line-y-intercept

*Medium · Student-produced response · route: either · techniques: T4*

In the $xy$-plane, line $\ell$ is parallel to the line with equation $2x + 3y = 12$ and passes through the point $(6, -1)$. The $y$-intercept of line $\ell$ is $(0, b)$, where $b$ is a constant. What is the value of $b$?

**Answer:** 3

<details><summary>Solutions</summary>

**By hand.** Solving 2x + 3y = 12 for y yields y = -2/3 x + 4, so the given line has slope -2/3, and a line parallel to it has the same slope. Line ℓ therefore has an equation of the form y = -2/3 x + b. Substituting the point (6, -1) yields -1 = -2/3(6) + b = -4 + b, so b = 3. Therefore, the y-intercept of line ℓ is (0, 3).

**Desmos** (not yet verified in Desmos). Type:<br><code>2x+3y=12</code><br><code>y=-\frac{2}{3}x+b</code><br><code>(6,-1)</code>

Add a slider for b and drag until the second line passes through (6, -1): b = 3, which is the y-intercept. Reading the slope and substituting the point by hand is about as fast.

</details>

---

### 22. alg-patio-tiles-table-missing-count

*Medium · Multiple choice · route: desmos-primary · techniques: T9*

A tile store lists combinations of small and large tiles that exactly cover a certain patio, and these combinations satisfy a linear equation. In the list, 12, 36, and $n$ small tiles are paired with 40, 32, and 17 large tiles, respectively. What is the value of $n$?

- **A.** $41$
- **B.** $45$
- **C.** $57$
- **D.** $81$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** From 40 large tiles to 32 large tiles, the number of small tiles rises from 12 to 36, so each large tile removed is replaced by $\frac{24}{8} = 3$ small tiles. Going from 32 to 17 large tiles removes 15 large tiles, which adds $15(3) = 45$ small tiles. Therefore, $n = 36 + 45 = 81$. Distractors: 41 inverts the rate, adding only $\frac{15}{3} = 5$ small tiles to 36; 45 is the number of small tiles added, an intermediate result; 57 adds the 45 small tiles to 12, the wrong starting pair.

**Desmos** (not yet verified in Desmos). Type:<br><code>g(x)=12+\frac{36-12}{32-40}(x-40)</code><br><code>g(17)</code>

g gives the number of small tiles for x large tiles, from the pairs (40, 12) and (32, 36). The value beside g(17) is 81.

</details>

---

### 23. alg-perpendicular-slope-standard-form

*Medium · Multiple choice · route: hand-primary · techniques: —*

In the $xy$-plane, line $\ell$ is perpendicular to the graph of $3x + 4y = 7$. What is the slope of line $\ell$?

- **A.** $-\frac{4}{3}$
- **B.** $-\frac{3}{4}$
- **C.** $\frac{3}{4}$
- **D.** $\frac{4}{3}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Solving 3x + 4y = 7 for y yields y = -3/4 x + 7/4, so the given graph has slope -3/4. Perpendicular lines have slopes whose product is -1, so the slope of line ℓ is the negative reciprocal of -3/4, which is 4/3. Distractors: -3/4 is the slope of the given line itself (a parallel line); 3/4 changes the sign but does not take the reciprocal; -4/3 takes the reciprocal but does not change the sign.

</details>

---

### 24. alg-perpendicular-to-vertical-y-crossing-spr

*Medium · Student-produced response · route: hand-primary · techniques: —*

In the $xy$-plane, line $\ell$ passes through the point $(5, -2)$ and is perpendicular to the graph of $x = 7$. At what value of $y$ does line $\ell$ cross the $y$-axis?

**Answer:** -2

<details><summary>Solutions</summary>

**By hand.** The graph of $x = 7$ is a vertical line. A line perpendicular to a vertical line is horizontal, so its slope is 0 and its equation has the form $y = b$. Since line $\ell$ passes through $(5, -2)$, its equation is $y = -2$. Every point on this line, including the point where it crosses the $y$-axis, has a $y$-coordinate of $-2$. Therefore, line $\ell$ crosses the $y$-axis at $y = -2$. A common slip is to use the slope $-\frac{1}{7}$, treating $x = 7$ as if it had slope 7.

</details>

---

### 25. alg-point-slope-to-standard-form

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

In the $xy$-plane, a line has equation $y - 4 = -\frac{3}{5}(x + 10)$. Which equation represents the same line?

- **A.** $3x + 5y = -10$
- **B.** $3x + 5y = -2$
- **C.** $3x + 5y = 50$
- **D.** $5x + 3y = -10$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Distributing yields y - 4 = -3/5 x - 6, and adding 4 to both sides yields y = -3/5 x - 2. Multiplying both sides by 5 yields 5y = -3x - 10, so 3x + 5y = -10. Distractors: 3x + 5y = -2 multiplies the x-term by 5 but not the constant -2; 3x + 5y = 50 reads x + 10 as x - 10, which gives y = -3/5 x + 10; 5x + 3y = -10 swaps the coefficients of x and y.

**Desmos** (not yet verified in Desmos). Type:<br><code>y-4=-\frac{3}{5}(x+10)</code><br><code>3x+5y=-10</code>

Type the given equation, then each choice in turn. The correct choice lies exactly on top of the given line; the others are separate lines (parallel or crossing).

</details>

---

### 26. alg-recycling-coefficient-meaning

*Medium · Multiple choice · route: hand-primary · techniques: —*

A recycling center buys aluminum and copper. The equation $0.8a + 3.2c = 56$ represents a load that earns 56.00 dollars, where $a$ is the number of kilograms of aluminum and $c$ is the number of kilograms of copper. Which of the following is the best interpretation of 3.2 in this context?

- **A.** The center pays 3.20 dollars for each kilogram of aluminum.
- **B.** The center pays 3.20 dollars more for a kilogram of copper than for a kilogram of aluminum.
- **C.** The center pays 3.20 dollars for each kilogram of copper.
- **D.** The load contains 3.2 kilograms of copper.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** In the equation 0.8a + 3.2c = 56, the term 3.2c is the amount earned, in dollars, from c kilograms of copper, so each kilogram of copper earns 3.20 dollars: the center pays 3.20 dollars for each kilogram of copper. Distractors: 'for each kilogram of aluminum' describes the coefficient of a, which is 0.8; '3.20 dollars more for a kilogram of copper' confuses the coefficient with the difference between the two rates, which is 3.2 - 0.8 = 2.4 dollars; 'contains 3.2 kilograms of copper' treats a coefficient as a value of the variable c, but the equation does not fix c.

</details>

---

### 27. alg-rewrite-to-standard-form-c

*Medium · Student-produced response · route: hand-primary · techniques: —*

In the $xy$-plane, a line has equation $y = -\frac{2}{5}x + 3$. When this equation is written in the form $2x + By = C$, where $B$ and $C$ are constants, what is the value of $C$?

**Answer:** 15

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of y = -2/5 x + 3 by 5 clears the fraction: 5y = -2x + 15. Adding 2x to both sides yields 2x + 5y = 15, which has the required coefficient 2 on x. Therefore, B = 5 and C = 15. A common slip is to multiply only the x-term by 5 and keep C = 3.

</details>

---

### 28. alg-table-line-find-x

*Medium · Student-produced response · route: desmos-primary · techniques: T5, T1*

Three ordered pairs $(x, y)$ that satisfy a certain linear equation in two variables are $(-3, 14)$, $(1, 2)$, and $(6, -13)$. What is the value of $x$ when $y = 50$?

**Answer:** -15

<details><summary>Solutions</summary>

**By hand.** The slope through (-3, 14) and (1, 2) is (2 - 14)/(1 - (-3)) = -12/4 = -3, and (6, -13) confirms it: (-13 - 2)/(6 - 1) = -3. Using (1, 2), the equation is y - 2 = -3(x - 1), so y = -3x + 5. Substituting 50 for y yields 50 = -3x + 5, so -3x = 45 and x = -15.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[-3,1,6]</code><br><code>y_1=[14,2,-13]</code><br><code>y_1\sim mx_1+b</code><br><code>y=mx+b</code><br><code>y=50</code>

The regression gives m = -3 and b = 5. Click the intersection of y = mx + b with y = 50: (-15, 50). Zoom out, since the point is far from the data.

</details>

---

### 29. alg-table-missing-y-entry-spr

*Medium · Student-produced response · route: desmos-primary · techniques: T9*

In a table for a linear relationship, $x$-values $2$, $6$, and $11$ correspond to $y$-values $7$, $17$, and $t$, respectively, where $t$ is a constant. What is the value of $t$?

**Answer:** 59/2 (≈ 29.5)

<details><summary>Solutions</summary>

**By hand.** The pairs $(2, 7)$ and $(6, 17)$ give a slope of $\frac{17 - 7}{6 - 2} = \frac{5}{2}$: each increase of 1 in $x$ increases $y$ by 2.5. From $x = 6$ to $x = 11$, $x$ increases by 5, so $y$ increases by $5(2.5) = 12.5$. Therefore, $t = 17 + 12.5 = 29.5$, which can be entered as 29.5 or 59/2.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=7+\frac{17-7}{6-2}(x-2)</code><br><code>f(11)</code>

f is the line through (2, 7) and (6, 17). The value beside f(11) is 29.5. Enter 29.5 or 59/2.

</details>

---

### 30. alg-tram-minutes-distance-equation

*Medium · Multiple choice · route: hand-primary · techniques: —*

A sightseeing tram travels exactly 48 kilometers, moving at 30 kilometers per hour for $x$ minutes and at 12 kilometers per hour for $y$ minutes. Which equation represents this situation?

- **A.** $30x + 12y = 0.8$
- **B.** $30x + 12y = 48$
- **C.** $30x + 12y = 2{,}880$
- **D.** $30x + 12y = 48{,}000$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The times are in minutes, so convert them to hours: $x$ minutes is $\frac{x}{60}$ hour and $y$ minutes is $\frac{y}{60}$ hour. Distance is rate times time, so $30\left(\frac{x}{60}\right) + 12\left(\frac{y}{60}\right) = 48$. Multiplying both sides by 60 yields $30x + 12y = 2{,}880$. Therefore, the situation is represented by $30x + 12y = 2{,}880$. Distractors: $30x + 12y = 0.8$ divides 48 by 60 instead of multiplying; $30x + 12y = 48$ ignores the conversion from minutes to hours; $30x + 12y = 48{,}000$ converts 48 kilometers to meters instead of converting the times.

</details>

---

### 31. alg-two-points-standard-form-equation

*Medium · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, a line passes through the points $(-4, 1)$ and $(2, 10)$. Which equation represents the line?

- **A.** $2x - 3y = -11$
- **B.** $3x - 2y = -14$
- **C.** $3x - 2y = 14$
- **D.** $3x + 2y = -10$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The slope is (10 - 1)/(2 - (-4)) = 9/6 = 3/2. Using the point (-4, 1), the line is y - 1 = 3/2 (x + 4). Multiplying both sides by 2 yields 2y - 2 = 3x + 12, and rearranging yields 3x - 2y = -14. Check: 3(2) - 2(10) = -14. Therefore, the line is 3x - 2y = -14. Distractors: 2x - 3y = -11 uses the inverted slope 2/3 through (-4, 1); 3x - 2y = 14 has the sign of the constant reversed; 3x + 2y = -10 uses slope -3/2 through (-4, 1).

**Desmos** (not yet verified in Desmos). Type:<br><code>(-4,1)</code><br><code>(2,10)</code><br><code>3x-2y=-14</code>

Plot both points, then type each choice; only 3x - 2y = -14 passes through both. Substituting the two points into each choice by hand is about as fast.

</details>

---

### 32. alg-two-points-x-axis-crossing-spr

*Medium · Student-produced response · route: desmos-primary · techniques: T5, T1*

In the $xy$-plane, a line passes through the points $(-2, 9)$ and $(4, -3)$. At what value of $x$ does this line cross the $x$-axis?

**Answer:** 5/2 (≈ 2.5)

<details><summary>Solutions</summary>

**By hand.** The slope of the line is (-3 - 9)/(4 - (-2)) = -12/6 = -2. Using the point (-2, 9), the equation of the line is y - 9 = -2(x + 2), which simplifies to y = -2x + 5. The line crosses the x-axis where y = 0, so 0 = -2x + 5 and x = 5/2.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[-2,4]</code><br><code>y_1=[9,-3]</code><br><code>y_1\sim mx_1+b</code><br><code>y=-2x+5</code>

The regression gives m = -2 and b = 5. Graph y = -2x + 5 and click where it crosses the x-axis: (2.5, 0). Enter 2.5 or 5/2.

</details>

---

### 33. alg-undefined-slope-points-with-k

*Medium · Multiple choice · route: either · techniques: T1*

In the $xy$-plane, a line passes through the points $(k + 1, 5)$ and $(3k - 7, -2)$, where $k$ is a constant. If the slope of the line is undefined, which equation represents the line?

- **A.** $x = -2$
- **B.** $x = 3$
- **C.** $x = 4$
- **D.** $x = 5$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A line with an undefined slope is vertical, so the two points have the same $x$-coordinate. Setting $k + 1 = 3k - 7$ yields $2k = 8$, so $k = 4$, and both points have $x$-coordinate $4 + 1 = 5$. Therefore, the line is $x = 5$. Distractors: $x = -2$ comes from writing $k + 1 = 3k + 7$, a sign error that gives $k = -3$; $x = 3$ comes from adding $k$ to $3k$ instead of subtracting, so $4k = 8$ and $k = 2$; $x = 4$ is the value of $k$, an intermediate result.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x+1</code><br><code>y=3x-7</code>

Here x stands for k. Click the intersection: (4, 5). It shows k = 4, and its y-value, 5, is the shared x-coordinate k + 1 of the two points, so the line is x = 5. Setting the x-coordinates equal by hand is about as fast.

</details>

---

### 34. alg-verbal-rate-x-axis-crossing

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

In the $xy$-plane, line $\ell$ passes through the point $(6, -1)$. Along line $\ell$, each increase of 3 in $x$ corresponds to a decrease of 2 in $y$. At what value of $x$ does line $\ell$ cross the $x$-axis?

- **A.** $3$
- **B.** $4.5$
- **C.** $\frac{16}{3}$
- **D.** $7.5$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A decrease of 2 in $y$ for each increase of 3 in $x$ means the slope is $\frac{-2}{3}$. Line $\ell$ is $y + 1 = -\frac{2}{3}(x - 6)$. Substituting 0 for $y$ yields $1 = -\frac{2}{3}(x - 6)$, so $x - 6 = -\frac{3}{2}$ and $x = 4.5$. Therefore, line $\ell$ crosses the $x$-axis at $x = 4.5$. Distractors: 3 is the value of $y$ where the line crosses the $y$-axis, the wrong intercept; $\frac{16}{3}$ uses the inverted slope $-\frac{3}{2}$; 7.5 uses the slope $\frac{2}{3}$, a sign error.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-1-\frac{2}{3}(x-6)</code>

The slope is the change in y over the change in x, -2/3. Click the x-intercept of the line: (4.5, 0).

</details>

---

### 35. alg-x-intercept-parallel-line-equation

*Medium · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, line $\ell$ has an $x$-intercept at $(-4, 0)$ and is parallel to the graph of $3x - 2y = 7$. Which equation represents line $\ell$?

- **A.** $3x - 2y = -12$
- **B.** $2x + 3y = -8$
- **C.** $3x - 2y = 8$
- **D.** $3x - 2y = 12$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Parallel lines have the same slope, and any line parallel to $3x - 2y = 7$ can be written as $3x - 2y = C$ for some constant $C$. Since line $\ell$ passes through $(-4, 0)$, substituting yields $C = 3(-4) - 2(0) = -12$. Therefore, line $\ell$ is represented by $3x - 2y = -12$. Distractors: $2x + 3y = -8$ passes through $(-4, 0)$ but is perpendicular to the given line; $3x - 2y = 8$ uses $(0, -4)$, treating the $x$-intercept as a $y$-intercept; $3x - 2y = 12$ uses $x = 4$, a sign error.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x-2y=7</code><br><code>(-4,0)</code><br><code>3x-2y=-12</code><br><code>2x+3y=-8</code><br><code>3x-2y=8</code><br><code>3x-2y=12</code>

Type each choice in turn. Keep only a line that runs parallel to 3x - 2y = 7 and passes through the plotted point (-4, 0): 3x - 2y = -12. Writing the equation by hand is about as fast.

</details>

---

### 36. alg-yarn-twine-combination-spr

*Medium · Student-produced response · route: desmos-primary · techniques: T9*

At a craft store, the combinations of skeins of yarn and balls of twine that cost exactly 60.00 dollars in all satisfy a linear equation. Two such combinations are 2 skeins with 12 balls and 6 skeins with 6 balls. How many balls of twine are in the combination with 8 skeins?

**Answer:** 3

<details><summary>Solutions</summary>

**By hand.** Let s be the number of skeins and b the number of balls of twine. The combinations (2, 12) and (6, 6) lie on one line, with slope (6 - 12)/(6 - 2) = -3/2: each extra skein replaces 1.5 balls of twine. From (6, 6), adding 2 skeins removes 2(1.5) = 3 balls, so b = 6 - 3 = 3. Equivalently, b = -3/2 s + 15 and -3/2(8) + 15 = 3. Therefore, the combination with 8 skeins has 3 balls of twine.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=12+\frac{6-12}{6-2}(x-2)</code><br><code>f(8)</code>

f(x) is the line through (2, 12) and (6, 6), with x skeins and f(x) balls of twine. The value beside f(8) is 3.

</details>

---

### 37. alg-art-club-canvases-greatest-count

*Hard · Multiple choice · route: either · techniques: T9*

An art club spends exactly 84.00 dollars on frames that cost 6.00 dollars each and canvases that cost 15.00 dollars each. What is the greatest number of canvases the club could have bought?

- **A.** $4$
- **B.** $5$
- **C.** $9$
- **D.** $14$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Let $f$ be the number of frames and $c$ the number of canvases, so $6f + 15c = 84$, or $2f + 5c = 28$, where $f$ and $c$ are nonnegative integers. Since $2f$ and 28 are even, $5c$ must be even, so $c$ is even. Also $5c \le 28$, so $c \le 5$. The greatest even value is $c = 4$, which gives $2f = 8$ and $f = 4$. Therefore, the greatest number of canvases is 4. Distractors: 5 rounds $\frac{84}{15} = 5.6$ down without checking that the remaining 9.00 dollars cannot buy a whole number of frames; 9 is the number of frames in the combination with 2 canvases, the wrong variable; 14 is the number of frames when no canvases are bought.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=\frac{84-15x}{6}</code><br><code>f(5)</code><br><code>f(4)</code>

f(x) is the number of frames bought with x canvases. f(5) = 1.5 is not a whole number, so 5 canvases is impossible; f(4) = 4 works. Testing values by hand is about as fast.

</details>

---

### 38. alg-barge-containers-slope-meaning

*Hard · Multiple choice · route: either · techniques: T1*

A cargo barge is fully loaded when $3a + 12b = 180$, where $a$ is the number of small containers and $b$ is the number of large containers on board. The equation is graphed in the $xy$-plane with $a$ on the $x$-axis and $b$ on the $y$-axis. Which statement is the best interpretation of the slope of the graph in this context?

- **A.** Adding 4 small containers requires removing 1 large container.
- **B.** Adding 1 small container requires removing 4 large containers.
- **C.** Adding 4 small containers requires adding 1 large container.
- **D.** Adding 4 large containers requires removing 1 small container.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Solving for b yields b = -1/4 a + 15, so the slope is -1/4: when a increases by 4, b decreases by 1, and the barge stays fully loaded. Therefore, adding 4 small containers requires removing 1 large container. Distractors: 'adding 1 small container requires removing 4 large containers' uses the reciprocal of the slope; 'adding 4 small containers requires adding 1 large container' ignores the negative sign; 'adding 4 large containers requires removing 1 small container' swaps the roles of a and b (adding 1 large container actually requires removing 4 small ones).

**Desmos** (not yet verified in Desmos). Type:<br><code>3x+12y=180</code>

Click the intercepts (60, 0) and (0, 15): replacing all 15 large containers takes 60 small ones, so 4 small containers take the place of 1 large one. Reading the slope -3/12 = -1/4 by hand is as fast.

</details>

---

### 39. alg-budget-x-intercept-meaning

*Hard · Multiple choice · route: hand-primary · techniques: —*

The equation $45x + 120y = 900$ represents the number of chairs, $x$, at 45.00 dollars each and the number of desks, $y$, at 120.00 dollars each that can be bought with a 900.00-dollar budget. In the $xy$-plane, what does the $x$-intercept of the graph of this equation represent?

- **A.** The cost, in dollars, of one chair and one desk together.
- **B.** The number of desks that can be bought if no chairs are bought.
- **C.** The number of chairs that can be bought for each desk that is bought.
- **D.** The number of chairs that can be bought if no desks are bought.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** At the x-intercept, y = 0, so no desks are bought, and 45x = 900 gives x = 20. Therefore, the x-intercept (20, 0) represents the number of chairs that can be bought if no desks are bought. Distractors: 'the number of desks that can be bought if no chairs are bought' describes the y-intercept, (0, 7.5); 'the number of chairs that can be bought for each desk' describes the ratio 120/45, which is related to the slope, not to an intercept; 'the cost of one chair and one desk together' is 165 dollars, a quantity the graph does not display.

</details>

---

### 40. alg-collinear-equal-spacing-k-spr

*Hard · Student-produced response · route: hand-primary · techniques: —*

In the $xy$-plane, the points $(0, k)$, $(3, 2k)$, and $(6, 10)$ lie on the same line, where $k$ is a constant. What is the value of $k$?

**Answer:** 10/3 (≈ 3.333)

<details><summary>Solutions</summary>

**By hand.** Three points lie on one line exactly when the slope between the first two equals the slope between the last two. The slopes are $\frac{2k - k}{3 - 0} = \frac{k}{3}$ and $\frac{10 - 2k}{6 - 3} = \frac{10 - 2k}{3}$. Setting them equal yields $k = 10 - 2k$, so $3k = 10$ and $k = \frac{10}{3}$. Alternate approach: the $x$-values 0, 3, 6 are equally spaced, so the middle $y$-value is the average of the outer two: $2k = \frac{k + 10}{2}$, which gives the same result. Therefore, the value of $k$ is $\frac{10}{3}$; enter 10/3 or 3.333.

</details>

---

### 41. alg-collinear-point-k-and-k-plus-13

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the points $(-2, 5)$, $(4, -7)$, and $(k, k + 13)$ lie on the same line, where $k$ is a constant. What is the value of $k$?

- **A.** $-6$
- **B.** $-4$
- **C.** $4$
- **D.** $9$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The slope of the line through $(-2, 5)$ and $(4, -7)$ is $\frac{-7 - 5}{4 - (-2)} = \frac{-12}{6} = -2$, so the line is $y - 5 = -2(x + 2)$, or $y = -2x + 1$. The point $(k, k + 13)$ lies on this line, so substituting yields $k + 13 = -2k + 1$, so $3k = -12$ and $k = -4$. Check: $(-4, 9)$ gives $\frac{9 - 5}{-4 + 2} = -2$. Therefore, the value of $k$ is $-4$. Distractors: $-6$ uses the reciprocal slope $-\frac{1}{2}$; $4$ comes from a sign error that makes the slope $2$; $9$ is the $y$-coordinate $k + 13$ of the third point, not $k$.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5+\frac{-7-5}{4+2}(x+2)</code><br><code>y=x+13</code>

The first line is the line through the two given points. Every point (k, k + 13) lies on y = x + 13, so click the intersection of the two lines: (-4, 9). The value of k is the x-coordinate, -4, not the y-coordinate 9.

</details>

---

### 42. alg-concrete-sand-gravel-total-spr

*Hard · Student-produced response · route: either · techniques: T2*

A crew mixes sand and gravel so that $5s = 3g$, where $s$ is the mass of sand, in kilograms, and $g$ is the mass of gravel, in kilograms. One batch has 45 more kilograms of gravel than sand. What is the total mass, in kilograms, of sand and gravel in the batch?

**Answer:** 180

<details><summary>Solutions</summary>

**By hand.** The equation $5s = 3g$ is a proportional relationship: $\frac{s}{g} = \frac{3}{5}$, so the batch has 3 parts sand to 5 parts gravel. The difference is $5 - 3 = 2$ parts, which is 45 kilograms, so 1 part is 22.5 kilograms. The total is $3 + 5 = 8$ parts, or $8(22.5) = 180$ kilograms. Alternate approach: substituting $g = s + 45$ yields $5s = 3s + 135$, so $s = 67.5$ and $g = 112.5$. Therefore, the total mass is 180 kilograms.

**Desmos** (not yet verified in Desmos). Type:<br><code>5x=3y</code><br><code>y-x=45</code>

Here x is the sand and y the gravel. Click the intersection: (67.5, 112.5). Add the coordinates: 67.5 + 112.5 = 180.

</details>

---

### 43. alg-fudge-toffee-intercepts-difference

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

A candy maker has 9 kilograms of sugar. A tray of fudge uses 450 grams of sugar, and a tray of toffee uses 300 grams. If all the sugar is used, how many more trays can be made by making only toffee than by making only fudge? (1 kilogram = 1,000 grams)

- **A.** $0.01$
- **B.** $10$
- **C.** $20$
- **D.** $50$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Converting, 9 kilograms is 9,000 grams. If f trays of fudge and t trays of toffee use all the sugar, 450f + 300t = 9,000. Making only fudge means t = 0, so f = 9,000/450 = 20; making only toffee means f = 0, so t = 9,000/300 = 30. Therefore, making only toffee yields 30 - 20 = 10 more trays. Distractors: 0.01 skips the unit conversion, 9/300 - 9/450; 20 is the number of fudge trays alone; 50 adds the two intercepts, 20 + 30.

**Desmos** (not yet verified in Desmos). Type:<br><code>450x+300y=9000</code>

Here x is trays of fudge and y is trays of toffee. Zoom out and click the intercepts (20, 0) and (0, 30); the difference 30 - 20 is 10.

</details>

---

### 44. alg-intercepts-relation-k-spr

*Hard · Student-produced response · route: hand-primary · techniques: —*

In the $xy$-plane, the graph of $kx - 3y = 12$ has $x$-intercept $(a, 0)$ and $y$-intercept $(0, b)$, where $k$, $a$ and $b$ are constants. If $a = 2b$, what is the value of $k$?

**Answer:** -3/2 (≈ -1.5)

<details><summary>Solutions</summary>

**By hand.** At the y-intercept, x = 0, so k(0) - 3b = 12 and b = -4. It's given that a = 2b, so a = -8. At the x-intercept, y = 0, so k(-8) - 3(0) = 12, which gives -8k = 12 and k = -12/8 = -3/2.

</details>

---

### 45. alg-intercepts-ten-units-apart-k

*Hard · Multiple choice · route: hand-primary · techniques: —*

In the $xy$-plane, the graph of $kx + 3y = 24$, where $k$ is a positive constant, crosses the $x$-axis and the $y$-axis at two points that are 10 units apart. What is the value of $k$?

- **A.** $2.4$
- **B.** $4$
- **C.** $6$
- **D.** $8$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting 0 for $x$ yields $3y = 24$, so the graph crosses the $y$-axis at $(0, 8)$. The graph crosses the $x$-axis at $(a, 0)$, where $a = \frac{24}{k}$ is positive because $k$ is positive. The two points and the origin form a right triangle with legs $a$ and 8 and hypotenuse 10, so by the Pythagorean theorem $a^2 + 64 = 100$ and $a = 6$. Then $\frac{24}{k} = 6$, so $k = 4$. Therefore, the value of $k$ is 4. Distractors: 2.4 is $\frac{24}{10}$, which treats the distance 10 as the $x$-intercept; 6 is the $x$-coordinate of the $x$-intercept, an intermediate result; 8 is the $y$-coordinate of the $y$-intercept.

</details>

---

### 46. alg-intercepts-to-constants

*Hard · Multiple choice · route: either · techniques: T4*

In the $xy$-plane, the graph of $ax + by = 24$, where $a$ and $b$ are constants, has $x$-intercept $(4, 0)$ and $y$-intercept $(0, -3)$. What is the value of $a - b$?

- **A.** $-2$
- **B.** $6$
- **C.** $8$
- **D.** $14$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Since (4, 0) is on the graph, substituting 4 for x and 0 for y yields 4a = 24, so a = 6. Since (0, -3) is on the graph, substituting 0 for x and -3 for y yields -3b = 24, so b = -8. Therefore, a - b = 6 - (-8) = 14. Distractors: -2 is a + b; 6 is the value of a alone; 8 is the value of -b alone, reported without adding a.

**Desmos** (not yet verified in Desmos). Type:<br><code>ax+by=24</code><br><code>(4,0)</code><br><code>(0,-3)</code>

Add sliders for a and b and drag until the line passes through both points: a = 6, b = -8, so a - b = 14. Two sliders are slow to tune; substituting each intercept by hand takes one step each.

</details>

---

### 47. alg-line-constant-x-intercept

*Hard · Multiple choice · route: either · techniques: T4, T1*

In the $xy$-plane, the graph of $ax + 4y = 20$, where $a$ is a constant, passes through the point $(-6, 2)$. At what value of $x$ does the graph cross the $x$-axis?

- **A.** $-10$
- **B.** $-2$
- **C.** $5$
- **D.** $10$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Substituting x = -6 and y = 2 into ax + 4y = 20 yields -6a + 8 = 20, so -6a = 12 and a = -2. The equation is -2x + 4y = 20. At the x-intercept, y = 0, so -2x = 20 and x = -10. Distractors: -2 is the value of a rather than the x-intercept; 5 is the y-coordinate of the y-intercept (4y = 20); 10 results from a sign error in solving -2x = 20.

**Desmos** (not yet verified in Desmos). Type:<br><code>ax+4y=20</code><br><code>(-6,2)</code>

Add a slider for a and drag until the line passes through the plotted point: a = -2. Then click the x-intercept: (-10, 0). Substituting the point by hand gives a exactly and is about as fast.

</details>

---

### 48. alg-origin-constant-slope

*Hard · Multiple choice · route: hand-primary · techniques: —*

In the $xy$-plane, the graph of $(k - 3)x + 4y = 2k - 10$, where $k$ is a constant, passes through the origin. What is the slope of the graph?

- **A.** $-\frac{1}{2}$
- **B.** $\frac{1}{2}$
- **C.** $2$
- **D.** $5$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that the graph passes through $(0, 0)$. Substituting 0 for $x$ and 0 for $y$ yields $0 = 2k - 10$, so $k = 5$. The equation becomes $2x + 4y = 0$, or $y = -\frac{1}{2}x$. Therefore, the slope of the graph is $-\frac{1}{2}$. Distractors: $\frac{1}{2}$ drops the negative sign when solving for $y$; $2$ divides the $y$-coefficient by the $x$-coefficient, $\frac{4}{2}$; $5$ is the value of $k$, an intermediate result.

</details>

---

### 49. alg-parallel-through-point-which-point

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

In the $xy$-plane, line $\ell$ passes through the point $(-3, 7)$ and is parallel to the graph of $4x + 6y = 5$. Which point also lies on line $\ell$?

- **A.** $(-1, 10)$
- **B.** $(1, 1)$
- **C.** $(3, 11)$
- **D.** $(6, 1)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Solving 4x + 6y = 5 for y yields y = -2/3 x + 5/6, so the slope is -2/3, and line ℓ has the same slope. Through (-3, 7), line ℓ is y - 7 = -2/3 (x + 3), or y = -2/3 x + 5. Substituting 6 for x yields -4 + 5 = 1, so (6, 1) lies on line ℓ. Distractors: (1, 1) lies on the line through (-3, 7) with slope -3/2, the inverted ratio; (3, 11) lies on the line with slope 2/3, a sign error; (-1, 10) lies on the line with slope 3/2, the perpendicular slope.

**Desmos** (not yet verified in Desmos). Type:<br><code>4x+6y=5</code><br><code>y-7=-\frac{2}{3}(x+3)</code><br><code>(-1,10)</code><br><code>(1,1)</code><br><code>(3,11)</code><br><code>(6,1)</code>

The second line is line ℓ (it should look parallel to the first). Plot the four points; only (6, 1) sits on line ℓ.

</details>

---

### 50. alg-perpendicular-line-equation

*Hard · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, line $\ell$ is perpendicular to the line with equation $x - 4y = 2$ and passes through the point $(-1, 5)$. Which equation represents line $\ell$?

- **A.** $y = -4x + 1$
- **B.** $y = -4x + 9$
- **C.** $y = 0.25x + 5.25$
- **D.** $y = 4x + 9$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Solving x - 4y = 2 for y yields y = 0.25x - 0.5, so the given line has slope 1/4. A line perpendicular to it has slope -4, the negative reciprocal. Using the point (-1, 5), the equation of line ℓ is y - 5 = -4(x + 1), which simplifies to y = -4x + 1. Distractors: y = -4x + 9 results from writing -4(x - 1) instead of -4(x + 1), a sign slip on the point; y = 0.25x + 5.25 uses the slope of the given line, which gives a parallel line, not a perpendicular one; y = 4x + 9 takes the reciprocal without changing the sign.

**Desmos** (not yet verified in Desmos). Type:<br><code>x-4y=2</code><br><code>(-1,5)</code><br><code>y=-4x+1</code>

Graph the given line and the point, then add each choice. Only y = -4x + 1 both passes through (-1, 5) and meets the given line at a right angle (set equal axis scales to see the right angle). y = -4x + 9 misses the point; the other two pass through it but are not perpendicular.

</details>

---

### 51. alg-perpendicular-shared-x-intercept

*Hard · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, line $\ell$ is perpendicular to the graph of $3x - 4y = 12$, and both lines have the same $x$-intercept. Which equation represents line $\ell$?

- **A.** $3x + 4y = 12$
- **B.** $4x + 3y = -9$
- **C.** $4x + 3y = 16$
- **D.** $4x - 3y = 16$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Solving 3x - 4y = 12 for y yields y = 3/4 x - 3, so the given graph has slope 3/4 and, substituting 0 for y, x-intercept (4, 0). Line ℓ has the negative reciprocal slope, -4/3, and passes through (4, 0): y = -4/3 (x - 4). Multiplying by 3 yields 3y = -4x + 16, so 4x + 3y = 16. Distractors: 3x + 4y = 12 has slope -3/4, which changes the sign without taking the reciprocal; 4x - 3y = 16 has slope 4/3, the reciprocal without the sign change; 4x + 3y = -9 has the correct slope but passes through the y-intercept (0, -3) instead of the x-intercept.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x-4y=12</code><br><code>4x+3y=16</code>

Graph the given line and each choice. Three choices cross the x-axis at (4, 0) with the given line (4x + 3y = -9 does not); of those three, only 4x + 3y = 16 meets it at a right angle (slopes 3/4 and -4/3). Use Desmos to confirm the shared intercept and check the slopes by hand.

</details>

---

### 52. alg-perpendicular-x-intercept

*Hard · Student-produced response · route: hand-primary · techniques: T1, T11*

In the $xy$-plane, line $\ell$ passes through the point $(-3, 7)$ and is perpendicular to the line with equation $4x - 6y = 5$. What is the $x$-coordinate of the $x$-intercept of line $\ell$?

**Answer:** 5/3 (≈ 1.667)

<details><summary>Solutions</summary>

**By hand.** 4x - 6y = 5 gives y = (2/3)x - 5/6, slope 2/3, so the perpendicular slope is -3/2. Line l: y - 7 = -3/2 (x + 3). Set y = 0: -7 = -3/2 (x + 3), so x + 3 = 14/3 and x = 5/3.

**Desmos** (not yet verified in Desmos). Type:<br><code>4x-6y=5</code><br><code>y-7=-\frac{3}{2}(x+3)</code>

After finding the perpendicular slope by hand, graph line l and click its x-intercept: 1.667, which the fraction toggle shows as 5/3. Enter 5/3, 1.666 or 1.667.

</details>

---

### 53. alg-point-on-every-line-r

*Hard · Student-produced response · route: hand-primary · techniques: T4, T2*

In the $xy$-plane, for every real number $r$, the graph of $(r + 2)x + (1 - 3r)y = 6r + 5$ passes through the point $(a, b)$. What is the value of $a - b$?

**Answer:** 4

<details><summary>Solutions</summary>

**By hand.** Rearrange so the r terms are together: r(x - 3y - 6) + (2x + y - 5) = 0. For this to hold for every r, both brackets must be zero: x - 3y = 6 and 2x + y = 5. From the second, y = 5 - 2x; substitute: x - 15 + 6x = 6, so x = 3 and y = -1. The point is (3, -1), and a - b = 3 - (-1) = 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>(r+2)x+(1-3r)y=6r+5</code><br><code>2x+y=5</code><br><code>3x-2y=11</code>

Add a slider for r and drag it: the line pivots around one fixed point. To pin the point down, type the r = 0 and r = 1 versions as separate lines and click their intersection, (3, -1). Then a - b = 4. This is slower than collecting the r terms by hand; use it as a check.

</details>

---

### 54. alg-point-shift-stays-on-line

*Hard · Multiple choice · route: hand-primary · techniques: —*

In the $xy$-plane, the point $(p, q)$ lies on the graph of $4x - 3y = 10$, where $p$ and $q$ are constants. Which of the following points must also lie on the graph?

- **A.** $(p + 3, q - 4)$
- **B.** $(p + 3, q + 4)$
- **C.** $(p + 4, q - 3)$
- **D.** $(p + 4, q + 3)$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** It's given that 4p - 3q = 10. Substituting (p + 3, q + 4) yields 4(p + 3) - 3(q + 4) = 4p + 12 - 3q - 12 = 4p - 3q = 10, so this point lies on the graph for every such (p, q). The structure reason: the slope of 4x - 3y = 10 is 4/3, so moving 3 right and 4 up stays on the line. Distractors: (p + 3, q - 4) uses slope -4/3, a sign error, and gives 4p - 3q + 24; (p + 4, q + 3) uses the inverted slope 3/4 and gives 4p - 3q + 7; (p + 4, q - 3) reads the coefficients 4 and -3 directly as the steps and gives 4p - 3q + 25.

</details>

---

### 55. alg-ribbon-pieces-unit-equation

*Hard · Multiple choice · route: either · techniques: T13*

A fabric shop cuts a 45-meter roll of ribbon entirely into short pieces that are 30 centimeters long and long pieces that are 1.2 meters long. If $a$ is the number of short pieces and $b$ is the number of long pieces, which equation represents this situation? (1 meter = 100 centimeters)

- **A.** $0.3a + 1.2b = 45$
- **B.** $0.03a + 1.2b = 45$
- **C.** $30a + 1.2b = 45$
- **D.** $30a + 120b = 45$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** All lengths must be in the same unit. Since 1 meter = 100 centimeters, 30 centimeters is 30/100 = 0.3 meter. The short pieces use 0.3a meters, the long pieces use 1.2b meters, and together they use the whole 45-meter roll, so 0.3a + 1.2b = 45. Distractors: 0.03a + 1.2b = 45 divides 30 by 1,000 instead of 100; 30a + 1.2b = 45 mixes centimeters and meters; 30a + 120b = 45 converts both piece lengths to centimeters but leaves the roll in meters (it should be 4,500).

**Desmos** (not yet verified in Desmos). Type:<br><code>(30,30)</code><br><code>0.3x+1.2y=45</code>

Find one combination that uses the whole roll, such as 30 long pieces (36 meters) and 30 short pieces (9 meters), and plot (30, 30). Type each choice with x for a and y for b; only 0.3x + 1.2y = 45 passes through the point. Building the equation by hand is about as fast.

</details>

---

### 56. alg-seed-packet-boxes-combination-count-spr

*Hard · Student-produced response · route: hand-primary · techniques: —*

A garden store packs exactly 60 seed packets into small boxes that hold 4 packets each and large boxes that hold 6 packets each, and every box is full. How many different combinations of numbers of small and large boxes are possible? (A combination that uses boxes of only one size counts as one of the combinations.)

**Answer:** 6

<details><summary>Solutions</summary>

**By hand.** Let $s$ be the number of small boxes and $b$ the number of large boxes, so $4s + 6b = 60$, or $2s + 3b = 30$, where $s$ and $b$ are nonnegative integers. Since $2s$ and 30 are even, $3b$ must be even, so $b$ is even. Also $3b \le 30$, so $b \le 10$. The possible values $b = 0, 2, 4, 6, 8, 10$ give $s = 15, 12, 9, 6, 3, 0$. Therefore, 6 combinations are possible. A common mistake is to drop the two one-size combinations and answer 4, or to count every $b$ from 0 to 10 and answer 11.

</details>

---

### 57. alg-shared-y-intercept-x-intercept-spr

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

In the $xy$-plane, line $\ell$ passes through the point $(3, -2)$ and has the same $y$-intercept as the graph of $2x + 5y = 15$. Line $\ell$ crosses the $x$-axis at the point $(r, 0)$. What is the value of $r$?

**Answer:** 9/5 (≈ 1.8)

<details><summary>Solutions</summary>

**By hand.** Substituting 0 for x in 2x + 5y = 15 yields 5y = 15, so the y-intercept is (0, 3), and line ℓ passes through (0, 3) and (3, -2). Its slope is (-2 - 3)/(3 - 0) = -5/3, so line ℓ is y = -5/3 x + 3. Substituting 0 for y yields 5/3 x = 3, so x = 9/5. Therefore, line ℓ crosses the x-axis at (9/5, 0), so r = 9/5, or 1.8. A common slip is to use the x-intercept (7.5, 0) of the given graph instead of its y-intercept.

**Desmos** (not yet verified in Desmos). Type:<br><code>2x+5y=15</code><br><code>(3,-2)</code><br><code>y=\frac{-2-3}{3-0}x+3</code>

Click where 2x + 5y = 15 crosses the y-axis: (0, 3). The third line goes through (0, 3) and (3, -2); click its x-intercept, (1.8, 0). Enter 1.8 or 9/5.

</details>

---

### 58. alg-slope-constant-x-intercept-spr

*Hard · Student-produced response · route: hand-primary · techniques: —*

In the $xy$-plane, the graph of $kx + 2y = 10$ is a line with a slope of $3$, where $k$ is a constant. If the graph crosses the $x$-axis at the point $(c, 0)$, what is the value of $c$?

**Answer:** -5/3 (≈ -1.667)

<details><summary>Solutions</summary>

**By hand.** Solving kx + 2y = 10 for y yields y = -k/2 x + 5, so the slope is -k/2. It's given that the slope is 3, so -k/2 = 3 and k = -6. The equation is -6x + 2y = 10. Substituting 0 for y yields -6x = 10, so x = -10/6 = -5/3. Therefore, the graph crosses the x-axis at (-5/3, 0), so c = -5/3 (enter -5/3, -1.666 or -1.667). A common slip is taking the slope as k/2, which gives k = 6 and x = 5/3.

</details>

---

### 59. alg-slope-two-points-with-k

*Hard · Multiple choice · route: either · techniques: T4*

In the $xy$-plane, a line with slope 2 passes through the points $(2, k)$ and $(k, 11)$, where $k$ is a constant. What is the value of $k$?

- **A.** $13$
- **B.** $8$
- **C.** $5$
- **D.** $-7$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The slope between (2, k) and (k, 11) is (11 - k)/(k - 2), and it's given that this equals 2. Multiplying both sides by k - 2 yields 11 - k = 2(k - 2) = 2k - 4. Adding k and 4 to both sides yields 15 = 3k, so k = 5. Check: the points (2, 5) and (5, 11) give slope 6/3 = 2. Distractors: 8 sets run over rise equal to 2, (k - 2)/(11 - k) = 2; -7 subtracts the coordinates in opposite orders, (11 - k)/(2 - k) = 2; 13 adds the slope to 11, as if the two points were 1 unit apart horizontally.

**Desmos** (not yet verified in Desmos). Type:<br><code>(2,k)</code><br><code>(k,11)</code><br><code>y=2x+b</code>

Add sliders for k and b and drag until both points lie on the line y = 2x + b: k = 5 (with b = 1). The slope formula by hand is faster.

</details>

---

### 60. alg-table-entries-p-and-2p

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

In a table for a linear relationship, $x$-values $1$, $3$, and $p$ correspond to $y$-values $5$, $11$, and $2p$, respectively, where $p$ is a constant. What is the value of $p$?

- **A.** $-4$
- **B.** $-2$
- **C.** $2$
- **D.** $\frac{14}{5}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The pairs $(1, 5)$ and $(3, 11)$ give a slope of $\frac{11 - 5}{3 - 1} = 3$, so the relationship is $y = 3x + 2$. The pair $(p, 2p)$ satisfies it, so $2p = 3p + 2$ and $p = -2$. Check: the pair is $(-2, -4)$, and $3(-2) + 2 = -4$. Therefore, the value of $p$ is $-2$. Distractors: $-4$ is the $y$-value $2p$, not $p$; $2$ comes from a sign error when moving $3p$ across, giving $p = 2$; $\frac{14}{5}$ uses the inverted slope $\frac{1}{3}$.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5+\frac{11-5}{3-1}(x-1)</code><br><code>y=2x</code>

The first line passes through (1, 5) and (3, 11). The third pair (p, 2p) lies on y = 2x, so click the intersection: (-2, -4). The value of p is the x-coordinate, -2.

</details>

---
