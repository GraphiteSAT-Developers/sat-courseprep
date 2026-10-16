# Linear inequalities in one or two variables

[← Question bank index](README.md) · Algebra · 70 questions, easiest first

### 1. alg-greatest-value-simple-inequality

*Easy · Multiple choice · route: either · techniques: T1*

If $2x + 7 \le 19$, what is the greatest possible value of $x$?

- **A.** $-6$
- **B.** $2.5$
- **C.** $6$
- **D.** $13$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Subtracting 7 from both sides of the given inequality yields 2x <= 12. Dividing both sides by 2 yields x <= 6, so the greatest possible value of x is 6. Distractors: 13 results from adding 7 instead of subtracting it, giving 2x <= 26; 2.5 results from dividing 19 by 2 before subtracting 7; -6 is a sign error.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x+7</code><br><code>y=19</code>

Click the intersection: (6, 19). To the left of x = 6 the line is below 19, so x ≤ 6 and the greatest value is 6. Two steps by hand are just as fast.

</details>

---

### 2. alg-ineq-collect-terms-easy

*Easy · Multiple choice · route: hand-primary · techniques: T1*

Which inequality is equivalent to $5x - 3 < 2x + 9$?

- **A.** $x < \frac{12}{7}$
- **B.** $x < 2$
- **C.** $x < 4$
- **D.** $x > 4$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Subtracting 2x from both sides of 5x - 3 < 2x + 9 yields 3x - 3 < 9. Adding 3 to both sides yields 3x < 12, and dividing both sides by the positive number 3 yields x < 4. Therefore, the given inequality is equivalent to x < 4. Distractors: x < 12/7 comes from adding 2x to both sides instead of subtracting it, which gives 7x < 12; x < 2 comes from subtracting 3 from 9 instead of adding it, which gives 3x < 6; x > 4 reverses the inequality sign, which is only needed when dividing by a negative number.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5x-3</code><br><code>y=2x+9</code>

The lines cross at (4, 17), and y = 5x - 3 is the lower graph to the left of x = 4, so x < 4. Desmos is slower here: two inverse operations solve it by hand, so use the graph only as a check.

</details>

---

### 3. alg-ineq-compound-middle-term

*Easy · Multiple choice · route: desmos-primary · techniques: T8*

Which of the following describes all solutions to the compound inequality $7 \le 4x - 5 < 19$?

- **A.** $\frac{1}{2} \le x < \frac{7}{2}$
- **B.** $3 \le x < 6$
- **C.** $3 < x \le 6$
- **D.** $3 \le x \le 6$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Adding 5 to all three parts of 7 <= 4x - 5 < 19 yields 12 <= 4x < 24. Dividing all three parts by 4 yields 3 <= x < 6. Therefore, the solutions are 3 <= x < 6. Distractors: 1/2 <= x < 7/2 comes from subtracting 5 from each outer part instead of adding it, which gives 2 <= 4x < 14; 3 < x <= 6 swaps which endpoint is included; 3 <= x <= 6 includes x = 6, although the right-hand inequality is strict.

**Desmos** (not yet verified in Desmos). Type:<br><code>7\le4x-5&lt;19</code>

Desmos shades a vertical strip between x = 3 and x = 6. The left edge is solid (x = 3 is included) and the right edge is dashed (x = 6 is not), so the solutions are 3 <= x < 6.

</details>

---

### 4. alg-ineq-dashed-boundary-shaded-below

*Easy · Multiple choice · route: either · techniques: T8*

In the $xy$-plane, the graph of an inequality consists of a dashed line with equation $y = 4x - 3$ and all points below that line. Which inequality does this graph represent?

- **A.** $y < 4x - 3$
- **B.** $y \le 4x - 3$
- **C.** $y > 4x - 3$
- **D.** $y \ge 4x - 3$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A dashed boundary line means the points on the line are not solutions, so the inequality is strict (< or >). Points below the line y = 4x - 3 have y-values less than 4x - 3. Therefore, the graph represents y < 4x - 3. Distractors: y <= 4x - 3 shades the correct side but would need a solid line; y > 4x - 3 shades above the line; y >= 4x - 3 shades above the line with a solid boundary.

**Desmos** (not yet verified in Desmos). Type:<br><code>y&lt;4x-3</code>

Type each choice in turn. y < 4x - 3 draws a dashed line and shades below it; the symbols <= and >= draw a solid line, and > and >= shade above. Reading the two rules by hand is just as fast.

</details>

---

### 5. alg-ineq-dashed-boundary-y-axis

*Easy · Multiple choice · route: either · techniques: T8*

The graph of $3x - 4y > 24$ in the $xy$-plane has a dashed boundary line. At which point does this boundary line intersect the $y$-axis?

- **A.** $(0, -6)$
- **B.** $(0, 6)$
- **C.** $(0, 8)$
- **D.** $(8, 0)$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The boundary line of the graph is 3x - 4y = 24. A point on the y-axis has x = 0. Substituting 0 for x yields -4y = 24, so y = -6. Therefore, the boundary line intersects the y-axis at (0, -6). Distractors: (0, 6) drops the negative sign of -4; (0, 8) divides 24 by the x-coefficient 3 instead of by -4; (8, 0) is where the boundary line intersects the x-axis.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x-4y&gt;24</code><br><code>3x-4y=24</code>

The first line shows the dashed boundary and its shading. Desmos may not label points on an inequality's boundary, so the second line draws the same line solid; click where it crosses the y-axis to read (0, -6). Substituting x = 0 by hand is just as fast.

</details>

---

### 6. alg-ineq-data-plan-music-hours

*Easy · Student-produced response · route: either · techniques: T1*

A phone plan includes 8 gigabytes of data per month. Streaming video uses 1.5 gigabytes per hour, and streaming music uses 0.1 gigabyte per hour. A customer streams 4 hours of video this month. What is the greatest number of hours of music the customer can stream without exceeding the plan's data?

**Answer:** 20

<details><summary>Solutions</summary>

**By hand.** Let m be the number of hours of music. The data used is 1.5(4) + 0.1m gigabytes, which must be at most 8: 1.5(4) + 0.1m <= 8. Simplifying yields 6 + 0.1m <= 8, so 0.1m <= 2 and m <= 20. Therefore, the customer can stream at most 20 hours of music. Forgetting the video data gives 8/0.1 = 80 hours.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=1.5\cdot4+0.1x</code><br><code>y=8</code>

The first line is the total data used with x hours of music. Click the intersection with y = 8 to read (20, 8); to the right of x = 20 the plan's data is exceeded. Solving by hand takes about as long.

</details>

---

### 7. alg-ineq-describe-graph-solid-above

*Easy · Multiple choice · route: desmos-primary · techniques: T8*

Which statement describes the graph of $y \ge -3x + 6$ in the $xy$-plane?

- **A.** The boundary line is dashed, and the region above it is shaded.
- **B.** The boundary line is dashed, and the region below it is shaded.
- **C.** The boundary line is solid, and the region above it is shaded.
- **D.** The boundary line is solid, and the region below it is shaded.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that y >= -3x + 6. The symbol >= includes equality, so points on the line y = -3x + 6 are solutions and the boundary line is solid. The y-values that are greater than -3x + 6 lie above the line, so the region above it is shaded. Therefore, the boundary line is solid and the region above it is shaded. Distractors: a dashed line with the region above shaded is the graph of y > -3x + 6; a dashed line with the region below shaded is the graph of y < -3x + 6; a solid line with the region below shaded is the graph of y <= -3x + 6, which reverses the direction.

**Desmos** (not yet verified in Desmos). Type:<br><code>y\ge-3x+6</code>

Desmos draws the boundary y = -3x + 6 as a solid line because the symbol includes equality, and it shades the side above the line (the shading contains (0, 10), for example).

</details>

---

### 8. alg-ineq-pin-length-tolerance

*Easy · Multiple choice · route: hand-primary · techniques: —*

A machine cuts metal pins. A pin is acceptable if its length is within 0.3 centimeter of 12 centimeters, inclusive. Which inequality gives all acceptable values of $L$, where $L$ is the length, in centimeters, of a pin?

- **A.** $11.4 \le L \le 12.6$
- **B.** $11.7 < L < 12.3$
- **C.** $11.7 \le L \le 12.3$
- **D.** $12 \le L \le 12.3$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A length within 0.3 centimeter of 12 centimeters is at least 12 - 0.3 = 11.7 centimeters and at most 12 + 0.3 = 12.3 centimeters. The word inclusive means both endpoints are acceptable. Therefore, the acceptable lengths satisfy 11.7 <= L <= 12.3. Distractors: 11.4 <= L <= 12.6 moves 0.6 centimeter from 12 in each direction, treating 0.3 as half of the allowed distance; 11.7 < L < 12.3 leaves out the endpoints even though they are included; 12 <= L <= 12.3 allows only pins longer than 12 centimeters.

</details>

---

### 9. alg-ineq-point-standard-form

*Easy · Multiple choice · route: either · techniques: T8*

Which ordered pair $(x, y)$ satisfies $4x - 3y \ge 12$?

- **A.** $(0, -3)$
- **B.** $(2, 5)$
- **C.** $(3, 1)$
- **D.** $(5, 2)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A point is a solution when substituting its coordinates makes the inequality true. For (5, 2): 4(5) - 3(2) = 20 - 6 = 14, and 14 >= 12 is true. Therefore, (5, 2) satisfies the inequality. Distractors: (0, -3) gives 0 + 9 = 9, which satisfies only the reversed inequality 4x - 3y <= 12; (2, 5) swaps the coordinates of the key and gives 8 - 15 = -7; (3, 1) gives 12 - 3 = 9 and is chosen when the sign of -3y is dropped, which gives 12 + 3 = 15.

**Desmos** (not yet verified in Desmos). Type:<br><code>4x-3y\ge12</code><br><code>(0,-3)</code><br><code>(2,5)</code><br><code>(3,1)</code><br><code>(5,2)</code>

Desmos shades the region on and below the solid line 4x - 3y = 12. Only (5, 2) lies in the shaded region. Substituting each point by hand is just as fast.

</details>

---

### 10. alg-ineq-swimmer-weekly-distance

*Easy · Multiple choice · route: hand-primary · techniques: —*

A swimmer has swum 1,200 meters so far this week and will swim 400 meters at each remaining practice. The swimmer's goal is at least 3,500 meters for the week. Which inequality represents this situation, where $p$ is the number of remaining practices?

- **A.** $400p + 1200 \ge 3500$
- **B.** $400p + 1200 \le 3500$
- **C.** $400p - 1200 \ge 3500$
- **D.** $1200p + 400 \ge 3500$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The swimmer swims 400 meters at each of p practices, which is 400p meters, in addition to the 1,200 meters already swum. The weekly total is 400p + 1200 meters, and 'at least 3,500' means the total is greater than or equal to 3,500. Therefore, 400p + 1200 >= 3500 represents the situation. Distractors: 400p + 1200 <= 3500 reads 'at least' as 'at most'; 400p - 1200 >= 3500 subtracts the distance already swum instead of adding it; 1200p + 400 >= 3500 swaps the per-practice distance and the distance already swum.

</details>

---

### 11. alg-ineq-which-value-solution

*Easy · Multiple choice · route: either · techniques: T8*

Which value of $x$ is a solution to the inequality $6x + 1 > 4x + 11$?

- **A.** $1$
- **B.** $3$
- **C.** $5$
- **D.** $7$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Subtracting 4x from both sides of 6x + 1 > 4x + 11 yields 2x + 1 > 11. Subtracting 1 from both sides yields 2x > 10, so x > 5. Of the choices, only 7 is greater than 5. Therefore, 7 is a solution. Distractors: 5 is the boundary value, which is excluded because the inequality is strict; 1 and 3 satisfy x < 5, the result of reversing the inequality sign.

**Desmos** (not yet verified in Desmos). Type:<br><code>6x+1&gt;4x+11</code>

Desmos shades the region to the right of a dashed vertical line at x = 5. The dashed line means x = 5 itself is not a solution, so of the choices only 7 lies in the shaded region.

</details>

---

### 12. alg-inequality-flip-sign-easy

*Easy · Multiple choice · route: either · techniques: T8*

Which inequality is equivalent to $-3x + 7 \ge 1$?

- **A.** $x \le -2$
- **B.** $x \le 2$
- **C.** $x \ge -2$
- **D.** $x \ge 2$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Subtracting 7 from both sides of -3x + 7 >= 1 yields -3x >= -6. Dividing both sides by -3 reverses the inequality symbol, yielding x <= 2. Distractors: x >= 2 divides by -3 without reversing the symbol; x <= -2 makes a sign error, treating -6 divided by -3 as -2, while reversing the symbol; x >= -2 makes the same sign error without reversing the symbol.

**Desmos** (not yet verified in Desmos). Type:<br><code>-3x+7\ge1</code>

Desmos shades the region x ≤ 2, with a solid boundary at x = 2. Two steps by hand are just as fast.

</details>

---

### 13. alg-point-satisfies-inequality

*Easy · Multiple choice · route: either · techniques: T8*

Which point $(x, y)$ is a solution to the inequality $y > 2x - 5$ in the $xy$-plane?

- **A.** $(1, -2)$
- **B.** $(2, -1)$
- **C.** $(3, 0)$
- **D.** $(4, 2)$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A point is a solution when its coordinates make the inequality true. For (1, -2): -2 > 2(1) - 5 = -3, which is true. Distractors: (2, -1) gives -1 > -1, false, because the point lies on the boundary line and the inequality is strict; (3, 0) gives 0 > 1, false; (4, 2) gives 2 > 3, false.

**Desmos** (not yet verified in Desmos). Type:<br><code>y&gt;2x-5</code><br><code>(1,-2)</code><br><code>(2,-1)</code><br><code>(3,0)</code><br><code>(4,2)</code>

Only (1, -2) lands in the shaded region. The boundary is dashed, so (2, -1), which lies on the line, is not a solution. Substituting by hand is as fast.

</details>

---

### 14. alg-elevator-crates-inequality

*Medium · Multiple choice · route: hand-primary · techniques: —*

A freight elevator can safely carry a total of at most 900 kilograms. A worker who weighs 80 kilograms will ride the elevator with some crates that each weigh 35 kilograms. Which inequality represents the possible values of $n$, where $n$ is the number of crates on the elevator?

- **A.** $35(n + 80) \le 900$
- **B.** $35n + 80 < 900$
- **C.** $35n + 80 \ge 900$
- **D.** $35n + 80 \le 900$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The total mass on the elevator is the worker's 80 kilograms plus 35 kilograms for each of the n crates, 35n + 80. 'At most 900' means the total is less than or equal to 900, so 35n + 80 <= 900. Distractors: 35n + 80 < 900 excludes a total of exactly 900, which 'at most' allows; 35n + 80 >= 900 reverses the direction of the inequality; 35(n + 80) <= 900 multiplies the worker's mass by the mass of a crate.

</details>

---

### 15. alg-fundraiser-tickets-inequality

*Medium · Multiple choice · route: hand-primary · techniques: —*

A fundraiser must raise at least 2,500 dollars from ticket sales. Raffle tickets cost 5 dollars each, and dinner tickets cost 40 dollars each. Which inequality represents the possible values of $r$ and $d$, where $r$ is the number of raffle tickets and $d$ is the number of dinner tickets sold?

- **A.** $5r + 40d \le 2,500$
- **B.** $5r + 40d \ge 2,500$
- **C.** $5r + 40d > 2,500$
- **D.** $40r + 5d \ge 2,500$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The r raffle tickets bring in 5r dollars and the d dinner tickets bring in 40d dollars, so ticket sales total 5r + 40d dollars. 'At least 2,500 dollars' means this total is greater than or equal to 2,500, so 5r + 40d >= 2,500. Distractors: 5r + 40d <= 2,500 reverses the direction, treating 2,500 as a maximum; 5r + 40d > 2,500 makes the inequality strict, which excludes raising exactly 2,500 dollars; 40r + 5d >= 2,500 swaps the two prices.

</details>

---

### 16. alg-garden-club-budget-inequality

*Medium · Multiple choice · route: hand-primary · techniques: —*

A garden club has at most 400 dollars to spend on soil and mulch. Soil costs 3 dollars per bag, and mulch costs 5 dollars per bag. Which inequality represents this situation, where $s$ is the number of bags of soil and $m$ is the number of bags of mulch the club buys?

- **A.** $3s + 5m < 400$
- **B.** $3s + 5m \le 400$
- **C.** $3s + 5m \ge 400$
- **D.** $5s + 3m \le 400$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The cost of s bags of soil is 3s dollars and the cost of m bags of mulch is 5m dollars, so the total cost is 3s + 5m dollars. 'At most 400' means the total can equal 400 but cannot exceed it, so 3s + 5m <= 400. Distractors: 3s + 5m < 400 excludes spending exactly 400 dollars, which 'at most' allows; 3s + 5m >= 400 reverses the direction of the inequality; 5s + 3m <= 400 swaps the prices of soil and mulch.

</details>

---

### 17. alg-greatest-integer-inequality

*Medium · Multiple choice · route: either · techniques: T1*

What is the greatest integer $x$ that satisfies the inequality $7 - 2x > 3x - 8$?

- **A.** $-1$
- **B.** $2$
- **C.** $3$
- **D.** $15$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Adding 2x to both sides of the given inequality yields 7 > 5x - 8. Adding 8 to both sides yields 15 > 5x, so x < 3. The greatest integer less than 3 is 2. Distractors: 3 treats the strict inequality as if x = 3 were allowed; 15 is the intermediate result before dividing by 5; -1 moves the -8 to the left side without changing its sign, giving 7 - 8 > 5x, so x < -1/5 and the greatest integer is -1.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=7-2x</code><br><code>y=3x-8</code>

The line y = 7 - 2x is above y = 3x - 8 to the left of their intersection at x = 3, so x < 3 and the greatest integer is 2.

</details>

---

### 18. alg-ineq-boundary-intercepts-constants

*Medium · Multiple choice · route: either · techniques: T8*

In the $xy$-plane, the graph of $ax + by < 12$, where $a$ and $b$ are constants, has a dashed boundary line that passes through $(4, 0)$ and $(0, -3)$. What is the value of $a + b$?

- **A.** $-7$
- **B.** $-1$
- **C.** $1$
- **D.** $7$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The boundary line is ax + by = 12. Substituting (4, 0) yields 4a = 12, so a = 3. Substituting (0, -3) yields -3b = 12, so b = -4. Therefore, a + b = 3 + (-4) = -1. Distractors: -7 makes both a and b negative; 1 uses the intercepts themselves, a = 4 and b = -3, as the coefficients; 7 drops the negative sign of b.

**Desmos** (not yet verified in Desmos). Type:<br><code>(4,0)</code><br><code>(0,-3)</code><br><code>3x-4y&lt;12</code>

Find a and b by substituting the two points (faster by hand), then type the inequality with them to confirm that the dashed boundary passes through both plotted points. With a = 3 and b = -4, a + b = -1.

</details>

---

### 19. alg-ineq-boundary-line-two-points

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

The solution set of an inequality in the $xy$-plane consists of all points on or above the line that passes through $(0, -2)$ and $(4, 4)$. Which inequality has this solution set?

- **A.** $y \ge \frac{2}{3}x - 2$
- **B.** $y \ge \frac{3}{2}x - 2$
- **C.** $y \le \frac{3}{2}x - 2$
- **D.** $y \ge \frac{3}{2}x + 2$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The slope of the line through (0, -2) and (4, 4) is (4 - (-2))/(4 - 0) = 6/4 = 3/2, and its y-intercept is -2, so the line is y = (3/2)x - 2. Points on or above the line have y-values greater than or equal to (3/2)x - 2. Therefore, the inequality is y >= (3/2)x - 2. Distractors: y >= (2/3)x - 2 inverts the slope, dividing the change in x by the change in y; y <= (3/2)x - 2 describes points on or below the line; y >= (3/2)x + 2 uses the wrong sign for the y-intercept.

**Desmos** (not yet verified in Desmos). Type:<br><code>(0,-2)</code><br><code>(4,4)</code><br><code>y\ge\frac{3}{2}x-2</code>

Plot the two points, then type each choice in turn. Keep the choice whose solid boundary passes through both points and whose shading is above the line: y >= (3/2)x - 2.

</details>

---

### 20. alg-ineq-compound-two-constants-sum

*Medium · Student-produced response · route: hand-primary · techniques: —*

The solution set of the inequality $a \le 3x - 6 \le b$, where $a$ and $b$ are constants, is $2 \le x \le 9$. What is the value of $a + b$?

**Answer:** 21

<details><summary>Solutions</summary>

**By hand.** It's given that the solution set is 2 <= x <= 9. Multiplying all three parts by 3 yields 6 <= 3x <= 27, and subtracting 6 yields 0 <= 3x - 6 <= 21. So the smallest value of 3x - 6 is a = 0 and the largest is b = 21. Therefore, a + b = 0 + 21 = 21. Alternate approach: the endpoints of the solution set make 3x - 6 equal to a and b, so a = 3(2) - 6 = 0 and b = 3(9) - 6 = 21. Adding 6 instead of subtracting gives a + b = 45.

</details>

---

### 21. alg-ineq-count-integers-chain

*Medium · Multiple choice · route: either · techniques: T1*

How many integers $x$ satisfy $3(x - 2) \le 5x + 4 < 2x + 34$?

- **A.** $13$
- **B.** $14$
- **C.** $15$
- **D.** $16$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The compound inequality holds when both parts hold. From 3(x - 2) <= 5x + 4: 3x - 6 <= 5x + 4 yields -10 <= 2x, so x >= -5. From 5x + 4 < 2x + 34: 3x < 30, so x < 10. The integers with -5 <= x < 10 are -5, -4, ..., 9, which is 9 - (-5) + 1 = 15 integers. Therefore, 15 integers satisfy the inequality. Distractors: 13 comes from distributing 3(x - 2) as 3x - 2, which gives x >= -3 and the integers -3 through 9; 14 leaves out x = -5, although the left part is not strict; 16 includes x = 10, although the right part is strict.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3(x-2)</code><br><code>y=5x+4</code><br><code>y=2x+34</code>

y = 3(x - 2) and y = 5x + 4 cross at x = -5, and y = 5x + 4 and y = 2x + 34 cross at x = 10. Check which side each condition holds on: x >= -5 (included) and x < 10 (excluded). Count the integers -5 through 9 by hand.

</details>

---

### 22. alg-ineq-count-listed-points-system

*Medium · Student-produced response · route: desmos-primary · techniques: T8*

Four points in the $xy$-plane are $(1, -5)$, $(0, 3)$, $(2, 2)$, and $(3, 2)$. How many of these four points are solutions to the system of inequalities $y > 3x - 8$ and $x + 2y < 7$?

**Answer:** 2

<details><summary>Solutions</summary>

**By hand.** A point is a solution to the system when it satisfies both inequalities. (1, -5): 3(1) - 8 = -5, and -5 > -5 is false. (0, 3): 3 > -8 is true and 0 + 6 = 6 < 7 is true. (2, 2): 2 > -2 is true and 2 + 4 = 6 < 7 is true. (3, 2): 2 > 1 is true, but 3 + 4 = 7 < 7 is false. Therefore, 2 of the points are solutions. Counting either boundary point as a solution gives 3; both inequalities are strict, so boundary points are excluded.

**Desmos** (not yet verified in Desmos). Type:<br><code>y&gt;3x-8</code><br><code>x+2y&lt;7</code><br><code>(1,-5)</code><br><code>(0,3)</code><br><code>(2,2)</code><br><code>(3,2)</code>

Count the points inside the darker overlap. (0, 3) and (2, 2) are inside. (1, -5) sits on the dashed line y = 3x - 8 and (3, 2) sits on the dashed line x + 2y = 7; zoom in to see that they are on the boundaries, which are excluded. The answer is 2.

</details>

---

### 23. alg-ineq-day-camp-staff-system

*Medium · Multiple choice · route: hand-primary · techniques: —*

A day camp needs at least 8 staff members. Counselors are paid 100 dollars per day, lifeguards 120 dollars per day, and the daily staff budget is at most 960 dollars. Which system represents this situation, where $c$ is the number of counselors and $g$ is the number of lifeguards?

- **A.** $c + g \le 8$ and $100c + 120g \ge 960$
- **B.** $100c + 120g \ge 8$ and $c + g \le 960$
- **C.** $c + g \ge 8$ and $120c + 100g \le 960$
- **D.** $c + g \ge 8$ and $100c + 120g \le 960$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The number of staff members is c + g, and at least 8 are needed, so c + g >= 8. Counselors cost 100 dollars each and lifeguards 120 dollars each, so the daily cost is 100c + 120g, and at most 960 dollars may be spent, so 100c + 120g <= 960. Therefore, the system is c + g >= 8 and 100c + 120g <= 960. Distractors: c + g <= 8 and 100c + 120g >= 960 reverses both directions, reading at least as at most and at most as at least; 100c + 120g >= 8 and c + g <= 960 pairs each limit with the wrong quantity; c + g >= 8 and 120c + 100g <= 960 attaches each pay rate to the wrong job.

</details>

---

### 24. alg-ineq-farm-stand-revenue-point

*Medium · Multiple choice · route: desmos-primary · techniques: T8*

A farm stand's goal is at least 1,800.00 dollars in sales this week. Melons sell for 6.00 dollars each and baskets of berries for 14.00 dollars each. Which ordered pair $(m, b)$, where $m$ is the number of melons and $b$ is the number of baskets sold, meets the goal?

- **A.** $(60, 105)$
- **B.** $(100, 50)$
- **C.** $(140, 40)$
- **D.** $(150, 60)$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The sales are 6m + 14b dollars, so the goal is 6m + 14b >= 1800. For (60, 105): 6(60) + 14(105) = 360 + 1470 = 1830, and 1830 >= 1800 is true. Therefore, (60, 105) meets the goal. Distractors: (150, 60) gives 900 + 840 = 1740 and is chosen when the prices are swapped, since 14(150) + 6(60) = 2460; (140, 40) gives 840 + 560 = 1400 and is chosen when both prices are averaged to 10.00 dollars, since 140 + 40 = 180 items at 10 dollars is 1,800; (100, 50) gives 600 + 700 = 1300 and satisfies only the reversed inequality 6m + 14b <= 1800.

**Desmos** (not yet verified in Desmos). Type:<br><code>6x+14y\ge1800</code><br><code>(60,105)</code><br><code>(100,50)</code><br><code>(140,40)</code><br><code>(150,60)</code>

Here x stands for m and y for b. Only (60, 105) lies in the shaded region on or above the line 6x + 14y = 1800; zoom out first, since the line crosses the axes at (300, 0) and about (0, 128.6).

</details>

---

### 25. alg-ineq-ferry-trucks

*Medium · Student-produced response · route: either · techniques: T1*

A ferry deck has 136 units of parking space. Each car uses 2 units and each truck uses 5 units. On one trip, the ferry carries 30 cars. What is the greatest number of trucks the ferry can also carry on this trip?

**Answer:** 15

<details><summary>Solutions</summary>

**By hand.** The 30 cars use 2(30) = 60 units, and t trucks use 5t units, so the space constraint is 60 + 5t <= 136. Subtracting 60 from both sides yields 5t <= 76, so t <= 15.2. The number of trucks is a whole number, so the greatest possible value is 15. Therefore, the ferry can also carry at most 15 trucks. Rounding 15.2 up to 16 would exceed the available space, since 60 + 5(16) = 140.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2\cdot30+5x</code><br><code>y=136</code>

The lines cross at x = 15.2. The number of trucks must be a whole number no greater than 15.2, so the answer is 15. The hand solution is about as fast.

</details>

---

### 26. alg-ineq-fractions-equivalent

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

Which inequality is equivalent to $\frac{x}{3} - 2 \ge \frac{x + 1}{2}$?

- **A.** $x \le -15$
- **B.** $x \le -13$
- **C.** $x \le -5$
- **D.** $x \ge -15$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of x/3 - 2 >= (x + 1)/2 by 6 yields 2x - 12 >= 3(x + 1), or 2x - 12 >= 3x + 3. Subtracting 3x from both sides and adding 12 yields -x >= 15. Multiplying by -1 reverses the inequality: x <= -15. Therefore, the inequality is equivalent to x <= -15. Distractors: x <= -13 comes from writing 3(x + 1) as 3x + 1; x <= -5 comes from not multiplying the -2 by 6, which gives 2x - 2 >= 3x + 3; x >= -15 forgets to reverse the inequality when multiplying by -1.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x}{3}-2</code><br><code>y=\frac{x+1}{2}</code>

The lines cross at (-15, -7). To the left of x = -15 the graph of y = x/3 - 2 is above the other line (at x = -18 it is -8 versus -8.5), so the solution is x <= -15, with x = -15 included because the inequality is not strict.

</details>

---

### 27. alg-ineq-function-values-compare

*Medium · Multiple choice · route: desmos-primary · techniques: T9, T1*

If $f(x) = 3x - 8$ and $g(x) = 12 - x$, which inequality gives all values of $x$ for which $f(x) > g(x)$?

- **A.** $x > 1$
- **B.** $x < 5$
- **C.** $x > 5$
- **D.** $x > 10$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The condition is 3x - 8 > 12 - x. Adding x to both sides yields 4x - 8 > 12, adding 8 yields 4x > 20, and dividing by 4 yields x > 5. Therefore, f(x) > g(x) for x > 5. Distractors: x > 1 comes from 4x > 4, moving -8 to the right side as -8 instead of +8; x < 5 reverses the direction, which is not needed when dividing by a positive number; x > 10 comes from 2x > 20, subtracting x instead of adding it.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=3x-8</code><br><code>g(x)=12-x</code>

Click the intersection of the two lines to read (5, 7). To the right of x = 5 the graph of f is above the graph of g (check f(6) = 10 and g(6) = 6 on new lines), so f(x) > g(x) for x > 5.

</details>

---

### 28. alg-ineq-gym-plans-months

*Medium · Student-produced response · route: desmos-primary · techniques: T1*

One gym charges a 40.00 dollar joining fee plus 25.00 dollars per month. A second gym charges no joining fee and 32.00 dollars per month. What is the least whole number of months for which the total cost at the first gym is less than at the second gym?

**Answer:** 6

<details><summary>Solutions</summary>

**By hand.** After m months the first gym costs 40 + 25m dollars and the second costs 32m dollars. The first is less when 40 + 25m < 32m. Subtracting 25m from both sides yields 40 < 7m, so m > 40/7, which is about 5.71. The least whole number greater than 40/7 is 6. Check: after 6 months the costs are 190 and 192 dollars; after 5 months they are 165 and 160 dollars. Therefore, the answer is 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=40+25x</code><br><code>y=32x</code>

The lines cross at about (5.714, 182.857). To the right of the crossing the first gym's line is lower, so the first gym costs less when x > 5.714; the least whole number of months is 6.

</details>

---

### 29. alg-ineq-intercepts-solid-above

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

In the $xy$-plane, the graph of an inequality is made up of a solid line that crosses the $x$-axis at $(6, 0)$ and the $y$-axis at $(0, -4)$, together with every point above that line. Which of the following inequalities has this graph?

- **A.** $2x - 3y < 12$
- **B.** $2x - 3y \le 12$
- **C.** $2x - 3y \ge 12$
- **D.** $3x - 2y \le 12$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The line through (6, 0) and (0, -4) is x/6 - y/4 = 1; multiplying by 12 yields 2x - 3y = 12. The line is solid, so the inequality includes equality. The origin (0, 0) is above the line, since the line's y-intercept is -4, and substituting it yields 0 <= 12, so the shaded side satisfies 2x - 3y <= 12. Therefore, the graph is 2x - 3y <= 12. Distractors: 2x - 3y < 12 needs a dashed line; 2x - 3y >= 12 is the region below the line, because solving for y reverses the sign; 3x - 2y <= 12 swaps the intercepts and has intercepts (4, 0) and (0, -6).

**Desmos** (not yet verified in Desmos). Type:<br><code>(6,0)</code><br><code>(0,-4)</code><br><code>2x-3y\le12</code>

Plot the two intercepts, then type each choice in turn. Keep the one whose solid boundary passes through both points and whose shading is above the line: 2x - 3y <= 12. The < choice has a dashed line, the >= choice shades below, and 3x - 2y <= 12 misses both points.

</details>

---

### 30. alg-ineq-least-integer-fraction-flip

*Medium · Student-produced response · route: hand-primary · techniques: T1*

What is the smallest integer solution to $5 - \frac{2}{3}x < 1$?

**Answer:** 7

<details><summary>Solutions</summary>

**By hand.** Subtracting 5 from both sides of 5 - (2/3)x < 1 yields -(2/3)x < -4. Multiplying both sides by -3/2 reverses the inequality and yields x > 6. The value 6 itself is not a solution because the inequality is strict, so the smallest integer solution is 7. Therefore, the answer is 7.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5-\frac{2}{3}x</code><br><code>y=1</code>

The line crosses y = 1 at (6, 1) and is below it to the right, so x > 6 and the smallest integer is 7. Desmos is slower than the two-step hand solution; use it as a check that the inequality points right.

</details>

---

### 31. alg-ineq-press-time-coefficient

*Medium · Multiple choice · route: hand-primary · techniques: —*

A print shop has at most 8 hours of press time per day. In the inequality $0.4b + 0.25f \le 8$, $b$ is the number of batches of booklets and $f$ is the number of batches of flyers printed in a day. What is the best interpretation of $0.4$ in this context?

- **A.** Each batch of booklets uses 0.4 hour of press time.
- **B.** Each batch of flyers uses 0.4 hour of press time.
- **C.** The shop prints 0.4 batch of booklets per hour.
- **D.** The shop has at most 0.4 hour of press time per day.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that 0.4b + 0.25f is the total press time, in hours, and that b is the number of batches of booklets. The term 0.4b is the press time for b batches of booklets, so each batch of booklets uses 0.4 hour of press time. Therefore, 0.4 is the press time, in hours, for one batch of booklets. Distractors: 'each batch of flyers uses 0.4 hour' attaches the coefficient to the wrong variable (flyers take 0.25 hour per batch); '0.4 batch of booklets per hour' inverts the rate, since the shop prints 1/0.4 = 2.5 batches per hour; 'at most 0.4 hour of press time' confuses the coefficient with the limit, which is 8 hours.

</details>

---

### 32. alg-ineq-rain-barrel-solution

*Medium · Multiple choice · route: either · techniques: T1*

A full rain barrel holds 480 liters of water and drains at 15 liters per minute. The inequality $480 - 15t \ge 120$ holds when at least 120 liters remain, where $t$ is the number of minutes since draining began. Which statement describes the solution to the inequality?

- **A.** At least 120 liters remain during the first 8 minutes of draining.
- **B.** At least 120 liters remain during the first 24 minutes of draining.
- **C.** At least 120 liters remain during the first 32 minutes of draining.
- **D.** At least 120 liters remain during the first 40 minutes of draining.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Subtracting 480 from both sides of 480 - 15t >= 120 yields -15t >= -360. Dividing both sides by -15 reverses the inequality and yields t <= 24. Therefore, at least 120 liters remain during the first 24 minutes of draining. Distractors: 8 minutes is 120/15, which divides the remaining amount by the rate; 32 minutes is 480/15, the time for the barrel to empty completely; 40 minutes is (480 + 120)/15, which adds 120 instead of subtracting it.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=480-15x</code><br><code>y=120</code>

The lines cross at (24, 120), and the draining line is above y = 120 to the left of x = 24, so t <= 24. Solving by hand takes two steps and is equally quick.

</details>

---

### 33. alg-ineq-recycling-credits-point-outside

*Medium · Multiple choice · route: hand-primary · techniques: —*

A school earns 2 credits per bag of cans and 5 credits per bag of glass it recycles. Its goal is $2a + 5g \ge 150$, where $a$ and $g$ are the numbers of bags of cans and of glass, respectively. The point $(30, 15)$ is not in the solution set. Which statement is the best interpretation of this fact?

- **A.** Recycling 15 bags of cans and 30 bags of glass earns fewer than 150 credits.
- **B.** Recycling 30 bags of cans and 15 bags of glass earns fewer than 150 credits.
- **C.** Recycling 30 bags of cans and 15 bags of glass earns exactly 150 credits.
- **D.** Recycling 30 bags of cans and 15 bags of glass earns more than 150 credits.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The point (30, 15) means a = 30 bags of cans and g = 15 bags of glass. Substituting yields 2(30) + 5(15) = 60 + 75 = 135 credits. A point is outside the solution set exactly when it fails the inequality, so 135 < 150 and the goal is not met. Therefore, recycling 30 bags of cans and 15 bags of glass earns fewer than 150 credits. Distractors: the statement about 15 bags of cans and 30 bags of glass swaps the coordinates, and that combination earns 180 credits; exactly 150 credits would put the point on the boundary, which is in the solution set; more than 150 credits would also put the point in the solution set.

</details>

---

### 34. alg-ineq-region-greatest-y

*Medium · Multiple choice · route: desmos-primary · techniques: T8*

In the $xy$-plane, a point $(x, y)$ satisfies both $x + y \le 10$ and $y \le 2x + 1$. What is the greatest possible value of $y$?

- **A.** $1$
- **B.** $3$
- **C.** $7$
- **D.** $10$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The first inequality is y <= 10 - x, so y must be at most both 10 - x and 2x + 1. The first bound decreases as x increases and the second increases, so the greatest possible y occurs where they are equal: 10 - x = 2x + 1 yields x = 3 and y = 7. Every other x makes one of the two bounds less than 7. Therefore, the greatest possible value of y is 7. Distractors: 1 is the y-intercept of y = 2x + 1; 3 is the x-coordinate of the corner rather than the y-coordinate; 10 ignores y <= 2x + 1, which allows only y <= 1 when x = 0.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y\le10</code><br><code>y\le2x+1</code>

The overlap is the region below both lines, and its highest point is the corner where the boundary lines cross. Click that intersection to read (3, 7); the greatest y-value is 7, not the x-coordinate 3.

</details>

---

### 35. alg-ineq-shifted-compound-same-set

*Medium · Multiple choice · route: either · techniques: T13*

Which inequality has the same solution set as $-4 \le x \le 10$?

- **A.** $-7 \le x - 3 \le 7$
- **B.** $-7 \le x + 3 \le 7$
- **C.** $-4 \le x - 3 \le 10$
- **D.** $-1 \le x - 3 \le 13$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Subtracting 3 from all three parts of -4 <= x <= 10 yields -4 - 3 <= x - 3 <= 10 - 3, or -7 <= x - 3 <= 7. Inequalities that are equivalent have the same solution set. Therefore, -7 <= x - 3 <= 7 has the same solution set. This form says x is within 7 of 3, the midpoint of -4 and 10. Distractors: -7 <= x + 3 <= 7 shifts in the wrong direction and gives -10 <= x <= 4; -4 <= x - 3 <= 10 changes the middle without changing the bounds and gives -1 <= x <= 13; -1 <= x - 3 <= 13 adds 3 to the bounds while subtracting 3 in the middle and gives 2 <= x <= 16.

**Desmos** (not yet verified in Desmos). Type:<br><code>-4\le x\le10</code><br><code>-7\le x-3\le7</code>

The first line shades the vertical band from x = -4 to x = 10. Type each choice on the next line; only -7 <= x - 3 <= 7 shades exactly the same band. Subtracting 3 from each part by hand is just as quick.

</details>

---

### 36. alg-ineq-table-boundary-least-k

*Medium · Student-produced response · route: hand-primary · techniques: —*

For the inequality $y > mx + b$, where $m$ and $b$ are constants, a table gives three points $(x, y)$ on the boundary line in the $xy$-plane: $(-1, 7)$, $(2, 1)$, and $(4, -3)$. The point $(0, k)$ is a solution to the inequality. What is the least possible integer value of $k$?

**Answer:** 6

<details><summary>Solutions</summary>

**By hand.** The slope of the boundary line is (1 - 7)/(2 - (-1)) = -6/3 = -2, and (4, -3) gives the same slope from (2, 1): (-3 - 1)/(4 - 2) = -2. Moving from x = -1 to x = 0 changes y by -2, so the y-intercept is b = 7 - 2 = 5 and the boundary is y = -2x + 5. Substituting (0, k) into y > -2x + 5 yields k > 5. Therefore, the least integer value of k is 6. Answering 5 ignores that the inequality is strict.

</details>

---

### 37. alg-ineq-tank-heater-hours

*Medium · Multiple choice · route: either · techniques: T1*

A heater warms the water in a fish tank from 14 degrees Celsius at 2 degrees Celsius per hour. The fish need water from 22 to 28 degrees Celsius, inclusive. Which inequality gives all values of $h$ that meet this need, where $h$ is the number of hours of heating?

- **A.** $4 < h < 7$
- **B.** $4 \le h \le 7$
- **C.** $8 \le h \le 14$
- **D.** $11 \le h \le 14$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** After h hours the temperature is 14 + 2h degrees Celsius. The need is 22 <= 14 + 2h <= 28. Subtracting 14 from all three parts yields 8 <= 2h <= 14, and dividing by 2 yields 4 <= h <= 7. Therefore, the water meets the need for 4 <= h <= 7. Distractors: 4 < h < 7 drops the endpoints even though the range is inclusive; 8 <= h <= 14 stops before dividing by the rate of 2 degrees per hour; 11 <= h <= 14 divides 22 and 28 by 2 without first subtracting the starting temperature.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=14+2x</code><br><code>y=22</code><br><code>y=28</code>

The temperature line meets y = 22 at (4, 22) and y = 28 at (7, 28). Between x = 4 and x = 7, including both, the line lies in the required band, so 4 <= h <= 7. Solving the compound inequality by hand takes about as long.

</details>

---

### 38. alg-inequality-bound-c

*Medium · Student-produced response · route: desmos-primary · techniques: T1*

The solution set of the inequality $\frac{2x - 1}{3} + 2 \le \frac{x}{2} + 4$ is $x \le c$, where $c$ is a constant. What is the value of $c$?

**Answer:** 14

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the given inequality by 6 yields 2(2x - 1) + 12 <= 3x + 24, which simplifies to 4x + 10 <= 3x + 24. Subtracting 3x and 10 from both sides yields x <= 14. Therefore, c = 14.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{2x-1}{3}+2</code><br><code>y=\frac{x}{2}+4</code>

Click the intersection: (14, 11). To the left of x = 14 the first line is below the second, and at x = 14 they are equal, so the solution set is x ≤ 14 and c = 14.

</details>

---

### 39. alg-inequality-integer-a

*Medium · Multiple choice · route: desmos-primary · techniques: T8*

The point $(a, 5)$ satisfies both $y > 3x - 7$ and $y \leq -x + 9$ in the $xy$-plane. What is the greatest possible integer value of $a$?

- **A.** $-1$
- **B.** $1$
- **C.** $3$
- **D.** $4$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Substitute y = 5. From 5 > 3a - 7, a < 4. From 5 ≤ -a + 9, a ≤ 4. Both hold when a < 4, so the greatest integer is 3. Distractors: 4 treats the strict inequality a < 4 as inclusive; 1 drops the -7, so 5 > 3a gives a < 5/3; -1 turns -7 into +7, so 5 > 3a + 7 gives a < -2/3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y&gt;3x-7</code><br><code>y\le-x+9</code><br><code>y=5</code><br><code>(4,5)</code>

Along y = 5 the doubly shaded region ends at x = 4. The boundary of y > 3x - 7 is dashed, so (4, 5) is excluded and the greatest integer is 3.

</details>

---

### 40. alg-point-system-inequalities-count-k

*Medium · Multiple choice · route: desmos-primary · techniques: T8*

In the $xy$-plane, the point $(3, k)$, where $k$ is an integer, satisfies both $y < 2x + 1$ and $y > -x + 2$. How many possible values of $k$ are there?

- **A.** $6$
- **B.** $7$
- **C.** $8$
- **D.** $9$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting 3 for x and k for y in the two inequalities yields k < 2(3) + 1 = 7 and k > -3 + 2 = -1. So -1 < k < 7, and since k is an integer, k can be 0, 1, 2, 3, 4, 5, or 6, which is 7 values. Distractors: 8 is the width 7 - (-1) of the interval, which counts the endpoints as if one were included; 9 includes both endpoints -1 and 7, but both inequalities are strict; 6 forgets that 0 is an integer in the range.

**Desmos** (not yet verified in Desmos). Type:<br><code>y&lt;2x+1</code><br><code>y&gt;-x+2</code><br><code>x=3</code>

Along the vertical line x = 3, the darker overlap runs from y = -1 up to y = 7, and both boundaries are dashed, so neither endpoint counts. The integers strictly between -1 and 7 are 0 through 6: seven values.

</details>

---

### 41. alg-point-x5-y-range

*Medium · Multiple choice · route: either · techniques: T8*

The ordered pair $(5, y)$ satisfies the inequality $3x - 2y < 7$. Which of the following must be true?

- **A.** $y < -4$
- **B.** $y < 4$
- **C.** $y > -4$
- **D.** $y > 4$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Substituting 5 for x in 3x - 2y < 7 yields 15 - 2y < 7. Subtracting 15 from both sides yields -2y < -8, and dividing both sides by -2 reverses the inequality symbol, yielding y > 4. Distractors: y < 4 divides by -2 without reversing the symbol; y > -4 and y < -4 make a sign error, treating -8 divided by -2 as -4, with and without reversing the symbol.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x-2y&lt;7</code><br><code>x=5</code>

Along the line x = 5, the shaded region lies above y = 4, and the boundary is dashed, so y > 4. Substituting x = 5 by hand is as fast.

</details>

---

### 42. alg-compound-inequality-flip

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

Which of the following gives all values of $x$ that satisfy $-4 < 3 - 2x \le 9$?

- **A.** $-3 \le x < 3.5$
- **B.** $-3 < x \le 3.5$
- **C.** $-3.5 \le x < 3$
- **D.** $-3.5 < x \le 3$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Subtracting 3 from each part of the given inequality yields -7 < -2x <= 6. Dividing each part by -2 reverses both inequality symbols, yielding 3.5 > x >= -3, which is the same as -3 <= x < 3.5. Distractors: -3 < x <= 3.5 keeps the symbols in their original places instead of reversing them when dividing by a negative number; -3.5 < x <= 3 divides by 2 instead of -2, a sign error on both endpoints; -3.5 <= x < 3 makes the sign error and also attaches the wrong symbol to each endpoint.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3-2x</code><br><code>y=-4</code><br><code>y=9</code>

The line y = 3 - 2x meets y = 9 at x = -3 and y = -4 at x = 3.5. Between those x-values the line lies between the two horizontal lines. The value 9 is allowed (≤), so x = -3 is included; the value -4 is not (<), so x = 3.5 is excluded: -3 ≤ x < 3.5.

</details>

---

### 43. alg-count-integers-two-inequalities

*Hard · Student-produced response · route: either · techniques: T1*

How many integers $x$ satisfy both $2x + 5 > -9$ and $4 - x \ge -3$?

**Answer:** 14

<details><summary>Solutions</summary>

**By hand.** From 2x + 5 > -9, subtracting 5 yields 2x > -14, so x > -7. From 4 - x >= -3, subtracting 4 yields -x >= -7, and dividing by -1 reverses the inequality: x <= 7. The integers x with -7 < x <= 7 are -6, -5, ..., 7, which is 7 - (-6) + 1 = 14 integers.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x+5</code><br><code>y=-9</code><br><code>y=4-x</code><br><code>y=-3</code>

The first pair of lines crosses at x = -7 and the second at x = 7, so the integers are -6 through 7: 14 of them. Solving each inequality by hand is as fast; the common slip is forgetting to reverse the inequality when dividing by -1.

</details>

---

### 44. alg-craft-fair-mugs-least

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

A potter pays 350 dollars to rent a booth at a craft fair and sells mugs for 12 dollars each. Each mug costs the potter 4.50 dollars to make. What is the least number of mugs the potter must sell for the profit from the fair to be at least 200 dollars?

- **A.** $20$
- **B.** $46$
- **C.** $73$
- **D.** $74$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Let n be the number of mugs sold. Each mug brings in 12 dollars and costs 4.50 dollars to make, so the profit, in dollars, is 12n - 4.5n - 350 = 7.5n - 350. 'At least 200 dollars' means 7.5n - 350 >= 200, so 7.5n >= 550 and n >= 550/7.5, which is about 73.33. The least whole number of mugs satisfying this is 74. Distractors: 73 rounds 73.33 down, but 7.5(73) - 350 = 197.5, which is less than 200; 46 ignores the 4.50-dollar cost of each mug and solves 12n - 350 >= 200; 20 subtracts the 200-dollar target from the rent instead of adding it, solving 7.5n >= 150.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=12x-4.5x-350</code><br><code>y=200</code>

Click the intersection: x is about 73.33. Profit rises with x, so the profit is at least 200 for x ≥ 73.33, and the least whole number of mugs is 74. Zoom out to see the point.

</details>

---

### 45. alg-fraction-inequality-k-bound

*Hard · Multiple choice · route: either · techniques: T4, T1*

The solution set of the inequality $\frac{x - k}{2} > \frac{x}{3} + 1$, where $k$ is a constant, is $x > 15$. What is the value of $k$?

- **A.** $-3$
- **B.** $3$
- **C.** $\frac{14}{3}$
- **D.** $9$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the given inequality by 6 yields 3(x - k) > 2x + 6, which simplifies to 3x - 3k > 2x + 6. Subtracting 2x from both sides and adding 3k to both sides yields x > 3k + 6. It's given that the solution set is x > 15, so 3k + 6 = 15 and k = 3. Distractors: -3 results from a sign error that gives x > 6 - 3k; 14/3 results from multiplying the 1 by 1 instead of by 6, giving x > 3k + 1; 9 results from not distributing the 3 over -k, giving 3x - k > 2x + 6 and x > k + 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x-k}{2}</code><br><code>y=\frac{x}{3}+1</code>

Add a slider for k and drag it until the two lines cross at x = 15; that happens at k = 3. To the right of the crossing the first line is higher, matching x > 15. Clearing the fractions by hand gives the exact value directly.

</details>

---

### 46. alg-ineq-bakery-greatest-batches

*Hard · Student-produced response · route: desmos-primary · techniques: T8*

Each week a bakery has at most 30 hours of oven time and 48 kilograms of flour for bread and cakes. A batch of bread uses 2 hours and 4 kilograms; a batch of cakes uses 3 hours and 3 kilograms. What is the greatest total number of batches the bakery can make in a week?

**Answer:** 13

<details><summary>Solutions</summary>

**By hand.** Let x be the number of batches of bread and y the number of batches of cakes. The constraints are 2x + 3y <= 30 (oven hours) and 4x + 3y <= 48 (flour), with x >= 0 and y >= 0. The greatest value of x + y on this region occurs at a corner. Subtracting the first boundary equation from the second yields 2x = 18, so x = 9 and y = 4, for a total of 13. The corner (12, 0) gives 12 and (0, 10) gives 10. Therefore, the greatest total is 13 batches. Using only the flour limit with all bread gives 12; using only the oven limit with all cakes gives 10.

**Desmos** (not yet verified in Desmos). Type:<br><code>2x+3y\le30</code><br><code>4x+3y\le48</code><br><code>x\ge0</code><br><code>y\ge0</code>

Here x is batches of bread and y batches of cakes. The overlap is a four-sided region; click the corner where the two slanted lines cross to read (9, 4), for 13 batches. The other corners give (12, 0) for 12 and (0, 10) for 10, so 13 is the greatest.

</details>

---

### 47. alg-ineq-candy-temperature-count

*Hard · Student-produced response · route: either · techniques: T1*

A candy mixture must be heated to a temperature from 112 to 116 degrees Celsius, inclusive. A temperature of $F$ degrees Fahrenheit equals $\frac{5}{9}(F - 32)$ degrees Celsius. How many integer temperatures, in degrees Fahrenheit, meet this requirement?

**Answer:** 7

<details><summary>Solutions</summary>

**By hand.** The requirement is 112 <= (5/9)(F - 32) <= 116. Multiplying all three parts by 9/5 yields 201.6 <= F - 32 <= 208.8, and adding 32 yields 233.6 <= F <= 240.8. The integers in this interval are 234, 235, ..., 240, which is 240 - 234 + 1 = 7 integers. Therefore, 7 integer Fahrenheit temperatures meet the requirement. Rounding the endpoints to 233 and 241 and counting them would give 9, but both lie outside the interval.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{5}{9}(x-32)</code><br><code>y=112</code><br><code>y=116</code>

The line crosses y = 112 at x = 233.6 and y = 116 at x = 240.8; zoom to that window. The integers from 234 through 240 lie between, which is 7 temperatures. The hand route is about as fast.

</details>

---

### 48. alg-ineq-difference-bounds

*Hard · Multiple choice · route: hand-primary · techniques: —*

If $x \ge 3$ and $y \le -2$, which inequality must be true?

- **A.** $x - y \le 1$
- **B.** $x - y \le 5$
- **C.** $x - y > 5$
- **D.** $x - y \ge 5$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that y <= -2. Multiplying both sides by -1 reverses the inequality: -y >= 2. Adding this to x >= 3, two inequalities in the same direction, yields x - y >= 5. Therefore, x - y >= 5 must be true. Distractors: x - y <= 1 adds the bounds 3 + (-2) without negating y and also reverses the direction; x - y <= 5 is false for x = 10 and y = -2, where x - y = 12; x - y > 5 is false for x = 3 and y = -2, where x - y = 5 exactly.

</details>

---

### 49. alg-ineq-every-x-solution-k

*Hard · Multiple choice · route: hand-primary · techniques: —*

Every real number $x$ is a solution to the inequality $3(2x - k) \le 6x + 12$, where $k$ is a constant. Which inequality gives all possible values of $k$?

- **A.** $k \le -4$
- **B.** $k \ge -4$
- **C.** $k \le 4$
- **D.** $k \ge 4$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Distributing yields 6x - 3k <= 6x + 12. Subtracting 6x from both sides yields -3k <= 12, a statement with no x. If it is true, every real number x is a solution; if it is false, no x is. Dividing -3k <= 12 by -3 reverses the inequality and yields k >= -4. Therefore, all possible values of k are given by k >= -4. Distractors: k <= -4 forgets to reverse the inequality when dividing by -3; k <= 4 drops the negative sign on -3k, which gives 3k <= 12; k >= 4 drops that sign and also reverses the inequality.

</details>

---

### 50. alg-ineq-four-constraints-greatest-sum

*Hard · Student-produced response · route: desmos-primary · techniques: T8*

The inequalities $x \ge 0$, $y \ge 0$, $3x + y \le 18$, and $x + 2y \le 16$ together define a region in the $xy$-plane. What is the greatest value of $x + y$ for any point $(x, y)$ in this region?

**Answer:** 10

<details><summary>Solutions</summary>

**By hand.** The greatest value of x + y on a region bounded by lines occurs at a corner. The corners are (0, 0), (6, 0) from 3x + y = 18 with y = 0, (0, 8) from x + 2y = 16 with x = 0, and the intersection of 3x + y = 18 and x + 2y = 16. Substituting y = 18 - 3x into the second equation yields x + 36 - 6x = 16, so x = 4 and y = 6. The sums are 0, 6, 8 and 10. Therefore, the greatest value of x + y is 10. Using only the intercepts gives 8 or 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>x\ge0</code><br><code>y\ge0</code><br><code>3x+y\le18</code><br><code>x+2y\le16</code><br><code>x+y=s</code>

Accept the slider for s and raise it until the line x + y = s last touches the overlap; that happens at the corner (4, 6), where s = 10. Alternatively click each corner of the overlap, (0, 0), (6, 0), (4, 6) and (0, 8), and add the coordinates.

</details>

---

### 51. alg-ineq-hike-distance-time-system

*Hard · Multiple choice · route: hand-primary · techniques: —*

A hiker walks 4 kilometers per hour on flat trail and 2 kilometers per hour on hilly trail, and plans to cover at least 16 kilometers in at most 6 hours. Which system represents this plan, where $d$ and $h$ are the distances, in kilometers, walked on flat and hilly trail, respectively?

- **A.** $d + h \ge 16$ and $0.25d + 0.5h \le 6$
- **B.** $d + h \ge 16$ and $0.5d + 0.25h \le 6$
- **C.** $d + h \ge 16$ and $4d + 2h \le 6$
- **D.** $d + h \le 16$ and $0.25d + 0.5h \ge 6$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The variables are distances, so the total distance is d + h, and at least 16 kilometers means d + h >= 16. Time equals distance divided by speed, so walking d kilometers at 4 kilometers per hour takes d/4 = 0.25d hours and walking h kilometers at 2 kilometers per hour takes h/2 = 0.5h hours. The total time is at most 6 hours, so 0.25d + 0.5h <= 6. Therefore, the system is d + h >= 16 and 0.25d + 0.5h <= 6. Distractors: d + h >= 16 and 0.5d + 0.25h <= 6 divides each distance by the other trail's speed; d + h >= 16 and 4d + 2h <= 6 multiplies distance by speed, which would be correct only if d and h were hours; d + h <= 16 and 0.25d + 0.5h >= 6 reverses both directions.

</details>

---

### 52. alg-ineq-interval-all-satisfy-k

*Hard · Multiple choice · route: either · techniques: T9*

Every value of $x$ with $2 \le x \le 5$ satisfies the inequality $x + k > 3x - 1$, where $k$ is a constant. What is the least possible integer value of $k$?

- **A.** $3$
- **B.** $4$
- **C.** $9$
- **D.** $10$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Subtracting x from both sides of x + k > 3x - 1 yields k > 2x - 1. This must hold for every x with 2 <= x <= 5. The expression 2x - 1 increases as x increases, so its greatest value on the interval is 2(5) - 1 = 9, and k must be greater than 9. Therefore, the least possible integer value of k is 10. Distractors: 3 is the value of 2x - 1 at x = 2, the wrong endpoint, taken as k itself; 4 is the least integer greater than 3, which only guarantees x = 2 works; 9 is the boundary value, which fails at x = 5 because the inequality is strict.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=2x-1</code><br><code>f(2)</code><br><code>f(5)</code>

The inequality rearranges to k > 2x - 1. Desmos shows f(2) = 3 and f(5) = 9; f increases, so its largest value on the interval is 9 and k must exceed 9. The least integer is 10.

</details>

---

### 53. alg-ineq-lattice-points-count

*Hard · Multiple choice · route: either · techniques: T8*

How many points $(x, y)$ in the $xy$-plane, where $x$ and $y$ are both positive integers, satisfy $3x + 4y \le 20$?

- **A.** $4$
- **B.** $11$
- **C.** $12$
- **D.** $24$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** For each positive integer y, count the positive integers x with 3x <= 20 - 4y. y = 1: 3x <= 16, so x = 1 to 5 (5 points). y = 2: 3x <= 12, so x = 1 to 4 (4 points). y = 3: 3x <= 8, so x = 1 or 2 (2 points). y = 4: 3x <= 4, so x = 1 (1 point). y = 5: 3x <= 0, no positive x. The total is 5 + 4 + 2 + 1 = 12. Therefore, 12 points satisfy the inequality. Distractors: 4 counts only the possible values of y; 11 leaves out the boundary point (4, 2), treating the inequality as strict; 24 also counts points with a zero coordinate, which are not positive.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x+4y\le20</code><br><code>x\ge1</code><br><code>y\ge1</code>

Turn the grid on and count the grid points in the darker overlap, including points on the solid line 3x + 4y = 20, such as (4, 2). Row y = 1 has 5 points, y = 2 has 4, y = 3 has 2 and y = 4 has 1, for 12. Counting by hand row by row is just as fast.

</details>

---

### 54. alg-ineq-no-solution-a

*Hard · Multiple choice · route: hand-primary · techniques: —*

The inequality $ax + 5 < 2(3x - 1)$, where $a$ is a constant, has no solution. What is the value of $a$?

- **A.** $-6$
- **B.** $3$
- **C.** $6$
- **D.** $7$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Distributing yields ax + 5 < 6x - 2, and subtracting 6x and 5 from both sides yields (a - 6)x < -7. If a - 6 is not 0, dividing by a - 6 gives a half-line of solutions, so the inequality has solutions. If a = 6, the inequality becomes 0 < -7, which is false for every x. Therefore, a = 6. Distractors: -6 comes from a sign error when moving 6x to the left side; 3 comes from not distributing the 2, which gives 3x - 1 on the right; 7 sets a equal to the constant 7 from (a - 6)x < -7 instead of making the x-coefficient 0.

</details>

---

### 55. alg-ineq-point-not-in-system-c

*Hard · Multiple choice · route: either · techniques: T8*

In the $xy$-plane, the point $(2, 1)$ is not a solution to the system of inequalities $y \ge 3x + c$ and $y \le -x + 4$, where $c$ is a constant. Which inequality must be true?

- **A.** $c < -5$
- **B.** $c \le -5$
- **C.** $c \ge -5$
- **D.** $c > -5$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Substituting (2, 1) into the second inequality yields 1 <= -2 + 4 = 2, which is true. So the point fails the system only if it fails the first inequality, 1 >= 3(2) + c, or 1 >= 6 + c. Failing means 1 < 6 + c, which yields c > -5. Therefore, c > -5 must be true. Distractors: c < -5 and c <= -5 are the values for which (2, 1) is a solution, the opposite of what is given; c >= -5 includes c = -5, where (2, 1) lies on the solid boundary and is a solution.

**Desmos** (not yet verified in Desmos). Type:<br><code>y\ge3x+c</code><br><code>y\le-x+4</code><br><code>(2,1)</code>

Accept the slider for c and drag it. The point stays inside the darker overlap while c <= -5; at c = -5 it sits on the solid boundary, which still counts. Once c is greater than -5 the point is outside. Reasoning by hand is about as fast.

</details>

---

### 56. alg-ineq-point-on-line-system-k

*Hard · Multiple choice · route: desmos-primary · techniques: T8*

In the $xy$-plane, the point $(k, 2k)$, where $k$ is a constant, is a solution to the system of inequalities $y > -x + 9$ and $y \le x + 7$. What is the greatest possible value of $k$?

- **A.** $3$
- **B.** $4$
- **C.** $7$
- **D.** $14$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Substituting k for x and 2k for y yields 2k > -k + 9 and 2k <= k + 7. The first gives 3k > 9, so k > 3; the second gives k <= 7. So 3 < k <= 7, and the greatest possible value of k is 7. Distractors: 3 is the lower bound, which is excluded; 4 is the least integer value of k; 14 is the y-coordinate 2k of the point when k = 7, not k itself.

**Desmos** (not yet verified in Desmos). Type:<br><code>y&gt;-x+9</code><br><code>y\le x+7</code><br><code>y=2x</code>

Every point (k, 2k) lies on the line y = 2x. The part of that line inside the darker overlap runs from (3, 6), on the dashed boundary and excluded, to (7, 14), on the solid boundary and included. Click (7, 14): the greatest k is its x-coordinate, 7.

</details>

---

### 57. alg-ineq-region-greatest-2x-plus-y

*Hard · Multiple choice · route: desmos-primary · techniques: T8*

A point $(x, y)$ in the $xy$-plane satisfies $y \le 8 - x$, $y \ge x - 2$, and $x \ge 0$. What is the greatest possible value of $2x + y$?

- **A.** $-2$
- **B.** $8$
- **C.** $11$
- **D.** $13$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The region is a triangle, and the greatest value of 2x + y occurs at a corner. The corners are (0, 8) and (0, -2) on the y-axis, and the intersection of y = 8 - x and y = x - 2, where 8 - x = x - 2 yields x = 5 and y = 3. The values of 2x + y are 8, -2 and 2(5) + 3 = 13. Therefore, the greatest possible value is 13. Distractors: -2 is the value at (0, -2), the least value rather than the greatest; 8 is the value at (0, 8), checking only the y-intercepts; 11 computes x + 2y at (5, 3), swapping the coefficients.

**Desmos** (not yet verified in Desmos). Type:<br><code>y\le8-x</code><br><code>y\ge x-2</code><br><code>x\ge0</code><br><code>2x+y=s</code>

The overlap is a triangle with corners (0, 8), (0, -2) and (5, 3). Accept the slider for s and raise it until the line 2x + y = s last touches the triangle, at (5, 3), where s = 13. Clicking the three corners and computing 2x + y at each works too.

</details>

---

### 58. alg-ineq-region-lines-through-points

*Hard · Multiple choice · route: desmos-primary · techniques: T13, T8*

A region in the $xy$-plane consists of all points that lie above the dashed line through $(-2, 0)$ and $(0, 4)$ and on or below the solid line through $(0, 4)$ and $(6, 1)$. Which system of inequalities describes this region?

- **A.** $y < 2x + 4$ and $x + 2y \ge 8$
- **B.** $y \ge 2x + 4$ and $x + 2y < 8$
- **C.** $y > 2x + 4$ and $2x + y \le 8$
- **D.** $y > 2x + 4$ and $x + 2y \le 8$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The dashed line through (-2, 0) and (0, 4) has slope (4 - 0)/(0 - (-2)) = 2 and y-intercept 4, so it is y = 2x + 4; dashed and above give y > 2x + 4. The solid line through (0, 4) and (6, 1) has slope (1 - 4)/(6 - 0) = -1/2 and y-intercept 4, so it is y = -(1/2)x + 4, and multiplying by 2 and rearranging yields x + 2y = 8. Points on or below this solid line have y <= -(1/2)x + 4, or x + 2y <= 8. Therefore, the system is y > 2x + 4 and x + 2y <= 8. Distractors: y < 2x + 4 and x + 2y >= 8 reverses both directions; y >= 2x + 4 and x + 2y < 8 swaps which line is dashed and which is solid; y > 2x + 4 and 2x + y <= 8 swaps the coefficients of the second line, which then passes through (4, 0) and (0, 8) instead of (6, 1).

**Desmos** (not yet verified in Desmos). Type:<br><code>(-2,0)</code><br><code>(0,4)</code><br><code>(6,1)</code><br><code>y&gt;2x+4</code><br><code>x+2y\le8</code>

Plot the three points, then type each choice's pair of inequalities. Keep the pair whose dashed line passes through (-2, 0) and (0, 4), whose solid line passes through (0, 4) and (6, 1), and whose overlap lies above the dashed line and below the solid one.

</details>

---

### 59. alg-ineq-signs-of-constants

*Hard · Multiple choice · route: hand-primary · techniques: —*

The solution set of the inequality $px + q < 0$, where $p$ and $q$ are constants, is $x > 3$. Which of the following must be true?

- **A.** $p > 0$ and $q > 0$
- **B.** $p > 0$ and $q < 0$
- **C.** $p < 0$ and $q > 0$
- **D.** $p < 0$ and $q < 0$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Subtracting q from both sides yields px < -q. The solution set x > 3 has the inequality pointing the other way, so dividing by p must have reversed it, which happens only when p < 0. Then x > -q/p, and -q/p = 3 yields q = -3p. Since p is negative, q = -3p is positive. Therefore, p < 0 and q > 0. A check: p = -1 and q = 3 give -x + 3 < 0, or x > 3. Distractors: p > 0 and q > 0 would give x < -q/p, a solution set pointing left; p > 0 and q < 0 gives x < 3 for p = 1 and q = -3, the same mistake of not reversing; p < 0 and q < 0 gets the sign of p right but then gives x > -q/p with -q/p negative, such as x > -3.

</details>

---

### 60. alg-ineq-stable-feed-least-cost

*Hard · Multiple choice · route: desmos-primary · techniques: T8*

A stable needs at least 600 kilograms of feed, including at least 200 kilograms of oats, and can store at most 350 kilograms of hay. Hay costs 0.30 dollar per kilogram and oats cost 0.50 dollar per kilogram. If the feed is only hay and oats, what is the least possible cost, in dollars, of the feed?

- **A.** $220$
- **B.** $230$
- **C.** $250$
- **D.** $300$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Let x be the kilograms of hay and y the kilograms of oats. The constraints are x + y >= 600, y >= 200 and x <= 350, and the cost is 0.30x + 0.50y. Hay is cheaper, so the least cost uses as much hay as allowed, 350 kilograms, and only as many oats as needed to reach 600 kilograms, 250 kilograms, which also meets y >= 200. The cost is 0.30(350) + 0.50(250) = 105 + 125 = 230. Therefore, the least possible cost is 230 dollars. Distractors: 220 uses 400 kilograms of hay and 200 of oats, which breaks the storage limit; 250 swaps the prices; 300 buys only oats.

**Desmos** (not yet verified in Desmos). Type:<br><code>x+y\ge600</code><br><code>y\ge200</code><br><code>x\le350</code><br><code>x\ge0</code><br><code>0.3x+0.5y=c</code>

Here x is kilograms of hay and y kilograms of oats; accept the slider for c. Lower c until the cost line last touches the overlap, which happens at the corner (350, 250); there c = 0.3(350) + 0.5(250) = 230. Zoom to a window of about 0 to 700 on both axes.

</details>

---

### 61. alg-ineq-two-inequalities-given-interval

*Hard · Student-produced response · route: either · techniques: T8*

The values of $x$ that satisfy both $5 - 2x \ge a$ and $3x + b > 0$, where $a$ and $b$ are constants, are exactly the values with $-2 < x \le 4$. What is the value of $b - a$?

**Answer:** 9

<details><summary>Solutions</summary>

**By hand.** Solving 5 - 2x >= a for x yields -2x >= a - 5, and dividing by -2 reverses the inequality: x <= (5 - a)/2. This gives the closed endpoint, so (5 - a)/2 = 4 and a = -3. Solving 3x + b > 0 yields x > -b/3, the open endpoint, so -b/3 = -2 and b = 6. Therefore, b - a = 6 - (-3) = 9. Forgetting to reverse the inequality pairs 5 - 2x >= a with the wrong endpoint; mixing up the signs gives b - a = 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>5-2x\ge-3</code><br><code>3x+6&gt;0</code>

Find a and b by hand first, then type the two inequalities with those values. The overlap should be the band from x = -2 (dashed) to x = 4 (solid). Desmos only confirms here; it does not find a and b quickly.

</details>

---

### 62. alg-ineq-wedge-greatest-x

*Hard · Multiple choice · route: desmos-primary · techniques: T8*

In the $xy$-plane, the solution set of the system of inequalities $y \le -\frac{1}{2}x + 6$ and $y \ge 2x - 4$ is a region. What is the greatest possible $x$-coordinate of a point in this region?

- **A.** $2$
- **B.** $4$
- **C.** $6$
- **D.** $12$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A point (x, y) is in the region when 2x - 4 <= y <= -(1/2)x + 6, which is possible only when 2x - 4 <= -(1/2)x + 6. Adding (1/2)x + 4 to both sides yields (5/2)x <= 10, so x <= 4. At x = 4 the point (4, 4) satisfies both inequalities. Therefore, the greatest possible x-coordinate is 4. Distractors: 2 is the x-intercept of y = 2x - 4; 6 is the y-intercept of y = -(1/2)x + 6; 12 is the x-intercept of y = -(1/2)x + 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y\le-\frac{1}{2}x+6</code><br><code>y\ge2x-4</code>

The darker overlap is a wedge that opens to the left and ends at the point where the two solid boundary lines cross. Click that intersection, (4, 4): no point of the region lies to its right, so the greatest x-coordinate is 4.

</details>

---

### 63. alg-ineq-workshop-tables

*Hard · Student-produced response · route: desmos-primary · techniques: T8*

A workshop has at most 120 hours to build chairs and tables. Each chair takes 3 hours and each table takes 7 hours. The workshop must build at least twice as many chairs as tables. What is the greatest number of tables the workshop can build?

**Answer:** 9

<details><summary>Solutions</summary>

**By hand.** Let c be the number of chairs and t the number of tables. The constraints are 3c + 7t <= 120 and c >= 2t. Using as few chairs as allowed leaves the most time for tables, so substituting c = 2t yields 6t + 7t <= 120, or 13t <= 120, so t <= 120/13, which is about 9.23. With t = 9 and c = 18 the time is 54 + 63 = 117 hours, which works. With t = 10 the workshop needs at least 20 chairs, and 60 + 70 = 130 hours is too many. Therefore, the greatest number of tables is 9. Ignoring the chair requirement gives 120/7, about 17.

**Desmos** (not yet verified in Desmos). Type:<br><code>3x+7y\le120</code><br><code>x\ge2y</code><br><code>y\ge0</code>

Here x is the number of chairs and y the number of tables. The overlap is a triangle whose top corner is about (18.46, 9.23), so y cannot exceed 9.23. The greatest whole number of tables is 9; click near (18, 9) to confirm it lies in the overlap.

</details>

---

### 64. alg-inequality-coefficient-k-flip

*Hard · Multiple choice · route: either · techniques: T4*

The solution set of the inequality $kx - 8 < 2x + 7$, where $k$ is a constant, is $x > -3$. What is the value of $k$?

- **A.** $-7$
- **B.** $-3$
- **C.** $3$
- **D.** $7$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Subtracting 2x from both sides and adding 8 to both sides of the given inequality yields (k - 2)x < 15. The solution set x > -3 has the inequality symbol reversed, so dividing by k - 2 must have reversed it, which means k - 2 is negative. Then x > 15/(k - 2), and 15/(k - 2) = -3 yields k - 2 = -5, so k = -3. Check: -3x - 8 < 2x + 7 gives -5x < 15, so x > -3. Distractors: 7 solves k - 2 = 5, ignoring that the symbol was reversed; 3 is a sign error on the final step; -7 subtracts 2 from -5 instead of adding 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=kx-8</code><br><code>y=2x+7</code>

Add a slider for k. Drag until the lines cross at x = -3 with y = kx - 8 below y = 2x + 7 to the right of the crossing: k = -3. By hand, the reversed symbol in x > -3 tells you k - 2 is negative.

</details>

---

### 65. alg-inequality-solution-set-c

*Hard · Multiple choice · route: either · techniques: T4, T1*

For the inequality $3x + c > 5x - 9$, where $c$ is a constant, the solution set is $x < 4$. What is the value of $c$?

- **A.** $-17$
- **B.** $-5$
- **C.** $-1$
- **D.** $1$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Subtracting 3x from both sides of the inequality and adding 9 yields c + 9 > 2x, so x < (c + 9)/2. For the solution set to be x < 4, (c + 9)/2 = 4, so c + 9 = 8 and c = -1. Distractors: 1 is a sign error (c = 9 - 8 instead of 8 - 9); -5 forgets to divide by 2 (c + 9 = 4); -17 moves the 9 to the wrong side and flips the sign (c = -(8 + 9)).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x+c</code><br><code>y=5x-9</code><br><code>x=4</code>

Add a slider for c and drag until the two lines cross on the vertical line x = 4: c = -1. To the left of x = 4 the line y = 3x + c is above y = 5x - 9, as the solution set requires. Solving by hand is faster.

</details>

---

### 66. alg-parallel-strip-combination

*Hard · Multiple choice · route: desmos-primary · techniques: T8*

In the $xy$-plane, the point $(p, q)$, where $p$ and $q$ are constants, lies in the solution set of the system of inequalities $y > 3x - 2$ and $y < 3x + 4$. Which of the following must be true?

- **A.** $q - 3p < -2$
- **B.** $-2 < q - 3p < 4$
- **C.** $q - 3p > 4$
- **D.** $-4 < q - 3p < 2$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since (p, q) satisfies both inequalities, q > 3p - 2 and q < 3p + 4. Subtracting 3p from each inequality yields q - 3p > -2 and q - 3p < 4, which together say -2 < q - 3p < 4. Distractors: q - 3p < -2 and q - 3p > 4 describe points below the lower line and above the upper line, outside the strip; -4 < q - 3p < 2 swaps the signs of the two bounds, as if the system were y > 3x - 4 and y < 3x + 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y&gt;3x-2</code><br><code>y&lt;3x+4</code>

The overlap is the strip between two parallel dashed lines. For any point in the strip, y - 3x is between -2 and 4, so -2 < q - 3p < 4. Check with a point in the strip such as (0, 0), where q - 3p = 0.

</details>

---

### 67. alg-scaled-inequality-max

*Hard · Multiple choice · route: hand-primary · techniques: —*

If $2x + 3y \le 12$, what is the greatest possible value of $4x + 6y$?

- **A.** $12$
- **B.** $24$
- **C.** $36$
- **D.** $48$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The expression 4x + 6y is 2(2x + 3y). Multiplying both sides of the given inequality by 2 yields 2(2x + 3y) <= 24, so 4x + 6y <= 24. The value 24 is attained, for example at x = 6 and y = 0, since 2(6) + 3(0) = 12. Therefore, the greatest possible value of 4x + 6y is 24. Distractors: 12 is the greatest value of 2x + 3y, not of its double; 36 multiplies 12 by 3, as if 4x + 6y were 3(2x + 3y); 48 multiplies 12 by 4, the coefficient of x alone.

</details>

---

### 68. alg-shelf-inequality-point-meaning

*Hard · Multiple choice · route: hand-primary · techniques: —*

A shelf holds at most 240 kilograms. The inequality $12m + 8s \le 240$ represents this situation, where $m$ is the number of medium boxes and $s$ is the number of small boxes on it. Which of the following is the best interpretation of $(m, s) = (10, 12)$ being a solution to the given inequality?

- **A.** The shelf can hold 10 medium boxes and 12 small boxes without exceeding 240 kilograms.
- **B.** A shelf holding 10 medium boxes can hold at most 12 small boxes.
- **C.** The combined weight of 10 medium boxes and 12 small boxes is exactly 240 kilograms.
- **D.** The shelf can hold either 10 medium boxes or 12 small boxes, but not both.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A solution (m, s) of the inequality is a pair of numbers of boxes whose total weight, 12m + 8s kilograms, does not exceed 240. Substituting 10 for m and 12 for s yields 12(10) + 8(12) = 120 + 96 = 216, and 216 <= 240, so the shelf can hold 10 medium boxes and 12 small boxes without exceeding 240 kilograms. Distractors: 'at most 12 small boxes' is false, since with 10 medium boxes on the shelf there is room for up to (240 - 120)/8 = 15 small boxes; 'exactly 240 kilograms' confuses a solution with a point on the boundary, but the combined weight is 216 kilograms; 'either 10 medium boxes or 12 small boxes, but not both' contradicts the solution, which shows that both sets of boxes fit together.

</details>

---

### 69. alg-system-inequalities-point

*Hard · Multiple choice · route: desmos-primary · techniques: T8*

In the $xy$-plane, which point $(x, y)$ is a solution to the system of inequalities $y \ge \frac{1}{2}x - 3$ and $2x + y < 6$?

- **A.** $(-2, -5)$
- **B.** $(1, 4)$
- **C.** $(2, -2)$
- **D.** $(4, -2)$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A point is a solution when it satisfies both inequalities. For (2, -2): -2 >= (1/2)(2) - 3 = -2 is true, because the first inequality is not strict, and 2(2) + (-2) = 2 < 6 is true. Distractors: (1, 4) gives 2(1) + 4 = 6, which is not less than 6, so the point lies on the strict boundary and is excluded; (-2, -5) fails the first inequality, since -5 < -4; (4, -2) fails the first inequality, since -2 < -1.

**Desmos** (not yet verified in Desmos). Type:<br><code>y\ge\frac{1}{2}x-3</code><br><code>2x+y&lt;6</code><br><code>(-2,-5)</code><br><code>(1,4)</code><br><code>(2,-2)</code><br><code>(4,-2)</code>

Plot the four points. Only (2, -2) lies in the doubly shaded region; it sits on the solid boundary of the first inequality, which is allowed. (1, 4) sits on the dashed boundary of 2x + y < 6, which is not.

</details>

---

### 70. alg-two-jobs-least-hours

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

A worker earns 14 dollars per hour at one job and 20 dollars per hour at a second job. In one week the worker works exactly 30 hours in all at the two jobs and earns at least 480 dollars. What is the least number of hours the worker could have worked at the second job that week?

**Answer:** 10

<details><summary>Solutions</summary>

**By hand.** Let h be the number of hours at the second job; then the worker works 30 - h hours at the first job. The week's earnings are 14(30 - h) + 20h = 420 + 6h dollars. 'At least 480' means 420 + 6h >= 480, so 6h >= 60 and h >= 10. Therefore, the least possible number of hours at the second job is 10.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=14(30-x)+20x</code><br><code>y=480</code>

Click the intersection: (10, 480). Earnings rise as x increases, so the earnings are at least 480 when x ≥ 10, and the least number of hours is 10.

</details>

---
