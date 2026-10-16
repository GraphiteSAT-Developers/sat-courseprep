# Nonlinear functions

[← Question bank index](README.md) · Advanced Math · 117 questions, easiest first

### 1. adv-cubic-evaluate-negative

*Easy · Multiple choice · route: either · techniques: T9*

The function $f$ is defined by $f(x) = 3x^3 - x^2 + 4$. What is the value of $f(-2)$?

- **A.** $-24$
- **B.** $-16$
- **C.** $24$
- **D.** $32$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Substituting -2 for x yields 3(-2)^3 - (-2)^2 + 4 = 3(-8) - 4 + 4 = -24. Distractors: -16 treats (-2)^2 as -4, giving -24 + 4 + 4; 24 treats (-2)^3 as 8, giving 24 - 4 + 4; 32 makes both sign errors.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=3x^3-x^2+4</code><br><code>f(-2)</code>

The second line shows -24. Typing the function once also lets f be evaluated at any other input.

</details>

---

### 2. adv-exponential-initial-value-club

*Easy · Multiple choice · route: hand-primary · techniques: —*

The function $N(t) = 640(1.08)^t$ models the number of members of a certain club $t$ years after the club was founded. Which of the following is the best interpretation of 640 in this context?

- **A.** The club had 640 members when it was founded.
- **B.** The club gained 640 members during its first year.
- **C.** The club had 640 members 1 year after it was founded.
- **D.** The number of members increases by 640 each year.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Substituting 0 for t yields N(0) = 640(1.08)^0 = 640, so 640 is the number of members at the time the club was founded. Distractors: 'had 640 members 1 year after it was founded' describes N(1) = 691.2, not 640; 'gained 640 members during its first year' confuses the initial value with the change N(1) - N(0) = 51.2; 'increases by 640 each year' treats the model as linear, but the factor 1.08 means the number grows by 8% each year, not by a fixed amount.

</details>

---

### 3. adv-exponential-model-evaluate-leaves

*Easy · Multiple choice · route: either · techniques: T9*

The function $f(t) = 3 \cdot 2^t + 1$ models the number of leaves on a certain plant $t$ weeks after it is planted. How many leaves does the model predict the plant has 3 weeks after it is planted?

- **A.** $19$
- **B.** $24$
- **C.** $25$
- **D.** $217$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Substituting 3 for t yields f(3) = 3 · 2^3 + 1 = 3 · 8 + 1 = 25. Distractors: 24 omits the + 1; 19 reads 2^t as 2t (3 · 6 + 1); 217 multiplies 3 by 2 before applying the exponent ((3 · 2)^3 + 1).

**Desmos** (not yet verified in Desmos). Type:<br><code>f(t)=3\cdot2^t+1</code><br><code>f(3)</code>

f(3) shows 25. Substituting by hand is just as quick.

</details>

---

### 4. adv-message-board-posts-weeks

*Easy · Multiple choice · route: either · techniques: T1, T9*

The function $N(w) = 4(2)^w$ models the number of posts on a message board $w$ weeks after the board opens. According to the model, after how many weeks does the board have 128 posts?

- **A.** $4$
- **B.** $5$
- **C.** $6$
- **D.** $32$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting 128 for N(w) yields 4(2)^w = 128. Dividing both sides by 4 yields 2^w = 32, and since 2^5 = 32, w = 5. Therefore, the board has 128 posts after 5 weeks. Distractors: 4 and 6 are off by one power of 2 (2^4 = 16 and 2^6 = 64 on the wrong side of 32); 32 is the value of 2^w, not of w.

**Desmos** (not yet verified in Desmos). Type:<br><code>N(w)=4(2)^w</code><br><code>y=N(x)</code><br><code>y=128</code>

Define N (T9), graph y = N(x) and the horizontal line y = 128, and click the intersection: (5, 128). The answer is 5 weeks.

</details>

---

### 5. adv-nf-channel-followers-weekly-percent

*Easy · Multiple choice · route: hand-primary · techniques: —*

The function $F(w) = 850(1.06)^w$ models the number of followers of an online cooking channel $w$ weeks after the channel launched. According to the model, by what percent does the number of followers increase each week?

- **A.** $0.06\%$
- **B.** $1.06\%$
- **C.** $6\%$
- **D.** $106\%$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that F(w) = 850(1.06)^w. An exponential model a(1 + r)^w increases by the rate r, written as a percent, for each increase of 1 in w. Since 1.06 = 1 + 0.06, the weekly growth rate is 0.06, or 6%. Therefore, the number of followers increases by 6% each week. Distractors: 0.06% writes the decimal rate 0.06 as if it were already a percent; 1.06% writes the growth factor 1.06 as a percent without subtracting 1; 106% is the growth factor as a percent, the percent of the previous week's followers, not the percent increase.

</details>

---

### 6. adv-nf-composition-quadratic-linear

*Easy · Multiple choice · route: desmos-primary · techniques: T9*

If $f(x) = x^2 - 3x$ and $g(x) = 2x + 1$, what is the value of $f(g(3))$?

- **A.** $1$
- **B.** $7$
- **C.** $28$
- **D.** $70$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Working from the inside out, g(3) = 2(3) + 1 = 7. Substituting 7 for x in f yields f(7) = 7^2 - 3(7) = 49 - 21 = 28. Therefore, the value of f(g(3)) is 28. Distractors: 1 is g(f(3)) = g(0), the composition in the wrong order; 7 is g(3), the inner value reported as final; 70 adds 3(7) instead of subtracting it, a sign slip (49 + 21).

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=x^2-3x</code><br><code>g(x)=2x+1</code><br><code>f(g(3))</code>

The last line shows 28. Typing f(g(3)) with both sets of parentheses keeps the order of the composition right.

</details>

---

### 7. adv-nf-cubic-negative-leading-term-right-end

*Easy · Multiple choice · route: hand-primary · techniques: —*

The function $f$ is defined by $f(x) = 2x - 3x^3$. Which statement describes the values of $f(x)$ as $x$ increases without bound?

- **A.** The values of $f(x)$ approach $-3$.
- **B.** The values of $f(x)$ approach $0$.
- **C.** The values of $f(x)$ decrease without bound.
- **D.** The values of $f(x)$ increase without bound.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** For large values of x, the term with the highest power, -3x^3, determines the size and sign of f(x). As x increases without bound, x^3 increases without bound, so -3x^3 decreases without bound, and adding 2x cannot offset it. For example, f(10) = 20 - 3,000 = -2,980. Therefore, the values of f(x) decrease without bound. Distractors: approach -3 treats the leading coefficient as a value the function levels off at; approach 0 applies the behavior of a function such as 1/x to a polynomial; increase without bound looks only at the first term written, 2x, which is positive.

</details>

---

### 8. adv-nf-cubic-x-intercept-point

*Easy · Multiple choice · route: either · techniques: T1, T13*

The function $f$ is defined by $f(x) = (x + 4)(x - 3)(2x - 5)$. Which of the following is an $x$-intercept of the graph of $y = f(x)$ in the $xy$-plane?

- **A.** $(-3, 0)$
- **B.** $(-2.5, 0)$
- **C.** $(0, 60)$
- **D.** $(3, 0)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The x-intercepts of the graph of y = f(x) are the points where f(x) = 0. A product is 0 when one of its factors is 0, so x + 4 = 0, x - 3 = 0 or 2x - 5 = 0, which yields x = -4, x = 3 or x = 2.5. Therefore, the x-intercepts are (-4, 0), (3, 0) and (2.5, 0), and of the choices only (3, 0) is one. Distractors: (-3, 0) takes the zero of x - 3 with the wrong sign; (-2.5, 0) takes the zero of 2x - 5 with the wrong sign; (0, 60) is the y-intercept, since f(0) = (4)(-3)(-5) = 60, a point on the graph but not an x-intercept.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x+4)(x-3)(2x-5)</code>

Click the gray x-intercepts: (-4, 0), (2.5, 0) and (3, 0). Of the choices, only (3, 0) is one. (0, 60) is on the graph, but it is the y-intercept. Reading the zeros from the factors is just as quick.

</details>

---

### 9. adv-nf-downward-vertex-form-vertex-point

*Easy · Multiple choice · route: hand-primary · techniques: —*

A parabola in the $xy$-plane has equation $y = -2(x - 7)^2 + 3$. Which point is the vertex of the parabola?

- **A.** $(-7, 3)$
- **B.** $(3, 7)$
- **C.** $(7, -3)$
- **D.** $(7, 3)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A parabola with equation y = a(x - h)^2 + k has its vertex at (h, k). The given equation has this form with a = -2, h = 7 and k = 3. Therefore, the vertex is (7, 3). The negative value of a only means the parabola opens downward, so (7, 3) is its highest point. Distractors: (-7, 3) takes h as -7, the sign shown inside the parentheses; (7, -3) changes the sign of k; (3, 7) swaps the two coordinates. Graphing the equation in Desmos and clicking the vertex confirms (7, 3), but reading vertex form is faster.

</details>

---

### 10. adv-nf-factored-vertex-x-coordinate

*Easy · Multiple choice · route: either · techniques: T1*

In the $xy$-plane, the graph of $y = (x - 4)(x + 10)$ is a parabola. At what value of $x$ does the vertex of the parabola occur?

- **A.** $-40$
- **B.** $-10$
- **C.** $-3$
- **D.** $3$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The x-intercepts of the parabola are at x = 4 and x = -10. A parabola is symmetric about the vertical line through its vertex, so the x-coordinate of the vertex is the mean of the zeros: (4 + (-10))/2 = -3. Therefore, the x-coordinate of the vertex is -3. Distractors: -40 is the value of y when x = 0, the y-coordinate of the y-intercept; -10 is one of the zeros, not the vertex; 3 averages the zeros with their signs reversed, (-4 + 10)/2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x-4)(x+10)</code>

Click the vertex of the parabola: (-3, -49). The question asks for the x-coordinate, -3. Zoom out if the vertex is below the window.

</details>

---

### 11. adv-nf-fireworks-height-gap-one-second

*Easy · Multiple choice · route: either · techniques: T9*

The functions $A(t) = -5t^2 + 40t + 2$ and $B(t) = -5t^2 + 34t + 6$ model the heights, in meters, of fireworks shells A and B $t$ seconds after launch. How many meters higher is shell A than shell B at $t = 1$?

- **A.** $2$
- **B.** $4$
- **C.** $6$
- **D.** $37$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Substituting 1 for t yields A(1) = -5 + 40 + 2 = 37 and B(1) = -5 + 34 + 6 = 35. The difference is 37 - 35 = 2. Therefore, shell A is 2 meters higher than shell B at t = 1. Distractors: 4 is the difference of the constant terms, 6 - 2, which compares the launch heights; 6 is the difference of the t coefficients, 40 - 34; 37 is A(1), the height of shell A alone.

**Desmos** (not yet verified in Desmos). Type:<br><code>A(x)=-5x^2+40x+2</code><br><code>B(x)=-5x^2+34x+6</code><br><code>A(1)-B(1)</code>

The third line shows 2, the number of meters by which shell A is higher.

</details>

---

### 12. adv-nf-parabola-shift-left-down-equation

*Easy · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, the graph of $y = x^2$ is moved 3 units left and 2 units down. Which equation represents the resulting graph?

- **A.** $y = (x + 3)^2 - 2$
- **B.** $y = (x + 3)^2 + 2$
- **C.** $y = (x - 3)^2 - 2$
- **D.** $y = (x + 2)^2 - 3$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Shifting a graph h units left replaces x with x + h, and shifting it k units down subtracts k from the output. Replacing x with x + 3 and subtracting 2 yields y = (x + 3)^2 - 2, whose vertex is (-3, -2). Therefore, the resulting graph is y = (x + 3)^2 - 2. Distractors: y = (x + 3)^2 + 2 moves the graph up instead of down; y = (x - 3)^2 - 2 moves it right instead of left; y = (x + 2)^2 - 3 swaps the horizontal and vertical shift amounts.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2</code><br><code>y=(x+3)^2-2</code>

Type y = x^2 and then each choice (T13). The correct graph has its vertex at (-3, -2), 3 units left of and 2 units below the vertex (0, 0) of y = x^2.

</details>

---

### 13. adv-nf-pool-chemical-half-life-amount

*Easy · Multiple choice · route: either · techniques: T9*

The function $A(t) = 96(\frac{1}{2})^{t/4}$ models the amount of a cleaning chemical remaining in a pool $t$ hours after it is added. According to the model, what is the amount, in grams, of the chemical remaining 12 hours after it is added?

- **A.** $12$
- **B.** $24$
- **C.** $32$
- **D.** $48$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Substituting 12 for t yields A(12) = 96(1/2)^(12/4) = 96(1/2)^3 = 96/8 = 12. The amount halves every 4 hours, and 12 hours is three halvings: 96, 48, 24, 12. Therefore, 12 grams of the chemical remain. Distractors: 24 stops after two halvings; 32 divides 96 by the number of halvings, 3, instead of by 2^3; 48 halves only once, treating 12 hours as a single halving period.

**Desmos** (not yet verified in Desmos). Type:<br><code>A(t)=96(1/2)^{t/4}</code><br><code>A(12)</code>

The evaluation line A(12) shows 12.

</details>

---

### 14. adv-nf-quadratic-evaluate-at-negative-two

*Easy · Multiple choice · route: either · techniques: T9*

For the function $f(x) = x^2 - 4x + 7$, what is the value of $f(-2)$?

- **A.** $-5$
- **B.** $3$
- **C.** $11$
- **D.** $19$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Substituting -2 for x in f(x) = x^2 - 4x + 7 yields (-2)^2 - 4(-2) + 7 = 4 + 8 + 7 = 19. Therefore, f(-2) = 19. Distractors: 11 results from evaluating (-2)^2 as -4; 3 results from evaluating -4(-2) as -8; -5 results from making both of those sign errors.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=x^2-4x+7</code><br><code>f(-2)</code>

The second line shows 19. Type the parentheses around -2 so Desmos squares the negative number.

</details>

---

### 15. adv-nf-quilt-width-rule-area

*Easy · Student-produced response · route: hand-primary · techniques: —*

A rectangular quilt is 2 feet longer than it is wide. The function $A$ gives the area, in square feet, of the quilt when its width is $x$ feet. What is the value of $A(6)$?

**Answer:** 48

<details><summary>Solutions</summary>

**By hand.** It's given that the quilt is 2 feet longer than it is wide, so a quilt of width x feet has length (x + 2) feet. The area of a rectangle is its length times its width, so A(x) = x(x + 2). Substituting 6 for x yields A(6) = 6(6 + 2) = 6(8) = 48. Therefore, the value of A(6) is 48. Desmos is no faster here: the work is writing the rule, after which A(6) is one multiplication.

</details>

---

### 16. adv-nf-radical-evaluate-scaled-root

*Easy · Multiple choice · route: hand-primary · techniques: T9*

The function $f$ is defined by $f(x) = 3\sqrt{2x - 1} + 4$. What is the value of $f(5)$?

- **A.** $9$
- **B.** $13$
- **C.** $21$
- **D.** $31$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting 5 for x yields f(5) = 3√(2(5) - 1) + 4 = 3√9 + 4 = 3(3) + 4 = 13. Therefore, the value of f(5) is 13. Distractors: 9 is 3√9 without the + 4; 21 adds 4 to the root before multiplying, 3(3 + 4), a grouping slip; 31 skips the square root, 3(9) + 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=3\sqrt{2x-1}+4</code><br><code>f(5)</code>

By hand this is one substitution, so Desmos is slower. As a check, the evaluation line f(5) shows 13.

</details>

---

### 17. adv-nf-rational-evaluate-at-five

*Easy · Multiple choice · route: either · techniques: T9*

The function $f$ is defined by $f(x) = \frac{2x + 10}{x - 3}$. What is the value of $f(5)$?

- **A.** $\frac{5}{2}$
- **B.** $10$
- **C.** $15$
- **D.** $20$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting 5 for x in the given function yields f(5) = (2(5) + 10)/(5 - 3) = 20/2 = 10. Therefore, the value of f(5) is 10. Distractors: 5/2 uses 5 + 3 = 8 in the denominator, a sign slip that gives 20/8; 15 divides only the 10 by 2 and then adds 2(5), an order-of-operations slip (10 + 10/2); 20 is the numerator, an intermediate result reported as final.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=\frac{2x+10}{x-3}</code><br><code>f(5)</code>

The evaluation line shows 10. Substituting by hand is just as fast.

</details>

---

### 18. adv-nf-rational-undefined-input

*Easy · Multiple choice · route: hand-primary · techniques: T9*

For the function $r$ defined by $r(x) = \frac{x + 6}{2x - 10}$, what value of $x$ makes $r(x)$ undefined?

- **A.** $-6$
- **B.** $-5$
- **C.** $5$
- **D.** $10$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A rational function is undefined where its denominator is 0. Setting 2x - 10 = 0 yields 2x = 10, so x = 5. Therefore, r(x) is undefined when x = 5. Distractors: -6 makes the numerator 0, where r(x) = 0 is defined; -5 is a sign error in solving 2x - 10 = 0; 10 sets x equal to the constant 10 without dividing by 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>r(x)=\frac{x+6}{2x-10}</code><br><code>r(5)</code>

Setting the denominator equal to 0 is faster by hand. As a check, the line r(5) shows undefined, and the graph of y = r(x) has a vertical asymptote at x = 5.

</details>

---

### 19. adv-nf-remainder-cubic-divided-by-binomial

*Easy · Multiple choice · route: either · techniques: T9*

Let $p(x) = x^3 - 4x^2 + 2x + 9$. What is the remainder when $p(x)$ is divided by $x - 3$?

- **A.** $-60$
- **B.** $0$
- **C.** $6$
- **D.** $9$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** By the remainder theorem, the remainder when a polynomial p(x) is divided by x - a is p(a). Substituting 3 for x yields p(3) = 27 - 4(9) + 2(3) + 9 = 27 - 36 + 6 + 9 = 6. Therefore, the remainder is 6. Distractors: -60 is p(-3), which uses the opposite sign of the number that makes x - 3 zero; 0 assumes that x - 3 is a factor of p(x) without checking; 9 is the constant term of p(x), which is p(0), not p(3).

**Desmos** (not yet verified in Desmos). Type:<br><code>p(x)=x^3-4x^2+2x+9</code><br><code>p(3)</code>

By the remainder theorem the remainder is p(3). The evaluation line p(3) shows 6. Evaluate at 3, not at -3.

</details>

---

### 20. adv-nf-shifted-exponential-y-intercept

*Easy · Multiple choice · route: either · techniques: T9*

At what point does the graph of $y = 5(3)^x - 2$ cross the $y$-axis in the $xy$-plane?

- **A.** $(0, 3)$
- **B.** $(0, 5)$
- **C.** $(0, 13)$
- **D.** $(0, 15)$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The graph crosses the y-axis where x = 0. Substituting 0 for x yields y = 5(3)^0 - 2 = 5(1) - 2 = 3. Therefore, the graph crosses the y-axis at (0, 3). Distractors: (0, 5) uses the coefficient alone and ignores the -2; (0, 13) uses the value at x = 1 instead of x = 0; (0, 15) multiplies 5 by the base 3, which treats 3^0 as 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5(3)^x-2</code>

Click the point where the curve crosses the y-axis: (0, 3).

</details>

---

### 21. adv-nf-vertex-form-minimum-value

*Easy · Multiple choice · route: hand-primary · techniques: —*

The function $f$ is defined by $f(x) = 4(x + 6)^2 - 11$. What is the minimum value of $f$?

- **A.** $-11$
- **B.** $-6$
- **C.** $6$
- **D.** $11$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A quadratic function in the form f(x) = a(x - h)^2 + k with a > 0 has its minimum value k at x = h. The given function can be written as f(x) = 4(x - (-6))^2 + (-11), and a = 4 is positive, so the minimum value of f is -11, which occurs at x = -6. Therefore, the minimum value of f is -11. Distractors: -6 is the x-value where the minimum occurs, not the minimum value; 6 is that x-value with the wrong sign; 11 drops the negative sign of the constant term.

</details>

---

### 22. adv-van-decay-factor-interpretation

*Easy · Multiple choice · route: hand-primary · techniques: —*

The function $V(t) = 38,000(0.85)^t$ models the value, in dollars, of a delivery van $t$ years after it is purchased. Which of the following is the best interpretation of $0.85$ in this context?

- **A.** The value of the van decreases by 85 dollars each year.
- **B.** The value of the van decreases by 85% each year.
- **C.** The value of the van decreases by 15% each year.
- **D.** The value of the van increases by 15% each year.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** In an exponential model V(t) = a · b^t, the value is multiplied by b for each increase of 1 in t. Here b = 0.85, so each year the value is 85% of the previous year's value, which is a decrease of 100% - 85% = 15% each year. Distractors: decreases by 85% each year reads the factor itself as the percent decrease; increases by 15% each year has the wrong direction (a factor less than 1 means decay); decreases by 85 dollars each year treats the factor as a constant amount subtracted each year, which would be a linear model.

</details>

---

### 23. adv-arch-symmetry-distance

*Medium · Multiple choice · route: either · techniques: T9, T1*

The function $h(x) = -0.05x^2 + 3x$ models the height $h(x)$, in meters, of an arch at a horizontal distance of $x$ meters from one end. The arch has the same height at distances of $10$ meters and $k$ meters from that end, where $k > 10$. What is the value of $k$?

- **A.** $25$
- **B.** $30$
- **C.** $40$
- **D.** $50$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A parabola is symmetric about the vertical line through its vertex. The vertex of y = -0.05x^2 + 3x is at x = -3/(2 · (-0.05)) = 30, so heights are equal at distances the same amount on either side of 30. Since 10 is 20 less than 30, k = 30 + 20 = 50. Alternate approach: h(10) = -5 + 30 = 25, and solving -0.05x^2 + 3x = 25 yields x^2 - 60x + 500 = 0, so (x - 10)(x - 50) = 0 and k = 50. Distractors: 30 is the axis of symmetry, not the second distance; 25 is the height h(10), the wrong quantity; 40 adds only 10 to the axis of symmetry instead of the full 20.

**Desmos** (not yet verified in Desmos). Type:<br><code>h(x)=-0.05x^2+3x</code><br><code>y=h(x)</code><br><code>y=h(10)</code>

The horizontal line y = h(10) = 25 crosses the arch twice; click the right-hand crossing: (50, 25). So k = 50. Alternatively click the vertex (30, 45) and use symmetry: 30 + (30 - 10) = 50.

</details>

---

### 24. adv-ball-vertex-form-interpret-max

*Medium · Multiple choice · route: hand-primary · techniques: T9, T1*

The function $h(t) = -5(t - 3)^2 + 50$ models the height, in meters, of a ball $t$ seconds after it is launched. Which of the following is the best interpretation of 50 in this context?

- **A.** The ball is launched from a height of 50 meters.
- **B.** The ball reaches its maximum height 50 seconds after it is launched.
- **C.** The maximum height of the ball is 50 meters.
- **D.** The height of the ball decreases by 50 meters each second.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The expression -5(t - 3)^2 + 50 is in vertex form. Since -5(t - 3)^2 ≤ 0 for every t, the height is at most 50, reached when t = 3. Therefore, 50 is the maximum height, in meters. Distractors: 'launched from a height of 50 meters' describes h(0), which is -5(9) + 50 = 5; 'maximum height 50 seconds after' confuses the maximum value with the time, 3 seconds, at which it occurs; 'decreases by 50 meters each second' treats the model as linear.

**Desmos** (not yet verified in Desmos). Type:<br><code>h(t)=-5(t-3)^2+50</code><br><code>y=h(x)</code><br><code>h(0)</code>

Graph y = h(x) and click the vertex: (3, 50), the highest point, so 50 is the maximum height. h(0) shows 5, the launch height, which rules out that reading. Reading the vertex form by hand is faster.

</details>

---

### 25. adv-decay-rate-interpretation

*Medium · Multiple choice · route: hand-primary · techniques: T9*

The function $M(t) = 820(0.94)^{t/3}$ models the mass, in grams, of a sample of a substance $t$ days after it was first measured. Which of the following is the best interpretation of the number 0.94 in this context?

- **A.** The mass decreases by 2% each day.
- **B.** The mass decreases by 6% each day.
- **C.** The mass decreases by 6% every 3 days.
- **D.** The mass decreases by 94% every 3 days.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The exponent t/3 increases by 1 when t increases by 3, so the mass is multiplied by 0.94 every 3 days, a 6% decrease. Distractors: '6% each day' ignores the division by 3 in the exponent; '2% each day' divides 6% by 3, but exponential change does not split evenly (the daily factor is 0.94^(1/3) ≈ 0.9796); '94% every 3 days' reads the factor as the percent removed instead of the percent remaining.

**Desmos** (not yet verified in Desmos). Type:<br><code>M(t)=820\cdot0.94^{t/3}</code><br><code>\frac{M(3)}{M(0)}</code><br><code>\frac{M(1)}{M(0)}</code>

M(3)/M(0) shows 0.94, a 6% drop over 3 days. M(1)/M(0) shows 0.9796, so the daily drop is about 2.04%, not exactly 2%. Reading the exponent by hand is faster; the ratios only confirm it.

</details>

---

### 26. adv-distinct-intercepts-multiplicity

*Medium · Multiple choice · route: either · techniques: T1*

The function $f$ is defined by $f(x) = x(x - 4)^2(x^2 + 1)$. How many distinct $x$-intercepts does the graph of $y = f(x)$ have in the $xy$-plane?

- **A.** $5$
- **B.** $4$
- **C.** $3$
- **D.** $2$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The x-intercepts of the graph of y = f(x) are the real solutions of f(x) = 0. Setting each factor equal to 0 yields x = 0, (x - 4)^2 = 0 so x = 4, and x^2 + 1 = 0, which has no real solutions because x^2 + 1 is at least 1. The factor (x - 4)^2 has a repeated zero, but it gives only one intercept, (4, 0). Therefore, the graph has 2 distinct x-intercepts. Distractors: 3 counts the double zero at x = 4 twice; 4 counts x = 0, x = 4, and two zeros from x^2 + 1, which has none; 5 is the degree of the polynomial, the maximum number of real zeros, not the actual number.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x(x-4)^2(x^2+1)</code>

Click along the x-axis: the graph crosses at (0, 0) and touches at (4, 0) and nowhere else, so there are 2 distinct x-intercepts. Zoom out to check that nothing else is hidden; the x^2 + 1 factor never reaches 0.

</details>

---

### 27. adv-exponential-translation-y-intercept

*Medium · Multiple choice · route: either · techniques: T9, T11*

In the $xy$-plane, the graph of $y = g(x)$ is the graph of $y = 2^x$ translated 3 units to the right and 4 units down. What is the value of $g(0)$?

- **A.** $-\frac{31}{8}$
- **B.** $-3$
- **C.** $4$
- **D.** $\frac{33}{8}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Translating 3 units to the right replaces x with x - 3, and translating 4 units down subtracts 4, so g(x) = 2^(x - 3) - 4. Then g(0) = 2^(-3) - 4 = 1/8 - 4 = -31/8. Distractors: -3 ignores the horizontal shift (2^0 - 4); 4 shifts left instead of right (2^3 - 4); 33/8 shifts up instead of down (1/8 + 4).

**Desmos** (not yet verified in Desmos). Type:<br><code>g(x)=2^{x-3}-4</code><br><code>g(0)</code><br><code>y=g(x)</code>

Define g and read g(0): -3.875, which the fraction toggle shows as -31/8. Graph y = g(x) to confirm the shift: the curve crosses the y-axis a little below -4 + 0.125.

</details>

---

### 28. adv-exponential-two-points

*Medium · Multiple choice · route: either · techniques: T5, T9*

The function $f$ is defined by $f(x) = a \cdot b^x$, where $a$ and $b$ are positive constants. If $f(1) = 12$ and $f(3) = 48$, what is the value of $f(0)$?

- **A.** $3$
- **B.** $4$
- **C.** $6$
- **D.** $12$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Divide: f(3)/f(1) = b^2 = 48/12 = 4, so b = 2. Then 12 = a · 2 gives a = 6, and f(0) = a = 6. Distractors: 4 is b^2 = 48/12, reported without taking the square root; 3 comes from using b = 4 (forgetting the square root), so a = 12/4 = 3; 12 is f(1).

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,3]</code><br><code>y_1=[12,48]</code><br><code>y_1\sim ab^{x_1}</code><br><code>f(x)=ab^x</code><br><code>f(0)</code>

The regression gives a = 6 and b = 2; f(0) shows 6.

</details>

---

### 29. adv-fountain-stream-zero

*Medium · Multiple choice · route: hand-primary · techniques: T9*

The function $h(x) = -0.5x^2 + 6x$ models the height $h(x)$, in feet, of a stream of water above a nozzle at a horizontal distance of $x$ feet from the nozzle. At what horizontal distance, in feet, from the nozzle does the water return to the height of the nozzle?

- **A.** $3$
- **B.** $6$
- **C.** $12$
- **D.** $18$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The water is at the height of the nozzle when h(x) = 0. Factoring yields x(-0.5x + 6) = 0, so x = 0 or x = 12. The distance 0 is the nozzle itself, so the water returns to the nozzle's height 12 feet away. Distractors: 6 is the horizontal distance of the highest point, the wrong quantity; 18 is the maximum height h(6); 3 multiplies 6 by 0.5 instead of dividing by it.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-0.5x^2+6x</code>

Click the x-intercept to the right of the origin: (12, 0). The other intercept, (0, 0), is the nozzle itself. Factoring by hand is faster.

</details>

---

### 30. adv-insect-colony-doubling-time

*Medium · Student-produced response · route: desmos-primary · techniques: T1*

The function $W(t) = 900(2)^{t/5}$ models the number of insects in a colony $t$ days after the colony is first observed. According to the model, how many days after the colony is first observed does the number of insects reach $7,200$?

**Answer:** 15

<details><summary>Solutions</summary>

**By hand.** Setting W(t) = 7,200 yields 900(2)^{t/5} = 7,200, so 2^{t/5} = 8 = 2^3. Equating exponents yields t/5 = 3, so t = 15. Therefore, the model predicts 7,200 insects after 15 days. Reading the exponent as 5t instead of t/5 gives 3/5 of a day, which is wrong.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=900\cdot2^{x/5}</code><br><code>y=7200</code>

Click the intersection: (15, 7200). Zoom out if it is off-screen; the y-value is large. The x-coordinate 15 is the number of days.

</details>

---

### 31. adv-medication-half-life-model

*Medium · Multiple choice · route: either · techniques: T9, T13*

A patient takes a 500-milligram dose of a medication. The amount of the medication in the patient's bloodstream decreases by half every 6 hours. Which function gives the amount $M(h)$, in milligrams, of the medication in the bloodstream $h$ hours after the dose is taken?

- **A.** $M(h) = 250(0.5)^{h/6}$
- **B.** $M(h) = 500(0.5)^{h}$
- **C.** $M(h) = 500(0.5)^{6h}$
- **D.** $M(h) = 500(0.5)^{h/6}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The initial amount is 500 milligrams. The amount is halved once every 6 hours, so after h hours it has been halved h/6 times, and M(h) = 500(0.5)^{h/6}. Checking: M(6) = 250 and M(12) = 125. Distractors: 500(0.5)^h halves the amount every hour instead of every 6 hours; 500(0.5)^(6h) halves it 6 times each hour (the exponent is inverted); 250(0.5)^(h/6) uses the amount after one half-life as the initial value.

**Desmos** (not yet verified in Desmos). Type:<br><code>M(h)=500(0.5)^{h/6}</code><br><code>M(0)</code><br><code>M(6)</code><br><code>M(12)</code>

The evaluation lines show 500, 250 and 125: the full dose at h = 0 and a halving every 6 hours, as the stem describes. The other choices (T13) fail this test: 500(0.5)^h gives 250 after 1 hour, 500(0.5)^{6h} gives 7.8125 after 1 hour, and 250(0.5)^{h/6} starts at 250.

</details>

---

### 32. adv-nf-caffeine-half-life-interpret

*Medium · Multiple choice · route: hand-primary · techniques: —*

The function $C(t) = 200(\frac{1}{2})^{t/5}$ models the amount, in milligrams, of caffeine in a person's body $t$ hours after the person drinks a certain beverage. Which statement is the best interpretation of 5 in this context?

- **A.** The amount of caffeine decreases by 5 milligrams each hour.
- **B.** The amount of caffeine decreases by 5% each hour.
- **C.** The amount of caffeine decreases by half every 5 hours.
- **D.** The amount of caffeine decreases by one-fifth each hour.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** When t increases by 5, the exponent t/5 increases by 1, so C(t) is multiplied by 1/2. For example, C(0) = 200 and C(5) = 100. Therefore, 5 is the number of hours it takes for the amount of caffeine to decrease by half: the amount of caffeine decreases by half every 5 hours. Distractors: decreases by 5 milligrams each hour reads 5 as a constant drop, but C(0) - C(1) is about 25.9 milligrams; decreases by 5% each hour reads 5 as a percent rate, but the hourly factor is (1/2)^(1/5), about 0.87, a decrease of about 13%; decreases by one-fifth each hour reads the division by 5 in the exponent as a factor of 4/5 per hour.

</details>

---

### 33. adv-nf-canoe-average-cost-long-run

*Medium · Multiple choice · route: hand-primary · techniques: —*

A workshop spends 18,000.00 dollars on tools and 400.00 dollars on materials for each canoe it builds. The average cost, in dollars per canoe, of building $x$ canoes is $C(x) = \frac{18,000 + 400x}{x}$. Which statement best describes $C(x)$ as $x$ increases without bound?

- **A.** The average cost gets closer to 0.00 dollars per canoe.
- **B.** The average cost gets closer to 400.00 dollars per canoe.
- **C.** The average cost gets closer to 18,000.00 dollars per canoe.
- **D.** The average cost gets closer to 18,400.00 dollars per canoe.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Dividing each term of the numerator by x yields C(x) = 18,000/x + 400. As x increases without bound, 18,000/x gets closer to 0, so C(x) gets closer to 400. For example, C(1,000) = 418 and C(100,000) = 400.18. Therefore, the average cost gets closer to 400.00 dollars per canoe: the tool cost is spread over more and more canoes, and only the materials cost remains. Distractors: closer to 0.00 dollars assumes the whole average shrinks because x is in the denominator; closer to 18,000.00 dollars is the one-time cost of the tools; closer to 18,400.00 dollars is C(1), the cost of building only one canoe. Desmos can confirm by graphing y=(18000+400x)/x and zooming out, but splitting the fraction is faster.

</details>

---

### 34. adv-nf-compare-maxima-vertex-standard

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

Consider the quadratic functions $f(x) = -(x - 3)^2 + 10$ and $g(x) = -2x^2 + 8x + 3$. Which function has the greater maximum value, and by how much?

- **A.** The maximum value of $f$ is greater, by 1.
- **B.** The maximum value of $f$ is greater, by 7.
- **C.** The maximum value of $g$ is greater, by 1.
- **D.** The maximum value of $g$ is greater, by 9.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The function f is in vertex form, so its maximum value is 10, at x = 3. For g, the vertex occurs at x = -8/(2(-2)) = 2, and g(2) = -8 + 16 + 3 = 11, so the maximum value of g is 11. Therefore, the maximum value of g is greater, by 11 - 10 = 1. Distractors: the maximum value of f is greater, by 1, evaluates g at x = 3, the x-coordinate of the vertex of f, and gets 9; the maximum value of f is greater, by 7, takes the constant term 3 as the maximum value of g; the maximum value of g is greater, by 9, computes the maximum of g as 3 + 8^2/4 = 19, leaving out the leading coefficient -2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-(x-3)^2+10</code><br><code>y=-2x^2+8x+3</code>

Click the top of each parabola: (3, 10) and (2, 11). The maximum values are the y-coordinates, 10 and 11, so g is greater by 1.

</details>

---

### 35. adv-nf-cubic-negative-between-zeros

*Medium · Multiple choice · route: either · techniques: T9*

For the function $f(x) = (x + 2)(x - 1)(x - 4)$, it is true that $f(a) < 0$. What is one possible value of $a$?

- **A.** $-1$
- **B.** $2$
- **C.** $4$
- **D.** $5$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The zeros of f are -2, 1 and 4, and f(x) has the sign of the product of its factors. For 1 < x < 4, the factor x + 2 is positive, x - 1 is positive and x - 4 is negative, so f(x) < 0. Checking, f(2) = (4)(1)(-2) = -8. Therefore, 2 is a possible value of a. Distractors: -1 lies between -2 and 1, where two factors are negative and f(-1) = 10 is positive; 4 is a zero, where f(4) = 0 is not less than 0; 5 lies to the right of every zero, where all three factors are positive and f(5) = 28.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=(x+2)(x-1)(x-4)</code><br><code>f(-1)</code><br><code>f(2)</code><br><code>f(4)</code><br><code>f(5)</code>

The evaluation lines show 10, -8, 0 and 28. Only f(2) is negative.

</details>

---

### 36. adv-nf-cubic-plus-constant-end-behavior

*Medium · Multiple choice · route: either · techniques: T1*

Let $f(x) = 4 + x^2(5 - x)$. Which statement correctly describes $f(x)$ as $x$ decreases without bound and as $x$ increases without bound?

- **A.** As $x$ decreases without bound, $f(x)$ increases without bound, and as $x$ increases without bound, $f(x)$ increases without bound.
- **B.** As $x$ decreases without bound, $f(x)$ increases without bound, and as $x$ increases without bound, $f(x)$ decreases without bound.
- **C.** As $x$ decreases without bound, $f(x)$ decreases without bound, and as $x$ increases without bound, $f(x)$ increases without bound.
- **D.** As $x$ decreases without bound, $f(x)$ decreases without bound, and as $x$ increases without bound, $f(x)$ decreases without bound.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Expanding yields f(x) = -x^3 + 5x^2 + 4. The leading term is -x^3: odd degree with a negative coefficient. As x decreases without bound, x^3 decreases without bound, so -x^3 increases without bound; as x increases without bound, -x^3 decreases without bound. Therefore, f(x) increases without bound on the left and decreases without bound on the right. Distractors: decreases without bound, and ... increases without bound is the end behavior of a cubic with a positive leading coefficient, which drops the minus sign in -x; increases without bound on both ends treats 5x^2 as the leading term; decreases without bound on both ends treats f as an even-degree polynomial with a negative leading coefficient.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=4+x^2(5-x)</code>

Zoom out until the graph runs off the screen at both ends. On the left it rises off the top; on the right it falls off the bottom.

</details>

---

### 37. adv-nf-equal-remainders-coefficient

*Medium · Student-produced response · route: hand-primary · techniques: T4*

For the quadratic function $q(x) = 3x^2 + bx - 7$, where $b$ is a constant, the remainder when $q(x)$ is divided by $x - 2$ equals the remainder when $q(x)$ is divided by $x + 1$. What is the value of $b$?

**Answer:** -3

<details><summary>Solutions</summary>

**By hand.** By the remainder theorem, the remainder when q(x) is divided by x - 2 is q(2), and the remainder when q(x) is divided by x + 1, that is, by x - (-1), is q(-1). Substituting yields q(2) = 12 + 2b - 7 = 5 + 2b and q(-1) = 3 - b - 7 = -4 - b. Setting 5 + 2b = -4 - b yields 3b = -9, so b = -3. Therefore, the value of b is -3. Alternate approach: q(2) = q(-1) means the parabola is symmetric about x = (2 + (-1))/2 = 1/2, so -b/(2(3)) = 1/2 and b = -3.

**Desmos** (not yet verified in Desmos). Type:<br><code>q(x)=3x^2+bx-7</code><br><code>q(2)</code><br><code>q(-1)</code>

By hand this is one linear equation, so Desmos is slower. As a check, add a slider for b (extend its range to negative values) and drag it until the lines q(2) and q(-1) show the same value; that happens at b = -3, where both show -1.

</details>

---

### 38. adv-nf-exponential-form-displays-y-intercept

*Medium · Multiple choice · route: either · techniques: T9, T13*

The function $f$ is defined by $f(x) = 3(4)^{x + 1}$. Which of the following equivalent forms of $f(x)$ displays, as a coefficient, the $y$-coordinate of the point where the graph of $y = f(x)$ crosses the $y$-axis in the $xy$-plane?

- **A.** $f(x) = 12(4)^x$
- **B.** $f(x) = 48(4)^{x - 1}$
- **C.** $f(x) = 0.75(4)^{x + 2}$
- **D.** $f(x) = 3(16)^{0.5x + 0.5}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The y-intercept of the graph of y = f(x) is (0, f(0)), and f(0) = 3(4)^(0 + 1) = 12. A function written as a(b)^x has f(0) = a(b)^0 = a, so the form 12(4)^x displays 12 as its coefficient. Using 4^(x + 1) = 4(4)^x confirms that 3(4)^(x + 1) = 12(4)^x. Therefore, the correct form is f(x) = 12(4)^x. Distractors: 48(4)^(x - 1) displays f(1) = 48, the value at x = 1; 0.75(4)^(x + 2) displays f(-2) = 0.75; 3(16)^(0.5x + 0.5) keeps the original coefficient 3, which is f(-1), not f(0).

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=3(4)^{x+1}</code><br><code>f(0)</code><br><code>y=12(4)^x</code><br><code>y=48(4)^{x-1}</code><br><code>y=0.75(4)^{x+2}</code><br><code>y=3(16)^{0.5x+0.5}</code>

f(0) shows 12, so the y-intercept is (0, 12). All four choice graphs lie on top of y = f(x), so graphing only confirms that the forms are equivalent; the answer is the form whose coefficient is 12.

</details>

---

### 39. adv-nf-exponential-from-three-values

*Medium · Multiple choice · route: desmos-primary · techniques: T5, T13*

For the exponential function $f$, $f(1) = 6$, $f(2) = 18$, and $f(4) = 162$. Which equation defines $f$?

- **A.** $f(x) = 2(3)^x$
- **B.** $f(x) = 2(9)^x$
- **C.** $f(x) = 3(2)^x$
- **D.** $f(x) = 6(3)^x$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** For an exponential function f(x) = a(b)^x, the ratio of two outputs whose inputs differ by 1 is b. Since f(2)/f(1) = 18/6 = 3, b = 3 (check: f(4)/f(2) = 162/18 = 9 = 3^2). Then f(1) = a(3) = 6, so a = 2. Therefore, f(x) = 2(3)^x. Distractors: 2(9)^x takes 162/18 = 9 as the base without noticing that x increases by 2 from f(2) to f(4); 3(2)^x swaps the base and the coefficient; 6(3)^x uses f(1) = 6 as the coefficient, but the coefficient is the value at x = 0.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,4]</code><br><code>y_1=[6,18,162]</code><br><code>y_1\sim ab^{x_1}</code>

The regression gives a = 2 and b = 3, so f(x) = 2(3)^x. To double-check, graph each choice and keep the one that passes through all three plotted points.

</details>

---

### 40. adv-nf-exponential-input-for-output

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

The function $g$ is defined by $g(x) = 5(3)^{x - 2} + 4$. For what value of $x$ is $g(x) = 139$?

- **A.** $1$
- **B.** $3$
- **C.** $5$
- **D.** $27$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Setting g(x) = 139 yields 5(3)^(x - 2) + 4 = 139. Subtracting 4 from both sides yields 5(3)^(x - 2) = 135, and dividing both sides by 5 yields 3^(x - 2) = 27 = 3^3. So x - 2 = 3, and x = 5. Therefore, g(x) = 139 when x = 5. Distractors: 1 solves x + 2 = 3, a sign slip in the exponent; 3 is the value of x - 2, an intermediate result; 27 is the value of 3^(x - 2), not of x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5(3)^{x-2}+4</code><br><code>y=139</code>

Zoom out until y = 139 is on screen, then click the intersection: (5, 139). The answer is the x-coordinate, 5.

</details>

---

### 41. adv-nf-hive-half-year-factor

*Medium · Student-produced response · route: hand-primary · techniques: T1*

The function $B(t) = 2,000(1.21)^t$ models the number of bees in a hive $t$ years after the hive was established. The function can be rewritten as $B(t) = 2,000b^{2t}$, where $b$ is a positive constant. What is the value of $b$?

**Answer:** 11/10 (≈ 1.1)

<details><summary>Solutions</summary>

**By hand.** Since b^(2t) = (b^2)^t, the two forms are equal for all t exactly when b^2 = 1.21. Because b is positive, b = √1.21 = 1.1. In context, 1.1 is the growth factor for each half year: the number of bees increases by 10% every 6 months. Therefore, the value of b is 1.1.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2</code><br><code>y=1.21</code>

Desmos is slower than the rewrite. To check, click the intersection with positive x: (1.1, 1.21). Enter 1.1 or 11/10.

</details>

---

### 42. adv-nf-island-rabbits-initial

*Medium · Student-produced response · route: desmos-primary · techniques: T5*

The number of rabbits on an island increased by the same percent each year after rabbits were introduced. There were 900 rabbits 2 years after the introduction and 1,296 rabbits 4 years after the introduction. How many rabbits were introduced to the island?

**Answer:** 625

<details><summary>Solutions</summary>

**By hand.** A quantity that increases by the same percent each year is modeled by N(t) = a(b)^t, where a is the value at t = 0. Dividing the two given values yields b^4/b^2 = 1,296/900 = 1.44, so b^2 = 1.44 and b = 1.2 (b is positive). Then a(1.2)^2 = 900, so a = 900/1.44 = 625. Therefore, 625 rabbits were introduced to the island.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[2,4]</code><br><code>y_1=[900,1296]</code><br><code>y_1\sim ab^{x_1}</code>

The regression gives a = 625 and b = 1.2. The value a is the number of rabbits at x = 0, the number introduced. Enter 625.

</details>

---

### 43. adv-nf-laptop-half-life-period

*Medium · Multiple choice · route: hand-primary · techniques: T13*

The function $V(t) = 640(\frac{1}{2})^{t/h}$ models the value, in dollars, of a certain laptop $t$ years after it is purchased, where $h$ is a positive constant. The model gives a value of 80 dollars 6 years after purchase. What is the value of $h$?

- **A.** $0.75$
- **B.** $2$
- **C.** $3$
- **D.** $8$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** It's given that V(6) = 80, so 640(1/2)^(6/h) = 80. Dividing both sides by 640 yields (1/2)^(6/h) = 1/8 = (1/2)^3, so 6/h = 3 and h = 2. The value halves every 2 years: 640, 320, 160, 80 over 6 years. Therefore, the value of h is 2. Distractors: 0.75 is 6/8, which divides the time by the ratio 640/80 = 8 instead of by the number of halvings; 3 is the number of halvings, not the length of each one; 8 is the ratio 640/80.

**Desmos** (not yet verified in Desmos). Type:<br><code>640(1/2)^{6/2}</code>

Counting halvings by hand is faster. As a check (T13), type 640(1/2)^{6/2} with the choice 2 in place of h; it shows 80. The other choices give different values.

</details>

---

### 44. adv-nf-linear-exponential-increase-gap

*Medium · Multiple choice · route: either · techniques: T9*

Let $f(x) = 12x + 5$ and $g(x) = 5(2)^x$. From $x = 0$ to $x = 5$, how much greater is the increase in $g(x)$ than the increase in $f(x)$?

- **A.** $160$
- **B.** $155$
- **C.** $95$
- **D.** $60$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Both functions equal 5 at x = 0. At x = 5, f(5) = 12(5) + 5 = 65 and g(5) = 5(2)^5 = 160. The increase in f(x) is 65 - 5 = 60, and the increase in g(x) is 160 - 5 = 155. Therefore, the increase in g(x) is 155 - 60 = 95 greater. Distractors: 160 is g(5), a value rather than an increase; 155 is the increase in g(x) alone; 60 is the increase in f(x) alone.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=12x+5</code><br><code>g(x)=5(2)^x</code><br><code>(g(5)-g(0))-(f(5)-f(0))</code>

The third line shows 95.

</details>

---

### 45. adv-nf-museum-visitors-point

*Medium · Multiple choice · route: hand-primary · techniques: —*

The function $V(d) = -3d^2 + 90d$ models the number of visitors to a museum exhibit on the day that is $d$ days after the exhibit opens. The point $(10, 600)$ lies on the graph of $y = V(d)$ in the $xy$-plane. Which statement is the best interpretation of this point?

- **A.** On the 10th day after the exhibit opens, the exhibit has 600 visitors.
- **B.** On the 600th day after the exhibit opens, the exhibit has 10 visitors.
- **C.** The greatest number of visitors the exhibit has on any day is 600.
- **D.** Over the first 10 days after the exhibit opens, the exhibit has a total of 600 visitors.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A point (a, b) on the graph of y = V(d) means V(a) = b: on day a after the exhibit opens, the model gives b visitors. Checking, V(10) = -3(10)^2 + 90(10) = -300 + 900 = 600. Therefore, the point (10, 600) means that on the 10th day after the exhibit opens, the exhibit has 600 visitors. Distractors: the 600th day with 10 visitors swaps the input and the output; the greatest number of visitors is not 600, because V is greatest at d = 90/6 = 15, where V(15) = 675; a total of 600 visitors over the first 10 days treats V(d) as a running total, but V gives the number of visitors on a single day.

</details>

---

### 46. adv-nf-podcast-linear-vs-percent

*Medium · Student-produced response · route: desmos-primary · techniques: T9*

Podcasts A and B each have 2,000 listeners now. Podcast A gains 300 listeners each month, and the number of listeners of podcast B increases by 10% each month. To the nearest whole number, how many more listeners does podcast B have than podcast A 12 months from now?

**Answer:** 677

<details><summary>Solutions</summary>

**By hand.** Podcast A grows by the same amount each month, so A(m) = 2,000 + 300m, and A(12) = 2,000 + 3,600 = 5,600. Podcast B grows by the same percent each month, so B(m) = 2,000(1.1)^m, and B(12) = 2,000(1.1)^12. By repeated squaring, (1.1)^2 = 1.21, (1.1)^4 = 1.4641 and (1.1)^8 = 2.14358881, so (1.1)^12 = 2.14358881 × 1.4641 ≈ 3.138428, and B(12) ≈ 6,276.86. The difference is about 6,276.86 - 5,600 = 676.86. Therefore, to the nearest whole number, podcast B has 677 more listeners than podcast A.

**Desmos** (not yet verified in Desmos). Type:<br><code>A(x)=2000+300x</code><br><code>B(x)=2000(1.1)^x</code><br><code>B(12)-A(12)</code>

The third line shows about 676.857. Round to the nearest whole number and enter 677.

</details>

---

### 47. adv-nf-poster-average-cost

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

Printing posters has a setup fee of 1,440.00 dollars plus 12.00 dollars per poster. The average cost, in dollars per poster, is $C(n) = \frac{1,440 + 12n}{n}$, where $n$ is the number of posters printed. For how many posters is the average cost 20.00 dollars per poster?

- **A.** $72$
- **B.** $84$
- **C.** $120$
- **D.** $180$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Setting C(n) = 20 yields (1,440 + 12n)/n = 20. Multiplying both sides by n yields 1,440 + 12n = 20n, so 1,440 = 8n and n = 180. Therefore, the average cost is 20.00 dollars per poster for 180 posters. Distractors: 72 is 1,440/20, which ignores the 12.00 dollars per poster; 84 is C(20), which evaluates the function at 20 instead of solving C(n) = 20; 120 is 1,440/12, which divides the fee by the cost per poster.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{1440+12x}{x}</code><br><code>y=20</code>

Zoom out, since the intersection is far to the right of the default window. Click it: (180, 20). The number of posters is the x-coordinate, 180.

</details>

---

### 48. adv-nf-quadratic-c-single-intercept

*Medium · Multiple choice · route: either · techniques: T4*

In the $xy$-plane, the graph of $y = 2x^2 + 12x + c$ intersects the $x$-axis at exactly one point, where $c$ is a constant. What is the value of $c$?

- **A.** $9$
- **B.** $18$
- **C.** $36$
- **D.** $72$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The graph intersects the x-axis at exactly one point when the equation 2x^2 + 12x + c = 0 has exactly one real solution, that is, when its discriminant is 0. The discriminant is 12^2 - 4(2)(c) = 144 - 8c. Setting 144 - 8c = 0 yields c = 18. Alternate approach: 2x^2 + 12x + c = 2(x + 3)^2 + c - 18, so the vertex is (-3, c - 18), which lies on the x-axis when c = 18. Distractors: 9 completes the square for x^2 + 6x and forgets to multiply by 2; 36 is 12^2/4, which ignores the leading coefficient 2; 72 drops the 4 from 4ac and solves 144 - 2c = 0.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x^2+12x+c</code>

Add a slider for c, set its range to 0 to 80 with step 1, and drag until the vertex sits on the x-axis: c = 18, vertex (-3, 0).

</details>

---

### 49. adv-nf-quadratic-positive-input

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

If $f(x) = 2x^2 - 8x - 1$, for what positive value of $x$ is $f(x) = 9$?

- **A.** $1$
- **B.** $2$
- **C.** $4$
- **D.** $5$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Setting f(x) = 9 yields 2x^2 - 8x - 1 = 9, or 2x^2 - 8x - 10 = 0. Dividing both sides by 2 yields x^2 - 4x - 5 = 0, which factors as (x - 5)(x + 1) = 0. So x = 5 or x = -1, and the positive value is 5. Distractors: 1 comes from factoring as (x + 5)(x - 1), a sign error, and keeping the positive root; 2 is the x-coordinate of the vertex, -(-8)/(2(2)), a feature of the graph but not a solution; 4 solves 2x^2 - 8x = 0, dropping the constant terms.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x^2-8x-1</code><br><code>y=9</code>

There are two intersections: (-1, 9) and (5, 9). The question asks for the positive value, 5.

</details>

---

### 50. adv-nf-radical-graph-endpoint

*Medium · Multiple choice · route: either · techniques: T13*

The function $g$ is defined by $g(x) = \sqrt{12 - 3x} + 2$. Which point is the endpoint of the graph of $y = g(x)$ in the $xy$-plane?

- **A.** $(-4, 2)$
- **B.** $(4, 0)$
- **C.** $(4, 2)$
- **D.** $(12, 2)$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** g(x) is defined only when 12 - 3x ≥ 0, that is, when x ≤ 4, so the graph ends at x = 4. Substituting 4 for x yields g(4) = √0 + 2 = 2. Therefore, the endpoint is (4, 2). Distractors: (-4, 2) is a sign error in solving 12 - 3x = 0; (4, 0) drops the + 2 and treats the endpoint as an x-intercept; (12, 2) solves 12 - x = 0, dropping the coefficient 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{12-3x}+2</code>

The graph runs to the left from a single endpoint; click it: (4, 2). Compare with the choices (T13); the graph does not reach x = 12 or x = -4 as an endpoint, and it never touches the x-axis.

</details>

---

### 51. adv-nf-radical-input-for-output

*Medium · Student-produced response · route: either · techniques: T1*

If $f(x) = 2\sqrt{x + 5} - 1$ and $f(a) = 11$, what is the value of $a$?

**Answer:** 31

<details><summary>Solutions</summary>

**By hand.** It's given that f(a) = 11, so 2√(a + 5) - 1 = 11. Adding 1 to both sides yields 2√(a + 5) = 12, and dividing both sides by 2 yields √(a + 5) = 6. Squaring both sides yields a + 5 = 36, so a = 31. Checking, f(31) = 2√36 - 1 = 11, so 31 is not an extraneous solution. Therefore, the value of a is 31.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2\sqrt{x+5}-1</code><br><code>y=11</code>

Click the intersection: (31, 11). Enter the x-coordinate, 31. Zoom out if the intersection is off screen.

</details>

---

### 52. adv-nf-rational-constant-from-value

*Medium · Multiple choice · route: either · techniques: T4, T9*

The function $f$ is defined by $f(x) = \frac{x + k}{x - 3}$, where $k$ is a constant. If $f(5) = 4$, what is the value of $f(1)$?

- **A.** $-2$
- **B.** $1$
- **C.** $2$
- **D.** $4$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that f(5) = 4, so (5 + k)/(5 - 3) = 4, or (5 + k)/2 = 4. Multiplying both sides by 2 yields 5 + k = 8, so k = 3. Then f(1) = (1 + 3)/(1 - 3) = 4/(-2) = -2. Therefore, the value of f(1) is -2. Distractors: 1 comes from dividing instead of multiplying, 5 + k = 4/2, which gives k = -3 and f(1) = (-2)/(-2) = 1; 2 computes the denominator as 3 - 1 instead of 1 - 3; 4 repeats the given value f(5).

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=\frac{x+k}{x-3}</code><br><code>f(5)</code><br><code>f(1)</code>

Add a slider for k and drag it until the line f(5) shows 4; that happens at k = 3. The line f(1) then shows -2.

</details>

---

### 53. adv-nf-rational-input-for-output-five

*Medium · Student-produced response · route: desmos-primary · techniques: T1*

The function $f$ is defined by $f(x) = \frac{3x + 1}{x - 2}$. For what value of $x$ is $f(x) = 5$?

**Answer:** 11/2 (≈ 5.5)

<details><summary>Solutions</summary>

**By hand.** Setting f(x) = 5 yields (3x + 1)/(x - 2) = 5. Multiplying both sides by x - 2 yields 3x + 1 = 5x - 10. Subtracting 3x and adding 10 to both sides yields 11 = 2x, so x = 11/2. Since x - 2 is not 0 at x = 11/2, the solution is valid. Therefore, f(x) = 5 when x = 11/2, or 5.5.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{3x+1}{x-2}</code><br><code>y=5</code>

Click the intersection: (5.5, 5). The answer is the x-coordinate; enter 5.5 or 11/2.

</details>

---

### 54. adv-nf-rational-shift-x-intercept

*Medium · Multiple choice · route: desmos-primary · techniques: T9, T1*

Let $f(x) = \frac{1}{x}$ and $g(x) = f(x + 3) - 2$. At what value of $x$ does the graph of $y = g(x)$ cross the $x$-axis in the $xy$-plane?

- **A.** $-\frac{7}{2}$
- **B.** $-\frac{5}{2}$
- **C.** $-\frac{5}{3}$
- **D.** $\frac{7}{2}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting x + 3 for x in f yields g(x) = 1/(x + 3) - 2. The x-intercept is where g(x) = 0, so 1/(x + 3) = 2, which yields x + 3 = 1/2 and x = -5/2. Therefore, the graph of y = g(x) crosses the x-axis at x = -5/2. Distractors: 7/2 shifts in the wrong direction, solving 1/(x - 3) = 2; -7/2 adds 2 instead of subtracting it, solving 1/(x + 3) = -2; -5/3 is g(0) = 1/3 - 2, the y-coordinate of the y-intercept, not the x-intercept.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=\frac{1}{x}</code><br><code>g(x)=f(x+3)-2</code><br><code>y=g(x)</code>

Click the x-intercept of y = g(x): (-2.5, 0). The answer is -5/2.

</details>

---

### 55. adv-nf-repeated-factor-touch-point

*Medium · Multiple choice · route: either · techniques: T1*

The function $f$ is defined by $f(x) = -2x(x - 5)^2(x + 4)$. The graph of $y = f(x)$ in the $xy$-plane touches the $x$-axis without crossing it at exactly one point. What is the $x$-coordinate of that point?

- **A.** $-5$
- **B.** $-4$
- **C.** $0$
- **D.** $5$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The zeros of f are the values that make a factor 0: x = 0, x = 5 and x = -4. A factor raised to an even power does not change sign, so the graph touches the x-axis without crossing it there; a factor to the first power changes sign, so the graph crosses. The factor (x - 5) is squared, so the graph touches the x-axis at x = 5. Therefore, the value is 5. Distractors: -5 reads the zero of (x - 5) with the wrong sign; -4 and 0 come from factors to the first power, where the graph crosses the x-axis.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-2x(x-5)^2(x+4)</code>

Zoom out until all three x-intercepts show. The graph crosses the x-axis at x = -4 and x = 0 and only touches it at x = 5, where it turns back down.

</details>

---

### 56. adv-nf-same-leading-coefficient-equal-input

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

If $f(x) = 2(x - 3)^2 + 1$ and $g(x) = 2(x + 1)^2 - 7$, at what value of $x$ does $f(x)$ equal $g(x)$?

- **A.** $-1$
- **B.** $1$
- **C.** $\frac{3}{2}$
- **D.** $3$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Expanding yields f(x) = 2x^2 - 12x + 19 and g(x) = 2x^2 + 4x - 5. Setting f(x) = g(x), the 2x^2 terms cancel, leaving -12x + 19 = 4x - 5, so 24 = 16x and x = 3/2. Because the leading coefficients are equal, the two parabolas have the same shape and cross exactly once. Distractors: 3 is the x-coordinate of the vertex of the graph of f; -1 is the x-coordinate of the vertex of the graph of g; 1 is the average of those two x-coordinates, which would be correct only if the two vertices had the same y-coordinate.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2(x-3)^2+1</code><br><code>y=2(x+1)^2-7</code>

Click the one intersection: (1.5, 5.5). The answer is the x-coordinate, 1.5, which is 3/2.

</details>

---

### 57. adv-nf-shift-right-new-x-intercept

*Medium · Multiple choice · route: desmos-primary · techniques: T9*

Let $f(x) = (x + 1)(x - 5)$. The function $g$ is defined so that its graph is the graph of $y = f(x)$ translated to the right by 2 units in the $xy$-plane. Which point is an $x$-intercept of the graph of $y = g(x)$?

- **A.** $(-3, 0)$
- **B.** $(-1, 0)$
- **C.** $(3, 0)$
- **D.** $(7, 0)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The x-intercepts of the graph of y = f(x) are (-1, 0) and (5, 0). Translating the graph 2 units to the right adds 2 to every x-coordinate, so the x-intercepts of the graph of y = g(x) are (1, 0) and (7, 0). Algebraically, g(x) = f(x - 2) = (x - 1)(x - 7). Therefore, (7, 0) is an x-intercept. Distractors: (-3, 0) moves the intercept (-1, 0) 2 units left instead of right; (-1, 0) is an x-intercept of the original graph, before the translation; (3, 0) moves the intercept (5, 0) 2 units left instead of right.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=(x+1)(x-5)</code><br><code>y=f(x-2)</code>

A shift to the right by 2 replaces x with x - 2. Click the x-intercepts of y = f(x - 2): (1, 0) and (7, 0). Only (7, 0) is a choice.

</details>

---

### 58. adv-nf-sqrt-reflect-translate-equation

*Medium · Multiple choice · route: either · techniques: T13*

The graph of $y = h(x)$ in the $xy$-plane is the result of reflecting the graph of $y = \sqrt{x}$ across the $x$-axis and then translating it 4 units up. Which equation defines $h$?

- **A.** $h(x) = -\sqrt{x} + 4$
- **B.** $h(x) = -\sqrt{x} - 4$
- **C.** $h(x) = -\sqrt{x + 4}$
- **D.** $h(x) = \sqrt{-x} + 4$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Reflecting the graph of y = √x across the x-axis multiplies every output by -1, giving y = -√x. Translating that graph 4 units up adds 4 to every output, giving y = -√x + 4. Therefore, h(x) = -√x + 4. Distractors: h(x) = -√x - 4 translates the graph down instead of up; h(x) = -√(x + 4) adds 4 to the input, which shifts the graph 4 units left instead of up; h(x) = √(-x) + 4 reflects across the y-axis instead of the x-axis.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{x}</code><br><code>y=-\sqrt{x}+4</code>

Type y = √x and each choice (T13). The correct graph starts at (0, 4), runs to the right and falls; it is the graph of y = √x flipped upside down and raised 4 units.

</details>

---

### 59. adv-nf-square-side-two-more-expression

*Medium · Multiple choice · route: hand-primary · techniques: —*

For $x > 0$, the function $A$ gives the area of a square whose side length is 2 more than $x$. Which expression is equal to $A(x)$?

- **A.** $x^2 + 2$
- **B.** $x^2 + 4$
- **C.** $4x + 8$
- **D.** $x^2 + 4x + 4$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The side length of the square is x + 2, and the area of a square is the square of its side length, so A(x) = (x + 2)^2 = x^2 + 4x + 4. Distractors: x^2 + 2 squares x and then adds 2; x^2 + 4 squares each term separately and drops the middle term 4x; 4x + 8 is 4(x + 2), the perimeter of the square rather than its area. As a check, a square with x = 1 has side 3 and area 9, and only x^2 + 4x + 4 gives 9.

</details>

---

### 60. adv-nf-syrup-fraction-long-run

*Medium · Multiple choice · route: desmos-primary · techniques: T9*

A pitcher holds 100 milliliters of a drink, 20 milliliters of which is syrup. After $x$ milliliters of syrup are added, the fraction of the drink that is syrup is $P(x) = \frac{20 + x}{100 + x}$. As $x$ increases without bound, what value does $P(x)$ approach?

- **A.** $0$
- **B.** $0.2$
- **C.** $1$
- **D.** $20$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** When x is very large, the 20 and the 100 are small compared with x, so the numerator and the denominator are both close to x and their quotient is close to 1. For example, P(900) = 920/1,000 = 0.92 and P(9,900) = 9,920/10,000 = 0.992. Therefore, P(x) approaches 1: the drink becomes almost entirely syrup. Distractors: 0 applies the pattern of 1/x, whose values shrink toward 0; 0.2 is P(0), the starting fraction of syrup; 20 is the starting amount of syrup, in milliliters, rather than a fraction.

**Desmos** (not yet verified in Desmos). Type:<br><code>P(x)=\frac{20+x}{100+x}</code><br><code>P(1000)</code><br><code>P(1000000)</code>

The lines show about 0.927 and 0.99992: the values climb toward 1. Graphing y=P(x) and zooming out shows the curve leveling off at y = 1.

</details>

---

### 61. adv-nf-table-shift-scale-evaluate

*Medium · Multiple choice · route: hand-primary · techniques: —*

For the function $f$, $f(-1) = 7$, $f(1) = 2$, $f(3) = -4$, and $f(5) = 9$. If $g(x) = 2f(x - 2) + 1$ for all $x$, what is the value of $g(3)$?

- **A.** $-7$
- **B.** $5$
- **C.** $6$
- **D.** $19$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Substituting 3 for x in g yields g(3) = 2f(3 - 2) + 1 = 2f(1) + 1. It's given that f(1) = 2, so g(3) = 2(2) + 1 = 5. Therefore, the value of g(3) is 5. Distractors: 19 is 2f(5) + 1, which uses f(x + 2), a shift in the wrong direction; 6 is 2(f(1) + 1), a grouping slip that adds 1 before doubling; -7 is 2f(3) + 1, which ignores the shift.

</details>

---

### 62. adv-nf-two-quadratics-difference-at-input

*Medium · Student-produced response · route: either · techniques: T9*

Two quadratic functions are given by $f(x) = (x - 4)^2 - 3$ and $g(x) = -x^2 + 6x$. What is the value of $f(-1) - g(-1)$?

**Answer:** 29

<details><summary>Solutions</summary>

**By hand.** Substituting -1 for x yields f(-1) = (-1 - 4)^2 - 3 = 25 - 3 = 22 and g(-1) = -(-1)^2 + 6(-1) = -1 - 6 = -7. Therefore, f(-1) - g(-1) = 22 - (-7) = 29. Two traps: -(-1)^2 is -1, not 1, and subtracting -7 adds 7.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=(x-4)^2-3</code><br><code>g(x)=-x^2+6x</code><br><code>f(-1)-g(-1)</code>

The third line shows 29.

</details>

---

### 63. adv-nf-wave-speed-depth

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

The function $v(x) = \sqrt{9.8x}$ models the speed $v(x)$, in meters per second, of a wave in shallow water that is $x$ meters deep. According to the model, what is the depth, in meters, of the water where the wave's speed is 7 meters per second?

- **A.** $0.7$
- **B.** $5$
- **C.** $8.3$
- **D.** $480.2$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Setting v(x) = 7 yields √(9.8x) = 7. Squaring both sides yields 9.8x = 49, so x = 49/9.8 = 5. Therefore, the depth of the water is 5 meters. Distractors: 0.7 divides 7 by 9.8 without squaring 7 first (about 0.71); 8.3 is v(7), about 8.3, which evaluates the function at 7 instead of solving v(x) = 7; 480.2 multiplies 49 by 9.8 instead of dividing.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{9.8x}</code><br><code>y=7</code>

Click the intersection: (5, 7). The depth is the x-coordinate, 5, not the speed.

</details>

---

### 64. adv-parabola-symmetry-other-intercept

*Medium · Student-produced response · route: either · techniques: T4, T1*

In the $xy$-plane, the graph of $y = f(x)$, where $f$ is a quadratic function, has its vertex at $(2, -9)$ and passes through the point $(5, 0)$. What is the $x$-coordinate of the other $x$-intercept of the graph?

**Answer:** -1

<details><summary>Solutions</summary>

**By hand.** A parabola is symmetric about the vertical line through its vertex, here x = 2. The x-intercept at x = 5 is 3 units to the right of that line, so the other x-intercept is 3 units to the left, at x = -1. Alternate approach: f(x) = a(x - 2)^2 - 9 with f(5) = 0 gives 9a = 9, so a = 1 and f(x) = (x - 2)^2 - 9 = (x - 5)(x + 1), whose zeros are 5 and -1.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=a(x-2)^2-9</code><br><code>(5,0)</code>

Add a slider for a (T4) and drag until the parabola passes through the plotted point (5, 0), at a = 1; then click the other x-intercept, (-1, 0). By hand, symmetry about x = 2 gives it immediately.

</details>

---

### 65. adv-shop-profit-max-price

*Medium · Multiple choice · route: desmos-primary · techniques: T1*

A shop sells a certain item for $x$ dollars each. The function $P(x) = -4x^2 + 96x - 200$ models the shop's weekly profit, in dollars, from sales of the item. What price, in dollars, gives the greatest weekly profit?

- **A.** $12$
- **B.** $24$
- **C.** $200$
- **D.** $376$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The profit function is a downward-opening parabola, so its maximum occurs at the vertex, x = -b/(2a) = -96/(2 · (-4)) = 12. Therefore, the price is 12 dollars. Distractors: 24 is -b/a, forgetting the factor 2 in the denominator; 376 is the maximum profit P(12) = -576 + 1152 - 200, the wrong quantity; 200 is the constant term of the model.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-4x^2+96x-200</code>

Click the vertex of the parabola: (12, 376). The question asks for the price, the x-coordinate 12; the y-coordinate 376 is the profit at that price.

</details>

---

### 66. adv-vertex-form-displays-minimum

*Medium · Multiple choice · route: desmos-primary · techniques: T13, T1*

The function $f$ is defined by $f(x) = x^2 + 8x + 3$. Which of the following equivalent forms of $f(x)$ displays the minimum value of $f$?

- **A.** $f(x) = (x + 1)(x + 7) - 4$
- **B.** $f(x) = (x + 4)^2 - 13$
- **C.** $f(x) = (x + 4)^2 + 3$
- **D.** $f(x) = (x - 4)^2 - 13$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Complete the square: x^2 + 8x + 3 = (x^2 + 8x + 16) - 16 + 3 = (x + 4)^2 - 13. Since (x + 4)^2 ≥ 0, the minimum value of f is -13, and this form displays it as its constant term. Distractors: (x + 4)^2 + 3 adds 16 inside the square without subtracting it, so it is not equivalent (it equals 19 at x = 0, but f(0) = 3); (x - 4)^2 - 13 shows the right minimum but has its vertex at x = 4, so it is not equivalent either; (x + 1)(x + 7) - 4 is equivalent but displays neither the minimum nor the zeros.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+8x+3</code><br><code>y=(x+4)^2-13</code>

Click the vertex of y = x^2 + 8x + 3: (-4, -13), so the minimum value is -13. Two choices show -13; graph each (T13), and only (x + 4)^2 - 13 lies on the original.

</details>

---

### 67. adv-video-views-exponential-model

*Medium · Multiple choice · route: desmos-primary · techniques: T5, T13*

A video had 20 views after 1 day, 60 views after 2 days, 180 views after 3 days, and 540 views after 4 days. Which function best models the number of views $V(d)$ the video has after $d$ days?

- **A.** $V(d) = 40d - 20$
- **B.** $V(d) = 20d^3$
- **C.** $V(d) = 20(3)^{d}$
- **D.** $V(d) = 20(3)^{d - 1}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Each day the number of views is multiplied by the same factor: 60/20 = 3, 180/60 = 3, and 540/180 = 3. A constant ratio means an exponential model with growth factor 3, and the value after 1 day is 20, so V(d) = 20(3)^(d - 1). Checking: V(4) = 20(27) = 540. Distractors: 40d - 20 is the line through the first two points, but it gives 100 after 3 days, not 180 (the differences 40, 120, 360 are not constant, so no linear model fits); 20d^3 matches at d = 1 but gives 160 after 2 days and 540 after 3 days; 20(3)^d is off by one day, giving 60 after 1 day.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4]</code><br><code>y_1=[20,60,180,540]</code><br><code>y_1\sim ab^{x_1}</code><br><code>y_1\sim mx_1+c</code>

The exponential regression (T5) returns a = 20/3 and b = 3 with every residual 0, so V(d) = (20/3)(3)^d = 20(3)^(d - 1) fits exactly. The linear regression leaves large residuals. To match the choice list (T13), graph each choice with the four points: only 20(3)^(d - 1) passes through all of them.

</details>

---

### 68. adv-algae-decay-every-two-days

*Hard · Multiple choice · route: either · techniques: T9, T13*

The area of a pond covered by algae is 80 square meters when a treatment begins, and the covered area decreases by 36% every 2 days. Which equation gives the covered area $A$, in square meters, $x$ days after the treatment begins?

- **A.** $A = 80(0.36)^{x/2}$
- **B.** $A = 80(0.64)^{2x}$
- **C.** $A = 80(0.64)^{x/2}$
- **D.** $A = 80(0.82)^{x}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A 36% decrease leaves 100% - 36% = 64% of the area, so every 2 days the area is multiplied by 0.64. In x days there are x/2 such periods, so A = 80(0.64)^(x/2). Distractors: A = 80(0.36)^(x/2) multiplies by the fraction removed rather than the fraction remaining; A = 80(0.64)^(2x) applies the factor 2x times in x days instead of x/2 times; A = 80(0.82)^x assumes the 36% splits into 18% per day, but exponential change does not divide evenly (the daily factor is 0.64^(1/2) = 0.8).

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=80(0.64)^{x/2}</code><br><code>f(0)</code><br><code>\frac{f(2)}{f(0)}</code>

Define each choice as f (T13) and check two things with T9: f(0) must be 80 and f(2)/f(0) must be 0.64, a 36% drop over 2 days. Only 80(0.64)^(x/2) passes; 80(0.82)^x gives 0.6724 and 80(0.64)^(2x) gives 0.168.

</details>

---

### 69. adv-barrel-percent-decrease

*Hard · Student-produced response · route: desmos-primary · techniques: T1, T11*

A barrel contains 250 liters of water and leaks so that the amount of water in the barrel decreases by $p\%$ each hour. After 3 hours, the barrel contains 54 liters of water. What is the value of $p$?

**Answer:** 40

<details><summary>Solutions</summary>

**By hand.** A decrease of p% each hour multiplies the amount by (1 - p/100) each hour, so after 3 hours the amount is 250(1 - p/100)^3. Setting this equal to 54 yields (1 - p/100)^3 = 54/250 = 0.216. Since 0.6^3 = 0.216, 1 - p/100 = 0.6, so p = 40. Treating the decrease as linear, 250 - 3(p/100)(250) = 54, gives about 26.1, which is wrong because the percent applies to the current amount each hour.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=250\left(1-\frac{x}{100}\right)^3</code><br><code>y=54</code>

The unknown p is typed as x. Click the intersection: (40, 54), so p = 40. The value is an exact integer; if the point shows a long decimal instead, re-check the parentheses around 1 - x/100.

</details>

---

### 70. adv-coin-value-monthly-function

*Hard · Multiple choice · route: hand-primary · techniques: T13, T9*

The value of a certain collectible coin increases by 6% each year. The coin is worth 1,200 dollars today. Which function gives the value $V(m)$, in dollars, of the coin, where $m$ is the number of months from today?

- **A.** $V(m) = 1,200(1.005)^{m}$
- **B.** $V(m) = 1,200(1.06)^{m/12}$
- **C.** $V(m) = 1,200(1.06)^{m}$
- **D.** $V(m) = 1,200(1.06)^{12m}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** An increase of 6% each year multiplies the value by 1.06 once per year. In m months, m/12 years pass, so the value has been multiplied by 1.06 a total of m/12 times, and V(m) = 1,200(1.06)^(m/12). Checking: V(12) = 1,200(1.06) = 1,272. Distractors: 1,200(1.005)^m divides the yearly 6% into 12 monthly increases of 0.5%, but twelve 0.5% increases compound to about 6.17%, not 6%; 1,200(1.06)^m applies a 6% increase every month; 1,200(1.06)^(12m) applies 12 yearly increases in every month (the exponent is inverted).

**Desmos** (not yet verified in Desmos). Type:<br><code>V(m)=1200(1.06)^{m/12}</code><br><code>V(12)</code><br><code>V(24)</code>

Define the function (T9) and evaluate at m = 12 and m = 24: 1272 and 1348.32, a 6% increase for each full year, as the stem requires. Test the other choices the same way (T13): 1200(1.005)^m gives 1274.01 at m = 12, not 1272, and the other two give far more than a 6% increase in 12 months.

</details>

---

### 71. adv-composite-from-table

*Hard · Multiple choice · route: either · techniques: T9, T7, T11*

For the functions $f$ and $g$, $f(1) = 3$, $f(2) = 1$, $f(3) = 4$, $f(4) = 2$, $g(1) = 2$, $g(2) = 4$, $g(3) = 1$, and $g(4) = 3$. The function $h$ is defined by $h(x) = \frac{2f(x) + 1}{g(x) - 1}$. What is the value of $h(4) - h(2)$?

- **A.** $\frac{3}{2}$
- **B.** $\frac{5}{2}$
- **C.** $\frac{7}{2}$
- **D.** $4$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** h(4) = (2f(4) + 1)/(g(4) - 1) = (2 · 2 + 1)/(3 - 1) = 5/2. h(2) = (2f(2) + 1)/(g(2) - 1) = (2 · 1 + 1)/(4 - 1) = 1. So h(4) - h(2) = 3/2. Distractors: 5/2 stops at h(4); 7/2 adds h(2) instead of subtracting; 4 reads f(4) = 2 in place of g(4) in the denominator (giving h(4) = 5).

**Desmos** (not yet verified in Desmos). Type:<br><code>F=[3,1,4,2]</code><br><code>G=[2,4,1,3]</code><br><code>f(x)=F[x]</code><br><code>g(x)=G[x]</code><br><code>h(x)=\frac{2f(x)+1}{g(x)-1}</code><br><code>h(4)-h(2)</code>

Store each table as a list and index it: F[x] is the xth entry, so f(4) = 2. The last line shows 1.5; the fraction toggle gives 3/2. Reading the table by hand is just as quick once you keep the rows straight.

</details>

---

### 72. adv-composition-positive-a

*Hard · Student-produced response · route: either · techniques: T1, T4*

The functions $f$ and $g$ are defined by $f(x) = 2x + a$ and $g(x) = x^2$, where $a$ is a positive constant. If $g(f(1)) = 49$, what is the value of $a$?

**Answer:** 5

<details><summary>Solutions</summary>

**By hand.** Substituting 1 for x in f yields f(1) = 2 + a. Then g(f(1)) = (2 + a)^2, so (2 + a)^2 = 49 and 2 + a = 7 or 2 + a = -7. Therefore, a = 5 or a = -9, and since a is positive, a = 5. Composing in the wrong order, f(g(1)) = 2(1) + a = 49, gives 47, which is wrong.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(2+x)^2</code><br><code>y=49</code>

The first line is g(f(1)) with the unknown a typed as x. The graphs cross at (-9, 49) and (5, 49); the stem says a is positive, so a = 5. A slider on a with g(f(1)) on its own line (T4) also works but takes longer.

</details>

---

### 73. adv-cubic-y-intercept-a

*Hard · Multiple choice · route: either · techniques: T4, T9*

The function $f$ is defined by $f(x) = (x - a)(x^2 + 4)$, where $a$ is a constant. In the $xy$-plane, the graph of $y = f(x)$ passes through the point $(0, -12)$. What is the value of $a$?

- **A.** $-12$
- **B.** $-3$
- **C.** $3$
- **D.** $12$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The graph passes through (0, -12), so f(0) = -12. Substituting 0 for x yields f(0) = (0 - a)(0 + 4) = -4a. Setting -4a = -12 yields a = 3. Distractors: -3 comes from the sign slip 4a = -12; 12 drops the factor x^2 + 4, setting -a = -12; -12 reads the y-coordinate of the given point as the value of a.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=(x-a)(x^2+4)</code><br><code>y=f(x)</code><br><code>a=3</code>

Add a slider for a and drag it until the curve passes through (0, -12); that happens at a = 3. Alternatively type (0-a)(0+4)=-12 as y=(0-x)(4) and y=-12 and click the intersection. The hand computation f(0) = -4a is quicker.

</details>

---

### 74. adv-exponential-quarterly-annual-percent

*Hard · Multiple choice · route: desmos-primary · techniques: T9*

The function $V(x) = 500(1.04)^{4x}$ models the value, in dollars, of an account $x$ years after it is opened. To the nearest percent, by what percent does the value of the account increase each year?

- **A.** $4\%$
- **B.** $16\%$
- **C.** $17\%$
- **D.** $117\%$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Each year the exponent 4x increases by 4, so the value is multiplied by (1.04)^4 = 1.16985856, about 1.17. Multiplying by 1.17 is a 17% increase. Distractors: 4% reads 1.04 as the yearly factor, ignoring the 4 in the exponent; 16% adds 4% four times, but percent changes compound rather than add; 117% reports the growth factor as the percent increase.

**Desmos** (not yet verified in Desmos). Type:<br><code>V(x)=500(1.04)^{4x}</code><br><code>\frac{V(1)}{V(0)}</code>

V(1)/V(0) shows 1.1699, so each year the value is multiplied by about 1.17, an increase of about 17%. Desmos does the fourth power; by hand, (1.04)^4 is the same computation.

</details>

---

### 75. adv-factored-form-displays-intercepts

*Hard · Multiple choice · route: desmos-primary · techniques: T13, T1*

The function $f$ is defined by $f(x) = 3(x - 2)^2 - 27$. Which of the following equivalent forms of $f(x)$ displays the $x$-intercepts of the graph of $y = f(x)$ in the $xy$-plane as constants or coefficients?

- **A.** $f(x) = 3(x - 5)(x + 1)$
- **B.** $f(x) = 3(x + 5)(x - 1)$
- **C.** $f(x) = 3(x^2 - 4x - 5)$
- **D.** $f(x) = 3x^2 - 12x - 15$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The x-intercepts are where f(x) = 0. Expanding the given form yields 3(x^2 - 4x + 4) - 27 = 3x^2 - 12x - 15 = 3(x^2 - 4x - 5) = 3(x - 5)(x + 1). The factored form shows the zeros 5 and -1 directly as the constants in the factors, so it displays the x-intercepts (5, 0) and (-1, 0). Distractors: 3(x + 5)(x - 1) is not equivalent to f(x) (it expands to 3x^2 + 12x - 15); 3x^2 - 12x - 15 is equivalent but displays the y-intercept -15, not the x-intercepts; 3(x^2 - 4x - 5) is equivalent but displays neither intercept as a constant.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3(x-2)^2-27</code><br><code>y=3(x-5)(x+1)</code>

Click the x-intercepts of the first graph: (-1, 0) and (5, 0). The factored form with factors x - 5 and x + 1 shows exactly those numbers, and its graph (second line) coincides with the first. The choice with factors x + 5 and x - 1 does not overlap at all (T13).

</details>

---

### 76. adv-factored-quadratic-y-intercept-a

*Hard · Multiple choice · route: desmos-primary · techniques: T4, T9*

The function $f$ is defined by $f(x) = a(x - 3)(x + 5)$, where $a$ is a constant. In the $xy$-plane, the $y$-intercept of the graph of $y = f(x)$ is $(0, 45)$. What is the value of $f(-1)$?

- **A.** $-48$
- **B.** $-16$
- **C.** $45$
- **D.** $48$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The y-intercept is the point where x = 0, so f(0) = a(-3)(5) = -15a = 45 and a = -3. Then f(-1) = -3(-1 - 3)(-1 + 5) = -3(-4)(4) = 48. Distractors: -48 uses a = 3 (a sign error in -15a = 45); -16 is (-4)(4), forgetting the factor a entirely; 45 repeats the y-intercept.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=a(x-3)(x+5)</code><br><code>y=f(x)</code><br><code>f(0)</code><br><code>f(-1)</code>

Add a slider for a (T4) and drag until f(0) shows 45, at a = -3; then f(-1) shows 48. Or solve f(0) = -15a = 45 by hand first and type a = -3.

</details>

---

### 77. adv-horizontal-compression-intercepts

*Hard · Multiple choice · route: desmos-primary · techniques: T9, T1*

The function $f$ is defined by $f(x) = (x - 6)(x + 2)$, and the function $g$ is defined by $g(x) = f(2x)$. What is the sum of the $x$-coordinates of the $x$-intercepts of the graph of $y = g(x)$ in the $xy$-plane?

- **A.** $-1$
- **B.** $2$
- **C.** $3$
- **D.** $4$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** g(x) = f(2x) = (2x - 6)(2x + 2). Setting g(x) = 0 yields 2x = 6 or 2x = -2, so x = 3 or x = -1. Replacing x with 2x compresses the graph horizontally by a factor of 1/2, so each x-intercept of f (6 and -2) is halved. Therefore, the sum is 3 + (-1) = 2. Distractors: 4 is the sum of the x-intercepts of f, with no compression; 3 and -1 are the individual x-intercepts of g, not their sum.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=(x-6)(x+2)</code><br><code>g(x)=f(2x)</code><br><code>y=g(x)</code>

Click the x-intercepts of y = g(x): (-1, 0) and (3, 0). Their x-coordinates sum to 2. Note the intercepts of f itself, -2 and 6, are not asked for.

</details>

---

### 78. adv-nf-bridge-cable-length-below

*Hard · Student-produced response · route: either · techniques: T1*

A bridge cable hangs between two towers. Its height above the road, in meters, is modeled by $h(x) = 0.02x^2 - 4x + 210$, where $x$ is the distance, in meters, along the road from one tower. Over what length of road, in meters, is the cable at most 12 meters above the road?

**Answer:** 20

<details><summary>Solutions</summary>

**By hand.** Setting h(x) ≤ 12 yields 0.02x^2 - 4x + 198 ≤ 0. Multiplying both sides by 50 yields x^2 - 200x + 9,900 ≤ 0, which factors as (x - 90)(x - 110) ≤ 0, so 90 ≤ x ≤ 110. Alternate approach: completing the square gives h(x) = 0.02(x - 100)^2 + 10, so h(x) ≤ 12 when (x - 100)^2 ≤ 100, that is, within 10 meters of x = 100. Therefore, the cable is at most 12 meters above the road over 110 - 90 = 20 meters of road.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=0.02x^2-4x+210</code><br><code>y=12</code>

Zoom out: the vertex is at (100, 10). Click the two intersections, (90, 12) and (110, 12). The length of road is 110 - 90 = 20.

</details>

---

### 79. adv-nf-composition-find-linear

*Hard · Multiple choice · route: hand-primary · techniques: —*

Let $f(x) = x^2 + 1$ and $g(x) = ax + b$, where $a$ and $b$ are constants and $a > 0$. If $f(g(x)) = 4x^2 - 12x + 10$ for all values of $x$, what is the value of $g(5)$?

- **A.** $-7$
- **B.** $7$
- **C.** $13$
- **D.** $50$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since f(g(x)) = (ax + b)^2 + 1 = a^2x^2 + 2abx + b^2 + 1, matching coefficients with 4x^2 - 12x + 10 yields a^2 = 4, 2ab = -12 and b^2 + 1 = 10. Because a > 0, a = 2, and then 4b = -12 yields b = -3 (check: (-3)^2 + 1 = 10). So g(x) = 2x - 3, and g(5) = 10 - 3 = 7. Therefore, the value of g(5) is 7. Distractors: -7 uses a = -2 and b = 3, the pair that the condition a > 0 rules out; 13 uses g(x) = 2x + 3, a sign slip on b; 50 is f(g(5)) = 7^2 + 1, the outer value instead of g(5).

</details>

---

### 80. adv-nf-coral-linear-vs-exponential-midpoint

*Hard · Student-produced response · route: desmos-primary · techniques: T9*

On each of reefs A and B, coral covers 200 square meters in year 0 and 260 square meters in year 6. On reef A the area grows by the same amount each year; on reef B it grows by the same percent each year. To the nearest square meter, how much greater is the area on reef A than on reef B in year 3?

**Answer:** 2

<details><summary>Solutions</summary>

**By hand.** Reef A grows by 260 - 200 = 60 square meters in 6 years, or 10 square meters per year, so its area in year 3 is 200 + 30 = 230. Reef B is multiplied by 260/200 = 1.3 every 6 years, so its area in year t is 200(1.3)^(t/6), and in year 3 it is 200(1.3)^(1/2) = 200√1.3 = √52,000. Since 228^2 = 51,984 and 228.5^2 = 52,212.25, this area is between 228 and 228.5 (about 228.04), so the difference is between 1.5 and 2 (about 230 - 228.04 = 1.96). Therefore, to the nearest square meter, the area on reef A is 2 square meters greater. Halfway through the interval, the exponential model lags the linear one because its growth is slowest at the start.

**Desmos** (not yet verified in Desmos). Type:<br><code>a(x)=200+10x</code><br><code>b(x)=200(1.3)^{x/6}</code><br><code>a(3)-b(3)</code>

The third line shows about 1.965. Round to the nearest square meter and enter 2.

</details>

---

### 81. adv-nf-cubic-end-behavior-sign-of-a

*Hard · Multiple choice · route: hand-primary · techniques: —*

For the cubic function $f(x) = a(x - 1)(x + 2)(x - 4)$, where $a$ is a nonzero constant, $f(x)$ decreases without bound as $x$ increases without bound. What is one possible value of $f(0)$?

- **A.** $-8$
- **B.** $0$
- **C.** $4$
- **D.** $8$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Expanding the product shows that the leading term of f(x) is ax^3. As x increases without bound, ax^3 decreases without bound only when a < 0. Substituting 0 for x yields f(0) = a(-1)(2)(-4) = 8a, which is negative because a < 0. Of the choices, only -8 is negative; it occurs when a = -1. Distractors: 0 treats x = 0 as a zero of f, but the zeros are 1, -2 and 4, and a is nonzero; 4 is an x-intercept, not the value of f(0); 8 is f(0) when a = 1, which ignores the end behavior. A Desmos slider for a can confirm the sign, but the reasoning is faster.

</details>

---

### 82. adv-nf-cubic-negative-leading-sign-interval

*Hard · Multiple choice · route: hand-primary · techniques: T1*

The function $f$ is defined by $f(x) = -(x + 3)(x - 2)^2$. Which of the following describes all values of $x$ for which $f(x) > 0$?

- **A.** $x < -3$
- **B.** $x > -3$
- **C.** $-3 < x < 2$
- **D.** $x > 2$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The factor (x - 2)^2 is positive for every x except 2, where it is 0. So for x ≠ 2, f(x) has the sign of -(x + 3), which is positive exactly when x + 3 < 0, that is, when x < -3. At x = 2, f(x) = 0. Therefore, f(x) > 0 for all x < -3 and no other x. Distractors: x > -3 drops the leading negative sign, which reverses every sign; -3 < x < 2 treats the squared factor as if it changed sign at x = 2, like a factor to the first power; x > 2 assumes the graph rises to the right, as for a cubic with a positive leading coefficient.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-(x+3)(x-2)^2</code>

A sign check by hand is quicker. As a check, the graph is above the x-axis only to the left of x = -3; at x = 2 it touches the x-axis and stays below it on both sides.

</details>

---

### 83. adv-nf-cubic-shift-up-intercept-count

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

The function $f$ is defined by $f(x) = (x - 1)(x + 3)^2$. How many $x$-intercepts does the graph of $y = f(x) + 4$ have in the $xy$-plane?

- **A.** $0$
- **B.** $1$
- **C.** $2$
- **D.** $3$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The graph of y = f(x) touches the x-axis at x = -3, where (x + 3)^2 has a double zero, and crosses it at x = 1. Since (x + 3)^2 ≥ 0, f(x) ≤ 0 for all x ≤ 1, so (-3, 0) is a local maximum, and between -3 and 1 the graph dips below the axis; for example, f(-1) = (-2)(2)^2 = -8. Adding 4 shifts the graph up 4 units: the point (-3, 0) moves to (-3, 4), above the x-axis, and (-1, -8) moves to (-1, -4), below it. The graph still falls without bound as x decreases and rises without bound as x increases, so the graph of y = f(x) + 4 crosses the x-axis once to the left of -3, once between -3 and -1, and once to the right of -1. Therefore, it has 3 x-intercepts. Distractors: 2 counts the distinct x-intercepts of y = f(x) itself; 1 is the count for y = f(x) - 4, a shift down instead of up; 0 assumes the shift lifts the whole graph above the x-axis, but the graph of a cubic always crosses the x-axis at least once.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x-1)(x+3)^2+4</code>

Zoom out to see the whole curve, then count the gray x-intercepts: three, near x = -3.9, x = -1.8 and x = 0.7 (only the count matters).

</details>

---

### 84. adv-nf-cubic-touch-cross-evaluate

*Hard · Student-produced response · route: either · techniques: T4, T9*

In the $xy$-plane, the graph of $y = p(x)$, where $p$ is a cubic polynomial function, crosses the $x$-axis at $x = -1$, touches the $x$-axis without crossing it at $x = 2$, and has no other $x$-intercepts. The $y$-intercept of the graph is $(0, 12)$. What is the value of $p(4)$?

**Answer:** 60

<details><summary>Solutions</summary>

**By hand.** A graph crosses the x-axis at a zero from a factor to an odd power and touches it without crossing at a zero from a factor to an even power. A cubic has degree 3, so p(x) = a(x + 1)(x - 2)^2, where a is a constant. It's given that p(0) = 12, so a(1)(4) = 12 and a = 3. Substituting 4 for x yields p(4) = 3(5)(2)^2 = 60. Therefore, the value of p(4) is 60.

**Desmos** (not yet verified in Desmos). Type:<br><code>p(x)=a(x+1)(x-2)^2</code><br><code>p(0)</code><br><code>p(4)</code>

Add a slider for a and drag it until the line p(0) shows 12; that happens at a = 3. The line p(4) then shows 60.

</details>

---

### 85. adv-nf-divers-maximum-height-gap

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

The functions $A(t) = -5t^2 + 6t + 3$ and $B(t) = -5t^2 + 4t + 10$ model the heights above the water, in meters, of divers A and B $t$ seconds after leaving their boards. How many meters greater is the maximum height of diver B than that of diver A?

**Answer:** 6

<details><summary>Solutions</summary>

**By hand.** A quadratic function at^2 + bt + c with a < 0 has its maximum at t = -b/(2a). For diver A, t = -6/(-10) = 0.6, and A(0.6) = -1.8 + 3.6 + 3 = 4.8. For diver B, t = -4/(-10) = 0.4, and B(0.4) = -0.8 + 1.6 + 10 = 10.8. Therefore, the maximum height of diver B is 10.8 - 4.8 = 6 meters greater. The difference of the starting heights, 10 - 3 = 7, is a trap: diver A rises more after leaving the board.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-5x^2+6x+3</code><br><code>y=-5x^2+4x+10</code>

Click the top of each parabola: (0.6, 4.8) and (0.4, 10.8). The maximum heights are the y-coordinates; 10.8 - 4.8 = 6.

</details>

---

### 86. adv-nf-equal-at-four-compare-at-six

*Hard · Multiple choice · route: desmos-primary · techniques: T9*

For the functions $f(x) = x^2 + kx$ and $g(x) = 2x^2 - 3x$, where $k$ is a constant, $f(4) = g(4)$. What is the value of $g(6) - f(6)$?

- **A.** $-12$
- **B.** $0$
- **C.** $12$
- **D.** $54$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Substituting 4 for x yields f(4) = 16 + 4k and g(4) = 32 - 12 = 20. Setting them equal yields 16 + 4k = 20, so k = 1. Then f(6) = 36 + 6 = 42 and g(6) = 72 - 18 = 54, so g(6) - f(6) = 54 - 42 = 12. Distractors: -12 computes f(6) - g(6), the difference in the wrong order; 0 assumes the functions are still equal at x = 6 because they are equal at x = 4; 54 is g(6) alone.

**Desmos** (not yet verified in Desmos). Type:<br><code>g(x)=2x^2-3x</code><br><code>k=\frac{g(4)-16}{4}</code><br><code>f(x)=x^2+kx</code><br><code>g(6)-f(6)</code>

The second line computes k = 1 from 16 + 4k = g(4). The last line shows 12.

</details>

---

### 87. adv-nf-exponential-doubling-period

*Hard · Multiple choice · route: hand-primary · techniques: T1*

The function $f$ is defined by $f(x) = 400(8)^{\frac{x}{9}}$. For each increase of $x$ by $k$, the value of $f(x)$ doubles, where $k$ is a constant. What is the value of $k$?

- **A.** $3$
- **B.** $4.5$
- **C.** $9$
- **D.** $72$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Since 8 = 2^3, f(x) = 400(2^3)^(x/9) = 400(2)^(x/3). In this form, f(x) is multiplied by 2 each time x/3 increases by 1, that is, each time x increases by 3. Therefore, k = 3. Alternate approach: f(x + k) = 2f(x) requires 8^(k/9) = 2, so 2^(3k/9) = 2^1 and k/3 = 1. Distractors: 9 is the increase in x that multiplies f(x) by 8, not by 2; 4.5 halves 9, as if doubling took half the time that multiplying by 8 does; 72 multiplies the base 8 by 9.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=400(8)^{x/9}</code><br><code>y=800</code>

Desmos is slower than the rewrite. To check, note that f(0) = 400 and click the intersection with y = 800, double that value: (3, 800). The increase in x is 3.

</details>

---

### 88. adv-nf-exponential-input-scale-rewrite

*Hard · Student-produced response · route: hand-primary · techniques: T9, T5*

The functions $f$ and $g$ satisfy $f(x) = 3(9)^x$ and $g(x) = f(\frac{x}{2} + 1)$ for all $x$. The function $g$ can be written as $g(x) = a(b)^x$, where $a$ and $b$ are positive constants. What is the value of $a + b$?

**Answer:** 30

<details><summary>Solutions</summary>

**By hand.** Substituting x/2 + 1 for x in f yields g(x) = 3(9)^(x/2 + 1) = 3(9)(9)^(x/2) = 27(9)^(x/2). Since 9^(x/2) = (9^(1/2))^x = 3^x, g(x) = 27(3)^x. So a = 27 and b = 3. Therefore, the value of a + b is 30.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=3(9)^x</code><br><code>g(x)=f(\frac{x}{2}+1)</code><br><code>x_1=[0,1,2]</code><br><code>y_1=g(x_1)</code><br><code>y_1\sim ab^{x_1}</code>

Desmos is slower than the rewrite. The regression on three points of g gives a = 27 and b = 3, so a + b = 30. Typing g(0) alone shows a = 27, and g(1)/g(0) shows b = 3.

</details>

---

### 89. adv-nf-factored-cubic-remainder-constant

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

The function $p$ is defined by $p(x) = (x - a)(x - 4)(x + 2)$, where $a$ is a constant. Dividing $p(x)$ by $x - 1$ leaves a remainder of 18. What is the value of $a$?

- **A.** $-2$
- **B.** $-1$
- **C.** $1$
- **D.** $3$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** By the remainder theorem, the remainder when p(x) is divided by x - 1 is p(1). Substituting 1 for x yields p(1) = (1 - a)(1 - 4)(1 + 2) = (1 - a)(-3)(3) = -9(1 - a). Setting -9(1 - a) = 18 yields 1 - a = -2, so a = 3. Therefore, the value of a is 3. Distractors: -2 is the value of 1 - a, an intermediate result; -1 drops the negative sign from 1 - 4 and solves 9(1 - a) = 18; 1 assumes that x - 1 is a factor of p(x), so that the remainder is 0.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(1-x)(1-4)(1+2)</code><br><code>y=18</code>

The first line is p(1) with a replaced by x. Click the intersection with y = 18: (3, 18). The value of a is the x-coordinate, 3.

</details>

---

### 90. adv-nf-factored-plus-c-y-intercept

*Hard · Multiple choice · route: either · techniques: T4, T1*

For the function $f(x) = (x - 2)(x - 8) + c$, where $c$ is a constant, the least value that $f(x)$ takes is $-7$. What is the value of $f(0)$?

- **A.** $0$
- **B.** $9$
- **C.** $16$
- **D.** $18$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The graph of y = (x - 2)(x - 8) is a parabola symmetric about x = (2 + 8)/2 = 5, and adding c does not move the axis of symmetry, so the least value of f(x) occurs at x = 5. Then f(5) = (3)(-3) + c = -9 + c = -7, which yields c = 2. Therefore, f(0) = (-2)(-8) + 2 = 18, the y-coordinate of the y-intercept of the graph. Distractors: 0 solves -9 + c = -7 with a sign slip, c = -16; 9 takes c = -7, treating the least value as c; 16 is (-2)(-8), ignoring c.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x-2)(x-8)+c</code>

Add a slider for c and drag until the vertex is at (5, -7), at c = 2. Then click the y-intercept: (0, 18); f(0) is its y-coordinate, 18. The symmetry argument by hand is about as fast.

</details>

---

### 91. adv-nf-half-life-ratio-constant

*Hard · Student-produced response · route: hand-primary · techniques: T1*

The function $f$ is defined by $f(x) = 500(\frac{1}{2})^{x/h}$, where $h$ is a positive constant. If $f(4) = 2f(10)$, what is the value of $h$?

**Answer:** 6

<details><summary>Solutions</summary>

**By hand.** Since f(x) is halved each time x increases by h, the condition f(4) = 2f(10), that is, f(10) = (1/2)f(4), says that the value is halved exactly once from x = 4 to x = 10. So h = 10 - 4 = 6. Algebraically, 500(1/2)^(4/h) = 2 · 500(1/2)^(10/h) yields (1/2)^(4/h - 10/h) = 2, or (1/2)^(-6/h) = 2^(6/h) = 2, so 6/h = 1 and h = 6. Therefore, the value of h is 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=500(1/2)^{4/x}</code><br><code>y=2\cdot500(1/2)^{10/x}</code>

The exponent argument by hand is faster. As a check, replace h with x on both sides of f(4) = 2f(10) and click the intersection, about (6, 315). The value of h is the x-coordinate, 6.

</details>

---

### 92. adv-nf-intercepts-six-apart-k

*Hard · Multiple choice · route: hand-primary · techniques: —*

For $f(x) = (x - 4)^2 + k$, where $k$ is a constant, the graph of $y = f(x)$ in the $xy$-plane has two $x$-intercepts that are 6 units apart. What is the value of $k$?

- **A.** $-36$
- **B.** $-9$
- **C.** $-3$
- **D.** $9$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The graph is a parabola with axis of symmetry x = 4, so its two x-intercepts are equally far from x = 4. Since they are 6 units apart, each is 3 units from x = 4: the x-intercepts are at x = 1 and x = 7. Substituting 7 for x in f(x) = 0 yields (7 - 4)^2 + k = 0, so 9 + k = 0 and k = -9. Distractors: 9 has the wrong sign, which would place the vertex above the x-axis and give no x-intercepts; -3 uses the distance 3 without squaring it; -36 squares the full distance 6 instead of half of it. A Desmos slider for k can confirm the answer, but symmetry is faster.

</details>

---

### 93. adv-nf-linear-vs-exponential-two-intervals

*Hard · Multiple choice · route: desmos-primary · techniques: T9*

A linear function $f$ and an exponential function $g$ satisfy $f(x) = 100 + 30x$ and $g(x) = 100(1.25)^x$. Which statement compares the increases in $f(x)$ and $g(x)$ over the intervals $0 \le x \le 2$ and $2 \le x \le 4$?

- **A.** From $x = 0$ to $x = 2$, $f(x)$ increases more; from $x = 2$ to $x = 4$, $f(x)$ increases more.
- **B.** From $x = 0$ to $x = 2$, $f(x)$ increases more; from $x = 2$ to $x = 4$, $g(x)$ increases more.
- **C.** From $x = 0$ to $x = 2$, $g(x)$ increases more; from $x = 2$ to $x = 4$, $f(x)$ increases more.
- **D.** From $x = 0$ to $x = 2$, $g(x)$ increases more; from $x = 2$ to $x = 4$, $g(x)$ increases more.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The function f is linear with slope 30, so f(x) increases by 30(2) = 60 over each interval of length 2. For g, g(0) = 100, g(2) = 100(1.25)^2 = 156.25 and g(4) = 100(1.25)^4 ≈ 244.14. So g(x) increases by 56.25 from x = 0 to x = 2 and by about 87.89 from x = 2 to x = 4. Therefore, f(x) increases more on the first interval and g(x) increases more on the second. Distractors: f(x) increases more on both intervals compares only the first interval, or compares 30 with the 25% rate; g(x) increases more on both intervals assumes exponential growth is always faster; g(x) increases more from x = 0 to x = 2, and f(x) increases more from x = 2 to x = 4 reverses the pattern, which is impossible because the increases in g(x) grow while those in f(x) stay at 60.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=100+30x</code><br><code>g(x)=100(1.25)^x</code><br><code>f(2)-f(0)</code><br><code>g(2)-g(0)</code><br><code>f(4)-f(2)</code><br><code>g(4)-g(2)</code>

The lines show 60, 56.25, 60 and about 87.89. On the first interval f increases more (60 > 56.25); on the second g increases more (87.89 > 60).

</details>

---

### 94. adv-nf-model-rocket-three-heights

*Hard · Student-produced response · route: desmos-primary · techniques: T5*

The height of a model rocket $t$ seconds after launch is a quadratic function of $t$. The height is 38 meters at $t = 1$, 63 meters at $t = 2$, and 78 meters at $t = 3$. According to the model, what is the maximum height, in meters, of the rocket?

**Answer:** 83

<details><summary>Solutions</summary>

**By hand.** Write h(t) = at^2 + bt + c. The data give a + b + c = 38, 4a + 2b + c = 63 and 9a + 3b + c = 78. Subtracting consecutive equations yields 3a + b = 25 and 5a + b = 15, so 2a = -10, a = -5, b = 40 and c = 3. Then h(t) = -5t^2 + 40t + 3, whose maximum occurs at t = -40/(2(-5)) = 4, where h(4) = -80 + 160 + 3 = 83. Therefore, the maximum height is 83 meters. Alternate approach: the differences 25 and 15 drop by 10 each second, so the next differences are 5 and -5, the height peaks at t = 4, and h(4) = 78 + 5 = 83.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3]</code><br><code>y_1=[38,63,78]</code><br><code>y_1\sim ax_1^2+bx_1+c</code><br><code>y=ax^2+bx+c</code>

The regression gives a = -5, b = 40, c = 3, an exact fit through the three points. Click the maximum of the graph: (4, 83). The maximum height is the y-coordinate, 83.

</details>

---

### 95. adv-nf-no-intercepts-greatest-b

*Hard · Student-produced response · route: either · techniques: T4*

In the $xy$-plane, the graph of $y = x^2 + bx + 16$ has no $x$-intercepts, where $b$ is a positive integer. What is the greatest possible value of $b$?

**Answer:** 7

<details><summary>Solutions</summary>

**By hand.** The graph has no x-intercepts when x^2 + bx + 16 = 0 has no real solutions, that is, when the discriminant b^2 - 4(1)(16) = b^2 - 64 is negative. b^2 < 64 means -8 < b < 8. The greatest positive integer less than 8 is 7. Therefore, the greatest possible value of b is 7. The value 8 is a trap: it makes the discriminant 0, so the graph touches the x-axis at one point.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+bx+16</code>

Add a slider for b and set its step to 1. Drag b up from 1: through b = 7 the parabola stays above the x-axis; at b = 8 the vertex touches it at (-4, 0). The greatest value is 7.

</details>

---

### 96. adv-nf-pen-wall-max-area

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

A rectangular pen is built against a long wall, so fencing is needed on only three sides of the pen. A total of 120 meters of fencing is used. What is the maximum possible area, in square meters, of the pen?

- **A.** $30$
- **B.** $900$
- **C.** $1,800$
- **D.** $3,600$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let x be the length, in meters, of each of the two sides perpendicular to the wall. The side parallel to the wall then uses 120 - 2x meters, so the area is A(x) = x(120 - 2x). The zeros of A are x = 0 and x = 60, so the maximum occurs halfway between them, at x = 30, where A(30) = 30(60) = 1,800. Therefore, the maximum possible area is 1,800 square meters. Distractors: 30 is the side length that gives the maximum, not the area; 900 is the area of a 30 by 30 square fenced on all four sides; 3,600 uses A(x) = x(120 - x), which fences only one side perpendicular to the wall and gives a 60 by 60 pen.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x(120-2x)</code>

Here x is the length of each side perpendicular to the wall. Zoom out and click the maximum: (30, 1800). The area is the y-coordinate, 1,800, not x = 30.

</details>

---

### 97. adv-nf-pendulum-longer-swing

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

The function $T(L) = 2\sqrt{L}$ models the time $T(L)$, in seconds, for one swing of a pendulum that is $L$ meters long. According to the model, how many meters longer is a pendulum with a swing time of 5 seconds than a pendulum with a swing time of 4 seconds?

**Answer:** 9/4 (≈ 2.25)

<details><summary>Solutions</summary>

**By hand.** Setting T(L) = 5 yields 2√L = 5, so √L = 2.5 and L = 6.25. Setting T(L) = 4 yields 2√L = 4, so √L = 2 and L = 4. The difference in lengths is 6.25 - 4 = 2.25. Therefore, the pendulum with a swing time of 5 seconds is 2.25 meters longer.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2\sqrt{x}</code><br><code>y=4</code><br><code>y=5</code>

Click the two intersections: (4, 4) and (6.25, 5). The lengths are the x-coordinates; subtract: 6.25 - 4 = 2.25. Enter 2.25 or 9/4.

</details>

---

### 98. adv-nf-quadratic-greater-than-interval

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

The quadratic functions $f$ and $g$ satisfy $f(x) = x^2 + 2x - 3$ and $g(x) = -x^2 + 4x + 9$ for all $x$. For which values of $x$ is $f(x)$ greater than $g(x)$?

- **A.** $-3 < x < 2$
- **B.** $-2 < x < 3$
- **C.** $x < -3$ or $x > 2$
- **D.** $x < -2$ or $x > 3$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** f(x) > g(x) means f(x) - g(x) > 0. Subtracting yields f(x) - g(x) = 2x^2 - 2x - 12 = 2(x - 3)(x + 2). This product is 0 at x = -2 and x = 3, and because the leading coefficient is positive, it is positive outside those values. Therefore, f(x) > g(x) for x < -2 or x > 3. Distractors: -2 < x < 3 is where g(x) > f(x); x < -3 or x > 2 factors 2x^2 - 2x - 12 with the signs reversed, as 2(x + 3)(x - 2); -3 < x < 2 makes both mistakes.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+2x-3</code><br><code>y=-x^2+4x+9</code>

Click the two intersections: (-2, -3) and (3, 12). The upward parabola, y = f(x), is above the downward one to the left of x = -2 and to the right of x = 3.

</details>

---

### 99. adv-nf-quadratic-symmetric-values

*Hard · Multiple choice · route: either · techniques: T5, T9*

For the quadratic function $f$, $f(-1) = 12$, $f(2) = -6$, and $f(5) = 12$. What is the value of $f(7)$?

- **A.** $24$
- **B.** $44$
- **C.** $50$
- **D.** $56$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since f(-1) = f(5), the axis of symmetry of the parabola is x = (-1 + 5)/2 = 2, so (2, -6) is the vertex and f(x) = a(x - 2)^2 - 6. Substituting f(5) = 12 yields 9a - 6 = 12, so a = 2. Then f(7) = 2(7 - 2)^2 - 6 = 50 - 6 = 44. Therefore, the value of f(7) is 44. Distractors: 24 continues the change from f(2) to f(5), 6 per unit, as if f were linear; 50 is 2(5)^2, leaving off the -6; 56 adds 6 instead of subtracting it.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[-1,2,5]</code><br><code>y_1=[12,-6,12]</code><br><code>y_1\sim ax_1^2+bx_1+c</code><br><code>f(x)=ax^2+bx+c</code><br><code>f(7)</code>

The regression gives a = 2, b = -8, c = 2, and f(7) shows 44. The symmetry argument by hand is about as fast.

</details>

---

### 100. adv-nf-rational-approach-find-a

*Hard · Student-produced response · route: hand-primary · techniques: —*

The function $f$ is defined by $f(x) = \frac{ax + 3}{x - 2}$, where $a$ is a constant. As $x$ increases without bound, the value of $f(x)$ gets closer to 5. What is the value of $f(4)$?

**Answer:** 23/2 (≈ 11.5)

<details><summary>Solutions</summary>

**By hand.** For very large x, the constants 3 and -2 are small compared with the x terms, so f(x) is close to ax/x = a. It's given that f(x) gets closer to 5, so a = 5. Then f(x) = (5x + 3)/(x - 2), and f(4) = (20 + 3)/(4 - 2) = 23/2. Therefore, the value of f(4) is 23/2; enter 23/2 or 11.5. A Desmos slider for a can confirm that the graph levels off at y = 5 when a = 5, but finding a by reasoning is faster.

</details>

---

### 101. adv-nf-rational-point-undefined-input

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

The function $f$ is defined by $f(x) = \frac{8}{x - k} + 3$, where $k$ is a constant. The graph of $y = f(x)$ in the $xy$-plane passes through the point $(5, 7)$. For what value of $x$ is $f(x)$ undefined?

- **A.** $5$
- **B.** $3$
- **C.** $1$
- **D.** $-3$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** It's given that f(5) = 7, so 8/(5 - k) + 3 = 7. Subtracting 3 from both sides yields 8/(5 - k) = 4, so 5 - k = 2 and k = 3. Then f(x) = 8/(x - 3) + 3, which is undefined when x - 3 = 0, that is, when x = 3. Therefore, f(x) is undefined at x = 3. Distractors: 5 is the x-coordinate of the given point, where f(5) = 7 is defined; 1 sets 5 - k = 4 instead of 8/(5 - k) = 4; -3 is the value of x that makes x + 3 zero, a sign error in the denominator x - k.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{8}{5-x}+3</code><br><code>y=7</code>

This is f(5) with k replaced by x. Click the intersection with y = 7: (3, 7), so k = 3. The denominator x - 3 of f is 0 at x = 3.

</details>

---

### 102. adv-nf-regression-reflect-shift-max

*Hard · Student-produced response · route: desmos-primary · techniques: T5, T9, T1*

For the quadratic function $f$, $f(-1) = 15$, $f(1) = 3$, and $f(5) = 27$. The function $h$ is defined by $h(x) = 10 - f(x - 2)$. What is the maximum value of $h$?

**Answer:** 15/2 (≈ 7.5)

<details><summary>Solutions</summary>

**By hand.** Write f(x) = ax^2 + bx + c. From f(1) = 3 and f(-1) = 15, a + b + c = 3 and a - b + c = 15; subtracting yields 2b = -12, so b = -6 and a + c = 9. From f(5) = 27, 25a + 5b + c = 27, or 25a + c = 57; subtracting a + c = 9 yields 24a = 48, so a = 2 and c = 7. Then f(x) = 2x^2 - 6x + 7, whose minimum occurs at x = 6/4 = 1.5, where f(1.5) = 4.5 - 9 + 7 = 2.5. The shift x - 2 moves the graph 2 units right but does not change the minimum value 2.5, and h(x) = 10 - f(x - 2) is greatest when f(x - 2) is least. Therefore, the maximum value of h is 10 - 2.5 = 7.5.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[-1,1,5]</code><br><code>y_1=[15,3,27]</code><br><code>y_1\sim ax_1^2+bx_1+c</code><br><code>f(x)=ax^2+bx+c</code><br><code>h(x)=10-f(x-2)</code><br><code>y=h(x)</code>

The regression gives a = 2, b = -6, c = 7. Define f from the fitted parameters, then build h from f (define by regression, then shift: the T15 move). Click the maximum of y = h(x): (3.5, 7.5). The maximum value is the y-coordinate; enter 7.5 or 15/2.

</details>

---

### 103. adv-nf-remainder-factor-of-shifted

*Hard · Multiple choice · route: hand-primary · techniques: —*

For a polynomial function $p$, $p(-3) = 5$. Which of the following must be a factor of $p(x) - 5$?

- **A.** $x - 5$
- **B.** $x - 3$
- **C.** $x + 3$
- **D.** $x + 5$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let q(x) = p(x) - 5. It's given that p(-3) = 5, so q(-3) = 5 - 5 = 0. By the factor theorem, if q(-3) = 0, then x - (-3), or x + 3, is a factor of q(x). Equivalently, the remainder when p(x) is divided by x + 3 is p(-3) = 5, so p(x) - 5 is divisible by x + 3. Therefore, x + 3 must be a factor of p(x) - 5. Distractors: x - 5 uses the output 5 as a zero; x - 3 uses the input with the wrong sign; x + 5 builds the factor from the output instead of the input.

</details>

---

### 104. adv-nf-shift-left-down-expanded

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

Let $f(x) = x^2 - 4x$. The graph of $y = g(x)$ in the $xy$-plane is obtained by shifting the graph of $y = f(x)$ to the left 2 units and down 5 units. Which equation defines $g$?

- **A.** $g(x) = x^2 - 8x + 7$
- **B.** $g(x) = x^2 - 9$
- **C.** $g(x) = x^2 - 1$
- **D.** $g(x) = x^2 + 1$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Shifting left 2 units replaces x with x + 2, and shifting down 5 units subtracts 5, so g(x) = f(x + 2) - 5 = (x + 2)^2 - 4(x + 2) - 5. Expanding yields x^2 + 4x + 4 - 4x - 8 - 5 = x^2 - 9. Therefore, g(x) = x^2 - 9. Distractors: x^2 - 8x + 7 shifts right instead of left, (x - 2)^2 - 4(x - 2) - 5; x^2 - 1 replaces x with x + 2 only in the x^2 term, (x + 2)^2 - 4x - 5; x^2 + 1 shifts up 5 instead of down.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=x^2-4x</code><br><code>y=f(x+2)-5</code><br><code>y=x^2-9</code>

A shift left by 2 replaces x with x + 2. Graph y = f(x + 2) - 5 and then each choice (T13); only y = x^2 - 9 lies exactly on top of it.

</details>

---

### 105. adv-nf-shifted-exponential-two-points

*Hard · Student-produced response · route: desmos-primary · techniques: T5, T1*

For the function $f(x) = a(b)^x - 5$, where $a$ and $b$ are positive constants, the graph of $y = f(x)$ in the $xy$-plane contains the points $(0, 11)$ and $(2, 139)$. For what value of $x$ is $f(x) = 1,291$?

**Answer:** 4

<details><summary>Solutions</summary>

**By hand.** Substituting the point (0, 11) yields a(b)^0 - 5 = 11, so a = 16. Substituting the point (2, 139) yields 16b^2 - 5 = 139, so b^2 = 9, and b = 3 because b is positive. Setting f(x) = 1,291 yields 16(3)^x - 5 = 1,291, so 16(3)^x = 1,296 and 3^x = 81 = 3^4. Therefore, x = 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,2]</code><br><code>y_1=[11,139]</code><br><code>y_1\sim ab^{x_1}-5</code><br><code>y=ab^x-5</code><br><code>y=1291</code>

The regression gives a = 16 and b = 3. Zoom out and click the intersection of y = ab^x - 5 with y = 1291: (4, 1291). Enter 4.

</details>

---

### 106. adv-nf-ski-pass-ten-percent-above

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

A ski pass costs a one-time fee of 120.00 dollars plus 30.00 dollars per day. The average cost, in dollars per day, for $d$ days is $A(d) = \frac{120 + 30d}{d}$. As $d$ increases, $A(d)$ approaches a certain value. For how many days is $A(d)$ 10% greater than that value?

- **A.** $4$
- **B.** $12$
- **C.** $33$
- **D.** $40$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Dividing each term by d yields A(d) = 120/d + 30. As d increases, 120/d gets closer to 0, so A(d) approaches 30. A value 10% greater than 30 is 1.1(30) = 33. Setting 120/d + 30 = 33 yields 120/d = 3, so d = 40. Therefore, the average cost is 10% greater than its long-run value for 40 days. Distractors: 4 is 120/30, the fee divided by the daily cost; 12 is 120/10, which uses 10 itself instead of 10% of 30; 33 is the average cost in dollars per day, not the number of days.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{120+30x}{x}</code><br><code>y=30</code><br><code>y=1.1\cdot30</code>

Zoom out: the curve levels off along y = 30, so the target is 1.1 times 30, or 33. Click the intersection of the curve with y = 33: (40, 33). The number of days is the x-coordinate, 40.

</details>

---

### 107. adv-nf-solar-panels-two-towns

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

The functions $A(t) = 500(1.2)^t$ and $B(t) = 2,000(1.05)^t$ model the numbers of solar panels in town A and town B, respectively, $t$ years after a program begins. What is the least whole number of years $t$ for which $A(t) > B(t)$?

- **A.** $4$
- **B.** $8$
- **C.** $10$
- **D.** $11$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The models are equal when 500(1.2)^t = 2,000(1.05)^t, or (1.2/1.05)^t = 4. Since 1.2/1.05 = 8/7, this is (8/7)^t = 4, and repeated squaring gives (8/7)^2 = 64/49 ≈ 1.306, (8/7)^4 ≈ 1.706, (8/7)^8 ≈ 2.909, so (8/7)^10 ≈ 2.909 × 1.306 ≈ 3.80 < 4 and (8/7)^11 ≈ 3.80 × 8/7 ≈ 4.34 > 4; the crossing is about t = 10.4. Checking whole numbers, A(10) is about 3,096 and B(10) is about 3,258, so A(10) < B(10); A(11) is about 3,715 and B(11) is about 3,421, so A(11) > B(11). Therefore, the least whole number of years is 11. Distractors: 4 is the ratio 2,000/500 of the starting values; 8 solves 500(1.2)^t = 2,000(1.05), applying the factor 1.05 only once (t is about 7.9); 10 rounds the crossing time 10.4 down, but at t = 10 town A still has fewer panels.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=500(1.2)^x</code><br><code>y=2000(1.05)^x</code>

Zoom out until the curves cross; click the intersection, about (10.38, 3319). A is below B before the crossing and above it after, so the least whole number of years is 11, not 10.

</details>

---

### 108. adv-nf-square-perimeter-rule-area

*Hard · Multiple choice · route: either · techniques: T9*

For $x > 0$, $A(x)$ is the area of a square with perimeter $x + 8$. What is the value of $A(12)$?

- **A.** $400$
- **B.** $121$
- **C.** $100$
- **D.** $25$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A square has 4 equal sides, so a square with perimeter x + 8 has side length (x + 8)/4, and its area is A(x) = ((x + 8)/4)^2. Substituting 12 for x yields a side length of 20/4 = 5 and A(12) = 5^2 = 25. Therefore, the value of A(12) is 25. Distractors: 400 treats the perimeter 20 as the side length; 121 divides only x by 4, getting a side length of 12/4 + 8 = 11; 100 uses half the perimeter, 10, as the side length.

**Desmos** (not yet verified in Desmos). Type:<br><code>A(x)=\left(\frac{x+8}{4}\right)^2</code><br><code>A(12)</code>

The second line shows 25. The work is writing the rule; parentheses around x+8 are required before dividing by 4.

</details>

---

### 109. adv-nf-tea-cooling-constant

*Hard · Multiple choice · route: either · techniques: T9*

The function $T(m) = 22 + 68(0.9)^m$ models the temperature, in degrees Celsius, of a cup of tea $m$ minutes after it is poured. Which statement is the best interpretation of 22 in this context?

- **A.** The tea's temperature when it is poured is 22 degrees Celsius.
- **B.** The tea's temperature decreases by 22 degrees Celsius each minute.
- **C.** The tea's temperature decreases by 22% each minute.
- **D.** The tea's temperature gets closer to 22 degrees Celsius as time passes.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** As m increases, (0.9)^m gets closer and closer to 0, so 68(0.9)^m shrinks toward 0 and T(m) gets closer to 22. Therefore, 22 is the temperature the tea approaches over time (the temperature of the room): the tea's temperature gets closer to 22 degrees Celsius as time passes. Distractors: the temperature when it is poured is T(0) = 22 + 68 = 90 degrees Celsius, not 22; the temperature does not drop by 22 degrees each minute, since T(0) - T(1) = 68 - 61.2 = 6.8; a decrease of 22% each minute misreads 22 as a percent rate, but the factor 0.9 means the gap between the tea and 22 degrees shrinks by 10% each minute.

**Desmos** (not yet verified in Desmos). Type:<br><code>T(x)=22+68(0.9)^x</code><br><code>T(0)</code><br><code>T(1)</code><br><code>T(100)</code><br><code>y=T(x)</code>

T(0) shows 90, so 22 is not the starting temperature; T(0) - T(1) is 6.8, not 22; T(100) shows about 22.002. Zoom out on y = T(x) to see the curve level off toward y = 22.

</details>

---

### 110. adv-nf-two-samples-equal-mass

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

The functions $A(t) = 400(\frac{1}{2})^{t/3}$ and $B(t) = 100(\frac{1}{2})^{t/6}$ model the masses, in grams, of two radioactive samples $t$ days after they are first measured. After how many days do the two samples have equal masses?

**Answer:** 12

<details><summary>Solutions</summary>

**By hand.** Setting A(t) = B(t) yields 400(1/2)^(t/3) = 100(1/2)^(t/6). Dividing both sides by 100(1/2)^(t/3) yields 4 = (1/2)^(t/6 - t/3) = (1/2)^(-t/6) = 2^(t/6). Since 4 = 2^2, t/6 = 2 and t = 12. Checking, A(12) = 400/16 = 25 and B(12) = 100/4 = 25. Therefore, the samples have equal masses after 12 days.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=400(1/2)^{x/3}</code><br><code>y=100(1/2)^{x/6}</code>

Click the intersection: (12, 25). The number of days is the x-coordinate, 12; the 25 is the common mass in grams.

</details>

---

### 111. adv-photo-frame-uniform-width

*Hard · Student-produced response · route: desmos-primary · techniques: T1*

A rectangular photo is 8 inches by 10 inches. A frame of uniform width surrounds the photo, and the combined area of the photo and the frame is 168 square inches. What is the width, in inches, of the frame?

**Answer:** 2

<details><summary>Solutions</summary>

**By hand.** Let w be the width, in inches, of the frame. The frame adds w inches on every side, so the outer rectangle is (8 + 2w) inches by (10 + 2w) inches, and its area is (8 + 2w)(10 + 2w) = 168. Expanding yields 4w^2 + 36w + 80 = 168, so 4w^2 + 36w - 88 = 0 and, dividing by 4, w^2 + 9w - 22 = 0. Factoring yields (w + 11)(w - 2) = 0, so w = 2 or w = -11. A width cannot be negative, so the frame is 2 inches wide. Using 8 + w and 10 + w (adding the width to only one side) gives w^2 + 18w - 88 = 0, or (w + 22)(w - 4) = 0, so w = 4; answering 4 is the common setup error.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(8+2x)(10+2x)</code><br><code>y=168</code>

The unknown width is typed as x; the frame adds x to each side of the photo, so each dimension grows by 2x. Click the intersection with a positive x-coordinate: (2, 168). The other intersection, at x = -11, is not a width. The answer is 2.

</details>

---

### 112. adv-quadratic-regression-shift-vertex

*Hard · Student-produced response · route: desmos-primary · techniques: T5, T9, T11*

The quadratic function $f$ satisfies $f(1) = 2$, $f(2) = 7$, and $f(4) = 29$. If $g(x) = f(x - 2)$ for all $x$, what is the $x$-coordinate of the vertex of the graph of $y = g(x)$ in the $xy$-plane?

**Answer:** 9/4 (≈ 2.25)

<details><summary>Solutions</summary>

**By hand.** Write f(x) = ax^2 + bx + c. The three values give a + b + c = 2, 4a + 2b + c = 7 and 16a + 4b + c = 29. Subtracting the first equation from the second yields 3a + b = 5; subtracting the second from the third yields 12a + 2b = 22, or 6a + b = 11. Then 3a = 6, so a = 2, b = -1 and c = 1. The vertex of f is at x = -b/(2a) = 1/4. Replacing x with x - 2 shifts the graph 2 units to the right, so the vertex of g is at x = 1/4 + 2 = 9/4.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,4]</code><br><code>y_1=[2,7,29]</code><br><code>y_1\sim ax_1^2+bx_1+c</code><br><code>f(x)=ax^2+bx+c</code><br><code>g(x)=f(x-2)</code><br><code>y=g(x)</code>

The regression gives a = 2, b = -1, c = 1 (define f by regression, then shift it: the proposed T15 move). Click the vertex of y = g(x): (2.25, 0.875). Enter 9/4 or 2.25.

</details>

---

### 113. adv-quartic-end-behavior-factored

*Hard · Multiple choice · route: desmos-primary · techniques: T1*

The function $f$ is defined by $f(x) = (2 - x)(x + 1)^2(x - 5)$. Which of the following describes the end behavior of the graph of $y = f(x)$ in the $xy$-plane?

- **A.** As $x$ decreases without bound, $f(x)$ decreases without bound, and as $x$ increases without bound, $f(x)$ decreases without bound.
- **B.** As $x$ decreases without bound, $f(x)$ decreases without bound, and as $x$ increases without bound, $f(x)$ increases without bound.
- **C.** As $x$ decreases without bound, $f(x)$ increases without bound, and as $x$ increases without bound, $f(x)$ decreases without bound.
- **D.** As $x$ decreases without bound, $f(x)$ increases without bound, and as $x$ increases without bound, $f(x)$ increases without bound.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The end behavior of a polynomial is set by its leading term. Multiplying the leading terms of the factors yields (-x)(x^2)(x) = -x^4, so f is a degree-4 polynomial with a negative leading coefficient. An even-degree polynomial has the same end behavior on both sides, and a negative leading coefficient makes both ends go down. Therefore, as x decreases without bound, f(x) decreases without bound, and as x increases without bound, f(x) decreases without bound. Distractors: the choice with f(x) decreasing on the left and increasing on the right describes an odd-degree polynomial with a positive leading coefficient, such as (x + 1)^2 (x - 5) alone; the choice with f(x) increasing on the left and decreasing on the right describes an odd-degree polynomial with a negative leading coefficient, as if the squared factor contributed only one power of x; the choice with f(x) increasing without bound on both sides ignores the negative sign hidden in the factor 2 - x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(2-x)(x+1)^2(x-5)</code>

Zoom out (T1) until the three x-intercepts are small on screen: both arms of the graph point downward, so f(x) decreases without bound in both directions. Near the intercepts the graph bounces at x = -1 and crosses at x = 2 and x = 5, but the question is only about the far left and far right.

</details>

---

### 114. adv-shift-from-table

*Hard · Multiple choice · route: desmos-primary · techniques: T5, T9*

For the quadratic function $f$, $f(-1) = 8$, $f(0) = 3$, $f(2) = 5$, and $f(3) = 12$. The function $g$ is defined by $g(x) = f(x + 4)$. What is the $y$-coordinate of the $y$-intercept of the graph of $y = g(x)$ in the $xy$-plane?

- **A.** $3$
- **B.** $7$
- **C.** $23$
- **D.** $47$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Write f(x) = ax^2 + bx + c. f(0) = 3 gives c = 3. f(-1) = 8 gives a - b = 5, and f(2) = 5 gives 4a + 2b = 2. Substituting b = a - 5 into the second: 6a - 10 = 2, so a = 2 and b = -3. (Check f(3) = 18 - 9 + 3 = 12.) The y-intercept of g is g(0) = f(4) = 32 - 12 + 3 = 23. Distractors: 47 is f(-4), shifting the wrong way; 7 adds 4 to f(0) instead of to the input; 3 is f(0), ignoring the shift.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[-1,0,2,3]</code><br><code>y_1=[8,3,5,12]</code><br><code>y_1\sim ax_1^2+bx_1+c</code><br><code>f(x)=ax^2+bx+c</code><br><code>g(x)=f(x+4)</code><br><code>g(0)</code>

The regression gives a = 2, b = -3, c = 3 (define f from the table by regression, then shift: the proposed T15 move). g(0) shows 23.

</details>

---

### 115. adv-table-shift-minimum-value

*Hard · Multiple choice · route: desmos-primary · techniques: T5, T9*

For the quadratic function $f$, $f(0) = 5$, $f(1) = 0$, and $f(2) = -3$. If $g(x) = f(x - 2) + 3$ for all $x$, what is the minimum value of $g$?

- **A.** $-4$
- **B.** $-1$
- **C.** $1$
- **D.** $5$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Let f(x) = ax^2 + bx + c. From f(0) = 5, c = 5. From f(1) = 0, a + b = -5, and from f(2) = -3, 4a + 2b = -8, so 2a + b = -4. Subtracting yields a = 1 and b = -6, so f(x) = x^2 - 6x + 5 = (x - 3)^2 - 4, whose minimum value is -4. Replacing x with x - 2 shifts the graph 2 units to the right without changing its minimum value, and adding 3 raises every value by 3. Therefore, the minimum value of g is -4 + 3 = -1. Distractors: -4 is the minimum value of f, ignoring the +3; 5 is the x-coordinate of the vertex of g, 3 + 2, not its minimum value; 1 adds both the horizontal shift 2 and the vertical shift 3 to -4.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2]</code><br><code>y_1=[5,0,-3]</code><br><code>y_1\sim ax_1^2+bx_1+c</code><br><code>f(x)=ax^2+bx+c</code><br><code>g(x)=f(x-2)+3</code><br><code>y=g(x)</code>

The regression gives a = 1, b = -6, c = 5. Defining g from the fitted f (the regression-then-shift move, T15) and graphing y = g(x), click the vertex: (5, -1). The minimum value is the y-coordinate, -1.

</details>

---

### 116. adv-vehicles-percent-per-year

*Hard · Multiple choice · route: hand-primary · techniques: T9*

The number of registered vehicles in a county can be modeled by an exponential function of time. The number increases by 44% every 2 years. By what percent does the number of registered vehicles increase each year?

- **A.** $20\%$
- **B.** $22\%$
- **C.** $44\%$
- **D.** $88\%$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** An increase of 44% every 2 years means the number is multiplied by 1.44 every 2 years. If the yearly growth factor is r, then r^2 = 1.44, so r = 1.2 (the positive root). A factor of 1.2 is an increase of 20% each year. Distractors: 22% halves the 2-year percent, but percent changes compound rather than add; 44% is the 2-year increase; 88% doubles the 2-year increase.

**Desmos** (not yet verified in Desmos). Type:<br><code>N(t)=1.44^{t/2}</code><br><code>N(1)</code>

N(1) shows 1.2: each year the number is multiplied by 1.2, an increase of 20%. The hand method is one square root, so Desmos only confirms it.

</details>

---

### 117. adv-vertex-evaluate

*Hard · Multiple choice · route: hand-primary · techniques: T9*

The function $f$ is defined by $f(x) = 2x^2 + bx + c$, where $b$ and $c$ are constants. The minimum value of $f$ is $-5$, and it occurs at $x = 3$. What is the value of $f(-1)$?

- **A.** $-3$
- **B.** $13$
- **C.** $27$
- **D.** $37$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Vertex (3, -5) with leading coefficient 2 gives f(x) = 2(x - 3)^2 - 5. Then f(-1) = 2(16) - 5 = 27. Distractors: 13 is c = f(0), 37 adds 5 instead of subtracting, -3 ignores the horizontal shift (2(-1)^2 - 5).

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=2(x-3)^2-5</code><br><code>f(-1)</code>

Once the vertex form is written, f(-1) shows 27. Desmos only does the arithmetic here.

</details>

---
