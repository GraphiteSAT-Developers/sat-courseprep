# Nonlinear equations in one variable and systems of equations in two variables

[← Question bank index](README.md) · Advanced Math · 133 questions, easiest first

### 1. adv-absolute-value-negative-zero-solutions

*Easy · Multiple choice · route: hand-primary · techniques: T1*

How many real solutions does the equation $|2x + 5| + 7 = 3$ have?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Subtracting 7 from both sides of the given equation yields |2x + 5| = -4. An absolute value is never negative, so no real number x makes |2x + 5| equal -4. Therefore, the equation has zero real solutions. Distractors: Exactly two comes from splitting into 2x + 5 = 4 or 2x + 5 = -4 without noticing that the absolute value cannot equal -4; Exactly one comes from solving only 2x + 5 = -4; Infinitely many confuses an equation that is never true with one that is always true.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left|2x+5\right|+7</code><br><code>y=3</code>

The structural argument takes seconds, so Desmos is slower. As a check (the absolute-value picture of T14), the V has its lowest point at (-2.5, 7), entirely above the line y = 3, so the graphs never meet: zero solutions.

</details>

---

### 2. adv-absolute-value-positive-solution

*Easy · Multiple choice · route: hand-primary · techniques: T1*

What is the positive solution to the equation $|2x - 7| = 11$?

- **A.** $2$
- **B.** $\frac{11}{2}$
- **C.** $9$
- **D.** $18$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that |2x - 7| = 11, so 2x - 7 = 11 or 2x - 7 = -11. The first yields 2x = 18 and x = 9; the second yields 2x = -4 and x = -2. Therefore, the positive solution is 9. Distractors: 2 subtracts 7 instead of adding it (2x = 4) and is also the absolute value of the negative solution; 11/2 ignores the -7 (2x = 11); 18 stops at 2x = 18 without dividing.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left|2x-7\right|</code><br><code>y=11</code>

The V meets the horizontal line at (-2, 11) and (9, 11); take the positive x-coordinate, 9. Splitting into two cases by hand is faster.

</details>

---

### 3. adv-exponential-power-of-two-easy

*Easy · Multiple choice · route: hand-primary · techniques: T1*

What value of $x$ satisfies the equation $2^{x - 1} = 32$?

- **A.** $4$
- **B.** $5$
- **C.** $6$
- **D.** $16$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Since 32 = 2^5, the given equation can be rewritten as 2^(x - 1) = 2^5. Two powers of the same base are equal when the exponents are equal, so x - 1 = 5 and x = 6. Distractors: 4 comes from subtracting 1 instead of adding it (x = 5 - 1); 5 is the exponent of 32, the value of x - 1 rather than x; 16 comes from dividing 32 by 2 instead of matching exponents.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2^{x-1}</code><br><code>y=32</code>

Writing 32 as a power of 2 is faster. As a check, click the intersection of the curve and the horizontal line: (6, 32), so x = 6.

</details>

---

### 4. adv-factored-cubic-least-solution

*Easy · Multiple choice · route: hand-primary · techniques: T1*

What is the least solution to the equation $x(x + 6)(3x - 2) = 0$?

- **A.** $-6$
- **B.** $-\frac{2}{3}$
- **C.** $\frac{2}{3}$
- **D.** $6$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A product equals 0 exactly when one of its factors equals 0. Setting x = 0, x + 6 = 0 and 3x - 2 = 0 yields x = 0, x = -6 and x = 2/3. Therefore, the least solution is -6. Distractors: -2/3 comes from a sign error in the factor 3x - 2; 2/3 is the greatest solution, not the least; 6 comes from a sign error in the factor x + 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x(x+6)(3x-2)</code>

Reading the zeros straight off the factors is faster than graphing. As a check, the cubic crosses the x-axis at x = -6, x = 0 and x = 0.667; the leftmost crossing is -6.

</details>

---

### 5. adv-ne2-factored-greatest-solution

*Easy · Multiple choice · route: hand-primary · techniques: T1, T11*

What is the greatest solution to the equation $(2x - 9)(x^2 - 16) = 0$?

- **A.** $4$
- **B.** $\frac{9}{2}$
- **C.** $9$
- **D.** $16$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A product equals 0 when one of its factors equals 0. Setting 2x - 9 = 0 yields x = 9/2, and setting x^2 - 16 = 0 yields x = 4 or x = -4. The solutions are -4, 4 and 9/2, and the greatest is 9/2 = 4.5. Distractors: 4 is the greatest solution of x^2 - 16 = 0 alone, overlooking 9/2; 9 drops the coefficient 2 in 2x - 9; 16 sets x = 16 instead of x^2 = 16.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(2x-9)(x^2-16)</code>

Reading the factors takes seconds, so Desmos is slower. As a check, the graph crosses the x-axis at -4, 4 and 4.5; the greatest is 4.5, which the fraction toggle (T11) shows as 9/2.

</details>

---

### 6. adv-ne2-line-parabola-which-point

*Easy · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $y = x^2$ and $y = x + 6$ intersect at two points. Which of the following is one of these points?

- **A.** $(-3, 3)$
- **B.** $(-2, 4)$
- **C.** $(2, 4)$
- **D.** $(2, 8)$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting x^2 for y in y = x + 6 yields x^2 = x + 6, so x^2 - x - 6 = 0, which factors as (x - 3)(x + 2) = 0. So x = 3 or x = -2, and y = x^2 gives the points (3, 9) and (-2, 4). Therefore, (-2, 4) is one of the points. Distractors: (-3, 3) lies on the line but not on the parabola, from the sign slip (x + 3)(x - 2) = 0; (2, 4) lies on the parabola but not on the line, from the same slip; (2, 8) lies on the line but not on the parabola.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2</code><br><code>y=x+6</code>

Click the two gray intersection points: (-2, 4) and (3, 9). Only (-2, 4) is among the choices.

</details>

---

### 7. adv-ne2-quartic-isolate-positive

*Easy · Multiple choice · route: hand-primary · techniques: T1*

What is the positive solution to the equation $2x^4 - 7 = 155$?

- **A.** $3$
- **B.** $9$
- **C.** $74$
- **D.** $81$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Adding 7 to both sides of the given equation yields 2x^4 = 162, and dividing both sides by 2 yields x^4 = 81. Since 3^4 = 81, the real solutions are x = 3 and x = -3. Therefore, the positive solution is 3. Distractors: 9 is the value of x^2, an intermediate result; 74 subtracts 7 instead of adding it and stops at (155 - 7)/2; 81 is the value of x^4, not of x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x^4-7</code><br><code>y=155</code>

Isolating x^4 takes two steps by hand, so Desmos is slower. As a check, the horizontal line meets the curve at x = -3 and x = 3; the positive solution is 3.

</details>

---

### 8. adv-ne2-rational-one-fraction-easy

*Easy · Multiple choice · route: hand-primary · techniques: T1*

What is the solution to the equation $\frac{x + 5}{x - 1} = 3$?

- **A.** $1$
- **B.** $3$
- **C.** $4$
- **D.** $8$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the given equation by x - 1, where x ≠ 1, yields x + 5 = 3(x - 1) = 3x - 3. Subtracting x from both sides and adding 3 to both sides yields 8 = 2x, so x = 4. Check: (4 + 5)/(4 - 1) = 9/3 = 3. Distractors: 1 is the excluded value that makes the denominator 0; 3 comes from writing 3(x - 1) as 3x - 1; 8 is the value of 2x, an intermediate result.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x+5}{x-1}</code><br><code>y=3</code>

Clearing the denominator is one line by hand, so Desmos is slower. As a check, the curve meets y = 3 once, at x = 4.

</details>

---

### 9. adv-ne2-rod-length-tolerance

*Easy · Student-produced response · route: hand-primary · techniques: T1*

A machine cuts metal rods. A rod is exactly at the limit of what is accepted when its length $L$, in centimeters, satisfies the equation $|L - 120| = 0.4$. What is the greater of the two possible lengths, in centimeters?

**Answer:** 602/5 (≈ 120.4)

<details><summary>Solutions</summary>

**By hand.** It's given that |L - 120| = 0.4, so L - 120 = 0.4 or L - 120 = -0.4. These yield L = 120.4 or L = 119.6. Therefore, the greater length is 120.4 centimeters.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=|x-120|</code><br><code>y=0.4</code>

One step by hand, so Desmos is slower. As a check, zoom out until x = 120 is on screen, then zoom in on the bottom of the V: it meets y = 0.4 at x = 119.6 and x = 120.4. Enter the greater value, 120.4.

</details>

---

### 10. adv-ne2-square-equals-twelve-radical

*Easy · Multiple choice · route: either · techniques: T1, T13*

What is the positive value of $x$ that satisfies $(x + 2)^2 = 12$?

- **A.** $-2 + \sqrt{6}$
- **B.** $-2 + 2\sqrt{3}$
- **C.** $-2 + 4\sqrt{3}$
- **D.** $2 + 2\sqrt{3}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Taking the square root of both sides of the given equation yields x + 2 = sqrt(12) or x + 2 = -sqrt(12). Since sqrt(12) = sqrt(4 · 3) = 2 sqrt(3), x = -2 + 2 sqrt(3) or x = -2 - 2 sqrt(3). The second is negative, so the positive solution is -2 + 2 sqrt(3), about 1.46. Distractors: -2 + sqrt(6) halves the radicand instead of taking the square root of 4; -2 + 4 sqrt(3) moves the 4 out of the radical without taking its square root; 2 + 2 sqrt(3) adds 2 instead of subtracting it.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x+2)^2</code><br><code>y=12</code><br><code>-2+\sqrt{6}</code><br><code>-2+2\sqrt{3}</code><br><code>-2+4\sqrt{3}</code><br><code>2+2\sqrt{3}</code>

Click the intersection with positive x: x is about 1.464. Then compare it with the values Desmos shows beside the four choice lines (T13): only -2 + 2 sqrt(3) is 1.464.

</details>

---

### 11. adv-ne3-base-four-sixty-four

*Easy · Multiple choice · route: hand-primary · techniques: T1*

What is the solution to the equation $4^{x + 1} = 64$?

- **A.** $2$
- **B.** $3$
- **C.** $15$
- **D.** $16$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Since 64 = 4^3, the given equation can be rewritten as 4^(x + 1) = 4^3. Setting the exponents equal yields x + 1 = 3, so x = 2. Therefore, the solution is 2. Distractors: 3 is the value of the exponent x + 1, not of x; 15 divides 64 by 4 and subtracts 1; 16 divides 64 by 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=4^{x+1}</code><br><code>y=64</code>

Rewriting 64 as a power of 4 is faster. As a check, zoom out until y = 64 is on screen and click the intersection: (2, 64).

</details>

---

### 12. adv-ne3-factored-repeated-count

*Easy · Multiple choice · route: desmos-primary · techniques: T1*

How many distinct real solutions does the equation $(x - 5)^2(x^2 - 25) = 0$ have?

- **A.** Exactly one
- **B.** Exactly two
- **C.** Exactly three
- **D.** Exactly four

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A product equals 0 when at least one factor equals 0. The factor (x - 5)^2 is 0 when x = 5. The factor x^2 - 25 = (x - 5)(x + 5) is 0 when x = 5 or x = -5. The distinct solutions are 5 and -5, so the equation has exactly two distinct real solutions. Distractors: Exactly one uses only the factor (x - 5)^2; Exactly three counts x = 5 once from each factor as if they were different solutions; Exactly four counts every factor of the expanded degree-4 polynomial, including the repeated one.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x-5)^2(x^2-25)</code>

Zoom out vertically until the curve's shape is clear, then click the x-intercepts. The graph crosses at (-5, 0) and touches at (5, 0): two distinct x-intercepts.

</details>

---

### 13. adv-ne3-five-times-power-two

*Easy · Student-produced response · route: desmos-primary · techniques: T1*

If $5 \cdot 2^{x} = 160$, what is the value of $x$?

**Answer:** 5

<details><summary>Solutions</summary>

**By hand.** Dividing both sides of the given equation by 5 yields 2^x = 32. Since 32 = 2^5, it follows that 2^x = 2^5, so x = 5. Therefore, the value of x is 5. A common slip is to divide 160 by 10 (multiplying 5 by 2 first) and get 2^x = 16, which gives 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5\cdot2^x</code><br><code>y=160</code>

Zoom out until the horizontal line y = 160 is on screen, then click the intersection: (5, 160). Enter 5.

</details>

---

### 14. adv-ne3-heating-coil-voltage

*Easy · Student-produced response · route: hand-primary · techniques: T1*

The power $P$, in watts, used by a certain heating coil is given by $P = \frac{V^2}{24}$, where $V$ is the positive voltage, in volts, across the coil. If the coil uses 150 watts, what is the value of $V$?

**Answer:** 60

<details><summary>Solutions</summary>

**By hand.** It's given that P = V^2/24 and P = 150. Substituting yields 150 = V^2/24. Multiplying both sides by 24 yields V^2 = 3,600, so V = 60 or V = -60. It's given that V is positive, so V = 60. Therefore, the value of V is 60.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^2}{24}</code><br><code>y=150</code>

Two quick steps by hand, so Desmos is slower. As a check, zoom out until y = 150 is on screen and click the intersection with positive x: (60, 150). The voltage is positive, so ignore (-60, 150).

</details>

---

### 15. adv-ne3-product-xy-line-easy

*Easy · Multiple choice · route: either · techniques: T2*

If $xy = 18$, $y = 2x$, and $x > 0$, what is the value of $x$?

- **A.** $3$
- **B.** $4.5$
- **C.** $6$
- **D.** $9$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Substituting 2x for y in xy = 18 yields x(2x) = 18, or 2x^2 = 18. Dividing both sides by 2 yields x^2 = 9, so x = 3 or x = -3. Since x > 0, x = 3. Therefore, the value of x is 3. Distractors: 4.5 squares the whole product, writing (2x)(2x) = 18, and stops at x^2 = 4.5; 6 is the value of y; 9 is the value of x^2, reported before taking the square root.

**Desmos** (not yet verified in Desmos). Type:<br><code>xy=18</code><br><code>y=2x</code>

The line crosses the two branches of xy = 18 at (-3, -6) and (3, 6). The condition x > 0 picks (3, 6); the value of x is 3.

</details>

---

### 16. adv-ne3-sqrt-plus-five-easy

*Easy · Multiple choice · route: hand-primary · techniques: T1*

What value of $x$ satisfies the equation $\sqrt{x} + 5 = 11$?

- **A.** $6$
- **B.** $36$
- **C.** $121$
- **D.** $256$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Subtracting 5 from both sides of the given equation yields sqrt(x) = 6. Squaring both sides yields x = 36. Check: sqrt(36) + 5 = 6 + 5 = 11. Therefore, x = 36. Distractors: 6 is the value of sqrt(x), not of x; 121 squares 11 and ignores the 5; 256 adds 5 to 11 instead of subtracting, sqrt(x) = 16, then squares.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{x}+5</code><br><code>y=11</code>

Two quick steps by hand, so Desmos is slower. As a check, zoom out until x = 36 is on screen and click the intersection: (36, 11).

</details>

---

### 17. adv-ne3-square-49-negative-root

*Easy · Multiple choice · route: hand-primary · techniques: T1*

If $x^2 = 49$ and $x < 0$, what is the value of $x$?

- **A.** $-49$
- **B.** $-24.5$
- **C.** $-7$
- **D.** $7$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that x^2 = 49. Taking the square root of both sides yields x = 7 or x = -7. It's also given that x < 0, so x = -7. Therefore, the value of x is -7. Distractors: -49 attaches a negative sign to 49 without taking the square root; -24.5 divides 49 by 2 instead of taking the square root; 7 is the positive root, which the condition x < 0 rules out.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2</code><br><code>y=49</code>

One step by hand, so Desmos is slower. As a check, zoom out until y = 49 is on screen: the line meets the parabola at (-7, 49) and (7, 49). The condition x < 0 picks -7.

</details>

---

### 18. adv-quadratic-negative-solution

*Easy · Multiple choice · route: desmos-primary · techniques: T1*

What is the negative solution to the equation $x^2 + 3x - 28 = 0$?

- **A.** $-28$
- **B.** $-7$
- **C.** $-4$
- **D.** $4$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Two numbers with product -28 and sum 3 are 7 and -4, so the left side factors as (x + 7)(x - 4). Setting each factor equal to 0 yields x = -7 or x = 4. Therefore, the negative solution is -7. Distractors: 4 is the positive solution; -4 is the solution 4 with its sign reversed; -28 is the constant term of the equation.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+3x-28</code>

Click the two x-intercepts of the parabola: (-7, 0) and (4, 0). The question asks for the negative one, so the answer is -7.

</details>

---

### 19. adv-radical-equation-coefficient

*Easy · Student-produced response · route: hand-primary · techniques: T1*

What is the solution to the equation $2\sqrt{x + 1} = 6$?

**Answer:** 8

<details><summary>Solutions</summary>

**By hand.** Dividing both sides of the given equation by 2 yields sqrt(x + 1) = 3. Squaring both sides yields x + 1 = 9, so x = 8. Checking: 2 · sqrt(9) = 6. Squaring before dividing, (2 sqrt(x + 1))^2 = 4(x + 1) = 36, gives the same answer, but squaring only the radical while keeping the 2, 2(x + 1) = 36, gives 17, which does not satisfy the equation.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2\sqrt{x+1}</code><br><code>y=6</code>

Click the single intersection: (8, 6). Isolating the radical by hand takes two steps, so Desmos is slower here.

</details>

---

### 20. adv-rational-equation-cross-multiply

*Easy · Student-produced response · route: desmos-primary · techniques: T1, T11*

What is the solution to the equation $\frac{3}{x - 2} = \frac{5}{x + 4}$?

**Answer:** 11

<details><summary>Solutions</summary>

**By hand.** Neither denominator is zero at the solution, so cross-multiplying yields 3(x + 4) = 5(x - 2), or 3x + 12 = 5x - 10. Subtracting 3x from and adding 10 to both sides yields 22 = 2x, so x = 11. Check: 3/9 = 1/3 and 5/15 = 1/3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{3}{x-2}</code><br><code>y=\frac{5}{x+4}</code>

The two curves cross once, at (11, 0.333); read x = 11. Zoom out: the crossing is to the right of both vertical asymptotes and off the default screen.

</details>

---

### 21. adv-rug-room-floor-strip

*Easy · Student-produced response · route: either · techniques: T1*

A square rug with side length $x$ feet lies in the center of a square room, leaving a strip of bare floor 3 feet wide along every wall. The floor of the room has an area of 324 square feet. What is the value of $x$?

**Answer:** 12

<details><summary>Solutions</summary>

**By hand.** The strip adds 3 feet on each of two opposite sides, so the room has side length x + 6 feet and floor area (x + 6)^2 = 324. Taking the positive square root (a length is positive) yields x + 6 = 18, so x = 12. A common slip is adding the strip only once (x + 3 = 18), which gives 15.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x+6)^2</code><br><code>y=324</code>

Click the intersection with positive x: (12, 324). The other intersection, x = -24, is not a length.

</details>

---

### 22. adv-square-equals-constant-greater-root

*Easy · Multiple choice · route: hand-primary · techniques: T1*

What is the greater of the two solutions to the equation $(x - 3)^2 = 25$?

- **A.** $2$
- **B.** $5$
- **C.** $8$
- **D.** $28$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Taking the square root of both sides of the given equation yields x - 3 = 5 or x - 3 = -5. Adding 3 to both sides of each yields x = 8 or x = -2. Therefore, the greater solution is 8. Distractors: 2 results from subtracting 3 from 5 instead of adding it; 5 is the square root of 25 without the 3 added back; 28 adds 3 to 25 without taking a square root.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x-3)^2</code><br><code>y=25</code>

Click the two intersections: (-2, 25) and (8, 25). The greater x-coordinate is 8. Taking the square root of both sides by hand is faster than graphing.

</details>

---

### 23. adv-square-isolate-positive-x

*Easy · Student-produced response · route: hand-primary · techniques: T1*

If $3x^2 + 5 = 80$ and $x > 0$, what is the value of $x$?

**Answer:** 5

<details><summary>Solutions</summary>

**By hand.** Subtracting 5 from both sides of the given equation yields 3x^2 = 75, and dividing both sides by 3 yields x^2 = 25. Taking square roots yields x = 5 or x = -5. It's given that x > 0, so x = 5. A common slip is dividing before subtracting (x^2 = 80/3 - 5), which does not give a perfect square.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x^2+5</code><br><code>y=80</code>

Isolating x^2 by hand takes two steps, so Desmos is slower here. As a check, the horizontal line meets the parabola at x = -5 and x = 5; take the positive one, 5.

</details>

---

### 24. adv-trinomial-larger-root-factor

*Easy · Multiple choice · route: either · techniques: T1*

The equation $x^2 - 13x + 36 = 0$ has two solutions. What is the larger solution?

- **A.** $4$
- **B.** $9$
- **C.** $13$
- **D.** $36$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Two numbers with a product of 36 and a sum of 13 are 4 and 9, so the given equation factors as (x - 4)(x - 9) = 0. Setting each factor equal to 0 yields x = 4 or x = 9. Therefore, the larger solution is 9. Distractors: 4 is the smaller solution; 13 is the sum of the solutions (the opposite of the x-coefficient); 36 is the product of the solutions (the constant term).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-13x+36</code>

The parabola crosses the x-axis at two points. Click both x-intercepts, (4, 0) and (9, 0), and take the larger x-value, 9.

</details>

---

### 25. adv-circle-line-no-solution

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

How many solutions $(x, y)$ does the system of equations $x^2 + y^2 = 9$ and $y = x + 5$ have?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Substituting x + 5 for y yields x^2 + (x + 5)^2 = 9, so 2x^2 + 10x + 16 = 0 and x^2 + 5x + 8 = 0. The discriminant is 25 - 32 = -7, which is negative, so there are no real solutions. Alternate approach: the circle has radius 3, and the closest point on the line to the origin is at distance 5/sqrt(2), about 3.54, which is greater than 3, so the line misses the circle. Distractors: Exactly one would require the discriminant to be 0 (a tangent line); Exactly two is the count for any line that passes within 3 units of the origin; Infinitely many would require the graphs to coincide, which a line and a circle cannot.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=9</code><br><code>y=x+5</code>

The circle of radius 3 and the line never meet: the line passes above and to the left of the circle. Zoom out to confirm there is no distant crossing; a line and a circle can meet at most twice, and here they meet zero times.

</details>

---

### 26. adv-circle-line-positive-x

*Medium · Student-produced response · route: desmos-primary · techniques: T2, T11*

In the $xy$-plane, the graphs of $x^2 + y^2 = 20$ and $y = 2x$ intersect at two points. One of these points has a positive $x$-coordinate. What is that $x$-coordinate?

**Answer:** 2

<details><summary>Solutions</summary>

**By hand.** Substituting 2x for y in the first equation yields x^2 + (2x)^2 = 20, so 5x^2 = 20 and x^2 = 4. Therefore, x = 2 or x = -2, and the positive x-coordinate is 2. A common slip is substituting 2x^2 instead of (2x)^2 = 4x^2, which gives 3x^2 = 20 and a non-integer value.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=20</code><br><code>y=2x</code>

Click the two intersection points: (2, 4) and (-2, -4). The one with positive x has x = 2. The values are exact integers, so no fraction toggle is needed.

</details>

---

### 27. adv-circle-line-which-point

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the circle with equation $(x - 2)^2 + (y + 1)^2 = 25$ and the line with equation $y = x - 2$ intersect at two points. Which of the following is one of these points?

- **A.** $(-5, -7)$
- **B.** $(-2, -4)$
- **C.** $(2, -1)$
- **D.** $(5, -3)$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting x - 2 for y in the circle's equation yields (x - 2)^2 + (x - 1)^2 = 25, so 2x^2 - 6x + 5 = 25, and x^2 - 3x - 10 = 0. This factors as (x - 5)(x + 2) = 0, so x = 5 or x = -2. Then y = x - 2 gives the points (5, 3) and (-2, -4). Therefore, (-2, -4) is one of the points. Distractors: (-5, -7) comes from factoring with the signs reversed, (x + 5)(x - 2), and is on the line but not the circle; (2, -1) is the center of the circle; (5, -3) has the correct x-coordinate with the sign of y flipped.

**Desmos** (not yet verified in Desmos). Type:<br><code>(x-2)^2+(y+1)^2=25</code><br><code>y=x-2</code>

Click the two intersection points: (-2, -4) and (5, 3). Only (-2, -4) appears among the choices.

</details>

---

### 28. adv-discriminant-zero-rearranged

*Medium · Multiple choice · route: either · techniques: T1*

How many distinct real solutions does the equation $4x^2 + 9 = 12x$ have?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Subtracting 12x from both sides yields 4x^2 - 12x + 9 = 0. A quadratic ax^2 + bx + c = 0 has exactly one real solution when b^2 - 4ac = 0. Here (-12)^2 - 4(4)(9) = 144 - 144 = 0, so there is exactly one real solution; indeed 4x^2 - 12x + 9 = (2x - 3)^2. Distractors: Zero comes from computing the discriminant of 4x^2 + 9 alone, forgetting to move 12x; Exactly two comes from adding 4ac instead of subtracting it; Infinitely many treats the equation as an identity.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=4x^2+9</code><br><code>y=12x</code>

The line touches the parabola at a single point, (1.5, 18), without crossing it: exactly one solution. Zoom in near the point to confirm there is not a second, nearby crossing.

</details>

---

### 29. adv-drone-distance-absolute-value

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

A drone flies along a straight path past a charging station. Its distance from the station, in meters, $t$ seconds after takeoff is $|3t - 45|$, for $0 \le t \le 30$. The drone is 15 meters from the station at two different times. What is the later of these times, in seconds?

- **A.** $5$
- **B.** $10$
- **C.** $15$
- **D.** $20$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Setting |3t - 45| = 15 gives two cases. 3t - 45 = 15 yields 3t = 60 and t = 20; 3t - 45 = -15 yields 3t = 30 and t = 10. Both are between 0 and 30. Therefore, the later time is 20 seconds. Distractors: 5 comes from dividing 15 by 3 and ignoring the 45; 10 is the earlier time; 15 is the time the drone is at the station.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left|3x-45\right|\left\{0\le x\le30\right\}</code><br><code>y=15</code>

Type t as x. The V (the absolute-value picture of T14) touches 0 at x = 15 and crosses y = 15 at (10, 15) and (20, 15). The later time is 20.

</details>

---

### 30. adv-exponential-equation-common-base

*Medium · Multiple choice · route: hand-primary · techniques: T1*

What is the solution to the equation $4^{2x + 1} = 8^{x - 2}$?

- **A.** $-8$
- **B.** $-3$
- **C.** $-\frac{7}{4}$
- **D.** $8$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Write both sides with base 2: 4^(2x+1) = 2^(4x+2) and 8^(x-2) = 2^(3x-6). Equal powers of the same base have equal exponents, so 4x + 2 = 3x - 6 and x = -8. Distractors: -3 sets the exponents equal without converting the bases (2x + 1 = x - 2); -7/4 swaps the conversions (3(2x + 1) = 2(x - 2)); 8 is a sign error in the final step.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=4^{2x+1}</code><br><code>y=8^{x-2}</code>

The curves cross at x = -8, where y is about 0.00003, so the intersection is invisible at normal zoom; zoom far in near the x-axis on the left, or graph y = 4^(2x+1) - 8^(x-2) and find its zero. Rewriting with base 2 by hand is much faster.

</details>

---

### 31. adv-exponential-product-same-base

*Medium · Multiple choice · route: hand-primary · techniques: T1*

What value of $x$ satisfies the equation $3^{x} \cdot 9^{x + 1} = 3^{11}$?

- **A.** $3$
- **B.** $\frac{10}{3}$
- **C.** $\frac{9}{2}$
- **D.** $5$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Since 9 = 3^2, 9^(x + 1) = 3^(2(x + 1)) = 3^(2x + 2). Multiplying powers of the same base adds the exponents, so the left side is 3^(x + 2x + 2) = 3^(3x + 2). Setting 3x + 2 = 11 yields x = 3. Distractors: 10/3 comes from distributing the 2 to x only, 3^(2x + 1); 9/2 comes from writing 9^(x + 1) as 3^(x + 2); 5 comes from adding the exponents x and x + 1 without changing the base 9 to 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3^{x}\cdot9^{x+1}</code><br><code>y=3^{11}</code>

Rewriting with base 3 is faster. As a check, the curve meets the horizontal line at x = 3; zoom out vertically, since 3^11 = 177,147.

</details>

---

### 32. adv-factored-cubic-sum-solutions

*Medium · Multiple choice · route: hand-primary · techniques: T1*

If $(x - 3)(x + 5)(2x - 1) = 0$, what is the sum of all possible values of $x$?

- **A.** $-3$
- **B.** $-\frac{3}{2}$
- **C.** $-1$
- **D.** $\frac{3}{2}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A product is zero when a factor is zero: x - 3 = 0 gives x = 3, x + 5 = 0 gives x = -5, and 2x - 1 = 0 gives x = 1/2. The sum is 3 + (-5) + 1/2 = -3/2. Distractors: -1 takes the third value as 1 (dropping the 2); -3 takes it as -1 (a sign slip); 3/2 flips the sign of every value (reading x - 3 = 0 as x = -3, and so on).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x-3)(x+5)(2x-1)</code>

Click the three x-intercepts: -5, 0.5 and 3; they add to -1.5. Reading the zeros from the factors by hand is faster.

</details>

---

### 33. adv-falling-object-solve-for-t

*Medium · Multiple choice · route: hand-primary · techniques: T9, T13*

An object is dropped from rest. The equation $d = 4.9t^2$ models its motion, where $d$ is the distance fallen, in meters, and $t$ is the time, in seconds, since the object was dropped. Which equation gives $t$ in terms of $d$, for $t > 0$?

- **A.** $t = \frac{d^2}{4.9}$
- **B.** $t = \frac{\sqrt{d}}{4.9}$
- **C.** $t = \sqrt{4.9d}$
- **D.** $t = \sqrt{\frac{d}{4.9}}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that d = 4.9t^2. Dividing both sides by 4.9 yields t^2 = d/4.9, and taking the positive square root (since t > 0) yields t = sqrt(d/4.9). Distractors: sqrt(d)/4.9 takes the square root of d alone before dividing; sqrt(4.9d) multiplies by 4.9 instead of dividing; d^2/4.9 squares instead of taking a square root.

**Desmos** (not yet verified in Desmos). Type:<br><code>d=19.6</code><br><code>t=\sqrt{\frac{d}{4.9}}</code><br><code>4.9t^2</code>

Pick a convenient d, such as 19.6 (so t should be 2). Define t by each choice in turn (T13) and check that 4.9t^2 returns 19.6; only the square root of d/4.9 does. Isolating t by hand is faster.

</details>

---

### 34. adv-garden-quadratic-perimeter

*Medium · Multiple choice · route: either · techniques: T2, T1*

A rectangular garden has an area of 12 square meters, and its length is 4 meters greater than its width. What is the perimeter, in meters, of the garden?

- **A.** $2$
- **B.** $6$
- **C.** $8$
- **D.** $16$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Let w be the width, in meters; the length is w + 4. The area equation is w(w + 4) = 12, so w^2 + 4w - 12 = 0 and (w + 6)(w - 2) = 0. Since w > 0, w = 2 and the length is 6. Therefore, the perimeter is 2(2 + 6) = 16 meters. Distractors: 2 is the width and 6 is the length; 8 is the sum of the length and the width, half the perimeter.

**Desmos** (not yet verified in Desmos). Type:<br><code>xy=12</code><br><code>x-y=4</code><br><code>2(x+y)</code>

Let x be the length and y the width; the hyperbola and the line meet at (6, 2) and at (-2, -6), and only the first has positive lengths. The perimeter is 2(6 + 2) = 16. Alternatively graph y = x(x + 4) and y = 12 and click the positive crossing at x = 2.

</details>

---

### 35. adv-horizon-distance-radical

*Medium · Multiple choice · route: hand-primary · techniques: T1*

The equation $D = 3.6\sqrt{h}$ estimates the distance to the horizon from a point above sea level, where $D$ is the distance, in kilometers, and $h$ is the height of the point, in meters. According to the model, at what height, in meters, is the distance to the horizon 18 kilometers?

- **A.** $5$
- **B.** $25$
- **C.** $64.8$
- **D.** $324$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Setting D = 18 yields 3.6 sqrt(h) = 18. Dividing both sides by 3.6 yields sqrt(h) = 5, and squaring both sides yields h = 25. Check: 3.6 sqrt(25) = 3.6 · 5 = 18. Therefore, the height is 25 meters. Distractors: 5 is the value of sqrt(h), not h; 64.8 comes from multiplying 18 by 3.6 instead of dividing; 324 comes from squaring 18 without first dividing by 3.6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3.6\sqrt{x}</code><br><code>y=18</code>

Dividing and squaring takes two steps, so Desmos is slower. As a check, type h as x; the curve meets y = 18 at x = 25.

</details>

---

### 36. adv-kinetic-energy-solve-v

*Medium · Multiple choice · route: hand-primary · techniques: T13*

The equation $E = \frac{1}{2}mv^2$ gives the kinetic energy $E$, in joules, of a moving object, where $m$ is the mass of the object, in kilograms, and $v$ is its speed, in meters per second. Which equation gives $v$ in terms of $E$ and $m$, for $v > 0$?

- **A.** $v = \frac{\sqrt{2E}}{m}$
- **B.** $v = \sqrt{\frac{E}{2m}}$
- **C.** $v = \sqrt{2Em}$
- **D.** $v = \sqrt{\frac{2E}{m}}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that E = (1/2)mv^2. Multiplying both sides by 2 yields 2E = mv^2, and dividing both sides by m yields v^2 = 2E/m. Since v > 0, taking the positive square root yields v = sqrt(2E/m). Distractors: v = sqrt(E/(2m)) divides by 2 instead of multiplying by 2; v = sqrt(2Em) multiplies by m instead of dividing; v = sqrt(2E)/m takes the square root of 2E alone and leaves m outside the radical.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{1}{2}\cdot2\cdot3^2</code><br><code>\sqrt{\frac{2\cdot9}{2}}</code>

Pick m = 2 and v = 3: the first line gives E = 9. The second line evaluates choice D with E = 9 and m = 2 and returns 3, the speed chosen. The other choices return different values. Rearranging by hand is faster.

</details>

---

### 37. adv-line-parabola-y-difference

*Medium · Student-produced response · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $y = 2x - 1$ and $y = x^2 - 4x + 4$ intersect at the points $(x_1, y_1)$ and $(x_2, y_2)$, where $x_1 < x_2$. What is the value of $y_2 - y_1$?

**Answer:** 8

<details><summary>Solutions</summary>

**By hand.** Setting the right-hand sides equal yields x^2 - 4x + 4 = 2x - 1, so x^2 - 6x + 5 = 0, which factors as (x - 1)(x - 5) = 0. So x\_1 = 1 and x\_2 = 5. Substituting into y = 2x - 1 yields y\_1 = 1 and y\_2 = 9. Therefore, y\_2 - y\_1 = 8. A common slip is reporting x\_2 - x\_1 = 4, the difference of the x-coordinates.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x-1</code><br><code>y=x^2-4x+4</code>

Click the two intersection points: (1, 1) and (5, 9). The point with the larger x-coordinate has y = 9, so y\_2 - y\_1 = 9 - 1 = 8.

</details>

---

### 38. adv-ne2-cabin-rental-group-size

*Medium · Multiple choice · route: either · techniques: T1*

A group of people splits the 360.00 dollar cost of renting a cabin equally. If 3 more people joined the group, each person would pay 6.00 dollars less. How many people are in the group?

- **A.** $30$
- **B.** $24$
- **C.** $15$
- **D.** $12$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** If n people are in the group, each pays 360/n dollars, and with 3 more people each would pay 360/(n + 3) dollars, so 360/n - 360/(n + 3) = 6. Multiplying both sides by n(n + 3) yields 360(n + 3) - 360n = 6n(n + 3), or 1,080 = 6n^2 + 18n. Dividing by 6 and rearranging yields n^2 + 3n - 180 = 0, which factors as (n + 15)(n - 12) = 0. Since n is positive, n = 12. Check: 360/12 = 30 and 360/15 = 24 differ by 6. Distractors: 30 is each person's share, in dollars, not the number of people; 24 is each share after 3 more join; 15 is the size of the larger group.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{360}{x}-\frac{360}{x+3}</code><br><code>y=6</code>

Write the equation first (n people pay 360/n each). The curve meets y = 6 at x = 12 and, on the far left, at x = -15; a number of people is positive, so take 12.

</details>

---

### 39. adv-ne2-catapult-balloon-height

*Medium · Student-produced response · route: desmos-primary · techniques: T2*

A toy catapult launches a pebble upward. Its height, in meters, $t$ seconds after launch is $-5t^2 + 25t$. At that moment a balloon starts rising from a platform, and its height, in meters, is $5t + 15$. What is the height, in meters, of the pebble the second time it is level with the balloon?

**Answer:** 30

<details><summary>Solutions</summary>

**By hand.** The pebble is level with the balloon when -5t^2 + 25t = 5t + 15. Rearranging yields 5t^2 - 20t + 15 = 0, or t^2 - 4t + 3 = 0, which factors as (t - 1)(t - 3) = 0. The second time is t = 3, when the height is 5(3) + 15 = 30 meters. Check: -5(9) + 25(3) = 30.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-5x^2+25x</code><br><code>y=5x+15</code>

Click both intersections: (1, 20) and (3, 30). The second time is x = 3; enter its y-coordinate, 30, not the time.

</details>

---

### 40. adv-ne2-complete-square-lesser

*Medium · Multiple choice · route: hand-primary · techniques: T1, T13*

What is the lesser of the two solutions to the equation $x^2 + 8x = 5$?

- **A.** $-4 - \sqrt{21}$
- **B.** $-4 + \sqrt{11}$
- **C.** $4 - \sqrt{21}$
- **D.** $4 + \sqrt{11}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Adding (8/2)^2 = 16 to both sides of the given equation yields x^2 + 8x + 16 = 21, or (x + 4)^2 = 21. So x + 4 = sqrt(21) or x + 4 = -sqrt(21), and x = -4 + sqrt(21) or x = -4 - sqrt(21). Therefore, the lesser solution is -4 - sqrt(21). Distractors: -4 + sqrt(11) subtracts 5 from 16 instead of adding 5 to 16; 4 - sqrt(21) writes (x - 4)^2, the wrong sign for half of 8; 4 + sqrt(11) makes both mistakes.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+8x</code><br><code>y=5</code><br><code>-4-\sqrt{21}</code>

Completing the square takes two lines, so Desmos is slower. As a check, the left intersection of the parabola and y = 5 is at x about -8.583, and the line -4-\sqrt{21} (T13) also shows -8.583.

</details>

---

### 41. adv-ne2-difference-of-squares-system-y

*Medium · Multiple choice · route: hand-primary · techniques: T2, T11*

If $x^2 - y^2 = 24$ and $x + y = 8$, what is the value of $y$?

- **A.** $\frac{5}{2}$
- **B.** $3$
- **C.** $\frac{11}{2}$
- **D.** $16$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Since x^2 - y^2 = (x + y)(x - y), substituting 8 for x + y yields 8(x - y) = 24, so x - y = 3. Adding x + y = 8 and x - y = 3 yields 2x = 11, so x = 11/2, and then y = 8 - 11/2 = 5/2. Distractors: 3 is the value of x - y, an intermediate result; 11/2 is the value of x, not of y; 16 subtracts 8 from 24 as if the equations could be combined like linear ones.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2-y^2=24</code><br><code>x+y=8</code>

Factoring finishes in two lines, so Desmos is slower. As a check, the line meets the hyperbola once, at (5.5, 2.5); the fraction toggle (T11) turns 2.5 into 5/2.

</details>

---

### 42. adv-ne2-exponential-line-count

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, how many points do the graphs of $y = 3^x$ and $y = x + 2$ have in common?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Substituting x = 1 yields 3^1 = 3 and 1 + 2 = 3, so (1, 3) is a common point. At x = -2, 3^(-2) = 1/9 is greater than -2 + 2 = 0, and at x = -1, 3^(-1) = 1/3 is less than -1 + 2 = 1, so the graphs also cross between x = -2 and x = -1. A curve that bends upward everywhere, like y = 3^x, can cross a line at most twice, so there are exactly two common points. Distractors: Zero assumes an exponential and a line can't meet because the equation 3^x = x + 2 can't be solved by algebra; Exactly one stops after finding (1, 3) and misses the crossing at negative x; Infinitely many confuses two crossings with graphs that coincide.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3^x</code><br><code>y=x+2</code>

Two gray intersection points appear: (1, 3) and about (-1.872, 0.128). Zoom out to confirm there are no others: far left, 3^x stays positive while the line drops below 0; right of x = 1 the curve stays above the line. Exactly two.

</details>

---

### 43. adv-ne2-hyperbola-line-other-point

*Medium · Multiple choice · route: either · techniques: T2*

In the $xy$-plane, the graphs of $y = \frac{k}{x}$ and $y = x + c$ intersect at $(3, 2)$ and at one other point, where $k$ and $c$ are constants. What is the $y$-coordinate of the other point?

- **A.** $-3$
- **B.** $-2$
- **C.** $-1$
- **D.** $6$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Since (3, 2) lies on both graphs, 2 = k/3 and 2 = 3 + c, so k = 6 and c = -1. Setting 6/x = x - 1 and multiplying both sides by x yields x^2 - x - 6 = 0, which factors as (x - 3)(x + 2) = 0. The other point has x = -2 and y = -2 - 1 = -3. Distractors: -2 is the x-coordinate of the other point, not the y-coordinate; -1 is the value of c; 6 is the value of k.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{6}{x}</code><br><code>y=x-1</code>

First find k = 6 and c = -1 from the given point (one line each), then graph. The line meets the hyperbola at (3, 2) and (-2, -3); read the y-coordinate of the other point, -3.

</details>

---

### 44. adv-ne2-illuminance-solve-distance

*Medium · Multiple choice · route: hand-primary · techniques: —*

The illuminance $E$, in lux, on a surface near a small lamp is given by $E = \frac{k}{d^2}$, where $d$ is the distance, in meters, from the lamp and $k$ is a positive constant. Which equation gives $d$ in terms of $E$ and $k$?

- **A.** $d = \sqrt{kE}$
- **B.** $d = \sqrt{\frac{E}{k}}$
- **C.** $d = \frac{\sqrt{k}}{E}$
- **D.** $d = \sqrt{\frac{k}{E}}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that E = k/d^2. Multiplying both sides by d^2 yields Ed^2 = k, and dividing both sides by E yields d^2 = k/E. Since d is a distance, it is positive, so d = sqrt(k/E). Distractors: d = sqrt(kE) multiplies by E instead of dividing; d = sqrt(E/k) inverts the ratio; d = sqrt(k)/E takes the square root of k but not of E.

</details>

---

### 45. adv-ne2-irrational-negative-solution

*Medium · Multiple choice · route: either · techniques: T1, T13*

What is the negative solution to the equation $3x^2 - 6x - 2 = 0$?

- **A.** $-1 - \frac{\sqrt{15}}{3}$
- **B.** $1 - \frac{2\sqrt{15}}{3}$
- **C.** $1 - \frac{\sqrt{15}}{3}$
- **D.** $1 - \frac{\sqrt{15}}{6}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Using the quadratic formula with a = 3, b = -6 and c = -2, the discriminant is (-6)^2 - 4(3)(-2) = 36 + 24 = 60, and sqrt(60) = 2 sqrt(15). So x = (6 ± 2 sqrt(15))/6 = 1 ± sqrt(15)/3. Since sqrt(15)/3 is about 1.29, the negative solution is 1 - sqrt(15)/3, about -0.29. Distractors: -1 - sqrt(15)/3 uses b instead of -b; 1 - 2 sqrt(15)/3 divides the radical term by a = 3 instead of 2a = 6; 1 - sqrt(15)/6 simplifies sqrt(60) as sqrt(15), dropping the factor 2 (and isn't even negative).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x^2-6x-2</code><br><code>-1-\frac{\sqrt{15}}{3}</code><br><code>1-\frac{2\sqrt{15}}{3}</code><br><code>1-\frac{\sqrt{15}}{3}</code><br><code>1-\frac{\sqrt{15}}{6}</code>

Click the negative x-intercept: x is about -0.291. Then compare it with the values beside the four choice lines (T13): only 1 - sqrt(15)/3 is -0.291.

</details>

---

### 46. adv-ne2-library-collections-later-time

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

A library's e-book collection has $1000(1.1)^t$ titles and its audiobook collection has $900 + 150t$ titles, where $t$ is the number of months since both opened. The collections have the same number of titles at two different times. To the nearest tenth, what is the later of these times, in months?

- **A.** $2.0$
- **B.** $2.3$
- **C.** $4.7$
- **D.** $7.0$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The equation 1000(1.1)^t = 900 + 150t can't be solved with algebra alone, so test whole-number values of t, finding powers of 1.1 by repeated multiplication. At t = 7, 1000(1.1)^7 is about 1,948.7 and 900 + 150(7) = 1,950, so the audiobooks are barely ahead; at t = 8, 1000(1.1)^8 is about 2,143.6 and 900 + 150(8) = 2,100, so the e-books are ahead. The later crossing is therefore between 7 and 8, and since the gap at t = 7 (about 1.3 titles) is tiny next to the gap at t = 8 (about 43.6 titles), it lies just above 7 (about 7.04). Of the choices, only 7.0 is in that range, so to the nearest tenth the later time is 7.0 months. Distractors: 2.0 treats 10% growth as simple growth, 1000 + 100t = 900 + 150t; 2.3 is the earlier time; 4.7 is the time between the two crossings.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=1000(1.1)^x</code><br><code>y=900+150x</code>

Zoom out to about x from 0 to 10 and y from 0 to 2500, then click both intersections: about (2.303, 1245) and (7.036, 1955). The later time is 7.036, which rounds to 7.0.

</details>

---

### 47. adv-ne2-quartic-in-form-greatest

*Medium · Multiple choice · route: either · techniques: T1*

What is the greatest solution to the equation $x^4 - 11x^2 + 18 = 0$?

- **A.** $2$
- **B.** $3$
- **C.** $9$
- **D.** $11$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since x^4 = (x^2)^2, letting u = x^2 turns the given equation into u^2 - 11u + 18 = 0, which factors as (u - 2)(u - 9) = 0. So x^2 = 2 or x^2 = 9, which gives x = ±sqrt(2) or x = ±3. Therefore, the greatest solution is 3. Distractors: 2 is the smaller value of u = x^2, not a value of x; 9 is the larger value of u, not of x; 11 is the sum of the two values of u.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^4-11x^2+18</code>

The graph crosses the x-axis four times, at about -3, -1.414, 1.414 and 3. The greatest x-intercept is 3.

</details>

---

### 48. adv-ne2-rational-two-fractions-positive

*Medium · Multiple choice · route: either · techniques: T1*

What is the positive solution to the equation $\frac{2}{x} + \frac{3}{x + 2} = 1$?

- **A.** $1$
- **B.** $\frac{3}{2}$
- **C.** $4$
- **D.** $5$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the given equation by x(x + 2), where x ≠ 0 and x ≠ -2, yields 2(x + 2) + 3x = x(x + 2), or 5x + 4 = x^2 + 2x. Rearranging yields x^2 - 3x - 4 = 0, which factors as (x - 4)(x + 1) = 0. So x = 4 or x = -1; neither is an excluded value, and the positive solution is 4. Distractors: 1 comes from the sign slip (x + 4)(x - 1) = 0; 3/2 adds the fractions straight across, as 5/(2x + 2) = 1; 5 treats both denominators as x, as 5/x = 1.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{2}{x}+\frac{3}{x+2}</code><br><code>y=1</code>

Zoom out to see both branches: the curve meets y = 1 at x = -1 and x = 4. The positive solution is 4.

</details>

---

### 49. adv-ne2-two-radicals-quadratic-radicand

*Medium · Student-produced response · route: either · techniques: T1*

What is the solution to the equation $\sqrt{x^2 - 8} = \sqrt{2x}$?

**Answer:** 4

<details><summary>Solutions</summary>

**By hand.** Squaring both sides of the given equation yields x^2 - 8 = 2x, so x^2 - 2x - 8 = 0, which factors as (x - 4)(x + 2) = 0. So x = 4 or x = -2. For x = -2, x^2 - 8 = -4 and 2x = -4, so neither square root is a real number and -2 is extraneous. For x = 4, both sides equal sqrt(8). Therefore, the solution is 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{x^2-8}</code><br><code>y=\sqrt{2x}</code>

The curves meet once, at about (4, 2.828). Neither curve exists at x = -2, so the extraneous root never appears. Enter the x-coordinate, 4.

</details>

---

### 50. adv-ne3-absolute-quadratic-four-count

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

How many real solutions does the equation $|x^2 - 5| = 4$ have?

- **A.** Exactly one
- **B.** Exactly two
- **C.** Exactly three
- **D.** Exactly four

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** An absolute value equals 4 when the expression inside equals 4 or -4. If x^2 - 5 = 4, then x^2 = 9, so x = 3 or x = -3. If x^2 - 5 = -4, then x^2 = 1, so x = 1 or x = -1. All four values are distinct, so the equation has exactly four real solutions. Distractors: Exactly one keeps only x = 3 from the positive case; Exactly two drops the case x^2 - 5 = -4; Exactly three takes both roots in one case but only the positive root in the other.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=|x^2-5|</code><br><code>y=4</code>

This is the absolute-value counting picture (T14): the parabola's part below the x-axis is reflected up, giving a W shape whose middle peak is (0, 5). The line y = 4 sits below that peak, so it crosses the W four times, at x = -3, -1, 1 and 3.

</details>

---

### 51. adv-ne3-auditorium-rows-seats

*Medium · Student-produced response · route: either · techniques: T1*

Each row of an auditorium has 8 more seats than the number of rows, and the auditorium seats 384 people in all. How many rows of seats does the auditorium have?

**Answer:** 16

<details><summary>Solutions</summary>

**By hand.** Let r be the number of rows. Each row has r + 8 seats, so the total number of seats is r(r + 8) = 384. Rearranging yields r^2 + 8r - 384 = 0, which factors as (r - 16)(r + 24) = 0, so r = 16 or r = -24. The number of rows must be positive, so r = 16. Check: 16 rows of 24 seats is 384 seats. Therefore, the auditorium has 16 rows. A common slip is to report 24, the number of seats in each row.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x(x+8)</code><br><code>y=384</code>

Here x is the number of rows. Zoom out until y = 384 is on screen. The line meets the parabola at x = -24 and x = 16. A number of rows must be positive, so enter 16.

</details>

---

### 52. adv-ne3-circles-external-tangent-count

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, how many points do the circles $x^2 + y^2 = 9$ and $(x - 5)^2 + y^2 = 4$ have in common?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Exactly four

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The first circle has center (0, 0) and radius 3; the second has center (5, 0) and radius 2. The distance between the centers is 5, which equals the sum of the radii, 3 + 2, so the circles touch at exactly one point. Algebraically, subtracting the second equation from the first yields x^2 - (x - 5)^2 = 5, or 10x - 25 = 5, so x = 3; then y^2 = 9 - 9 = 0 gives only (3, 0). Therefore, the circles have exactly one point in common. Distractors: Zero treats circles whose centers are 5 apart as too far apart to meet; Exactly two assumes that two overlapping-looking circles always cross twice; Exactly four counts the largest number of solutions a system of two second-degree equations can have.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=9</code><br><code>(x-5)^2+y^2=4</code>

The two circles touch at (3, 0). Zoom in near (3, 0) to confirm that they touch rather than cross or miss: exactly one common point.

</details>

---

### 53. adv-ne3-f-equals-f-double-quadratic

*Medium · Student-produced response · route: either · techniques: T1*

If $f(x) = x^2 - 6x + 10$, what is the nonzero value of $x$ such that $f(x) = f(2x)$?

**Answer:** 2

<details><summary>Solutions</summary>

**By hand.** Substituting 2x for x in f yields f(2x) = (2x)^2 - 6(2x) + 10 = 4x^2 - 12x + 10. Setting f(x) = f(2x) yields x^2 - 6x + 10 = 4x^2 - 12x + 10. Subtracting the left side from both sides yields 3x^2 - 6x = 0, or 3x(x - 2) = 0, so x = 0 or x = 2. Therefore, the nonzero value of x is 2. Check: f(2) = 2 and f(4) = 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=x^2-6x+10</code><br><code>y=f(x)</code><br><code>y=f(2x)</code>

The two parabolas meet at (0, 10) and (2, 2). The nonzero x-coordinate is 2. Enter 2.

</details>

---

### 54. adv-ne3-given-root-other-fraction

*Medium · Student-produced response · route: hand-primary · techniques: T4, T11*

The equation $3x^2 + kx - 20 = 0$, where $k$ is a constant, is true when $x = -4$. What other value of $x$ makes the equation true?

**Answer:** 5/3 (≈ 1.667)

<details><summary>Solutions</summary>

**By hand.** Substituting -4 for x in the given equation yields 3(16) + k(-4) - 20 = 0, or 28 - 4k = 0, so k = 7. The equation is 3x^2 + 7x - 20 = 0, which factors as (3x - 5)(x + 4) = 0, so x = 5/3 or x = -4. Therefore, the other value of x is 5/3. Alternate approach: the product of the solutions of ax^2 + bx + c = 0 is c/a = -20/3, so the other solution is (-20/3)/(-4) = 5/3, without finding k.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x^2+kx-20</code>

The product of the roots gives the answer by hand in seconds, so Desmos is slower. As a check, add a slider for k and set k = 7 (the value that makes x = -4 an x-intercept). The other x-intercept reads 1.667. It is not a terminating decimal: enter the fraction 5/3 (fraction toggle, T11) or the full-width decimal 1.666 or 1.667.

</details>

---

### 55. adv-ne3-line-parabola-second-point-y

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $y = x^2 - 2x + 3$ and $y = 2x + 3$ meet at $(0, 3)$ and at one other point. What is the $y$-coordinate of that other point?

- **A.** $3$
- **B.** $4$
- **C.** $8$
- **D.** $11$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Setting the right sides equal yields x^2 - 2x + 3 = 2x + 3, or x^2 - 4x = 0. Factoring yields x(x - 4) = 0, so x = 0 or x = 4. The point with x = 0 is the given point (0, 3), so the other point has x = 4. Substituting 4 for x in y = 2x + 3 yields y = 2(4) + 3 = 11. Therefore, the y-coordinate of the other point is 11. Distractors: 3 is the y-coordinate of the given point; 4 is the x-coordinate of the other point; 8 evaluates only 2x at x = 4 and drops the + 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-2x+3</code><br><code>y=2x+3</code>

Click the two gray intersection points: (0, 3) and (4, 11). The other point is (4, 11); its y-coordinate is 11. Read the y-coordinate, not the x-coordinate.

</details>

---

### 56. adv-ne3-meeting-handshakes

*Medium · Multiple choice · route: either · techniques: T1*

At a meeting, each of the $n$ people present shakes hands with every other person exactly once, for a total of $\frac{n(n - 1)}{2}$ handshakes. If there are 45 handshakes in all, how many people are at the meeting?

- **A.** $9$
- **B.** $10$
- **C.** $45$
- **D.** $90$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** It's given that n(n - 1)/2 = 45. Multiplying both sides by 2 yields n(n - 1) = 90, or n^2 - n - 90 = 0. Factoring yields (n - 10)(n + 9) = 0, so n = 10 or n = -9. The number of people must be positive, so n = 10. Therefore, 10 people are at the meeting. Distractors: 9 is the value of n - 1, the number of hands each person shakes; 45 is the number of handshakes; 90 is the value of n(n - 1), reported before solving for n.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x(x-1)}{2}</code><br><code>y=45</code>

Zoom out until y = 45 is on screen. The line meets the parabola at x = -9 and x = 10. A number of people must be positive, so there are 10 people.

</details>

---

### 57. adv-ne3-one-ninth-base-three

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

What is the solution to the equation $\left(\frac{1}{9}\right)^{x} = 3^{x + 6}$?

- **A.** $6$
- **B.** $2$
- **C.** $-2$
- **D.** $-3$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Since 1/9 = 3^(-2), the left side is (3^(-2))^x = 3^(-2x). The equation becomes 3^(-2x) = 3^(x + 6), so -2x = x + 6. Subtracting x from both sides yields -3x = 6, so x = -2. Therefore, the solution is -2. Distractors: 6 ignores the reciprocal and writes (1/9)^x as 3^(2x), so 2x = x + 6; 2 makes a sign slip in the last step, dividing 6 by 3 instead of by -3; -3 writes 1/9 as 3^(-1), so -x = x + 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left(\frac{1}{9}\right)^x</code><br><code>y=3^{x+6}</code>

Click the intersection of the falling and rising curves: (-2, 81). Zoom out vertically if the point is off-screen. The solution is the x-coordinate, -2.

</details>

---

### 58. adv-ne3-podcast-base-four-weeks

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

The number of downloads of a new podcast is modeled by $N = 25 \cdot 4^{\frac{t}{2}}$, where $t$ is the number of weeks since the podcast launched. According to the model, how many weeks after launch will the podcast reach 1,600 downloads?

- **A.** $1.5$
- **B.** $3$
- **C.** $6$
- **D.** $12$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that N = 25 \* 4^(t/2) and N = 1,600. Dividing both sides of 1,600 = 25 \* 4^(t/2) by 25 yields 4^(t/2) = 64. Since 64 = 4^3, it follows that t/2 = 3, so t = 6. Therefore, the podcast reaches 1,600 downloads 6 weeks after launch. Distractors: 1.5 divides 3 by 2 instead of multiplying; 3 is the value of t/2, not of t; 12 writes 64 as 2^6, treating the base 4 as 2, and then doubles 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=25\cdot4^{\frac{x}{2}}</code><br><code>y=1600</code>

Zoom out until y = 1600 is on screen and click the intersection: (6, 1600). The podcast reaches 1,600 downloads 6 weeks after launch.

</details>

---

### 59. adv-ne3-product-sum-squares

*Medium · Multiple choice · route: hand-primary · techniques: T2*

If $xy = 12$ and $x + y = 7$, what is the value of $x^2 + y^2$?

- **A.** $25$
- **B.** $37$
- **C.** $49$
- **D.** $73$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Squaring x + y = 7 yields x^2 + 2xy + y^2 = 49. It's given that xy = 12, so 2xy = 24. Subtracting 24 from both sides yields x^2 + y^2 = 25. Therefore, the value of x^2 + y^2 is 25. Distractors: 37 subtracts xy instead of 2xy; 49 is (x + y)^2, which still contains the 2xy term; 73 adds 2xy instead of subtracting it.

**Desmos** (not yet verified in Desmos). Type:<br><code>xy=12</code><br><code>x+y=7</code>

The identity is faster by hand. As a check, the graphs meet at (3, 4) and (4, 3); either point gives x^2 + y^2 = 9 + 16 = 25.

</details>

---

### 60. adv-ne3-quadratic-formula-expression

*Medium · Multiple choice · route: either · techniques: T1, T13*

Which expression gives the solutions to the equation $x^2 - 6x + 4 = 0$?

- **A.** $3 \pm \sqrt{5}$
- **B.** $3 \pm \sqrt{13}$
- **C.** $-3 \pm \sqrt{5}$
- **D.** $6 \pm 2\sqrt{5}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Completing the square: subtracting 4 from both sides yields x^2 - 6x = -4. Adding 9 to both sides yields x^2 - 6x + 9 = 5, or (x - 3)^2 = 5. Taking square roots yields x - 3 = ±sqrt(5), so x = 3 ± sqrt(5). Therefore, the solutions are given by 3 ± sqrt(5). Alternate approach: the quadratic formula gives x = (6 ± sqrt(36 - 16))/2 = (6 ± 2sqrt(5))/2 = 3 ± sqrt(5). Distractors: 3 ± sqrt(13) adds 4 to the 9 instead of subtracting it when completing the square; -3 ± sqrt(5) uses b = 6 instead of -b = 6 for the center; 6 ± 2sqrt(5) forgets to divide by 2a = 2 in the quadratic formula.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-6x+4</code><br><code>3+\sqrt{5}</code><br><code>3-\sqrt{5}</code>

Click the two x-intercepts of the parabola: about 0.764 and 5.236. Typing each choice (T13) shows that 3 + sqrt(5) = 5.236 and 3 - sqrt(5) = 0.764 match; the other choices do not.

</details>

---

### 61. adv-ne3-train-braking-domain

*Medium · Multiple choice · route: either · techniques: T1*

A subway train brakes to a stop. Its distance, in meters, from its stopping point $t$ seconds after braking begins is $3(12 - t)^2$, for $0 \le t \le 12$. How many seconds after braking begins is the train 75 meters from its stopping point?

- **A.** $7$
- **B.** $12$
- **C.** $17$
- **D.** $25$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that 3(12 - t)^2 = 75. Dividing both sides by 3 yields (12 - t)^2 = 25, so 12 - t = 5 or 12 - t = -5. These yield t = 7 or t = 17. The model applies only for 0 ≤ t ≤ 12, so t = 7. Therefore, the train is 75 meters from its stopping point 7 seconds after braking begins. Distractors: 12 is the time at which the train stops; 17 is the root outside the model's interval; 25 is the value of (12 - t)^2, not of t.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3(12-x)^2</code><br><code>y=75</code>

Zoom out until y = 75 is on screen. The line meets the parabola at x = 7 and x = 17. Only times from 0 to 12 are in the model, so the answer is 7.

</details>

---

### 62. adv-one-solution-leading-k

*Medium · Student-produced response · route: hand-primary · techniques: T4*

The equation $kx^2 + 12x + 9 = 0$, where $k$ is a nonzero constant, has exactly one real solution. What is the value of $k$?

**Answer:** 4

<details><summary>Solutions</summary>

**By hand.** A quadratic equation ax^2 + bx + c = 0 has exactly one real solution when its discriminant b^2 - 4ac equals 0. Here 12^2 - 4(k)(9) = 144 - 36k = 0, so k = 4. Alternate approach: a perfect square (2x + 3)^2 = 4x^2 + 12x + 9 matches the equation when k = 4. A sign slip, 144 + 36k = 0, gives -4, for which the equation has two real solutions.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=kx^2+12x+9</code><br><code>k=4</code>

Add a slider for k and drag it until the parabola touches the x-axis at a single point; that happens at k = 4. Setting the discriminant to 0 by hand is faster than tuning the slider.

</details>

---

### 63. adv-parabola-line-y-product

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $y = x^2 - 3x - 4$ and $y = 2x + 10$ intersect at two points. What is the product of the $y$-coordinates of these two points?

- **A.** $-144$
- **B.** $-14$
- **C.** $30$
- **D.** $144$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Set equal: x^2 - 5x - 14 = 0, so (x - 7)(x + 2) = 0 and x = 7 or x = -2. Then y = 24 and y = 6, product 144. Distractors: -14 is the product of the x-coordinates, 30 is the sum of the y-coordinates, -144 is a sign error.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-3x-4</code><br><code>y=2x+10</code>

Click the intersections: (-2, 6) and (7, 24). The product is 6 · 24 = 144.

</details>

---

### 64. adv-pendulum-solve-for-length

*Medium · Multiple choice · route: hand-primary · techniques: T13*

The equation $T = 2\pi\sqrt{\frac{L}{g}}$ gives the period $T$, in seconds, of a pendulum of length $L$ meters, where $g$ is a positive constant. Which equation gives $L$ in terms of $T$ and $g$?

- **A.** $L = \frac{T^2}{4\pi^2 g}$
- **B.** $L = \frac{gT^2}{4\pi^2}$
- **C.** $L = \frac{gT}{2\pi}$
- **D.** $L = \frac{4\pi^2 g}{T^2}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** It's given that T = 2π sqrt(L/g). Dividing both sides by 2π yields T/(2π) = sqrt(L/g). Squaring both sides yields T^2/(4π^2) = L/g. Multiplying both sides by g yields L = (gT^2)/(4π^2). Distractors: L = (T^2)/(4π^2 g) divides by g instead of multiplying (it treats g as if it were in the numerator of L/g); L = (gT)/(2π) forgets to square after dividing by 2π; L = (4π^2 g)/(T^2) inverts the fraction when clearing the square root.

**Desmos** (not yet verified in Desmos). Type:<br><code>g=9.8</code><br><code>L=2</code><br><code>T=2\pi\sqrt{\frac{L}{g}}</code><br><code>\frac{gT^2}{4\pi^2}</code>

Pick numbers (T13): with g = 9.8 and L = 2, the third line gives T ≈ 2.838. Type each choice's right-hand side as its own line; only gT^2/(4π^2) returns 2, the L that was chosen. Isolating L by hand takes two steps and is faster.

</details>

---

### 65. adv-product-of-solutions-noninteger

*Medium · Multiple choice · route: hand-primary · techniques: T1, T11*

What is the product of the solutions to the equation $3x^2 - 10x - 4 = 0$?

- **A.** $-4$
- **B.** $-\frac{4}{3}$
- **C.** $\frac{4}{3}$
- **D.** $\frac{10}{3}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** For a quadratic equation ax^2 + bx + c = 0 with two solutions, the product of the solutions is c/a. The discriminant (-10)^2 - 4(3)(-4) = 148 is positive, so the given equation has two real solutions, and their product is -4/3. Distractors: -4 is the constant term, forgetting to divide by a = 3; 4/3 drops the sign of c; 10/3 is the sum of the solutions, -b/a.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x^2-10x-4</code>

The relationship between coefficients and solutions is faster. As a check, click both x-intercepts (about -0.361 and 3.694) and multiply them in a new line; the product is -1.333, which the fraction toggle (T11) shows as -4/3.

</details>

---

### 66. adv-quadratic-formula-positive-radical

*Medium · Multiple choice · route: either · techniques: T1, T13*

What is the positive solution to the equation $x^2 + 4x - 6 = 0$?

- **A.** $-2 + \sqrt{10}$
- **B.** $-4 + 2\sqrt{10}$
- **C.** $-2 + 2\sqrt{10}$
- **D.** $2 + \sqrt{10}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The given equation doesn't factor over the integers, so use the quadratic formula with a = 1, b = 4 and c = -6. The discriminant is 4^2 - 4(1)(-6) = 40, and sqrt(40) = 2 sqrt(10). Then x = (-4 ± 2 sqrt(10))/2 = -2 ± sqrt(10). Since sqrt(10) is about 3.16, the positive solution is -2 + sqrt(10). Alternate approach: completing the square gives (x + 2)^2 = 10. Distractors: -4 + 2 sqrt(10) forgets to divide the numerator by 2a = 2; -2 + 2 sqrt(10) divides -b by 2 but not the radical; 2 + sqrt(10) uses b instead of -b.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+4x-6</code><br><code>-2+\sqrt{10}</code><br><code>-4+2\sqrt{10}</code><br><code>-2+2\sqrt{10}</code><br><code>2+\sqrt{10}</code>

Click the positive x-intercept: x is about 1.162. Then type each choice as its own line (T13) and compare: only -2 + sqrt(10) evaluates to 1.162.

</details>

---

### 67. adv-radical-equals-x-extraneous

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

What is the solution to the equation $\sqrt{5x + 6} = x$?

- **A.** $-6$
- **B.** $-1$
- **C.** $1$
- **D.** $6$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Squaring both sides of the given equation yields 5x + 6 = x^2, so x^2 - 5x - 6 = 0, which factors as (x - 6)(x + 1) = 0. This gives x = 6 or x = -1. Checking x = -1: sqrt(5(-1) + 6) = sqrt(1) = 1, not -1, so -1 is extraneous. Checking x = 6: sqrt(36) = 6. Therefore, the solution is 6. Distractors: -1 is the extraneous root kept without checking; -6 and 1 come from factoring with the signs reversed, (x + 6)(x - 1).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{5x+6}</code><br><code>y=x</code>

The square-root curve and the line cross once, at (6, 6). There is no crossing at x = -1, because the curve is never below the x-axis; the graph discards the extraneous root for free.

</details>

---

### 68. adv-raffle-price-revenue

*Medium · Multiple choice · route: either · techniques: T1*

A club sells raffle tickets and expects to sell $200 - 10p$ tickets, where $p$ is the price of one ticket, in dollars. The expected revenue (the price times the number of tickets sold) is 750.00 dollars at two different prices. What is the higher of these prices, in dollars?

- **A.** $5$
- **B.** $10$
- **C.** $15$
- **D.** $20$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Revenue is price times number sold, so p(200 - 10p) = 750. Expanding yields 200p - 10p^2 = 750, so 10p^2 - 200p + 750 = 0, and dividing by 10 yields p^2 - 20p + 75 = 0. This factors as (p - 5)(p - 15) = 0, so p = 5 or p = 15. Therefore, the higher price is 15 dollars. Distractors: 5 is the lower price; 10 is the price that maximizes revenue, halfway between the two prices; 20 is the price at which no tickets are sold.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x(200-10x)</code><br><code>y=750</code>

Type p as x. The horizontal line crosses the revenue parabola at (5, 750) and (15, 750); the higher price is 15.

</details>

---

### 69. adv-rational-common-denominator-extraneous

*Medium · Student-produced response · route: desmos-primary · techniques: T1*

What is the solution to the equation $\frac{x^2 + 3x}{x + 5} = \frac{10}{x + 5}$?

**Answer:** 2

<details><summary>Solutions</summary>

**By hand.** The two sides have the same denominator, and x ≠ -5. Multiplying both sides by x + 5 yields x^2 + 3x = 10, so x^2 + 3x - 10 = 0, which factors as (x + 5)(x - 2) = 0. This gives x = -5 or x = 2. But x = -5 makes the denominators 0, so it is extraneous. Therefore, the only solution is 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^2+3x}{x+5}</code><br><code>y=\frac{10}{x+5}</code>

The two graphs meet at exactly one point, (2, 1.429); the solution is x = 2. Both graphs have a vertical asymptote at x = -5, so there is no intersection there.

</details>

---

### 70. adv-tossed-ball-second-time

*Medium · Multiple choice · route: either · techniques: T1*

A ball is tossed upward from a platform. The equation $h = -5t^2 + 20t + 1.8$ models its height, where $h$ is the height, in meters, above the ground $t$ seconds after the toss. At what time, in seconds, does the ball reach a height of 16.8 meters for the second time?

- **A.** $1$
- **B.** $2$
- **C.** $3$
- **D.** $4$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Setting h = 16.8 yields -5t^2 + 20t + 1.8 = 16.8, so -5t^2 + 20t - 15 = 0. Dividing by -5 yields t^2 - 4t + 3 = 0, which factors as (t - 1)(t - 3) = 0. The ball is at 16.8 meters at t = 1 (going up) and t = 3 (coming down). Therefore, the second time is 3 seconds. Distractors: 1 is the first time; 2 is the time of the maximum height, halfway between the two times; 4 is the sum of the two times (and the time the ball is back at its starting height of 1.8 meters).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-5x^2+20x+1.8</code><br><code>y=16.8</code>

Type t as x. The horizontal line crosses the parabola at (1, 16.8) and (3, 16.8); the second time is the larger x-value, 3.

</details>

---

### 71. adv-two-parabolas-no-common-point

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $y = x^2 + 2x + 5$ and $y = -x^2 + 2x + 1$ are parabolas. How many points do the two parabolas have in common?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A common point satisfies both equations, so x^2 + 2x + 5 = -x^2 + 2x + 1. Adding x^2 - 2x - 1 to both sides yields 2x^2 + 4 = 0, so x^2 = -2, which has no real solutions. Therefore, the parabolas have zero points in common. Alternate approach: the minimum value of x^2 + 2x + 5 is 4 (at x = -1) and the maximum value of -x^2 + 2x + 1 is 2 (at x = 1), so the first graph lies entirely above the second. Distractors: Exactly one would need the graphs to touch at a single point, which requires 2x^2 + 4 = 0 to have a double root; Exactly two is the count whenever the upward parabola's minimum is below the downward parabola's maximum; Infinitely many would require the two equations to be the same.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+2x+5</code><br><code>y=-x^2+2x+1</code>

The upward parabola has its vertex at (-1, 4) and the downward parabola has its vertex at (1, 2), so the lowest point of the first graph is above the highest point of the second: they never meet. Zoom out (T1) before answering zero; an opposite-opening pair can only meet near their vertices, and here they do not.

</details>

---

### 72. adv-two-parabolas-tangent-y-coordinate

*Medium · Student-produced response · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $y = 2x^2 - 3x + 1$ and $y = x^2 + x - 3$ intersect at exactly one point. What is the $y$-coordinate of that point?

**Answer:** 3

<details><summary>Solutions</summary>

**By hand.** At a common point the y-values are equal, so 2x^2 - 3x + 1 = x^2 + x - 3. Subtracting x^2 + x - 3 from both sides yields x^2 - 4x + 4 = 0, which factors as (x - 2)^2 = 0, so x = 2 is the only solution (the graphs are tangent there). Substituting 2 for x in y = x^2 + x - 3 yields y = 4 + 2 - 3 = 3. Therefore, the y-coordinate of the point is 3. Reporting x = 2 answers the wrong coordinate.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x^2-3x+1</code><br><code>y=x^2+x-3</code>

Click the point where the two parabolas touch: (2, 3). The y-coordinate is 3. Only one gray point appears because the graphs are tangent; zoom in to confirm they do not cross.

</details>

---

### 73. adv-two-parabolas-x-difference

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the graphs of $y = x^2 - 4x + 1$ and $y = -x^2 + 2x + 9$ intersect at two points. If $a$ and $c$ are the $x$-coordinates of these points and $a < c$, what is the value of $c - a$?

- **A.** $-1$
- **B.** $3$
- **C.** $4$
- **D.** $5$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Setting the two expressions for y equal yields x^2 - 4x + 1 = -x^2 + 2x + 9, so 2x^2 - 6x - 8 = 0 and x^2 - 3x - 4 = 0. Factoring yields (x - 4)(x + 1) = 0, so the x-coordinates are -1 and 4. Therefore, a = -1, c = 4, and c - a = 5. Distractors: -1 is a itself; 4 is c itself; 3 is a + c, the sum rather than the difference.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-4x+1</code><br><code>y=-x^2+2x+9</code>

Click the two intersection points: (-1, 6) and (4, 1). So a = -1, c = 4, and c - a = 5.

</details>

---

### 74. sample-positive-root

*Medium · Student-produced response · route: desmos-primary · techniques: T1, T11*

What is the positive solution to $6x^2 - x - 2 = 0$?

**Answer:** 2/3 (≈ 0.6667)

<details><summary>Solutions</summary>

**By hand.** Factor: (3x - 2)(2x + 1) = 0, so x = 2/3 or x = -1/2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=6x^2-x-2</code>

Click the positive x-intercept: 0.667. Enter 2/3, or a full-width decimal like .6667. 0.67 is marked wrong.

</details>

---

### 75. sample-tangent-system

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

How many solutions does the system $y = x^2 - 6x + 11$ and $y = 2x - 5$ have?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Set equal: x^2 - 8x + 16 = 0, so (x - 4)^2 = 0. The discriminant is 0, so there is exactly one solution. Distractors: Zero comes from misreading a discriminant of 0 as negative; Exactly two assumes a line always crosses a parabola twice; Infinitely many would need the two graphs to be the same, which a line and a parabola never are.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-6x+11</code><br><code>y=2x-5</code>

The line touches the parabola at one point, (4, 3). Zoom in to confirm it doesn't cross twice.

</details>

---

### 76. adv-absolute-no-solution-c

*Hard · Multiple choice · route: desmos-primary · techniques: T4, T1*

In the equation $|4x - 1| + c = 2$, $c$ is a constant. For which values of $c$ does the equation have no real solutions?

- **A.** $c < -2$
- **B.** $c < 2$
- **C.** $c > -2$
- **D.** $c > 2$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Isolate the absolute value: |4x - 1| = 2 - c. An absolute value can equal any nonnegative number, so there is no solution exactly when 2 - c < 0, that is, c > 2. Distractors: c < 2 is the condition for two solutions (the sign flipped when moving c across); c > -2 and c < -2 come from solving |4x - 1| = c - 2 or c + 2 after a sign slip.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left|4x-1\right|+c</code><br><code>y=2</code>

Add a slider for c (the proposed T14 move). Drag c upward: the V rises, and the moment its vertex passes y = 2 the intersections disappear. That happens at c = 2, and there are none for every c > 2. At c = 2 exactly the vertex touches the line, so that is one solution, not none.

</details>

---

### 77. adv-absolute-one-solution-k

*Hard · Multiple choice · route: desmos-primary · techniques: T4, T1*

In the equation $-2|x - 5| + 9 = k$, $k$ is a constant. If the equation has exactly one solution, what is the value of $k$?

- **A.** $-9$
- **B.** $5$
- **C.** $9$
- **D.** $14$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The graph of y = -2|x - 5| + 9 is an upside-down V with vertex (5, 9). A horizontal line y = k meets it exactly once only at the vertex, so k = 9. Algebraically, |x - 5| = (9 - k)/2 has one solution when the right side is 0. Distractors: 5 is the x-coordinate of the vertex; -9 is a sign error on the constant; 14 adds the 5 and the 9.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-2\left|x-5\right|+9</code><br><code>y=k</code>

Add a slider for k with step 1 (the proposed T14 move: absolute value with a slider). Below the vertex the horizontal line crosses the V twice, above it not at all; it touches exactly once at the vertex, k = 9.

</details>

---

### 78. adv-absolute-value-line-one-solution-c

*Hard · Multiple choice · route: desmos-primary · techniques: T1, T4*

The equation $|x - 3| = \frac{1}{2}x + c$, where $c$ is a constant, has exactly one real solution. What is the value of $c$?

- **A.** $-3$
- **B.** $-\frac{3}{2}$
- **C.** $\frac{3}{2}$
- **D.** $3$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The graph of y = |x - 3| is a V with vertex (3, 0) and sides of slope 1 and -1. The line y = (1/2)x + c is less steep than either side, so it meets the V twice when it passes above the vertex, never when it passes below, and exactly once when it passes through the vertex. Substituting (3, 0) yields 0 = (1/2)(3) + c, so c = -3/2. Check: with c = -3/2 the case x ≥ 3 gives x = 3, and the case x < 3 gives x = 3, which is not less than 3, so there is one solution. Distractors: -3 forgets the 1/2 in (1/2)(3); 3/2 is a sign error in solving 0 = 3/2 + c; 3 makes both mistakes.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left|x-3\right|</code><br><code>y=\frac{1}{2}x+c</code><br><code>c=0</code>

Add a slider for c (T4) and count intersections of the line with the V: the absolute-value solution-counting move proposed as T14. Dragging c down, the two crossings move toward the vertex (3, 0); at c = -1.5 the line passes through the vertex and there is exactly one; below that there are none. Set the step to 0.5 to land on -1.5, which is -3/2.

</details>

---

### 79. adv-absolute-value-midpoint-c

*Hard · Multiple choice · route: either · techniques: T4, T1*

The equation $|2x - c| = 6$, where $c$ is a constant, has solutions $x = 1$ and $x = 7$. What is the value of $c$?

- **A.** $-4$
- **B.** $4$
- **C.** $6$
- **D.** $8$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** If |2x - c| = 6, then 2x - c = 6 or 2x - c = -6, so x = (c + 6)/2 or x = (c - 6)/2. The two solutions are symmetric about x = c/2, so c/2 is the midpoint of 1 and 7, which is 4. Therefore, c = 8. Checking: |2 - 8| = 6 and |14 - 8| = 6. Distractors: 4 is the midpoint of the solutions without the factor 2; -4 uses only x = 1 with the branch 2 - c = 6; 6 is the number on the right side of the equation.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left|2x-c\right|</code><br><code>y=6</code><br><code>c=8</code>

Add a slider for c and drag it until the two intersections of the V with the line y = 6 sit at x = 1 and x = 7 (the slider-and-count move, T14). That happens at c = 8; set the step to 1 to land on it.

</details>

---

### 80. adv-absolute-value-steep-line-count

*Hard · Multiple choice · route: desmos-primary · techniques: T1, T4*

Consider the equation $|x - 4| = 2x + c$, where $c$ is a constant. Which statement about the number of real solutions of the equation is true?

- **A.** It has zero or two real solutions, depending on the value of $c$.
- **B.** It has zero, one, or two real solutions, depending on the value of $c$.
- **C.** It has exactly two real solutions for every value of $c$.
- **D.** It has exactly one real solution for every value of $c$.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Let f(x) = 2x + c - |x - 4|. For x ≥ 4, f(x) = x + c + 4, and for x < 4, f(x) = 3x + c - 4. Both pieces increase, so f is increasing everywhere, and it takes every real value, so f(x) = 0 has exactly one solution for every c. Graphically, the line y = 2x + c has slope 2, steeper than both sides of the V (slopes 1 and -1), so it crosses the V exactly once. Distractors: zero or two, depending on c, is the picture for a line flatter than the V that misses or crosses it; zero, one, or two, depending on c, adds the case where that flatter line passes through the vertex; exactly two for every value of c treats every line as crossing both sides of the V.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left|x-4\right|</code><br><code>y=2x+c</code><br><code>c=0</code>

Add a slider for c (T4), widen its range to -30 to 30 and drag it through the whole range, counting intersections of the line with the V (the absolute-value solution-counting move proposed as T14). The line is steeper than both sides of the V, so it always crosses exactly once, whatever c is.

</details>

---

### 81. adv-absolute-value-sum-of-solutions

*Hard · Multiple choice · route: desmos-primary · techniques: T1, T11*

What is the sum of all solutions to the equation $|3x - 4| = 2x + 1$?

- **A.** $\frac{3}{5}$
- **B.** $\frac{22}{5}$
- **C.** $5$
- **D.** $\frac{28}{5}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Since |3x - 4| ≥ 0, any solution needs 2x + 1 ≥ 0. Case 1: 3x - 4 = 2x + 1 gives x = 5. Case 2: 3x - 4 = -(2x + 1) gives 5x = 3 and x = 3/5. Both make 2x + 1 positive, so both are solutions, and the sum is 5 + 3/5 = 28/5. Distractors: 5 and 3/5 are single solutions reported as the sum; 22/5 is the difference 5 - 3/5.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left|3x-4\right|</code><br><code>y=2x+1</code>

The V and the line cross twice (the proposed T14 picture: an absolute-value graph against a line). Click both points: x = 0.6 and x = 5. The sum is 5.6; the fraction toggle gives 28/5.

</details>

---

### 82. adv-biquadratic-real-solution-count

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

How many distinct real solutions does the equation $x^4 - 5x^2 - 36 = 0$ have?

- **A.** $0$
- **B.** $1$
- **C.** $2$
- **D.** $4$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The given equation is quadratic in x^2: it factors as (x^2 - 9)(x^2 + 4) = 0. So x^2 = 9 or x^2 = -4. The first gives x = 3 or x = -3. The second has no real solutions, because a square is never negative. Therefore, the equation has 2 distinct real solutions. Distractors: 0 comes from deciding the negative case makes the whole equation unsolvable; 1 keeps only the positive square root of 9; 4 counts x^2 = -4 as giving two more real solutions.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^4-5x^2-36</code>

Zoom out until the whole W-shaped curve is visible (its minimum is near y = -42). It crosses the x-axis exactly twice, at x = -3 and x = 3, so there are 2 real solutions.

</details>

---

### 83. adv-circle-tangent-line-c

*Hard · Multiple choice · route: either · techniques: T4, T2*

In the $xy$-plane, the graph of $x^2 + y^2 = c$ intersects the line with equation $y = x + 4$ at exactly one point, where $c$ is a positive constant. What is the value of $c$?

- **A.** $4$
- **B.** $8$
- **C.** $16$
- **D.** $24$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting x + 4 for y yields x^2 + (x + 4)^2 = c, which simplifies to 2x^2 + 8x + 16 - c = 0. The graphs meet at exactly one point when this quadratic has exactly one solution, so its discriminant is 0: 8^2 - 4(2)(16 - c) = 64 - 128 + 8c = 0, which yields c = 8. Alternate approach: the circle is centered at the origin, so the radius is the distance from the origin to the line, 4/sqrt(2) = 2 sqrt(2), and c = (2 sqrt(2))^2 = 8. Distractors: 16 treats the y-intercept 4 of the line as the radius; 4 takes the y-intercept of the line as the value of c; 24 comes from adding 4ac in the discriminant instead of subtracting it.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=c</code><br><code>y=x+4</code><br><code>c=8</code>

Add a slider for c and drag it: for c < 8 the circle misses the line, for c > 8 it crosses twice, and at c = 8 the line just touches the circle at (-2, 2). Set the slider step to 1 to land on it exactly.

</details>

---

### 84. adv-discriminant-max-ac

*Hard · Multiple choice · route: hand-primary · techniques: T4*

In the equation $ax^2 + 18x + c = 0$, $a$ and $c$ are positive integers. If the equation has two distinct real solutions, what is the greatest possible value of $ac$?

- **A.** $80$
- **B.** $81$
- **C.** $162$
- **D.** $324$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Two distinct real solutions need a positive discriminant: 18^2 - 4ac > 0, so 4ac < 324 and ac < 81. Since a and c are integers, ac is an integer, and the greatest integer less than 81 is 80 (for example a = 8, c = 10). Distractors: 81 uses 'greater than or equal to' and allows the repeated root; 162 divides 324 by 2 instead of 4; 324 forgets to divide by 4 at all.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=ax^2+18x+c</code>

Sliders for a and c only illustrate: with a = 1, step c from 80 to 81 and watch the two x-intercepts merge into one. The slider cannot search all integer pairs, so the discriminant argument by hand is the real method.

</details>

---

### 85. adv-double-radical-equation

*Hard · Multiple choice · route: either · techniques: T1*

What is the solution to the equation $\sqrt{x + 7} = \sqrt{x} + 1$?

- **A.** $3$
- **B.** $6$
- **C.** $9$
- **D.** $36$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Squaring both sides of the given equation yields x + 7 = (sqrt(x) + 1)^2 = x + 2 sqrt(x) + 1. Subtracting x + 1 from both sides yields 6 = 2 sqrt(x), so sqrt(x) = 3 and x = 9. Check: sqrt(16) = 4 and sqrt(9) + 1 = 4. Therefore, the solution is 9. Distractors: 3 is the value of sqrt(x), an intermediate result; 6 is the value of 2 sqrt(x); 36 comes from dropping the 2 in the middle term, so that sqrt(x) = 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{x+7}</code><br><code>y=\sqrt{x}+1</code>

The two curves cross once, at (9, 4). The solution is the x-coordinate, 9, not the y-coordinate.

</details>

---

### 86. adv-exponential-difference-common-factor

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

If $2^{x + 3} - 2^x = 56$, what is the value of $x$?

**Answer:** 3

<details><summary>Solutions</summary>

**By hand.** Since 2^(x + 3) = 2^x · 2^3 = 8 · 2^x, the left side of the given equation is 8 · 2^x - 2^x = 7 · 2^x. Therefore, 7 · 2^x = 56, so 2^x = 8 = 2^3 and x = 3. Subtracting the exponents to get 2^3 = 56 is a common error; the exponent rule for a difference of powers is a common factor, not a subtraction of exponents.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2^{x+3}-2^x</code><br><code>y=56</code>

Click the intersection: (3, 56), so x = 3. The left side is increasing, so there is only one crossing; if the point is off-screen, zoom out.

</details>

---

### 87. adv-exponential-quadratic-in-two-power

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

The equation $4^x - 3 \cdot 2^{x + 1} + 8 = 0$ has two real solutions. What is their sum?

- **A.** $2$
- **B.** $3$
- **C.** $6$
- **D.** $8$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since 4^x = (2^x)^2 and 2^(x + 1) = 2 · 2^x, letting u = 2^x turns the given equation into u^2 - 6u + 8 = 0, which factors as (u - 2)(u - 4) = 0. So 2^x = 2 or 2^x = 4, which gives x = 1 or x = 2. Therefore, the sum of the solutions is 3. Distractors: 2 is the larger solution alone; 6 is the sum of the values of u = 2^x, not of x; 8 is the product of the values of u.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=4^{x}-3\cdot2^{x+1}+8</code>

The curve crosses the x-axis at (1, 0) and (2, 0). Add the x-values: 1 + 2 = 3.

</details>

---

### 88. adv-factored-cubic-two-distinct-c

*Hard · Multiple choice · route: hand-primary · techniques: T4*

The equation $x(x^2 - 6x + c) = 0$, where $c$ is a nonzero constant, has exactly two distinct real solutions. What is the value of $c$?

- **A.** $-9$
- **B.** $3$
- **C.** $9$
- **D.** $36$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that x(x^2 - 6x + c) = 0, so x = 0 is always a solution. Since c ≠ 0, x = 0 is not a solution of x^2 - 6x + c = 0. For exactly two distinct solutions in all, the quadratic factor must have exactly one solution, so its discriminant is 0: (-6)^2 - 4c = 0, so c = 9. Then x^2 - 6x + 9 = (x - 3)^2, and the solutions are 0 and 3. Distractors: -9 has the sign of c reversed and gives three solutions; 3 is the repeated solution, not c; 36 is b^2 without dividing by 4 and gives only the solution x = 0.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x(x^2-6x+c)</code><br><code>c=9</code>

The factor-and-discriminant argument is faster. As a check, add a slider for c (T4): at c = 9 the cubic crosses at x = 0 and only touches the x-axis at x = 3, two distinct x-intercepts; nearby values of c give three or one.

</details>

---

### 89. adv-line-circle-tangent-intercept-b

*Hard · Student-produced response · route: either · techniques: T4, T2*

In the $xy$-plane, the line $y = 3x + b$ and the circle $x^2 + y^2 = 10$ have exactly one point in common, where $b$ is a positive constant. What is the value of $b$?

**Answer:** 10

<details><summary>Solutions</summary>

**By hand.** Substituting 3x + b for y yields x^2 + (3x + b)^2 = 10, so 10x^2 + 6bx + b^2 - 10 = 0. The line and circle share exactly one point when this has exactly one solution, so the discriminant is 0: (6b)^2 - 4(10)(b^2 - 10) = 0, which gives 400 - 4b^2 = 0 and b^2 = 100. Since b is positive, b = 10. A common slip is expanding (3x + b)^2 as 9x^2 + b^2, dropping the 6bx term.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=10</code><br><code>y=3x+b</code><br><code>b=1</code>

Add a slider for b (T4) and widen its range to 0 to 20. Drag b up until the line just touches the circle on its upper left; that happens at b = 10, with the touching point (-3, 1). Set the step to 1 to land on it.

</details>

---

### 90. adv-ne2-absolute-quadratic-three-solutions-k

*Hard · Student-produced response · route: desmos-primary · techniques: T4*

The equation $|x^2 - 6x + 5| = k$, where $k$ is a positive constant, has exactly three real solutions. What is the value of $k$?

**Answer:** 4

<details><summary>Solutions</summary>

**By hand.** Completing the square yields x^2 - 6x + 5 = (x - 3)^2 - 4, a parabola with vertex (3, -4) that crosses the x-axis at x = 1 and x = 5. Taking the absolute value reflects the part between x = 1 and x = 5 above the axis, creating a peak at (3, 4). A horizontal line y = k meets this graph 4 times when 0 < k < 4, 3 times when k = 4 (once at the peak and twice outside 1 ≤ x ≤ 5), and 2 times when k > 4. Therefore, k = 4. Check: (x - 3)^2 - 4 = 4 gives x = 3 ± 2 sqrt(2), and (x - 3)^2 - 4 = -4 gives x = 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=|x^2-6x+5|</code><br><code>y=k</code>

Add a slider for k (T4) and count crossings with the W-shaped graph, the absolute-value counting move (T14): four crossings for small k, three when the line touches the peak at (3, 4), two above it. Set the step to 1 to land on k = 4.

</details>

---

### 91. adv-ne2-base-five-solution-count

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

How many real solutions does the equation $5^{2x} + 4 \cdot 5^x - 5 = 0$ have?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since 5^(2x) = (5^x)^2, letting u = 5^x turns the given equation into u^2 + 4u - 5 = 0, which factors as (u + 5)(u - 1) = 0. So 5^x = -5 or 5^x = 1. A power of 5 is always positive, so 5^x = -5 has no solution, and 5^x = 1 gives x = 0. Therefore, the equation has exactly one real solution. Distractors: Zero rejects the whole equation once one value of u turns out negative; Exactly two counts both values of u without checking that 5^x must be positive; Infinitely many confuses the infinitely many inputs of u = 5^x with solutions of the equation.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5^{2x}+4\cdot5^{x}-5</code>

The curve crosses the x-axis once, at x = 0. Zoom out to the left: the curve levels off toward y = -5 and never comes back up to the axis. Exactly one.

</details>

---

### 92. adv-ne2-base-three-product-solutions

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

The equation $3^{2x + 1} - 28 \cdot 3^x + 9 = 0$ has two real solutions. What is the product of the solutions?

**Answer:** -2

<details><summary>Solutions</summary>

**By hand.** Since 3^(2x + 1) = 3 · (3^x)^2, letting u = 3^x turns the given equation into 3u^2 - 28u + 9 = 0, which factors as (3u - 1)(u - 9) = 0. So 3^x = 1/3 or 3^x = 9, which gives x = -1 or x = 2. Therefore, the product of the solutions is (-1)(2) = -2. A common slip is reporting the product of the values of u, (1/3)(9) = 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3^{2x+1}-28\cdot3^{x}+9</code>

The curve crosses the x-axis at x = -1 and x = 2. Zoom out vertically (y from about -60 to 20) to see the whole dip below the axis. Multiply the x-intercepts: (-1)(2) = -2.

</details>

---

### 93. adv-ne2-cube-root-quadratic-form

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

What is the sum of the real numbers $x$ that satisfy $x^{\frac{2}{3}} - 5x^{\frac{1}{3}} + 4 = 0$?

- **A.** $5$
- **B.** $17$
- **C.** $64$
- **D.** $65$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Since x^(2/3) = (x^(1/3))^2, letting u = x^(1/3) turns the given equation into u^2 - 5u + 4 = 0, which factors as (u - 1)(u - 4) = 0. So x^(1/3) = 1 or x^(1/3) = 4, and cubing yields x = 1 or x = 64. Therefore, the sum is 1 + 64 = 65. Distractors: 5 is the sum of the values of u, not of x; 17 squares u instead of cubing it (1 + 16); 64 is the greater solution alone.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^{\frac{2}{3}}-5x^{\frac{1}{3}}+4</code>

The curve crosses the x-axis at x = 1 and, after zooming out to about x = 80, again at x = 64. Add the x-intercepts: 1 + 64 = 65.

</details>

---

### 94. adv-ne2-hiker-round-trip-speed

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

A hiker walks 12 kilometers to a waterfall at an average speed of $s$ kilometers per hour and returns by the same trail at an average speed 1 kilometer per hour faster. The round trip takes 7 hours of walking. What is the value of $s$?

**Answer:** 3

<details><summary>Solutions</summary>

**By hand.** Time is distance divided by speed, so the walk out takes 12/s hours and the walk back takes 12/(s + 1) hours. So 12/s + 12/(s + 1) = 7. Multiplying both sides by s(s + 1) yields 12(s + 1) + 12s = 7s(s + 1), or 24s + 12 = 7s^2 + 7s. Rearranging yields 7s^2 - 17s - 12 = 0, which factors as (7s + 4)(s - 3) = 0. A speed is positive, so s = 3. Check: 12/3 + 12/4 = 4 + 3 = 7.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{12}{x}+\frac{12}{x+1}</code><br><code>y=7</code>

Write the time equation first (time is distance divided by speed). Click the intersection with positive x: (3, 7). The other intersection, x = -4/7 (about -0.571), is not a speed. Enter 3.

</details>

---

### 95. adv-ne2-k-at-both-ends-one-solution

*Hard · Multiple choice · route: either · techniques: T4*

The equation $kx^2 + 6x + k = 0$, where $k$ is a positive constant, has exactly one real solution. What is the value of $k$?

- **A.** $3$
- **B.** $6$
- **C.** $9$
- **D.** $36$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A quadratic equation ax^2 + bx + c = 0 has exactly one real solution when its discriminant b^2 - 4ac equals 0. Here a = k, b = 6 and c = k, so 36 - 4k^2 = 0, which gives k^2 = 9 and k = 3 or k = -3. Since k is positive, k = 3. Check: 3x^2 + 6x + 3 = 3(x + 1)^2. Distractors: 6 drops the 4 from 4ac, as 36 - k^2 = 0; 9 is the value of k^2, not of k; 36 is the value of b^2, an intermediate result.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=kx^2+6x+k</code>

Add a slider for k (T4) with a range of 0 to 10 and step 0.5. Drag it until the parabola just touches the x-axis: k = 3, touching at (-1, 0). The discriminant gives the exact value faster.

</details>

---

### 96. adv-ne2-parabola-absolute-three-points

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, at how many points do the graphs of $y = x^2 - 2x + 1$ and $y = |x - 1|$ intersect?

- **A.** Exactly one
- **B.** Exactly two
- **C.** Exactly three
- **D.** Exactly four

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Since x^2 - 2x + 1 = (x - 1)^2 = |x - 1|^2, letting u = |x - 1| turns the system into u^2 = u, so u = 0 or u = 1. Then |x - 1| = 0 gives x = 1, and |x - 1| = 1 gives x = 0 or x = 2. The intersection points are (0, 1), (1, 0) and (2, 1), so there are exactly three. Distractors: Exactly one keeps only (1, 0), where both graphs touch the x-axis; Exactly two divides u^2 = u by u and loses u = 0; Exactly four counts two points for u = 0 as well as for u = 1, although |x - 1| = 0 has only one solution.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-2x+1</code><br><code>y=|x-1|</code>

This is the absolute-value counting picture (T14): the V and the parabola share the low point (1, 0) and cross again at (0, 1) and (2, 1). Zoom in near (1, 0) to see that the graphs really meet there. Three points.

</details>

---

### 97. adv-ne2-rational-restriction-extraneous

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

What is the solution to the equation $\frac{x}{x - 2} - \frac{3}{x + 1} = \frac{9}{x^2 - x - 2}$?

**Answer:** 3

<details><summary>Solutions</summary>

**By hand.** Since x^2 - x - 2 = (x - 2)(x + 1), multiplying both sides of the given equation by (x - 2)(x + 1), where x ≠ 2 and x ≠ -1, yields x(x + 1) - 3(x - 2) = 9. Expanding yields x^2 - 2x + 6 = 9, or x^2 - 2x - 3 = 0, which factors as (x - 3)(x + 1) = 0. The value x = -1 makes two denominators 0, so it is extraneous. Therefore, the only solution is 3. Check: 3/1 - 3/4 = 9/4 and 9/(9 - 3 - 2) = 9/4.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x}{x-2}-\frac{3}{x+1}</code><br><code>y=\frac{9}{x^2-x-2}</code>

The graphs meet at (3, 2.25). Near x = -1 both graphs shoot off vertically and never share a point, so -1 is not a solution. Enter 3.

</details>

---

### 98. adv-ne2-rational-tangent-positive-k

*Hard · Multiple choice · route: either · techniques: T4*

The equation $\frac{9}{x} = k - x$, where $k$ is a positive constant, has exactly one real solution. What is the value of $k$?

- **A.** $3$
- **B.** $6$
- **C.** $18$
- **D.** $36$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the given equation by x, where x ≠ 0, yields 9 = kx - x^2, or x^2 - kx + 9 = 0. This quadratic has exactly one real solution when its discriminant (-k)^2 - 4(1)(9) = k^2 - 36 equals 0, so k = 6 or k = -6. Since k is positive, k = 6, and the solution is x = 3, which is not excluded. Distractors: 3 is the solution x, not k; 18 halves 36 instead of taking its square root; 36 is the value of k^2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{9}{x}</code><br><code>y=k-x</code>

Add a slider for k (T4) with step 1 and drag it until the line just touches the right branch of the hyperbola: k = 6, touching at (3, 3). Smaller positive k gives no intersection and larger k gives two.

</details>

---

### 99. adv-ne2-tabletop-diagonal-perimeter

*Hard · Multiple choice · route: hand-primary · techniques: T2*

A rectangular tabletop has a diagonal of length 6 feet and an area of 14 square feet. What is the perimeter, in feet, of the tabletop?

- **A.** $8$
- **B.** $12$
- **C.** $16$
- **D.** $64$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let the side lengths be l feet and w feet. By the Pythagorean theorem, l^2 + w^2 = 36, and the area gives lw = 14. Since (l + w)^2 = l^2 + w^2 + 2lw, it follows that (l + w)^2 = 36 + 28 = 64, so l + w = 8. Therefore, the perimeter is 2(l + w) = 16 feet. (The sides are 4 + sqrt(2) and 4 - sqrt(2) feet, so guessing whole-number sides fails.) Distractors: 8 is l + w, half the perimeter; 12 doubles the diagonal; 64 is the value of (l + w)^2, an intermediate result.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=36</code><br><code>xy=14</code>

The identity below is faster, so Desmos is a check only (T2). The circle and the curve xy = 14 meet at about (5.414, 2.586) in the first quadrant, and 2(5.414 + 2.586) = 16.

</details>

---

### 100. adv-ne2-tangent-at-given-point-bc

*Hard · Student-produced response · route: either · techniques: T4*

In the $xy$-plane, the graphs of $y = x^2 + bx + c$ and $y = 2x - 1$ have only the point $(2, 3)$ in common, where $b$ and $c$ are constants. What is the value of $bc$?

**Answer:** -6

<details><summary>Solutions</summary>

**By hand.** Setting x^2 + bx + c = 2x - 1 yields x^2 + (b - 2)x + (c + 1) = 0. Since the graphs meet only at x = 2, this quadratic has 2 as its only solution, so it must equal (x - 2)^2 = x^2 - 4x + 4. Matching coefficients yields b - 2 = -4 and c + 1 = 4, so b = -2 and c = 3. Therefore, bc = -6. Check: (2, 3) lies on y = x^2 - 2x + 3, since 4 - 4 + 3 = 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+bx-1-2b</code><br><code>y=2x-1</code>

Since (2, 3) is on the parabola, 4 + 2b + c = 3, so c = -1 - 2b; that is why the first line uses -1-2b for c. Add a slider for b (T4) with step 1 and drag until the parabola only touches the line: b = -2, so c = 3 and bc = -6.

</details>

---

### 101. adv-ne2-two-radicals-no-solution

*Hard · Multiple choice · route: hand-primary · techniques: T1*

How many real solutions does the equation $\sqrt{5x - 4} = 2\sqrt{x - 1}$ have?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Squaring both sides of the given equation yields 5x - 4 = 4(x - 1) = 4x - 4, so x = 0. Checking x = 0 in the given equation: 5(0) - 4 = -4 and 0 - 1 = -1, so neither square root is a real number. The only candidate is extraneous, so the equation has zero real solutions. Distractors: Exactly one accepts x = 0 without checking it in the given equation; Exactly two assumes that squaring always leads to a quadratic with two roots; Infinitely many treats the squared equation as an identity, but 5x - 4 = 4x - 4 holds only for x = 0.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{5x-4}</code><br><code>y=2\sqrt{x-1}</code>

Squaring and checking is quicker by hand, so use Desmos as a check. The curves start at x = 0.8 and x = 1, and the first stays above the second everywhere; zoom in near x = 1 and out to the right to confirm they never meet. Zero solutions.

</details>

---

### 102. adv-ne2-two-radicals-sum-solutions

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

What is the sum of all real solutions to $\sqrt{2x + 3} - \sqrt{x - 2} = 2$?

- **A.** $3$
- **B.** $11$
- **C.** $14$
- **D.** $33$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Adding sqrt(x - 2) to both sides yields sqrt(2x + 3) = 2 + sqrt(x - 2). Squaring yields 2x + 3 = 4 + 4 sqrt(x - 2) + x - 2, so x + 1 = 4 sqrt(x - 2). Squaring again yields x^2 + 2x + 1 = 16x - 32, or x^2 - 14x + 33 = 0, which factors as (x - 3)(x - 11) = 0. Both values check: sqrt(9) - sqrt(1) = 2 and sqrt(25) - sqrt(9) = 2. Therefore, the sum is 3 + 11 = 14. Distractors: 3 and 11 each keep one solution and reject the other as extraneous without checking it; 33 is the product of the solutions.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{2x+3}-\sqrt{x-2}</code><br><code>y=2</code>

The curve starts at x = 2, dips below y = 2 and comes back up. Zoom out to see both crossings: x = 3 and x = 11. Add them: 14.

</details>

---

### 103. adv-ne3-circle-parabola-three-count

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, how many points do the graphs of $x^2 + y^2 = 16$ and $y = x^2 - 4$ have in common?

- **A.** Exactly one
- **B.** Exactly two
- **C.** Exactly three
- **D.** Exactly four

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** From y = x^2 - 4, x^2 = y + 4. Substituting into the circle yields (y + 4) + y^2 = 16, or y^2 + y - 12 = 0, which factors as (y + 4)(y - 3) = 0. If y = 3, then x^2 = 7, so x = sqrt(7) or x = -sqrt(7): two points. If y = -4, then x^2 = 0, so x = 0: one point, (0, -4). Therefore, the graphs have exactly three points in common. Distractors: Exactly one keeps only the vertex (0, -4); Exactly two keeps y = 3 and misses the touching point at the bottom of the circle; Exactly four counts x = 0 twice, as if x^2 = 0 gave two points.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=16</code><br><code>y=x^2-4</code>

The parabola crosses the circle at about (-2.646, 3) and (2.646, 3), and its vertex (0, -4) is the bottom of the circle. Zoom in near (0, -4) to see that the graphs touch there. Three common points.

</details>

---

### 104. adv-ne3-circles-other-point-b

*Hard · Student-produced response · route: desmos-primary · techniques: T2*

In the $xy$-plane, the circles $x^2 + y^2 = 25$ and $(x - 7)^2 + (y - 1)^2 = 25$ have $(3, 4)$ as one common point. What is the $y$-coordinate of the other common point?

**Answer:** -3

<details><summary>Solutions</summary>

**By hand.** Subtracting the second equation from the first: x^2 + y^2 - (x - 7)^2 - (y - 1)^2 = 0. Expanding yields 14x - 49 + 2y - 1 = 0, so y = 25 - 7x; every common point lies on this line. Substituting into x^2 + y^2 = 25 yields x^2 + (25 - 7x)^2 = 25, or 50x^2 - 350x + 600 = 0, which simplifies to x^2 - 7x + 12 = 0. So x = 3 or x = 4. The point with x = 3 is (3, 4), so the other point has x = 4 and y = 25 - 7(4) = -3. Therefore, the y-coordinate of the other common point is -3.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=25</code><br><code>(x-7)^2+(y-1)^2=25</code>

Click the two gray intersection points: (3, 4) and (4, -3). The other point is (4, -3). Enter -3, its y-coordinate.

</details>

---

### 105. adv-ne3-dance-floor-enlarged-area

*Hard · Multiple choice · route: either · techniques: T1*

A square dance floor is enlarged by adding 4 feet to one side length and 6 feet to the other, forming a rectangle whose area is twice the area of the original floor. What is the area, in square feet, of the enlarged floor?

- **A.** $12$
- **B.** $144$
- **C.** $216$
- **D.** $288$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Let s be the side length, in feet, of the original floor. The enlarged floor measures (s + 4) feet by (s + 6) feet, and its area is twice s^2, so (s + 4)(s + 6) = 2s^2. Expanding yields s^2 + 10s + 24 = 2s^2, or s^2 - 10s - 24 = 0, which factors as (s - 12)(s + 2) = 0. A length must be positive, so s = 12. The enlarged area is (12 + 4)(12 + 6) = 16(18) = 288. Therefore, the enlarged floor has an area of 288 square feet. Distractors: 12 is the original side length, not an area; 144 is the area of the original floor; 216 enlarges only one side, 12 times 18.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x+4)(x+6)</code><br><code>y=2x^2</code>

Here x is the original side length. The graphs meet at x = -2 and x = 12; a length must be positive, so x = 12. The point (12, 288) gives the enlarged area directly: 288.

</details>

---

### 106. adv-ne3-exponential-system-sum

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

If $3^{x} \cdot 9^{y} = 81$ and $\frac{9^{x}}{3^{y}} = 27$, what is the value of $x + y$?

- **A.** $1$
- **B.** $2$
- **C.** $3$
- **D.** $7$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Writing every term as a power of 3: 3^x \* 3^(2y) = 3^4 gives x + 2y = 4, and 3^(2x)/3^y = 3^3 gives 2x - y = 3. Multiplying the second equation by 2 and adding it to the first yields 5x = 10, so x = 2; then y = 2x - 3 = 1. Therefore, x + y = 3. Distractors: 1 is the value of y alone; 2 is the value of x alone; 7 adds the exponent equations, 3x + y = 7, and reports that sum as x + y.

**Desmos** (not yet verified in Desmos). Type:<br><code>3^x\cdot9^y=81</code><br><code>\frac{9^x}{3^y}=27</code>

Each equation graphs as a line. Click their intersection: (2, 1). Then x + y = 2 + 1 = 3; the question asks for the sum, not a coordinate.

</details>

---

### 107. adv-ne3-f-equals-f-double-rational

*Hard · Multiple choice · route: either · techniques: T1, T13*

The function $f$ is defined by $f(x) = x + \frac{12}{x}$. What is the positive value of $x$ for which $f(x) = f(2x)$?

- **A.** $\sqrt{3}$
- **B.** $\sqrt{6}$
- **C.** $2\sqrt{3}$
- **D.** $3\sqrt{2}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting 2x for x in f yields f(2x) = 2x + 12/(2x) = 2x + 6/x. Setting f(x) = f(2x) yields x + 12/x = 2x + 6/x. Subtracting x and 6/x from both sides yields 6/x = x, so x^2 = 6 and x = sqrt(6) or x = -sqrt(6). Therefore, the positive value is sqrt(6). Distractors: sqrt(3) writes 2x - x as 2x, so 2x = 6/x and x^2 = 3; 2sqrt(3) drops the 6/x term when collecting the fractions, so 12/x = x and x^2 = 12; 3sqrt(2) adds 6/x to 12/x instead of subtracting it, so x^2 = 18.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=x+\frac{12}{x}</code><br><code>y=f(x)</code><br><code>y=f(2x)</code><br><code>\sqrt{6}</code>

The graphs of y = f(x) and y = f(2x) cross in the first quadrant at about (2.449, 7.348). Typing the choice sqrt(6) (T13) shows 2.449, so the key is sqrt(6).

</details>

---

### 108. adv-ne3-product-ellipse-x-plus-2y

*Hard · Student-produced response · route: hand-primary · techniques: T2*

If $xy = 10$ and $x^2 + 4y^2 = 41$, where $x > 0$ and $y > 0$, what is the value of $x + 2y$?

**Answer:** 9

<details><summary>Solutions</summary>

**By hand.** Squaring x + 2y yields (x + 2y)^2 = x^2 + 4xy + 4y^2 = (x^2 + 4y^2) + 4xy. It's given that x^2 + 4y^2 = 41 and xy = 10, so (x + 2y)^2 = 41 + 40 = 81. Since x and y are positive, x + 2y is positive, so x + 2y = 9. Therefore, the value of x + 2y is 9. Two different points, (5, 2) and (4, 2.5), satisfy the system, but both give the same sum. A common slip is to use 2xy instead of 4xy, which gives (x + 2y)^2 = 61.

**Desmos** (not yet verified in Desmos). Type:<br><code>xy=10</code><br><code>x^2+4y^2=41</code>

The square of x + 2y is faster by hand. As a check, the graphs meet in the first quadrant at (4, 2.5) and (5, 2); both give x + 2y = 9.

</details>

---

### 109. adv-ne3-quartic-substitution-product

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

What is the product of all real solutions to the equation $(x^2 - 3x)^2 - (x^2 - 3x) - 12 = 0$?

- **A.** $-12$
- **B.** $-4$
- **C.** $-1$
- **D.** $4$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Let u = x^2 - 3x. The equation becomes u^2 - u - 12 = 0, which factors as (u - 4)(u + 3) = 0, so u = 4 or u = -3. If x^2 - 3x = 4, then x^2 - 3x - 4 = 0, which factors as (x - 4)(x + 1) = 0, so x = 4 or x = -1. If x^2 - 3x = -3, then x^2 - 3x + 3 = 0, whose discriminant is 9 - 12 = -3 < 0, so there are no real solutions. The real solutions are 4 and -1, and their product is -4. Distractors: -12 is the constant term of the expanded quartic, the product of all four solutions including the two non-real ones; -1 and 4 are each one of the real solutions, not their product.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x^2-3x)^2-(x^2-3x)-12</code>

Zoom out vertically until the curve's shape is clear, then click the x-intercepts: only (-1, 0) and (4, 0). The product of the real solutions is (-1)(4) = -4.

</details>

---

### 110. adv-ne3-robots-north-east

*Hard · Multiple choice · route: either · techniques: T1*

Two delivery robots leave the same depot at the same time; one travels due north, and the other travels due east at a speed 2 kilometers per hour greater. After 2 hours, they are 20 kilometers apart. What is the speed, in kilometers per hour, of the northbound robot?

- **A.** $6$
- **B.** $8$
- **C.** $12$
- **D.** $14$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Let s be the northbound speed, in kilometers per hour. After 2 hours the northbound robot has gone 2s kilometers and the eastbound robot 2(s + 2) kilometers, along perpendicular paths. By the Pythagorean theorem, (2s)^2 + (2s + 4)^2 = 20^2. Dividing both sides by 4 yields s^2 + (s + 2)^2 = 100, or 2s^2 + 4s - 96 = 0, so s^2 + 2s - 48 = 0. Factoring yields (s + 8)(s - 6) = 0, so s = 6 (the speed is positive). Therefore, the northbound robot travels at 6 kilometers per hour. Distractors: 8 is the eastbound speed; 12 is the northbound distance after 2 hours, not the speed; 14 adds the two speeds.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(2x)^2+(2(x+2))^2</code><br><code>y=400</code>

Zoom out until y = 400 is on screen. The line meets the parabola at x = -8 and x = 6. A speed must be positive, so the northbound speed is 6.

</details>

---

### 111. adv-ne3-root-difference-squared

*Hard · Multiple choice · route: hand-primary · techniques: T1*

What is the square of the difference between the two solutions to the equation $2x^2 - 4x - 3 = 0$?

- **A.** $-2$
- **B.** $4$
- **C.** $10$
- **D.** $16$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** For ax^2 + bx + c = 0, the sum of the solutions is -b/a and the product is c/a. Let p and q be the two solutions. Then p + q = 4/2 = 2 and pq = -3/2. Since (p - q)^2 = (p + q)^2 - 4pq, it follows that (p - q)^2 = 4 - 4(-3/2) = 4 + 6 = 10. Therefore, the square of the difference between the solutions is 10. (Equivalently, (p - q)^2 is the discriminant divided by a^2: (16 + 24)/4 = 10.) Distractors: -2 uses pq = 3/2, dropping the negative sign of c; 4 is (p + q)^2; 16 uses pq = -3, forgetting to divide c by a.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x^2-4x-3</code>

The sum and product of the roots are faster by hand. As a check, the x-intercepts are about -0.581 and 2.581; their difference is about 3.162, and 3.162^2 is about 10.

</details>

---

### 112. adv-ne3-roots-differ-by-one-k

*Hard · Multiple choice · route: hand-primary · techniques: T4*

The two solutions to the equation $x^2 + kx + 12 = 0$, where $k$ is a positive constant, differ by 1. What is the value of $k$?

- **A.** $-7$
- **B.** $1$
- **C.** $4$
- **D.** $7$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Let the solutions be r and r + 1. The product of the solutions is 12, so r(r + 1) = 12, which gives r = 3 or r = -4. The pairs are 3 and 4, or -4 and -3. The sum of the solutions is -k, so k = -7 for the first pair and k = 7 for the second. Since k is positive, k = 7. Alternate approach: the difference of the solutions is sqrt(k^2 - 48), the square root of the discriminant, so k^2 - 48 = 1, k^2 = 49 and k = 7. Distractors: -7 takes the pair 3 and 4 and ignores that k is positive; 1 is the difference of the solutions; 4 is one of the solutions for k = -7, not the constant.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+kx+12</code>

Reasoning about the roots is faster. As a check, add a slider for k and set k = 7: the x-intercepts are -4 and -3, which differ by 1.

</details>

---

### 113. adv-ne3-sixteen-four-quadratic-exponent

*Hard · Student-produced response · route: either · techniques: T1*

What is the positive solution to the equation $16^{x^2} = 4^{x + 3}$?

**Answer:** 3/2 (≈ 1.5)

<details><summary>Solutions</summary>

**By hand.** Since 16 = 4^2, the left side is (4^2)^(x^2) = 4^(2x^2). The equation becomes 4^(2x^2) = 4^(x + 3), so 2x^2 = x + 3. Rearranging yields 2x^2 - x - 3 = 0, which factors as (2x - 3)(x + 1) = 0, so x = 3/2 or x = -1. Therefore, the positive solution is 3/2. A common slip is to write 16^(x^2) as 4^(x^2 + 2), which leads to x^2 - x - 1 = 0 and an irrational answer.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=16^{x^2}</code><br><code>y=4^{x+3}</code>

The curves meet at (-1, 16) and again much higher up: zoom out vertically to about y = 600, then click the intersection with positive x: (1.5, 512). Enter 1.5 or 3/2.

</details>

---

### 114. adv-ne3-v-graph-circle-count

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, how many points do the graphs of $y = |x| + 1$ and $x^2 + y^2 = 25$ have in common?

- **A.** Exactly one
- **B.** Exactly two
- **C.** Exactly three
- **D.** Exactly four

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** For x ≥ 0, y = x + 1. Substituting into the circle yields x^2 + (x + 1)^2 = 25, or 2x^2 + 2x - 24 = 0, so x^2 + x - 12 = 0 and x = 3 or x = -4. Only x = 3 satisfies x ≥ 0, giving (3, 4). By symmetry (the V and the circle are both symmetric about the y-axis), the arm for x < 0 gives (-3, 4). Therefore, the graphs have exactly two points in common. Distractors: Exactly one stops at (3, 4) and forgets the left arm; Exactly three adds the vertex (0, 1), which lies inside the circle, not on it; Exactly four keeps x = -4 on the right arm and its mirror image, although x = -4 is not on the arm y = x + 1 with x ≥ 0.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=|x|+1</code><br><code>x^2+y^2=25</code>

This is the absolute-value counting picture (T14): the V opens upward from (0, 1), inside the circle, and each arm leaves the circle once, at (-3, 4) and (3, 4). Two common points.

</details>

---

### 115. adv-parabola-line-no-intersection-k

*Hard · Student-produced response · route: desmos-primary · techniques: T4, T2*

In the $xy$-plane, the parabola $y = x^2 - 5x + 2$ and the line $y = x + k$ do not intersect, where $k$ is an integer constant. What is the largest possible value of $k$?

**Answer:** -8

<details><summary>Solutions</summary>

**By hand.** Setting the right-hand sides equal yields x^2 - 5x + 2 = x + k, so x^2 - 6x + (2 - k) = 0. The graphs do not intersect when this has no real solutions, so the discriminant is negative: 36 - 4(2 - k) < 0, so 28 + 4k < 0 and k < -7. The largest integer less than -7 is -8. A common slip is answering -7, the value at which the line is tangent to the parabola and there is one intersection point.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-5x+2</code><br><code>y=x+k</code><br><code>k=0</code>

Add a slider for k (T4), set its range to -15 to 5 and its step to 1. Dragging k down, the line still crosses the parabola at k = -7 (where it just touches at (3, -4)) and misses it at k = -8. The largest integer with no intersection is -8.

</details>

---

### 116. adv-parabola-line-tangent-c

*Hard · Multiple choice · route: either · techniques: T4, T2*

In the $xy$-plane, the graphs of $y = x^2 + 6x + c$ and $y = 2x + 3$ intersect at exactly one point, where $c$ is a constant. What is the value of $c$?

- **A.** $-1$
- **B.** $3$
- **C.** $7$
- **D.** $11$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Setting the expressions for y equal yields x^2 + 6x + c = 2x + 3, so x^2 + 4x + (c - 3) = 0. Exactly one intersection means this equation has exactly one solution, so its discriminant is zero: 16 - 4(c - 3) = 0, so c - 3 = 4 and c = 7. Distractors: 3 sets c - 3 = 0, forgetting the 16; -1 solves c - 3 = -4 (a sign error); 11 uses 16 - 2(c - 3) = 0, halving the 4ac term.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+6x+c</code><br><code>y=2x+3</code>

Add a slider for c (T4) with step 1 and drag until the line just touches the parabola: c = 7. Zoom in to confirm one point rather than two close crossings. Setting the discriminant to zero by hand gives the same value exactly.

</details>

---

### 117. adv-quadratic-formula-radicand

*Hard · Student-produced response · route: hand-primary · techniques: T1, T11*

The solutions to the equation $2x^2 - 8x + 3 = 0$ are $x = 2 + \frac{\sqrt{k}}{2}$ and $x = 2 - \frac{\sqrt{k}}{2}$, where $k$ is a positive constant. What is the value of $k$?

**Answer:** 10

<details><summary>Solutions</summary>

**By hand.** By the quadratic formula, x = (8 ± sqrt(64 - 24))/4 = (8 ± sqrt(40))/4 = 2 ± sqrt(40)/4. Since sqrt(40) = 2 sqrt(10), this is 2 ± sqrt(10)/2. Matching the given form yields k = 10. Alternate approach: divide by 2 and complete the square: x^2 - 4x = -3/2, so (x - 2)^2 = 5/2 and x - 2 = ± sqrt(10)/2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x^2-8x+3</code><br><code>(2(3.5811-2))^2</code>

Click the right x-intercept, 3.5811; then sqrt(k)/2 = 1.5811, and the second line shows (2 · 1.5811)^2 ≈ 10.0. The decimal only approximates; the quadratic formula gives k = 10 exactly, which an SPR needs.

</details>

---

### 118. adv-quadratic-in-disguise-sum

*Hard · Multiple choice · route: hand-primary · techniques: T1*

What is the sum of the solutions to the equation $(x - 4)^2 - 3(x - 4) - 10 = 0$?

- **A.** $3$
- **B.** $7$
- **C.** $11$
- **D.** $18$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let u = x - 4. The equation becomes u^2 - 3u - 10 = 0, which factors as (u - 5)(u + 2) = 0, so u = 5 or u = -2. Then x = u + 4, so x = 9 or x = 2, and the sum of the solutions is 11. Alternate approach: expanding yields x^2 - 11x + 18 = 0, whose solutions sum to 11. Distractors: 3 is the sum of the values of u, before adding 4 back; 7 adds 4 only once to that sum; 18 is the product of the solutions.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x-4)^2-3(x-4)-10</code>

Click the two x-intercepts, (2, 0) and (9, 0), and add: 2 + 9 = 11. Typing the expression and clicking is about as fast as the substitution by hand.

</details>

---

### 119. adv-radical-constant-extraneous-sum

*Hard · Multiple choice · route: either · techniques: T1*

The equation $\sqrt{3x + c} = x - 1$, where $c$ is a constant, has $8$ as a solution. What is the sum of all values of $x$ that satisfy the equation?

- **A.** $5$
- **B.** $8$
- **C.** $11$
- **D.** $25$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting 8 for x yields sqrt(24 + c) = 7, so 24 + c = 49 and c = 25. The equation is then sqrt(3x + 25) = x - 1. Squaring both sides yields 3x + 25 = x^2 - 2x + 1, so x^2 - 5x - 24 = 0 and (x - 8)(x + 3) = 0. The candidate x = -3 gives sqrt(16) = 4 on the left and -4 on the right, so it is extraneous. Therefore, 8 is the only solution, and the sum of all solutions is 8. Distractors: 5 includes the extraneous value -3 in the sum; 11 adds 3 instead of -3 after a sign slip; 25 is the value of c.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{3x+25}</code><br><code>y=x-1</code>

First find c by hand (c = 25), then graph. The curve and the line meet once, at (8, 7); there is no second intersection, so the sum of all solutions is 8.

</details>

---

### 120. adv-rational-all-extraneous-zero

*Hard · Multiple choice · route: hand-primary · techniques: T1*

How many real solutions does the equation $\frac{x}{x + 2} + \frac{8}{x^2 - 4} = \frac{2}{x - 2}$ have?

- **A.** Zero
- **B.** Exactly one
- **C.** Exactly two
- **D.** Infinitely many

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Since x^2 - 4 = (x + 2)(x - 2), the values x = 2 and x = -2 are excluded. Multiplying both sides by (x + 2)(x - 2) yields x(x - 2) + 8 = 2(x + 2), so x^2 - 2x + 8 = 2x + 4 and x^2 - 4x + 4 = 0, which is (x - 2)^2 = 0. The only candidate, x = 2, is excluded, so it is extraneous. Therefore, the equation has zero real solutions. Distractors: Exactly one keeps the extraneous root x = 2; Exactly two counts the repeated root twice; Infinitely many treats the cleared equation as an identity, but the difference of the two sides simplifies to (x - 2)/(x + 2), which is not 0 for any allowed x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x}{x+2}+\frac{8}{x^2-4}-\frac{2}{x-2}</code>

Desmos is slower and can mislead here: the graph of the difference looks like it crosses the x-axis at x = 2, but that point is a hole, since x = 2 makes denominators 0. Type the expression with x=2 substituted in a new line to see it is undefined. Solve by hand and use the graph only to confirm there is no other crossing.

</details>

---

### 121. adv-rational-equation-extraneous

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

What is the solution to the equation $\frac{x}{x - 3} + \frac{2}{x} = \frac{3}{x - 3}$?

**Answer:** -2

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides by x(x - 3), which is nonzero when x ≠ 0 and x ≠ 3, yields x^2 + 2(x - 3) = 3x, so x^2 - x - 6 = 0 and (x - 3)(x + 2) = 0. The candidate x = 3 makes the denominators x - 3 zero, so it is extraneous. Check x = -2: -2/(-5) + 2/(-2) = 2/5 - 1 = -3/5, and 3/(-5) = -3/5. Therefore, the solution is -2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x}{x-3}+\frac{2}{x}</code><br><code>y=\frac{3}{x-3}</code>

The graphs cross exactly once, at (-2, -0.6); read x = -2. Both sides are undefined at x = 3, so no point appears there: the algebra produces x = 3 as an extraneous root, and the graph shows there is nothing to click.

</details>

---

### 122. adv-rational-equation-sum-solutions

*Hard · Multiple choice · route: desmos-primary · techniques: T1, T11*

The equation $\frac{6}{x} + \frac{x}{x + 1} = 2$ has two solutions. What is the sum of these solutions?

- **A.** $-6$
- **B.** $-4$
- **C.** $4$
- **D.** $6$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides by x(x + 1), which is nonzero for any solution, yields 6(x + 1) + x^2 = 2x(x + 1), so 6x + 6 + x^2 = 2x^2 + 2x and x^2 - 4x - 6 = 0. The solutions are 2 ± sqrt(10); neither equals 0 or -1, so neither is extraneous. Their sum is -(-4)/1 = 4. Distractors: -4 is the coefficient of x read as the sum, without the sign change; -6 is the product of the solutions; 6 is that product with its sign reversed.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{6}{x}+\frac{x}{x+1}</code><br><code>y=2</code><br><code>2+\sqrt{10}</code><br><code>2-\sqrt{10}</code>

Click the two intersections: x ≈ 5.162 and x ≈ -1.162. Their sum is 4. The exact values are 2 ± sqrt(10), which the last two lines confirm; the sum is exact even though each value on screen is rounded.

</details>

---

### 123. adv-root-twice-other-c

*Hard · Multiple choice · route: either · techniques: T4*

The equation $x^2 - 9x + c = 0$, where $c$ is a constant, has two real solutions, and one of them is twice the other. What is the value of $c$?

- **A.** $3$
- **B.** $6$
- **C.** $9$
- **D.** $18$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Let the solutions be r and 2r. The sum of the solutions of x^2 - 9x + c = 0 is 9 and the product is c. So r + 2r = 9, which gives r = 3, and the solutions are 3 and 6. Therefore, c = 3 · 6 = 18. Check: x^2 - 9x + 18 = (x - 3)(x - 6). Distractors: 3 is the smaller solution; 6 is the larger solution; 9 is the sum of the solutions, not the product.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-9x+c</code><br><code>c=10</code>

Add a slider for c (T4) with step 1 and click the two x-intercepts as you drag. At c = 18 they are (3, 0) and (6, 0), and 6 is twice 3.

</details>

---

### 124. adv-sqrt-extraneous-root

*Hard · Multiple choice · route: hand-primary · techniques: T1*

The equation $\sqrt{2x + 11} = x - 2$ has exactly one real solution. What is that solution?

- **A.** $-1$
- **B.** $2$
- **C.** $5$
- **D.** $7$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Square both sides: 2x + 11 = x^2 - 4x + 4, so x^2 - 6x - 7 = 0 and (x - 7)(x + 1) = 0. Check both in the original: x = 7 gives sqrt(25) = 5 = 7 - 2, valid; x = -1 gives sqrt(9) = 3 but -1 - 2 = -3, extraneous. Distractors: -1 is the extraneous root; 2 is where the right side is zero; 5 comes from squaring the right side as x^2 - 4 instead of x^2 - 4x + 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{2x+11}</code><br><code>y=x-2</code>

The curve and the line cross once, at (7, 5); the extraneous root -1 never appears because the line is below the x-axis there. Graphing here is about as fast as squaring, and it is the safer check against the extraneous root.

</details>

---

### 125. adv-stopping-distance-speed

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

The equation $d = \frac{v^2}{20} + v$ models the stopping distance of a car, where $d$ is the distance, in feet, and $v$ is the car's speed, in miles per hour. According to the model, at what speed, in miles per hour, is the stopping distance 120 feet?

**Answer:** 40

<details><summary>Solutions</summary>

**By hand.** Setting d = 120 yields v^2/20 + v = 120. Multiplying both sides by 20 yields v^2 + 20v = 2,400, so v^2 + 20v - 2,400 = 0. Two numbers with a product of -2,400 and a sum of 20 are 60 and -40, so the equation factors as (v + 60)(v - 40) = 0, giving v = -60 or v = 40. A speed is positive, so v = 40. Common slips: forgetting to multiply the v term by 20 (v^2 + v = 2,400) or ignoring the v term (v^2 = 2,400), neither of which gives an integer.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^2}{20}+x</code><br><code>y=120</code>

Type v as x. The parabola meets y = 120 at x = -60 and x = 40; zoom out to see both. A speed is positive, so the answer is 40.

</details>

---

### 126. adv-tangent-k

*Hard · Multiple choice · route: desmos-primary · techniques: T1, T4*

In the equation $x^2 - 2kx + 5k = 0$, $k$ is a positive constant. If the equation has exactly one real solution, what is the value of $k$?

- **A.** $\frac{5}{2}$
- **B.** $5$
- **C.** $10$
- **D.** $25$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** One real solution means the discriminant is zero: (2k)^2 - 4(5k) = 4k^2 - 20k = 4k(k - 5) = 0, so k = 5 since k > 0. Distractors: 5/2 uses 2ac in place of 4ac (4k^2 - 10k = 0); 10 squares only the k in (2k)^2, solving 2k^2 - 20k = 0; 25 is k^2, the square of the correct value, reported instead of k.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-2kx+5k</code>

Add a slider for k with step 1. The parabola touches the x-axis at exactly one point when k = 5 (vertex at (5, 0)).

</details>

---

### 127. adv-two-machines-rational-time

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

Working alone, machine A completes a certain job in $x$ hours, and machine B completes the same job in $x + 3$ hours. Working together at these rates, the two machines complete the job in 2 hours. What is the value of $x$?

**Answer:** 3

<details><summary>Solutions</summary>

**By hand.** Machine A does 1/x of the job each hour and machine B does 1/(x + 3), so together they do 1/2 of the job each hour: 1/x + 1/(x + 3) = 1/2. Multiplying both sides by 2x(x + 3) yields 2(x + 3) + 2x = x(x + 3), so 4x + 6 = x^2 + 3x and x^2 - x - 6 = 0. This factors as (x - 3)(x + 2) = 0, so x = 3 or x = -2. A time can't be negative, so x = 3. Check: 1/3 + 1/6 = 1/2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{1}{x}+\frac{1}{x+3}</code><br><code>y=\frac{1}{2}</code>

The combined-rate curve meets y = 1/2 at x = -2 and x = 3. A time must be positive, so take x = 3.

</details>

---

### 128. adv-two-parabolas-greatest-integer-k

*Hard · Multiple choice · route: either · techniques: T4, T2*

The graphs of $y = x^2 + k$ and $y = -x^2 + 6x$ in the $xy$-plane intersect at exactly two points, where $k$ is an integer constant. What is the greatest possible value of $k$?

- **A.** $4$
- **B.** $5$
- **C.** $8$
- **D.** $9$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Setting the right-hand sides equal yields x^2 + k = -x^2 + 6x, so 2x^2 - 6x + k = 0. The graphs meet at two points when this equation has two real solutions, which happens when the discriminant is positive: (-6)^2 - 4(2)(k) > 0, so 36 - 8k > 0 and k < 4.5. The greatest integer less than 4.5 is 4. Distractors: 5 rounds 4.5 up; 8 and 9 come from dropping one of the x^2 terms (x^2 - 6x + k = 0 gives 36 - 4k > 0, so k < 9), with 9 also using the boundary itself.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+k</code><br><code>y=-x^2+6x</code><br><code>k=4</code>

Add a slider for k with step 1 (T4). At k = 4 the parabolas cross twice; at k = 5 the upward parabola sits entirely above the downward one and they don't meet. So the greatest integer with two intersections is 4.

</details>

---

### 129. adv-two-parabolas-tangent-k

*Hard · Multiple choice · route: desmos-primary · techniques: T4, T2*

The graphs of $y = (x - 1)^2 + k$ and $y = -(x - 3)^2 + 5$ in the $xy$-plane have exactly one point in common, where $k$ is a constant. What is the value of $k$?

- **A.** $-3$
- **B.** $1$
- **C.** $3$
- **D.** $5$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** At a common point the y-values are equal, so (x - 1)^2 + k = -(x - 3)^2 + 5. Expanding and collecting terms yields x^2 - 2x + 1 + k + x^2 - 6x + 9 - 5 = 0, or 2x^2 - 8x + 5 + k = 0. The graphs have exactly one point in common when this equation has exactly one real solution, which happens when its discriminant is 0: (-8)^2 - 4(2)(5 + k) = 64 - 40 - 8k = 24 - 8k = 0, so k = 3. Distractors: -3 results from the sign error 5 - 8 = -3 when solving 8(5 + k) = 64; 1 assumes the common point is the vertex (1, k) of the first parabola and sets k equal to the second parabola's value there; 5 copies the constant from the second equation as if the vertices had to share a y-coordinate.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x-1)^2+k</code><br><code>y=-(x-3)^2+5</code><br><code>k=0</code>

Add a slider for k (T4) and drag it: for small k the upward parabola cuts the downward one twice; as k grows the two crossings merge into a single touching point and then vanish. Set the slider step to 1 and stop where exactly one gray point remains: k = 3, with the common point at (2, 4).

</details>

---

### 130. adv-two-real-solutions-least-integer-k

*Hard · Multiple choice · route: either · techniques: T4, T1*

The equation $x^2 - 2kx + 5k - 6 = 0$ has exactly two distinct real solutions, where $k$ is a positive integer constant. What is the least possible value of $k$?

- **A.** $4$
- **B.** $3$
- **C.** $2$
- **D.** $1$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A quadratic equation ax^2 + bx + c = 0 has exactly two distinct real solutions when its discriminant b^2 - 4ac is positive. Here the discriminant is (-2k)^2 - 4(1)(5k - 6) = 4k^2 - 20k + 24 = 4(k - 2)(k - 3), which is positive when k < 2 or k > 3. The positive integers that satisfy this are 1, 4, 5, and so on, so the least possible value of k is 1. Checking: k = 1 gives x^2 - 2x - 1 = 0, whose discriminant is 8. Distractors: 2 and 3 make the discriminant 0, so the equation has exactly one real solution for each; 4 is the least integer greater than 3 and is chosen by a student who finds only the k > 3 branch of the inequality.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-2kx+5k-6</code><br><code>k=1</code>

Add a slider for k (T4) with step 1 and count the x-intercepts for each value, the same slider-and-count move as T14: at k = 1 the parabola crosses the x-axis twice (vertex at (1, -2)); at k = 2 and k = 3 it only touches the axis; at k = 4 it crosses twice again. The least positive integer with two crossings is 1.

</details>

---

### 131. adv-two-solutions-k-condition

*Hard · Multiple choice · route: either · techniques: T4*

The equation $2x^2 - 8x + k = 0$, where $k$ is a constant, has two distinct real solutions. Which of the following must be true?

- **A.** $k < 8$
- **B.** $k < 32$
- **C.** $k > 8$
- **D.** $k > 32$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A quadratic equation ax^2 + bx + c = 0 has two distinct real solutions when its discriminant b^2 - 4ac is positive. Here (-8)^2 - 4(2)(k) = 64 - 8k > 0, so 8k < 64 and k < 8. Distractors: k > 8 flips the inequality (that is the condition for no real solutions); k < 32 and k > 32 use 64 - 2k, forgetting the factor of 4 in the discriminant.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x^2-8x+k</code>

Add a slider for k (T4) and drag it: the parabola crosses the x-axis twice while its vertex is below the axis, which happens for every k less than 8; at k = 8 it touches once, and above 8 it never crosses. The slider shows the picture; the discriminant gives the exact boundary.

</details>

---

### 132. adv-vieta-other-root

*Hard · Student-produced response · route: hand-primary · techniques: T4, T1, T11*

One solution of the equation $4x^2 - 11x + c = 0$ is $x = 3$, where $c$ is a constant. What is the other solution?

**Answer:** -1/4 (≈ -0.25)

<details><summary>Solutions</summary>

**By hand.** The roots of 4x^2 - 11x + c = 0 add to 11/4. One root is 3, so the other is 11/4 - 3 = -1/4. (Check: substituting x = 3 gives 36 - 33 + c = 0, so c = -3, and 4x^2 - 11x - 3 = (x - 3)(4x + 1).)

**Desmos** (not yet verified in Desmos). Type:<br><code>y=4x^2-11x+c</code>

Add a slider for c and drag until one x-intercept sits at 3 (c = -3); then click the other intercept, -0.25. Enter -1/4 or -0.25. Vieta's sum is faster: the roots add to 11/4.

</details>

---

### 133. adv-vieta-sum-to-product

*Hard · Multiple choice · route: hand-primary · techniques: T4, T1*

In the equation $3x^2 - (k + 5)x + 2k = 0$, $k$ is a constant. If the sum of the two solutions of the equation is $6$, what is the product of the solutions?

- **A.** $\frac{13}{3}$
- **B.** $\frac{26}{3}$
- **C.** $13$
- **D.** $26$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** For ax^2 + bx + c = 0 the sum of the roots is -b/a and the product is c/a. Here the sum is (k + 5)/3 = 6, so k + 5 = 18 and k = 13. The product is 2k/3 = 26/3. (The discriminant 18^2 - 4 · 3 · 26 = 12 is positive, so the two roots are real.) Distractors: 26 is 2k without dividing by the leading coefficient; 13 is k itself; 13/3 is k/3, forgetting the factor of 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x^2-(k+5)x+2k</code>

Desmos cannot name the sum of the roots directly. With a slider for k you can drag until the two x-intercepts (click them) add to 6, at k = 13, then multiply the intercepts: 8.667, or 26/3 with the fraction toggle. Vieta by hand is much faster.

</details>

---
