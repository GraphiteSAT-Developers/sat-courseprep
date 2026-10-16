# Equivalent expressions

[← Question bank index](README.md) · Advanced Math · 100 questions, easiest first

### 1. adv-common-factor-xy

*Easy · Multiple choice · route: hand-primary · techniques: —*

Which expression is equivalent to $12x^3y - 18x^2y^2$?

- **A.** $6xy(2x - 3y)$
- **B.** $6x^2y(2x + 3y)$
- **C.** $6x^2y^2(2x - 3)$
- **D.** $6x^2y(2x - 3y)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The greatest common factor of 12x^3y and 18x^2y^2 is 6x^2y. Factoring it out yields 6x^2y(2x - 3y), since 6x^2y · 2x = 12x^3y and 6x^2y · 3y = 18x^2y^2. Desmos cannot factor an expression; a graph of each choice in one variable would need y fixed first, so the hand method is the one to use. Distractors: 6xy(2x - 3y) leaves out one factor of x, so it expands to 12x^2y - 18xy^2; 6x^2y(2x + 3y) has the wrong sign on the second term; 6x^2y^2(2x - 3) takes y^2 as a common factor although the first term has only one factor of y.

</details>

---

### 2. adv-cube-root-power

*Easy · Multiple choice · route: hand-primary · techniques: T13*

For $x > 0$, which expression is equivalent to $\left(27x^6\right)^{1/3}$?

- **A.** $3x^2$
- **B.** $3x^3$
- **C.** $9x^2$
- **D.** $9x^3$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A power of a product is the product of the powers, so (27x^6)^{1/3} = 27^{1/3} · (x^6)^{1/3}. Since 3^3 = 27, 27^{1/3} = 3, and (x^6)^{1/3} = x^{6 · 1/3} = x^2. Therefore, the expression is equivalent to 3x^2. Distractors: 3x^3 subtracts 3 from the exponent 6 instead of multiplying by 1/3; 9x^2 divides 27 by 3 instead of taking its cube root; 9x^3 makes both of those errors.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(27x^6)^{1/3}</code><br><code>y=3x^2</code>

The two graphs coincide for every x > 0; toggling the second line off and on shows no change. Typing all four choices (T13) is slower than the two-line hand computation, so use Desmos only to confirm.

</details>

---

### 3. adv-difference-of-squares-factor

*Easy · Multiple choice · route: hand-primary · techniques: —*

Which expression is equivalent to $49x^2 - 36y^2$?

- **A.** $(7x - 6y)^2$
- **B.** $(7x - 6y)(7x + 6y)$
- **C.** $(7x + 6y)^2$
- **D.** $(49x - 36y)(x + y)$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The expression is a difference of two squares: 49x^2 = (7x)^2 and 36y^2 = (6y)^2, and a^2 - b^2 = (a - b)(a + b). Therefore, 49x^2 - 36y^2 = (7x - 6y)(7x + 6y). Distractors: (7x - 6y)^2 expands to 49x^2 - 84xy + 36y^2 and (7x + 6y)^2 to 49x^2 + 84xy + 36y^2, each with an extra middle term and the wrong sign on 36y^2; (49x - 36y)(x + y) keeps the original coefficients instead of their square roots and expands to 49x^2 + 13xy - 36y^2.

</details>

---

### 4. adv-ee3-difference-squares-fraction-coefficient

*Easy · Multiple choice · route: hand-primary · techniques: T13*

Which expression is equivalent to $\frac{x^2}{4} - 25$?

- **A.** $\left(\frac{x}{2} - 5\right)^2$
- **B.** $\left(\frac{x}{4} - 5\right)\left(\frac{x}{4} + 5\right)$
- **C.** $\left(\frac{x}{2} - 25\right)\left(\frac{x}{2} + 25\right)$
- **D.** $\left(\frac{x}{2} - 5\right)\left(\frac{x}{2} + 5\right)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The expression is a difference of two squares: x^2/4 = (x/2)^2 and 25 = 5^2. Since a^2 - b^2 = (a - b)(a + b), it follows that x^2/4 - 25 = (x/2 - 5)(x/2 + 5). Therefore, the key is (x/2 - 5)(x/2 + 5). Distractors: (x/2 - 5)^2 squares a difference, which yields x^2/4 - 5x + 25, not a difference of squares; (x/4 - 5)(x/4 + 5) uses 4 instead of its square root 2, which yields x^2/16 - 25; (x/2 - 25)(x/2 + 25) uses 25 instead of its square root 5, which yields x^2/4 - 625.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^2}{4}-25</code><br><code>y=\left(\frac{x}{2}-5\right)\left(\frac{x}{2}+5\right)</code>

Graph the given expression and each choice (T13); only (x/2 - 5)(x/2 + 5) coincides with it everywhere. Recognizing the difference of squares by hand is faster, so use the graphs only as a check.

</details>

---

### 5. adv-ee3-divide-trinomial-by-monomial

*Easy · Multiple choice · route: either · techniques: T13*

For $x \neq 0$, which expression is equivalent to $\frac{6x^3 + 9x^2 - 3x}{3x}$?

- **A.** $2x^2 + 3x$
- **B.** $2x^2 + 3x - 1$
- **C.** $2x^3 + 3x^2 - x$
- **D.** $6x^2 + 9x - 3$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Dividing each term of the numerator by 3x yields 6x^3/(3x) = 2x^2, 9x^2/(3x) = 3x and -3x/(3x) = -1. Therefore, the expression is equivalent to 2x^2 + 3x - 1. Distractors: 2x^2 + 3x treats -3x/(3x) as 0 instead of -1; 2x^3 + 3x^2 - x divides the coefficients by 3 but leaves the powers of x unchanged; 6x^2 + 9x - 3 divides each term by x but not by 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{6x^3+9x^2-3x}{3x}</code><br><code>y=2x^2+3x-1</code>

Graph the given expression and then each choice in turn (T13). Only 2x^2 + 3x - 1 lies on top of the given graph; the given graph has a hole at x = 0, which the stem excludes. Dividing each term by hand is about as fast.

</details>

---

### 6. adv-ee3-gcf-identify-two-variable

*Easy · Multiple choice · route: hand-primary · techniques: —*

Which expression is the greatest common factor of the two terms of $18x^5y^2 - 24x^3y^4$?

- **A.** $3x^3y^2$
- **B.** $6x^2y^2$
- **C.** $6x^3y^2$
- **D.** $6x^5y^4$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The greatest common factor of the coefficients 18 and 24 is 6. For each variable, the common factor uses the smaller exponent that appears: x^5 and x^3 share x^3, and y^2 and y^4 share y^2. Therefore, the greatest common factor is 6x^3y^2, and 18x^5y^2 - 24x^3y^4 = 6x^3y^2(3x^2 - 4y^2). Distractors: 3x^3y^2 uses a common factor of 18 and 24 that is not the greatest; 6x^2y^2 subtracts the exponents of x (5 - 3 = 2) instead of taking the smaller one; 6x^5y^4 takes the larger exponent of each variable, which does not divide either term.

</details>

---

### 7. adv-ee3-store-shelves-cans-total

*Easy · Multiple choice · route: either · techniques: T13*

A store displays cans of soup on $(x + 3)$ shelves, with $(2x - 1)$ cans on each shelf. Another 5 cans are kept in a back room. Which expression represents the total number of cans?

- **A.** $2x^2 + 5x + 2$
- **B.** $2x^2 + 5x - 3$
- **C.** $2x^2 + 7x + 2$
- **D.** $2x^2 + 2$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The cans on the shelves number (x + 3)(2x - 1), the number of shelves times the cans per shelf. Expanding yields 2x^2 - x + 6x - 3 = 2x^2 + 5x - 3. Adding the 5 cans in the back room yields 2x^2 + 5x + 2. Therefore, the total number of cans is 2x^2 + 5x + 2. Distractors: 2x^2 + 5x - 3 counts only the cans on the shelves and leaves out the 5 in the back room; 2x^2 + 7x + 2 adds 6x and x instead of 6x and -x; 2x^2 + 2 multiplies only the first terms and the last terms and drops the middle terms.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x+3)(2x-1)+5</code><br><code>y=2x^2+5x+2</code>

Graph the total, (x + 3)(2x - 1) + 5, and then each choice (T13). Only 2x^2 + 5x + 2 coincides with it. Expanding by hand is about as fast.

</details>

---

### 8. adv-ee3-trinomial-two-variable-factor

*Easy · Multiple choice · route: hand-primary · techniques: T13*

Which expression is equivalent to $x^2 - 3xy - 28y^2$?

- **A.** $(x - 14y)(x + 2y)$
- **B.** $(x - 7y)(x + 4y)$
- **C.** $(x - 4y)(x + 7y)$
- **D.** $(x - 28y)(x + y)$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The trinomial factors as (x + my)(x + ny), where mn = -28 and m + n = -3. The pair -7 and 4 has a product of -28 and a sum of -3. Therefore, x^2 - 3xy - 28y^2 = (x - 7y)(x + 4y). Expanding confirms it: x^2 + 4xy - 7xy - 28y^2. Distractors: (x - 14y)(x + 2y) has the right product of constants, -28, but a sum of -12; (x - 4y)(x + 7y) swaps the signs and has a middle term of +3xy; (x - 28y)(x + y) also has product -28 but a middle term of -27xy.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-6x-112</code><br><code>y=(x-14)(x+8)</code>

Desmos is slower here because the expression has two variables. One check (T13): replace y with 2 by hand, so the given expression becomes x^2 - 6x - 112, then graph it beside each choice with y = 2 substituted; only (x - 7y)(x + 4y), which becomes (x - 14)(x + 8), coincides with it. Factoring by hand takes a few seconds.

</details>

---

### 9. adv-expand-monomial-two-binomials

*Easy · Multiple choice · route: either · techniques: T13*

Which expression is equivalent to $2x(x + 3)(x - 4)$?

- **A.** $2x^2 - 2x - 24$
- **B.** $2x^3 - 2x^2 - 24x$
- **C.** $2x^3 - 2x^2 - 12x$
- **D.** $2x^3 + 2x^2 - 24x$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Multiplying the two binomials first yields (x + 3)(x - 4) = x^2 - 4x + 3x - 12 = x^2 - x - 12. Multiplying each term by 2x yields 2x(x^2 - x - 12) = 2x^3 - 2x^2 - 24x. Therefore, the given expression is equivalent to 2x^3 - 2x^2 - 24x. Distractors: 2x^2 - 2x - 24 multiplies by 2 instead of 2x; 2x^3 - 2x^2 - 12x multiplies the constant -12 by x instead of by 2x; 2x^3 + 2x^2 - 24x comes from a sign error in the middle term, taking (x + 3)(x - 4) as x^2 + x - 12.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x(x+3)(x-4)</code><br><code>y=2x^3-2x^2-24x</code>

Type the given expression and then each choice as y = ... (T13). Only the graph of 2x^3 - 2x^2 - 24x lies exactly on top of the first graph; zoom out to confirm the end behavior matches too.

</details>

---

### 10. adv-exponential-shift-coefficient

*Easy · Multiple choice · route: hand-primary · techniques: T13*

Which expression is equivalent to $5 \cdot 3^{x + 2}$?

- **A.** $10 \cdot 3^x$
- **B.** $15 \cdot 3^x$
- **C.** $45 \cdot 3^x$
- **D.** $15^{x + 2}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** By the product rule for exponents, 3^(x + 2) = 3^x \* 3^2 = 9 \* 3^x. Substituting yields 5 \* 3^(x + 2) = 5 \* 9 \* 3^x = 45 \* 3^x. Therefore, the given expression is equivalent to 45 \* 3^x. Distractors: 10·3^x multiplies 5 by the exponent 2 instead of by 3^2; 15·3^x multiplies 5 by 3 instead of by 3^2 = 9; 15^(x + 2) multiplies the coefficient 5 into the base, but 5 \* 3^(x + 2) is not (5 \* 3)^(x + 2).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=5\cdot3^{x+2}</code><br><code>y=45\cdot3^x</code>

By hand this is one step, so Desmos is slower. As a check (T13), graph the given expression and a choice; the graph of 45 \* 3^x coincides with it, while 15 \* 3^x runs below it.

</details>

---

### 11. adv-floor-tile-area-square-binomial

*Easy · Multiple choice · route: hand-primary · techniques: T13*

A square floor tile has a side length of $(x + 4)$ inches. Which expression represents the area, in square inches, of the tile?

- **A.** $4x + 16$
- **B.** $x^2 + 16$
- **C.** $x^2 + 4x + 16$
- **D.** $x^2 + 8x + 16$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The area of a square is the side length squared, so the area is (x + 4)^2 = (x + 4)(x + 4). Expanding yields x^2 + 4x + 4x + 16 = x^2 + 8x + 16. Therefore, the area, in square inches, is x^2 + 8x + 16. Distractors: 4x + 16 is the perimeter, 4(x + 4); x^2 + 16 squares each term and leaves out the middle term; x^2 + 4x + 16 includes only one of the two middle products.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x+4)^2</code><br><code>y=x^2+8x+16</code>

By hand this is one expansion, so Desmos is slower. As a check (T13), graph (x + 4)^2 and a choice; only x^2 + 8x + 16 coincides with it.

</details>

---

### 12. adv-gcf-monomial-three-terms

*Easy · Multiple choice · route: hand-primary · techniques: T13*

Which expression is equivalent to $15x^4 - 10x^3 + 5x^2$?

- **A.** $5x^2(3x^2 - 2x)$
- **B.** $5x^2(3x^2 - 2x + 1)$
- **C.** $5x^2(3x^2 - 2x + 5)$
- **D.** $5x^2(3x^2 + 2x + 1)$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Each term has a factor of 5 and a factor of x^2, so the greatest common factor is 5x^2. Dividing each term by 5x^2 yields 15x^4/(5x^2) = 3x^2, -10x^3/(5x^2) = -2x, and 5x^2/(5x^2) = 1. Therefore, the expression is equivalent to 5x^2(3x^2 - 2x + 1). Distractors: 5x^2(3x^2 - 2x) drops the last term, treating 5x^2 divided by itself as 0 instead of 1; 5x^2(3x^2 - 2x + 5) divides 5x^2 by x^2 only and keeps the 5; 5x^2(3x^2 + 2x + 1) loses the negative sign of the middle term.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=15x^4-10x^3+5x^2</code><br><code>y=5x^2(3x^2-2x+1)</code>

The two graphs coincide; toggling the second line off and on shows no change. Factoring out 5x^2 by hand is faster, so use Desmos only to check the chosen factorization (T13).

</details>

---

### 13. adv-mural-area-product

*Easy · Multiple choice · route: either · techniques: T13*

A rectangular mural has a length of $(2x + 3)$ meters and a width of $(x + 5)$ meters. Which expression represents the area, in square meters, of the mural?

- **A.** $2x^2 + 15$
- **B.** $2x^2 + 8x + 15$
- **C.** $2x^2 + 13x + 15$
- **D.** $2x^2 + 13x + 8$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The area of a rectangle is length times width, so the area is (2x + 3)(x + 5). Distributing yields 2x · x + 2x · 5 + 3 · x + 3 · 5 = 2x^2 + 10x + 3x + 15 = 2x^2 + 13x + 15. Therefore, the area, in square meters, is 2x^2 + 13x + 15. Distractors: 2x^2 + 15 multiplies only the first terms and the last terms; 2x^2 + 8x + 15 multiplies 5 by x instead of by 2x; 2x^2 + 13x + 8 adds the constants 3 and 5 instead of multiplying them.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(2x+3)(x+5)</code><br><code>y=2x^2+13x+15</code>

Type the product and each choice (T13); only y = 2x^2 + 13x + 15 lies on top of the product. Distributing by hand is about as fast.

</details>

---

### 14. adv-negative-exponents-product-two-variable

*Easy · Multiple choice · route: hand-primary · techniques: —*

Which expression is equivalent to $x^{-3}y^{2} \cdot x^{5}y^{-4}$, where $x$ and $y$ are nonzero?

- **A.** $\frac{x^2}{y^2}$
- **B.** $x^2y^2$
- **C.** $\frac{y^2}{x^2}$
- **D.** $\frac{x^8}{y^6}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** When powers of the same base are multiplied, the exponents are added. For x, the exponents give -3 + 5 = 2, and for y, they give 2 + (-4) = -2. It follows that the product is x^2 y^(-2), and since y^(-2) = 1/y^2, the product is x^2/y^2. Therefore, the given expression is equivalent to x^2/y^2. Distractors: x^2y^2 drops the negative sign on the y exponent; (y^2)/(x^2) reverses the signs of both exponent sums; (x^8)/(y^6) subtracts the exponents, as for a quotient, instead of adding them.

</details>

---

### 15. adv-poly-add-two-variable

*Easy · Multiple choice · route: hand-primary · techniques: —*

Which expression is equivalent to $(4x^2 - 3xy + y^2) + (-x^2 + 5xy - 6y^2)$?

- **A.** $3x^2 - 8xy - 5y^2$
- **B.** $3x^2 + 2xy + 7y^2$
- **C.** $5x^2 + 2xy - 5y^2$
- **D.** $3x^2 + 2xy - 5y^2$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Adding the polynomials means combining like terms. The x^2 terms give 4x^2 + (-x^2) = 3x^2, the xy terms give -3xy + 5xy = 2xy, and the y^2 terms give y^2 + (-6y^2) = -5y^2. Therefore, the sum is 3x^2 + 2xy - 5y^2. Distractors: 3x^2 - 8xy - 5y^2 subtracts 5xy from -3xy instead of adding; 3x^2 + 2xy + 7y^2 adds 6y^2 instead of -6y^2; 5x^2 + 2xy - 5y^2 adds x^2 instead of -x^2.

</details>

---

### 16. adv-poly-multiply-binomial-trinomial

*Easy · Multiple choice · route: either · techniques: T13*

Which expression is equivalent to $(2x - 5)(x^2 + 3x - 1)$?

- **A.** $2x^3 + x^2 - 13x + 5$
- **B.** $2x^3 + 6x^2 - 17x + 5$
- **C.** $2x^3 + x^2 - 17x + 5$
- **D.** $2x^3 + 11x^2 + 13x - 5$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Distributing each term of 2x - 5 over x^2 + 3x - 1 yields 2x(x^2 + 3x - 1) - 5(x^2 + 3x - 1) = 2x^3 + 6x^2 - 2x - 5x^2 - 15x + 5. Combining like terms yields 2x^3 + (6 - 5)x^2 + (-2 - 15)x + 5 = 2x^3 + x^2 - 17x + 5. Distractors: 2x^3 + x^2 - 13x + 5 combines -2x and -15x as -13x instead of -17x; 2x^3 + 6x^2 - 17x + 5 omits the -5x^2 term that comes from -5 times x^2; 2x^3 + 11x^2 + 13x - 5 distributes 5 instead of -5 over the trinomial.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(2x-5)(x^2+3x-1)</code><br><code>y=2x^3+x^2-17x+5</code>

Graph the product and each choice (T13); only y = 2x^3 + x^2 - 17x + 5 coincides with the first graph everywhere. The other three choices cross it at a few points but separate elsewhere; zoom out to see the separation.

</details>

---

### 17. adv-poly-subtract-fluency

*Easy · Multiple choice · route: either · techniques: T13*

Which expression is equivalent to $(3x^2 - 5x + 4) - (x^2 + 2x - 9)$?

- **A.** $2x^2 - 7x - 5$
- **B.** $2x^2 - 3x - 5$
- **C.** $2x^2 - 7x + 13$
- **D.** $4x^2 - 3x - 5$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Distribute the minus sign: 3x^2 - 5x + 4 - x^2 - 2x + 9. Combining like terms yields (3 - 1)x^2 + (-5 - 2)x + (4 + 9) = 2x^2 - 7x + 13. Distractors: 2x^2 - 7x - 5 subtracts the x^2 and x terms but not the constant (4 - 9 instead of 4 + 9); 2x^2 - 3x - 5 never distributes the minus sign to the x term or the constant; 4x^2 - 3x - 5 adds the two polynomials instead of subtracting.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(3x^2-5x+4)-(x^2+2x-9)</code><br><code>y=2x^2-7x+13</code>

Graph the original and each choice (T13); only y = 2x^2 - 7x + 13 lies exactly on top of the original. Toggle the other choices on and off to see them separate. Combining like terms by hand is about as fast.

</details>

---

### 18. adv-poly-sum-difference-coefficient-total

*Easy · Student-produced response · route: either · techniques: T9*

When $(3x^2 + 2x - 7) + (x^2 - 6x + 4) - (2x^2 - x - 1)$ is simplified, the result is $ax^2 + bx + c$, where $a$, $b$ and $c$ are constants. What is the value of $a + b + c$?

**Answer:** -3

<details><summary>Solutions</summary>

**By hand.** Combining like terms, with the subtraction applied to every term of the third polynomial, yields x^2 terms 3 + 1 - 2 = 2, x terms 2 - 6 + 1 = -3, and constants -7 + 4 + 1 = -2. It follows that the expression is equivalent to 2x^2 - 3x - 2, so a = 2, b = -3, and c = -2. Therefore, a + b + c = 2 + (-3) + (-2) = -3. Alternate approach: a + b + c is the value of the expression at x = 1, which is (3 + 2 - 7) + (1 - 6 + 4) - (2 - 1 - 1) = -2 - 1 - 0 = -3.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=(3x^2+2x-7)+(x^2-6x+4)-(2x^2-x-1)</code><br><code>f(1)</code>

Define the whole expression as f (T9). Since f(1) = a + b + c, the second line shows -3 directly; enter -3.

</details>

---

### 19. adv-power-of-monomial

*Easy · Multiple choice · route: hand-primary · techniques: T13*

Which expression is equivalent to $(2x^3)^4$?

- **A.** $2x^{12}$
- **B.** $8x^{12}$
- **C.** $16x^{12}$
- **D.** $16x^{7}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A power of a product is the product of the powers: (2x^3)^4 = 2^4 · (x^3)^4. Since 2^4 = 16 and a power of a power multiplies the exponents, (x^3)^4 = x^{3 · 4} = x^{12}. Therefore, the expression is equivalent to 16x^{12}. Distractors: 2x^{12} raises only x^3 to the 4th power and leaves the 2; 8x^{12} multiplies 2 by 4 instead of raising 2 to the 4th power; 16x^{7} adds the exponents 3 and 4 instead of multiplying them.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(2x^3)^4</code><br><code>y=16x^{12}</code>

The two graphs coincide. The exponent rules take a few seconds by hand, so Desmos is only a check here (T13).

</details>

---

### 20. adv-radical-simplify-even-power

*Easy · Multiple choice · route: hand-primary · techniques: T13*

For $x > 0$, which expression is equivalent to $\sqrt{50x^6}$?

- **A.** $5x^3\sqrt{2}$
- **B.** $5x^4\sqrt{2}$
- **C.** $10x^3\sqrt{5}$
- **D.** $25x^3\sqrt{2}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that x > 0. Writing 50 as 25 times 2 and x^6 as (x^3)^2 yields sqrt(50x^6) = sqrt(25 · 2 · (x^3)^2). The square root of a product is the product of the square roots, so this equals 5 · x^3 · sqrt(2). Therefore, the expression is equivalent to 5x^3 sqrt(2). Distractors: 5x^4\sqrt{2} takes the square root of x^6 as x^4 (subtracting 2 from the exponent instead of halving it); 10x^3\sqrt{5} splits 50 as 10 times 5 and takes 10 outside the radical, but 10 is not a perfect square; 25x^3\sqrt{2} takes the perfect-square factor 25 outside without taking its square root.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt{50x^6}</code><br><code>y=5x^3\sqrt{2}</code>

Graph the given expression and each choice for x > 0 (T13); only y = 5x^3 sqrt(2) lies on top of the first graph. Splitting 50 into 25 times 2 by hand takes a few seconds, so Desmos is only a check here.

</details>

---

### 21. adv-rational-exponent-to-radical

*Easy · Multiple choice · route: hand-primary · techniques: T13*

For $x > 0$, which expression is equivalent to $x^{2/5}$?

- **A.** $\sqrt[5]{x^2}$
- **B.** $\sqrt[5]{2x}$
- **C.** $\sqrt{x^5}$
- **D.** $2\sqrt[5]{x}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** For x > 0, x^{m/n} is the nth root of x^m: the denominator of the exponent is the index of the root and the numerator is the power. Here m = 2 and n = 5, so x^{2/5} is the fifth root of x^2, written sqrt[5](x^2). Distractors: the fifth root of 2x multiplies x by 2 instead of squaring it; the square root of x^5 swaps the power and the index, which is x^{5/2}; 2 times the fifth root of x turns the numerator 2 into a coefficient.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^{2/5}</code><br><code>y=\sqrt[5]{x^2}</code>

For x > 0 the two graphs coincide (T13). Reading the exponent as power over root is one step by hand, so Desmos is only a check.

</details>

---

### 22. adv-banner-perimeter-factor

*Medium · Multiple choice · route: either · techniques: T13*

A rectangular banner has an area of $6x^2 + 23x + 20$ square feet. The width of the banner is $2x + 5$ feet. Which expression represents the perimeter, in feet, of the banner?

- **A.** $3x + 4$
- **B.** $5x + 9$
- **C.** $6x + 8$
- **D.** $10x + 18$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The area is the width times the length, so the length is (6x^2 + 23x + 20)/(2x + 5). Factoring yields 6x^2 + 23x + 20 = (2x + 5)(3x + 4), so the length is 3x + 4 feet. The perimeter is 2(3x + 4) + 2(2x + 5) = 6x + 8 + 4x + 10 = 10x + 18. Therefore, the perimeter, in feet, is 10x + 18. Distractors: 3x + 4 is the length, an intermediate result; 5x + 9 adds the length and width once instead of twice; 6x + 8 doubles the length but leaves out the two widths.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=6x^2+23x+20</code><br><code>y=(2x+5)(3x+4)</code>

The two graphs coincide (T13), which confirms that the length is 3x + 4. Then the perimeter is 2(3x + 4) + 2(2x + 5) = 10x + 18; that last step is by hand.

</details>

---

### 23. adv-complete-square-equivalent

*Medium · Multiple choice · route: either · techniques: T13*

Which expression is equivalent to $x^2 - 10x + 7$?

- **A.** $(x - 5)^2 - 25$
- **B.** $(x - 5)^2 - 18$
- **C.** $(x - 5)^2 + 7$
- **D.** $(x + 5)^2 - 18$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Complete the square: half of -10 is -5, and (-5)^2 = 25, so x^2 - 10x + 7 = (x^2 - 10x + 25) - 25 + 7 = (x - 5)^2 - 18. Distractors: (x - 5)^2 + 7 adds 25 inside the square without subtracting it outside; (x - 5)^2 - 25 drops the constant 7; (x + 5)^2 - 18 uses the wrong sign for half the coefficient of x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2-10x+7</code><br><code>y=(x-5)^2-18</code>

Click the vertex of y = x^2 - 10x + 7: (5, -18), so the matching vertex form is (x - 5)^2 - 18. Or graph each choice (T13) and keep the one that coincides with the original.

</details>

---

### 24. adv-complete-square-leading-two-k

*Medium · Student-produced response · route: either · techniques: T6, T11*

The expression $2x^2 + 6x + 5$ is equivalent to $2(x + h)^2 + k$, where $h$ and $k$ are constants. What is the value of $k$?

**Answer:** 1/2 (≈ 0.5)

<details><summary>Solutions</summary>

**By hand.** Factor 2 out of the x-terms: 2x^2 + 6x + 5 = 2(x^2 + 3x) + 5. Half of 3 is 3/2, and (3/2)^2 = 9/4, so 2(x^2 + 3x + 9/4) - 2 · 9/4 + 5 = 2(x + 3/2)^2 - 9/2 + 5 = 2(x + 3/2)^2 + 1/2. Therefore, h = 3/2 and k = 1/2. A common error is subtracting only 9/4 instead of 2 · 9/4, which gives 11/4.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3]</code><br><code>2x_1^2+6x_1+5\sim2(x_1+h)^2+k</code><br><code>k</code>

The tilde regression (T6) returns h = 1.5 and k = 0.5. Enter 1/2 or .5 (T11). As a check, the vertex of y = 2x^2 + 6x + 5 is (-1.5, 0.5).

</details>

---

### 25. adv-complex-fraction-sum-numerator

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

For $x \neq -8$ and $x \neq 0$, which expression is equivalent to $\frac{\frac{2}{x} + \frac{1}{4}}{\frac{x + 8}{2}}$?

- **A.** $\frac{1}{4x}$
- **B.** $\frac{1}{2x}$
- **C.** $\frac{x + 2}{2x(x + 8)}$
- **D.** $\frac{(x + 8)^2}{8x}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Writing the numerator over the common denominator 4x yields 2/x + 1/4 = 8/(4x) + x/(4x) = (x + 8)/(4x). Dividing by (x + 8)/2 is multiplying by 2/(x + 8): ((x + 8)/(4x)) \* (2/(x + 8)) = 2/(4x) = 1/(2x), since x + 8 is not 0. Therefore, the expression is equivalent to 1/(2x). Distractors: (1)/(4x) divides by x + 8 but ignores the 2 in the main denominator; (x + 2)/(2x(x + 8)) rewrites 2/x as 2/(4x) without multiplying the numerator by 4; ((x + 8)^2)/(8x) multiplies by (x + 8)/2 instead of dividing by it.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{\frac{2}{x}+\frac{1}{4}}{\frac{x+8}{2}}</code><br><code>y=\frac{1}{2x}</code>

Type the complex fraction with the fraction template (typing / inside a fraction nests it), then graph each choice (T13). Only 1/(2x) lies on the first graph; the hole at x = -8 does not show at normal zoom.

</details>

---

### 26. adv-cubic-product-coefficient-c

*Medium · Student-produced response · route: either · techniques: T6*

The expression $(3x - 4)(x^2 + 2x - 5)$ is equivalent to $ax^3 + bx^2 + cx + d$, where $a$, $b$, $c$, and $d$ are constants. What is the value of $c$?

**Answer:** -23

<details><summary>Solutions</summary>

**By hand.** The x-term of the product comes from two products: 3x times -5 and -4 times 2x. These yield -15x and -8x, so cx = -23x. Therefore, c = -23. Expanding fully confirms it: 3x^3 + 6x^2 - 15x - 4x^2 - 8x + 20 = 3x^3 + 2x^2 - 23x + 20.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4,5]</code><br><code>(3x_1-4)(x_1^2+2x_1-5)\sim ax_1^3+bx_1^2+cx_1+d</code>

The tilde regression (T6) returns a = 3, b = 2, c = -23 and d = 20. Read c = -23. By hand, only the two products that make an x-term are needed, which is about as fast.

</details>

---

### 27. adv-difference-of-binomial-squares-factor

*Medium · Multiple choice · route: either · techniques: T13*

Which expression is equivalent to $(2x + 3)^2 - (x - 1)^2$?

- **A.** $(x + 2)(3x + 2)$
- **B.** $(x + 2)(3x + 4)$
- **C.** $(x + 4)(3x + 2)$
- **D.** $(x + 4)(3x + 4)$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The expression has the form A^2 - B^2 = (A - B)(A + B), with A = 2x + 3 and B = x - 1. Then A - B = 2x + 3 - x + 1 = x + 4, and A + B = 2x + 3 + x - 1 = 3x + 2. Therefore, the expression is equivalent to (x + 4)(3x + 2). Alternate approach: expanding yields 4x^2 + 12x + 9 - (x^2 - 2x + 1) = 3x^2 + 14x + 8, which factors as (x + 4)(3x + 2). Distractors: (x + 2)(3x + 2) subtracts only the x in x - 1, computing A - B as x + 2; (x + 2)(3x + 4) uses x + 1 in place of x - 1; (x + 4)(3x + 4) gets the difference right but adds +1 instead of -1 in the sum.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(2x+3)^2-(x-1)^2</code><br><code>y=(x+4)(3x+2)</code>

Graph the given expression and each choice (T13). Only (x + 4)(3x + 2) gives the same parabola; the others have different x-intercepts.

</details>

---

### 28. adv-difference-squares-quartic-ab

*Medium · Student-produced response · route: either · techniques: T6, T13*

The expression $16x^4 - 81$ is equivalent to $(ax^2 + 9)(bx + 3)(bx - 3)$, where $a$ and $b$ are positive constants. What is the value of $ab$?

**Answer:** 8

<details><summary>Solutions</summary>

**By hand.** The expression 16x^4 - 81 is a difference of squares, (4x^2)^2 - 9^2 = (4x^2 + 9)(4x^2 - 9). The second factor is again a difference of squares, (2x)^2 - 3^2 = (2x + 3)(2x - 3). Therefore, 16x^4 - 81 = (4x^2 + 9)(2x + 3)(2x - 3), so a = 4, b = 2, and ab = 8. Expanding (bx + 3)(bx - 3) = b^2 x^2 - 9 also shows that b^2 = 4, and the restriction b > 0 selects b = 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4,5]</code><br><code>16x_1^4-81\sim(ax_1^2+9)(bx_1+3)(bx_1-3)</code>

The tilde regression (T6) returns a = 4 and b = 2 or b = -2 (the product (bx + 3)(bx - 3) is the same for b and -b). The stem says b is positive, so b = 2 and ab = 8. As a check (T13), graph y = 16x^4 - 81 and y = (4x^2 + 9)(2x + 3)(2x - 3): they coincide.

</details>

---

### 29. adv-ee3-absolute-value-two-terms-negative

*Medium · Multiple choice · route: desmos-primary · techniques: T9, T13*

For $x < -2$, which expression is equivalent to $|x - 3| - |x + 2| + x$?

- **A.** $-x + 1$
- **B.** $x - 5$
- **C.** $x + 5$
- **D.** $3x - 1$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** For x < -2, both x - 3 and x + 2 are negative. So |x - 3| = -(x - 3) = 3 - x and |x + 2| = -(x + 2) = -x - 2. Substituting yields (3 - x) - (-x - 2) + x = 3 - x + x + 2 + x = x + 5. Therefore, the expression is equivalent to x + 5. Distractors: x - 5 drops both absolute value bars; -x + 1 rewrites only |x - 3| as 3 - x and keeps |x + 2| as x + 2; 3x - 1 rewrites only |x + 2| as -x - 2 and keeps |x - 3| as x - 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=\left|x-3\right|-\left|x+2\right|+x</code><br><code>f(-4)</code><br><code>f(-10)</code>

Desmos shows f(-4) = 1 and f(-10) = -5 (T9); both inputs satisfy x < -2. Substitute the same inputs into each choice (T13): only x + 5 gives 1 and -5. Graphing y = f(x) also shows a straight line with slope 1 through (-5, 0) to the left of x = -2.

</details>

---

### 30. adv-ee3-cube-of-sum-k

*Medium · Multiple choice · route: either · techniques: T6*

For all values of $x$, $(x + 2)^3 - (x^3 + 8) = kx(x + 2)$, where $k$ is a constant. What is the value of $k$?

- **A.** $0$
- **B.** $2$
- **C.** $3$
- **D.** $6$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The cube of a sum is not the sum of the cubes. Expanding yields (x + 2)^3 = (x + 2)(x^2 + 4x + 4) = x^3 + 6x^2 + 12x + 8. Subtracting x^3 + 8 yields 6x^2 + 12x = 6x(x + 2). Therefore, k = 6. Alternate approach: substituting x = 1 yields 27 - 9 = 18 on the left and 3k on the right, so k = 6. Distractors: 0 treats (x + 2)^3 as x^3 + 8, so the difference is 0; 2 squares x + 2 as x^2 + 4, which yields (x + 2)^3 = x^3 + 2x^2 + 4x + 8; 3 takes the coefficient 3 from the pattern a^3 + 3a^2b + 3ab^2 + b^3 without the powers of 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3]</code><br><code>(x_1+2)^3-(x_1^3+8)\sim kx_1(x_1+2)</code>

The tilde regression (T6) returns k = 6. Substituting x = 1 by hand gives 27 - 9 = 18 = 3k, which is just as fast.

</details>

---

### 31. adv-ee3-factored-form-zero-p

*Medium · Student-produced response · route: either · techniques: T6, T11*

The expression $3x^2 + 4x - 15$ is equivalent to $3(x - p)(x - q)$, where $p$ and $q$ are constants and $p > q$. What is the value of $p$?

**Answer:** 5/3 (≈ 1.667)

<details><summary>Solutions</summary>

**By hand.** Factoring 3x^2 + 4x - 15: the product 3(-15) = -45 has the factor pair 9 and -5 with sum 4, so 3x^2 + 9x - 5x - 15 = 3x(x + 3) - 5(x + 3) = (3x - 5)(x + 3). Factoring 3 out of 3x - 5 yields 3(x - 5/3)(x + 3) = 3(x - 5/3)(x - (-3)). So the constants are 5/3 and -3, and since p > q, p = 5/3. Therefore, the value of p is 5/3.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3,4]</code><br><code>3x_1^2+4x_1-15\sim3(x_1-p)(x_1-q)</code>

The tilde regression (T6) returns p and q; they may come back in either order, so take the larger one, 1.66667, as p (the other is -3). Use the fraction toggle (T11) to read 5/3 and enter 5/3 (or 1.666 or 1.667), not 1.67.

</details>

---

### 32. adv-ee3-gcf-variable-exponent-n

*Medium · Multiple choice · route: hand-primary · techniques: —*

Which expression is equivalent to $x^{n + 4} - 9x^{n + 2}$, where $n$ is a positive integer?

- **A.** $x^{n + 2}(x - 3)(x + 3)$
- **B.** $x^{n + 2}(x - 3)^2$
- **C.** $x^{n + 2}(x^2 - 9x)$
- **D.** $x^{2}(x^{n} - 3)(x^{n} + 3)$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Both terms share the factor x^(n + 2), the power with the smaller exponent. Since x^(n + 4) = x^(n + 2) · x^2, factoring yields x^(n + 2)(x^2 - 9). The factor x^2 - 9 is a difference of squares, (x - 3)(x + 3). Therefore, the expression is equivalent to x^(n + 2)(x - 3)(x + 3). Distractors: x^(n + 2)(x - 3)^2 factors x^2 - 9 as a perfect square, which yields x^2 - 6x + 9; x^(n + 2)(x^2 - 9x) leaves an extra factor of x in the second term, which yields x^(n + 4) - 9x^(n + 3); x^(2)(x^(n) - 3)(x^(n) + 3) multiplies out to x^(2n + 2) - 9x^2, which moves n into the wrong exponents.

</details>

---

### 33. adv-ee3-negative-rational-exponent-radical

*Medium · Multiple choice · route: hand-primary · techniques: T9*

Which expression is equivalent to $x^{-\frac{3}{2}}$ for all positive values of $x$?

- **A.** $\frac{1}{x \sqrt{x}}$
- **B.** $\frac{1}{\sqrt[3]{x^2}}$
- **C.** $\frac{\sqrt{x}}{x}$
- **D.** $-x \sqrt{x}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A negative exponent means a reciprocal, so x^(-3/2) = 1/x^(3/2). Since 3/2 = 1 + 1/2, x^(3/2) = x · x^(1/2) = x sqrt(x). Therefore, x^(-3/2) = 1/(x sqrt(x)). Distractors: 1/cbrt(x^2) inverts the fraction in the exponent, giving x^(-2/3); sqrt(x)/x equals x^(-1/2), which splits -3/2 as -1 + 1/2 instead of -1 - 1/2; -x sqrt(x) treats the negative exponent as a negative sign in front of x^(3/2).

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=x^{-\frac{3}{2}}</code><br><code>f(4)</code><br><code>g(x)=\frac{1}{x\sqrt{x}}</code><br><code>g(4)</code>

Desmos is slower than the exponent rules here. As a check (T9), define f and read f(4) = 0.125, then evaluate each choice at x = 4 (g(4) = 0.125 for the first choice): 1/(4·2) = 0.125, 1/cbrt(16) ≈ 0.397, 2/4 = 0.5 and -8. Only 1/(x sqrt(x)) matches.

</details>

---

### 34. adv-ee3-not-equivalent-product-forms

*Medium · Multiple choice · route: either · techniques: T13*

Which of the following is NOT equivalent to $(x - 4)(x + 6)$?

- **A.** $x^2 + 2x - 24$
- **B.** $(x + 1)^2 - 25$
- **C.** $(x - 1)^2 - 25$
- **D.** $(4 - x)(-6 - x)$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Expanding the given product yields x^2 + 6x - 4x - 24 = x^2 + 2x - 24. Check each choice against x^2 + 2x - 24. Expanding (x + 1)^2 - 25 yields x^2 + 2x + 1 - 25 = x^2 + 2x - 24. Factoring -1 out of each factor of (4 - x)(-6 - x) yields (-1)(x - 4)(-1)(x + 6) = (x - 4)(x + 6). But (x - 1)^2 - 25 = x^2 - 2x - 24, which has the wrong sign on the x-term. Therefore, (x - 1)^2 - 25 is not equivalent. Distractors: x^2 + 2x - 24 is the expanded product itself; (x + 1)^2 - 25 is the completed-square form, which only looks different; (4 - x)(-6 - x) negates both factors, and the two factors of -1 multiply to 1, so it is equivalent even though each factor changed sign.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x-4)(x+6)</code><br><code>y=(x-1)^2-25</code>

Graph the given product and then each choice (T13). Three choices coincide with it; (x - 1)^2 - 25 is a parabola shifted 2 units to the right, so it is the expression that is not equivalent.

</details>

---

### 35. adv-ee3-solar-panels-area-difference

*Medium · Multiple choice · route: either · techniques: T13*

A square solar panel has a side length of $(x + 3)$ meters, and a smaller square panel has a side length of $(x - 3)$ meters, where $x > 3$. Which expression represents the difference, in square meters, between the areas of the two panels?

- **A.** $6x$
- **B.** $12x$
- **C.** $12x + 18$
- **D.** $2x^2 + 18$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The areas are (x + 3)^2 and (x - 3)^2 square meters. A squared binomial has a middle term: (x + 3)^2 = x^2 + 6x + 9 and (x - 3)^2 = x^2 - 6x + 9. Subtracting yields (x^2 + 6x + 9) - (x^2 - 6x + 9) = 12x. Therefore, the difference is 12x square meters. Distractors: 6x expands (x - 3)^2 as x^2 + 9 without its middle term; 12x + 18 expands (x - 3)^2 as x^2 - 6x - 9; 2x^2 + 18 adds the two areas instead of subtracting them.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x+3)^2-(x-3)^2</code><br><code>y=12x</code>

Graph the difference of the areas and then each choice (T13); only 12x coincides with it for x > 3. Expanding by hand is about as fast.

</details>

---

### 36. adv-ee3-substitution-u-shift

*Medium · Multiple choice · route: desmos-primary · techniques: T9*

If $u$ is defined as $x - 3$, which expression, written in terms of $u$, is equivalent to $x^2 - 6x + 4$?

- **A.** $u^2 - 12u + 31$
- **B.** $u^2 - 5$
- **C.** $u^2 - 6u - 5$
- **D.** $u^2 + 31$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** It's given that u = x - 3, so x = u + 3. Substituting u + 3 for x yields (u + 3)^2 - 6(u + 3) + 4 = u^2 + 6u + 9 - 6u - 18 + 4 = u^2 - 5. Therefore, the expression is equivalent to u^2 - 5. Distractors: u^2 - 12u + 31 substitutes u - 3 for x, solving u = x - 3 for x with the wrong sign; u^2 - 6u - 5 squares u + 3 as u^2 + 9 and drops the middle term 6u; u^2 + 31 distributes -6 over u + 3 as -6u + 18.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=x^2-6x+4</code><br><code>f(3)</code><br><code>f(4)</code>

When x = 3, u = 0, and Desmos shows f(3) = -5 (T9), so the correct choice equals -5 when u = 0; that rules out u^2 - 12u + 31 and u^2 + 31. When x = 4, u = 1, and f(4) = -4: u^2 - 5 gives -4 but u^2 - 6u - 5 gives -10. The answer is u^2 - 5.

</details>

---

### 37. adv-ee3-theater-ticket-revenue-b

*Medium · Student-produced response · route: desmos-primary · techniques: T6*

A theater raises its 12.00-dollar ticket price by $x$ dollars and expects to sell $(300 - 15x)$ tickets, for a revenue, in dollars, of $(12 + x)(300 - 15x)$. This expression is equivalent to $ax^2 + bx + c$, where $a$, $b$, and $c$ are constants. What is the value of $b$?

**Answer:** 120

<details><summary>Solutions</summary>

**By hand.** Expanding the product yields 12(300) + 12(-15x) + x(300) + x(-15x) = 3600 - 180x + 300x - 15x^2 = -15x^2 + 120x + 3600. Matching this with ax^2 + bx + c gives a = -15, b = 120 and c = 3600. Therefore, the value of b is 120.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3]</code><br><code>(12+x_1)(300-15x_1)\sim ax_1^2+bx_1+c</code>

The tilde regression (T6) returns a = -15, b = 120 and c = 3600. Read b = 120.

</details>

---

### 38. adv-exponential-difference-rewrite-coefficient

*Medium · Multiple choice · route: either · techniques: T13*

Which expression is equivalent to $3^{x + 2} - 3^x$?

- **A.** $2 \cdot 3^x$
- **B.** $5 \cdot 3^x$
- **C.** $8 \cdot 3^x$
- **D.** $9 \cdot 3^x$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** By the product rule for exponents, 3^(x + 2) = 9 \* 3^x. Substituting yields 9 \* 3^x - 3^x = (9 - 1) \* 3^x = 8 \* 3^x. Therefore, the given expression is equivalent to 8 \* 3^x. Distractors: 2·3^x subtracts the exponents, (x + 2) - x = 2, as if the terms were divided; 5·3^x takes 3^2 as 6; 9·3^x rewrites 3^(x + 2) correctly but drops the subtracted 3^x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3^{x+2}-3^x</code><br><code>y=8\cdot3^x</code>

Graph the given expression and each choice (T13). Only 8 \* 3^x coincides with it; check at x = 0, where the given expression is 9 - 1 = 8.

</details>

---

### 39. adv-fractional-negative-exponent-power-two-variable

*Medium · Multiple choice · route: hand-primary · techniques: —*

If $x$ and $y$ are positive, which expression is equivalent to $\left(x^{\frac{1}{2}}y^{-3}\right)^{-2} \cdot x^{2}y^{-4}$?

- **A.** $\frac{x}{y^{10}}$
- **B.** $\frac{x}{y^7}$
- **C.** $x^3y^2$
- **D.** $xy^2$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Raising a power to a power multiplies the exponents: (x^(1/2) y^(-3))^(-2) = x^((1/2)(-2)) y^((-3)(-2)) = x^(-1) y^6. Multiplying by x^2 y^(-4) adds exponents: x^(-1 + 2) y^(6 - 4) = x y^2. Therefore, the given expression is equivalent to xy^2. Distractors: (x)/(y^(10)) takes (-3)(-2) as -6; (x)/(y^7) applies the outer exponent -2 only to x, leaving y^(-3); x^3y^2 drops the negative sign of the outer exponent for x, taking (x^(1/2))^(-2) as x.

</details>

---

### 40. adv-gcf-then-difference-squares

*Medium · Multiple choice · route: hand-primary · techniques: T13*

Which expression is equivalent to $3x^3 - 48x$?

- **A.** $3x(x - 4)(x + 4)$
- **B.** $3x(x - 4)^2$
- **C.** $3x(x - 8)(x + 8)$
- **D.** $x(3x - 4)(3x + 4)$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Both terms share the factor 3x, so 3x^3 - 48x = 3x(x^2 - 16). The binomial x^2 - 16 is a difference of squares, x^2 - 4^2 = (x - 4)(x + 4). Therefore, the expression is equivalent to 3x(x - 4)(x + 4). Distractors: 3x(x - 4)^2 factors x^2 - 16 as a perfect square, which expands to x^2 - 8x + 16; 3x(x - 8)(x + 8) halves 16 instead of taking its square root; x(3x - 4)(3x + 4) moves the 3 into both binomials, which gives 9x^3 - 16x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=3x^3-48x</code><br><code>y=3x(x-4)(x+4)</code>

The two graphs coincide (T13). Factoring takes two quick steps by hand, so Desmos is slower and serves only as a check.

</details>

---

### 41. adv-grouping-cubic-four-terms

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

Which expression is equivalent to $x^3 - 5x^2 - 4x + 20$?

- **A.** $(x - 5)(x^2 + 4)$
- **B.** $(x - 5)(x - 2)(x + 2)$
- **C.** $(x + 5)(x - 2)(x + 2)$
- **D.** $(x - 5)(x - 2)^2$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Group the first two terms and the last two terms: x^3 - 5x^2 - 4x + 20 = x^2(x - 5) - 4(x - 5) = (x - 5)(x^2 - 4). Since x^2 - 4 is a difference of squares, (x - 5)(x^2 - 4) = (x - 5)(x - 2)(x + 2). Distractors: (x - 5)(x^2 + 4) factors -4 out of the second group as +4, so it expands to x^3 - 5x^2 + 4x - 20, with +4x - 20 in place of -4x + 20; (x + 5)(x - 2)(x + 2) has the wrong sign in the common factor; (x - 5)(x - 2)^2 writes x^2 - 4 as a perfect square.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^3-5x^2-4x+20</code><br><code>y=(x-5)(x-2)(x+2)</code>

The graph of the first line crosses the x-axis at x = -2, x = 2 and x = 5, so its factors are (x + 2), (x - 2) and (x - 5); only choice B has all three. The second line lies exactly on top of the first (T13).

</details>

---

### 42. adv-long-division-linear-negative-remainder

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

Which of the following is equivalent to $\frac{2x^2 + 5x - 4}{x + 3}$ for all $x \neq -3$?

- **A.** $2x - 1 - \frac{1}{x + 3}$
- **B.** $2x - 1 + \frac{1}{x + 3}$
- **C.** $2x - 1 - \frac{7}{x + 3}$
- **D.** $2x + 11 + \frac{29}{x + 3}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Dividing 2x^2 + 5x - 4 by x + 3: 2x^2 divided by x is 2x, and 2x(x + 3) = 2x^2 + 6x; subtracting leaves -x - 4. Then -x divided by x is -1, and -1(x + 3) = -x - 3; subtracting leaves -4 - (-3) = -1. It follows that 2x^2 + 5x - 4 = (x + 3)(2x - 1) - 1, so the expression is equivalent to 2x - 1 - 1/(x + 3). Therefore, the correct choice is 2x - 1 - 1/(x + 3). Distractors: 2x - 1 + (1)/(x + 3) drops the sign of the remainder; 2x - 1 - (7)/(x + 3) computes the last subtraction as -4 - 3 instead of -4 - (-3); 2x + 11 + (29)/(x + 3) runs synthetic division with 3 instead of -3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{2x^2+5x-4}{x+3}</code><br><code>y=2x-1-\frac{1}{x+3}</code>

Graph the given expression, then type each choice as a second line (T13). Only 2x - 1 - 1/(x + 3) lies exactly on the first graph, on both branches; the others separate visibly near the asymptote x = -3.

</details>

---

### 43. adv-negative-exponent-quotient

*Medium · Multiple choice · route: hand-primary · techniques: —*

For $x \neq 0$ and $y \neq 0$, which expression is equivalent to $\frac{(3x^{-2}y^3)^2}{x^{-5}y}$?

- **A.** $6xy^5$
- **B.** $9xy^5$
- **C.** $9xy^7$
- **D.** $9x^{-9}y^5$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Squaring the numerator yields 3^2 · x^{-2 · 2} · y^{3 · 2} = 9x^{-4}y^6. Dividing powers with the same base subtracts exponents: x^{-4 - (-5)} = x^1 and y^{6 - 1} = y^5. Therefore, the expression is equivalent to 9xy^5. Distractors: 6xy^5 multiplies 3 by 2 instead of squaring it; 9xy^7 adds the exponent of y in the denominator instead of subtracting it; 9x^{-9}y^5 adds -4 and -5 instead of subtracting -5.

</details>

---

### 44. adv-parallel-resistance-complex-fraction

*Medium · Multiple choice · route: hand-primary · techniques: T13*

Two resistors with resistances of $x$ ohms and $(x + 6)$ ohms, where $x > 0$, are connected in parallel. Their combined resistance, in ohms, is $\frac{1}{\frac{1}{x} + \frac{1}{x + 6}}$. Which expression is equivalent to the combined resistance?

- **A.** $\frac{x(x + 6)}{2x + 6}$
- **B.** $\frac{x^2 + 6}{2x + 6}$
- **C.** $\frac{2x + 6}{x(x + 6)}$
- **D.** $2x + 6$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Writing the sum in the denominator over the common denominator x(x + 6) yields 1/x + 1/(x + 6) = (x + 6 + x)/(x(x + 6)) = (2x + 6)/(x(x + 6)). The combined resistance is the reciprocal of this sum, x(x + 6)/(2x + 6). Therefore, the combined resistance, in ohms, is equivalent to x(x + 6)/(2x + 6). Distractors: (x^2 + 6)/(2x + 6) distributes x(x + 6) as x^2 + 6; (2x + 6)/(x(x + 6)) is the sum of the reciprocals, without taking the reciprocal at the end; 2x + 6 is the sum of the two resistances, which is the series resistance, not the parallel one.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{1}{\frac{1}{x}+\frac{1}{x+6}}</code><br><code>y=\frac{x(x+6)}{2x+6}</code>

Combining the fractions by hand is faster. As a check (T13), graph the given expression and each choice for x > 0; only x(x + 6)/(2x + 6) coincides with it.

</details>

---

### 45. adv-perfect-square-identity-ab

*Medium · Student-produced response · route: desmos-primary · techniques: T6*

For all values of $x$, $(ax + b)^2 = 9x^2 - 24x + 16$, where $a$ and $b$ are constants and $a > 0$. What is the value of $ab$?

**Answer:** -12

<details><summary>Solutions</summary>

**By hand.** Expanding yields (ax + b)^2 = a^2x^2 + 2abx + b^2. Matching the x terms with 9x^2 - 24x + 16 yields 2ab = -24, so ab = -12. As a check, a^2 = 9 with a > 0 gives a = 3, and then b = -4, and b^2 = 16 matches the constant term. Therefore, the value of ab is -12.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3]</code><br><code>(ax_1+b)^2\sim9x_1^2-24x_1+16</code>

The tilde regression (T6) returns a and b. It may return a = -3 and b = 4 instead of a = 3 and b = -4, because both pairs give the same square; the stem's a > 0 selects a = 3, b = -4. Either way ab = -12; enter -12.

</details>

---

### 46. adv-radical-product-rational-exponent

*Medium · Multiple choice · route: hand-primary · techniques: T13*

Which expression is equivalent to $\sqrt[4]{x^3} \cdot \sqrt{x}$, where $x > 0$?

- **A.** $x^{3/8}$
- **B.** $x^{2/3}$
- **C.** $x^{5/4}$
- **D.** $x^{7/2}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The fourth root of x^3 is x^(3/4), and the square root of x is x^(1/2). Multiplying powers of the same base adds the exponents, so the product is x^(3/4 + 1/2) = x^(3/4 + 2/4) = x^(5/4). Distractors: x^(3/8) multiplies the exponents 3/4 and 1/2 instead of adding them; x^(2/3) adds numerators and denominators separately (3 + 1 over 4 + 2); x^(7/2) treats the fourth root of x^3 as x^3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sqrt[4]{x^3}\sqrt{x}</code><br><code>y=x^{5/4}</code>

Graph the product and each choice for x > 0 (T13); only y = x^(5/4) coincides with it. Type the fourth root with nthroot or as (x^3)^(1/4). Adding two exponents by hand is faster than typing the four graphs.

</details>

---

### 47. adv-rational-add-unlike-denominators

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

For $x \neq -4$ and $x \neq 0$, which expression is equivalent to $\frac{3}{x} + \frac{2}{x + 4}$?

- **A.** $\frac{5}{2x + 4}$
- **B.** $\frac{5}{x(x + 4)}$
- **C.** $\frac{5x + 4}{x(x + 4)}$
- **D.** $\frac{5x + 12}{x(x + 4)}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The common denominator is x(x + 4). Rewriting each fraction yields 3(x + 4)/(x(x + 4)) + 2x/(x(x + 4)), and the numerator is 3x + 12 + 2x = 5x + 12. Therefore, the sum is (5x + 12)/(x(x + 4)). Distractors: (5)/(2x + 4) adds the numerators and adds the denominators; (5)/(x(x + 4)) adds the numerators over the common denominator without rewriting them; (5x + 4)/(x(x + 4)) distributes the 3 to x but not to 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{3}{x}+\frac{2}{x+4}</code><br><code>y=\frac{5x+12}{x(x+4)}</code>

Graph the given expression and each choice (T13); only the last choice lies exactly on top of it. The graphs have breaks at x = 0 and x = -4, so compare both branches.

</details>

---

### 48. adv-rational-combine-constants

*Medium · Student-produced response · route: desmos-primary · techniques: T6, T11*

For $x \neq -2$ and $x \neq 1$, the expression $\frac{5}{x + 2} - \frac{3}{x - 1}$ is equivalent to $\frac{ax + b}{(x + 2)(x - 1)}$, where $a$ and $b$ are constants. What is the value of $a + b$?

**Answer:** -9

<details><summary>Solutions</summary>

**By hand.** Rewrite both fractions over the common denominator (x + 2)(x - 1): the first numerator becomes 5(x - 1) and the second 3(x + 2). Subtracting yields 5(x - 1) - 3(x + 2) = 5x - 5 - 3x - 6 = 2x - 11. Therefore, a = 2, b = -11, and a + b = -9.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[2,3,4]</code><br><code>\frac{5}{x_1+2}-\frac{3}{x_1-1}\sim\frac{ax_1+b}{(x_1+2)(x_1-1)}</code><br><code>a+b</code>

The regression returns a = 2 and b = -11, and the last line shows -9. Keep -2 and 1 out of the x\_1 list, since the expression is undefined there.

</details>

---

### 49. adv-rational-divide-simplify

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

For $x \neq -4$, $x \neq -2$, $x \neq 1$, and $x \neq 4$, which expression is equivalent to $\frac{x^2 - 16}{x^2 - 2x - 8} \div \frac{x + 4}{x - 1}$?

- **A.** $\frac{x + 2}{x - 1}$
- **B.** $\frac{(x + 4)^2}{(x + 2)(x - 1)}$
- **C.** $\frac{x - 1}{x + 2}$
- **D.** $\frac{(x - 4)(x - 1)}{(x + 2)(x + 4)}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Dividing by a fraction is multiplying by its reciprocal, so the expression equals (x^2 - 16)/(x^2 - 2x - 8) · (x - 1)/(x + 4). Factoring yields (x - 4)(x + 4)/((x - 4)(x + 2)) · (x - 1)/(x + 4). Dividing out the common factors x - 4 and x + 4, which are nonzero for the given values of x, yields (x - 1)/(x + 2). Distractors: ((x + 4)^2)/((x + 2)(x - 1)) multiplies by the second fraction without taking its reciprocal; (x + 2)/(x - 1) takes the reciprocal of the first fraction instead of the second; ((x - 4)(x - 1))/((x + 2)(x + 4)) factors x^2 - 16 as (x - 4)^2 instead of (x - 4)(x + 4), so only one x - 4 cancels and x + 4 is left in the denominator.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^2-16}{x^2-2x-8}\div\frac{x+4}{x-1}</code><br><code>y=\frac{x-1}{x+2}</code>

The second graph lies on the first everywhere except the holes at x = -4, x = 1 and x = 4. Swap in each other choice (T13): the other three graphs visibly separate from the first.

</details>

---

### 50. adv-rational-multiply-cancel-monomial

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

For $x \neq -5$ and $x \neq 0$, which expression is equivalent to $\frac{x^2 - 25}{3x} \cdot \frac{6x^2}{x + 5}$?

- **A.** $2x(x - 5)$
- **B.** $2x(x + 5)$
- **C.** $2(x - 5)$
- **D.** $\frac{x - 5}{2x}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Factor the difference of squares: x^2 - 25 = (x - 5)(x + 5). The product is then (x - 5)(x + 5) · 6x^2 / (3x(x + 5)). Canceling x + 5 and dividing 6x^2 by 3x yields (x - 5) · 2x. Therefore, the expression is equivalent to 2x(x - 5). Distractors: 2x(x + 5) cancels the factor x - 5 instead of x + 5; 2(x - 5) divides 6x^2 by 3x as 2 instead of 2x; (x - 5)/(2x) inverts the ratio of 6x^2 to 3x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^2-25}{3x}\cdot\frac{6x^2}{x+5}</code><br><code>y=2x(x-5)</code>

Graph the product and each choice (T13). The parabola y = 2x(x - 5) lies on top of the product everywhere except the holes at x = -5 and x = 0.

</details>

---

### 51. adv-rational-simplify-factor-cancel

*Medium · Multiple choice · route: desmos-primary · techniques: T13*

For $x \neq -3$ and $x \neq -2$, which expression is equivalent to $\frac{x^2 - 9}{x^2 + 5x + 6}$?

- **A.** $\frac{x - 3}{x + 2}$
- **B.** $\frac{x - 3}{x + 3}$
- **C.** $\frac{x + 3}{x + 2}$
- **D.** $\frac{-9}{5x + 6}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Factor the numerator as a difference of squares, (x - 3)(x + 3), and the denominator as (x + 2)(x + 3). The common factor x + 3 is nonzero for x ≠ -3, so it cancels, leaving (x - 3)/(x + 2). Distractors: (x - 3)/(x + 3) cancels x + 2 instead of x + 3; (x + 3)/(x + 2) cancels the wrong factor of the numerator; (-9)/(5x + 6) cancels the x^2 terms, which are terms, not factors.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^2-9}{x^2+5x+6}</code><br><code>y=\frac{x-3}{x+2}</code>

Graph the original and each choice (T13). Only (x - 3)/(x + 2) lies on top of the original everywhere except the hole at x = -3, which the stem excludes. Zoom out to compare the branches on both sides of the vertical asymptote at x = -2.

</details>

---

### 52. adv-rational-subtract-difference-squares

*Medium · Multiple choice · route: either · techniques: T13*

For $x \neq -2$ and $x \neq 2$, which expression is equivalent to $\frac{2}{x^2 - 4} - \frac{1}{x - 2}$?

- **A.** $\frac{-x}{x^2 - 4}$
- **B.** $\frac{x}{x^2 - 4}$
- **C.** $\frac{4 - x}{x^2 - 4}$
- **D.** $\frac{1}{x^2 - x - 2}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Since x^2 - 4 = (x - 2)(x + 2), the common denominator is x^2 - 4. Rewriting the second fraction yields (x + 2)/(x^2 - 4), so the difference is (2 - (x + 2))/(x^2 - 4) = (-x)/(x^2 - 4). Distractors: (4 - x)/(x^2 - 4) subtracts x but adds 2 instead of subtracting the whole numerator x + 2; (x)/(x^2 - 4) reverses the sign of the result; (1)/(x^2 - x - 2) subtracts the numerators and the denominators separately.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{2}{x^2-4}-\frac{1}{x-2}</code><br><code>y=\frac{-x}{x^2-4}</code>

The second graph coincides with the first, including both vertical asymptotes at x = -2 and x = 2. Replace the second line by each other choice (T13) to see that none of them overlaps.

</details>

---

### 53. adv-rational-undefined-values-sum

*Medium · Student-produced response · route: either · techniques: T1, T11*

The expression $\frac{x + 4}{2x^2 - 7x + 3}$ is undefined for exactly two values of $x$. What is the sum of these two values?

**Answer:** 7/2 (≈ 3.5)

<details><summary>Solutions</summary>

**By hand.** A rational expression is undefined where its denominator equals 0. Factoring the denominator yields 2x^2 - 7x + 3 = (2x - 1)(x - 3), which equals 0 when x = 1/2 or x = 3. Therefore, the sum of the two values is 1/2 + 3 = 7/2. The numerator's zero, x = -4, makes the expression equal to 0, not undefined, so it is not one of the values.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2x^2-7x+3</code>

The expression is undefined where the denominator is 0, so graph the denominator alone and click its x-intercepts: (0.5, 0) and (3, 0). The sum is 3.5; enter 3.5 or 7/2 (T11). Graphing the whole fraction also works, but the vertical asymptotes are harder to click than the zeros.

</details>

---

### 54. adv-rationalize-radical-difference-denominator

*Medium · Multiple choice · route: hand-primary · techniques: T13*

For $x > 0$, which expression is equivalent to $\frac{6}{\sqrt{x + 3} - \sqrt{x}}$?

- **A.** $\frac{2}{3}\sqrt{x + 3} + \frac{2}{3}\sqrt{x}$
- **B.** $2\sqrt{x + 3} + 2\sqrt{x}$
- **C.** $2\sqrt{x + 3} - 2\sqrt{x}$
- **D.** $6\sqrt{x + 3} + 6\sqrt{x}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Multiplying the numerator and the denominator by the conjugate, sqrt(x + 3) + sqrt(x), turns the denominator into a difference of squares: (sqrt(x + 3))^2 - (sqrt(x))^2 = (x + 3) - x = 3. The numerator becomes 6(sqrt(x + 3) + sqrt(x)). It follows that the expression equals 6(sqrt(x + 3) + sqrt(x))/3 = 2 sqrt(x + 3) + 2 sqrt(x). Therefore, the correct choice is 2 sqrt(x + 3) + 2 sqrt(x). Distractors: (2/3) sqrt(x + 3) + (2/3) sqrt(x) squares sqrt(x + 3) as x + 9, which makes the denominator 9; 2 sqrt(x + 3) - 2 sqrt(x) keeps the minus sign in the numerator instead of using the conjugate; 6 sqrt(x + 3) + 6 sqrt(x) multiplies by the conjugate but does not divide by the new denominator 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{6}{\sqrt{x+3}-\sqrt{x}}</code><br><code>y=2\sqrt{x+3}+2\sqrt{x}</code>

The conjugate step by hand takes under 15 seconds, so Desmos is slower. As a check (T13), graph the given expression and each choice for x > 0; only 2 sqrt(x + 3) + 2 sqrt(x) lies on top of it.

</details>

---

### 55. adv-revenue-vertex-form

*Medium · Multiple choice · route: either · techniques: T13*

A kayak rental business charges $x$ dollars for each rental. Its daily revenue, in dollars, is given by the expression $-5x^2 + 150x$. Which expression is equivalent to the given expression?

- **A.** $-5(x - 15)^2 + 1,125$
- **B.** $-5(x - 15)^2 + 225$
- **C.** $-5(x - 30)^2 + 1,125$
- **D.** $-5(x + 15)^2 + 1,125$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Factor -5 from both terms: -5x^2 + 150x = -5(x^2 - 30x). Half of -30 is -15, and (-15)^2 = 225, so -5(x^2 - 30x + 225) + 5 · 225 = -5(x - 15)^2 + 1,125. Therefore, the revenue expression is equivalent to -5(x - 15)^2 + 1,125. Distractors: -5(x - 15)^2 + 225 adds back 225 without multiplying by 5; -5(x - 30)^2 + 1,125 uses 30 instead of half of 30; -5(x + 15)^2 + 1,125 uses the wrong sign for half the coefficient of x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=-5x^2+150x</code><br><code>y=-5(x-15)^2+1125</code>

Click the vertex of y = -5x^2 + 150x: (15, 1125), so the vertex form is -5(x - 15)^2 + 1,125. Graphing that choice (T13) shows it lies exactly on the original.

</details>

---

### 56. adv-storage-bin-volume-three-binomials

*Medium · Multiple choice · route: either · techniques: T13*

A storage bin in the shape of a rectangular box has a length of $(x + 3)$ feet, a width of $(x + 2)$ feet, and a height of $(x - 1)$ feet. Which expression represents the volume, in cubic feet, of the bin?

- **A.** $x^3 + 6x^2 + 11x + 6$
- **B.** $x^3 + 5x^2 + 6x - 6$
- **C.** $x^3 + 4x^2 + x - 6$
- **D.** $x^3 + 4x^2 - x - 6$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The volume of a rectangular box is length times width times height, so the volume is (x + 3)(x + 2)(x - 1). Multiplying the first two factors yields x^2 + 5x + 6. Multiplying by x - 1 yields x^3 + 5x^2 + 6x - x^2 - 5x - 6 = x^3 + 4x^2 + x - 6. Therefore, the volume, in cubic feet, is x^3 + 4x^2 + x - 6. Distractors: x^3 + 6x^2 + 11x + 6 uses x + 1 for the height; x^3 + 5x^2 + 6x - 6 multiplies only the constant 6 by -1 and leaves out -x^2 - 5x; x^3 + 4x^2 - x - 6 combines 6x - 5x as -x.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(x+3)(x+2)(x-1)</code><br><code>y=x^3+4x^2+x-6</code>

Graph the product and each choice (T13). Only x^3 + 4x^2 + x - 6 coincides with it; the zeros at x = -3, -2 and 1 are a quick visual check.

</details>

---

### 57. adv-tilde-square-minus-product-b

*Medium · Student-produced response · route: desmos-primary · techniques: T6*

For all values of $x$, $(3x - 2)^2 - (x + 5)(x - 1) = ax^2 + bx + c$, where $a$, $b$, and $c$ are constants. What is the value of $b$?

**Answer:** -16

<details><summary>Solutions</summary>

**By hand.** Expanding (3x - 2)^2 yields 9x^2 - 12x + 4, and expanding (x + 5)(x - 1) yields x^2 + 4x - 5. Subtracting the second from the first yields 9x^2 - 12x + 4 - x^2 - 4x + 5 = 8x^2 - 16x + 9. Matching coefficients with ax^2 + bx + c gives b = -16. A common slip is subtracting only the x^2 term of the product and adding the rest, which gives -8; the whole product is subtracted.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3]</code><br><code>(3x_1-2)^2-(x_1+5)(x_1-1)\sim ax_1^2+bx_1+c</code>

Read the parameters under the regression line: a = 8, b = -16, c = 9. The fit is exact, so the residuals are zero. Enter -16.

</details>

---

### 58. adv-trinomial-leading-ten

*Medium · Multiple choice · route: hand-primary · techniques: T13*

Which expression is equivalent to $10x^2 - 11x - 6$?

- **A.** $(5x - 2)(2x + 3)$
- **B.** $(5x + 3)(2x - 2)$
- **C.** $(5x + 2)(2x - 3)$
- **D.** $(10x + 3)(x - 2)$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The product ac is 10 · (-6) = -60, and the two factors of -60 that add to -11 are -15 and 4. Splitting the middle term yields 10x^2 - 15x + 4x - 6 = 5x(2x - 3) + 2(2x - 3) = (5x + 2)(2x - 3). Expanding confirms it: 10x^2 - 15x + 4x - 6 = 10x^2 - 11x - 6. Distractors: (5x - 2)(2x + 3) swaps the signs and expands to 10x^2 + 11x - 6; (5x + 3)(2x - 2) has the right first and last products but expands to 10x^2 - 4x - 6; (10x + 3)(x - 2) expands to 10x^2 - 17x - 6.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=10x^2-11x-6</code><br><code>y=(5x+2)(2x-3)</code>

Graph the trinomial and each choice (T13); only y = (5x + 2)(2x - 3) coincides with it. Expanding the middle terms of each choice by hand is faster than typing all four.

</details>

---

### 59. adv-complete-square-unknown-k

*Hard · Student-produced response · route: either · techniques: T6*

The expression $x^2 - 6kx + 50$ is equivalent to $(x - h)^2 + 14$, where $h$ and $k$ are positive constants. What is the value of $k$?

**Answer:** 2

<details><summary>Solutions</summary>

**By hand.** Expanding the target form yields (x - h)^2 + 14 = x^2 - 2hx + h^2 + 14. Matching constant terms gives h^2 + 14 = 50, so h^2 = 36 and, since h is positive, h = 6. Matching x-coefficients gives -6k = -2h = -12, so k = 2. Common errors: reporting h = 6 instead of k, or setting h^2 = 50 and ignoring the 14.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3]</code><br><code>x_1^2-6kx_1+50\sim(x_1-h)^2+14</code>

The tilde regression (T6) returns h and k with the same sign, either h = 6 and k = 2 or h = -6 and k = -2. The stem says both are positive, so k = 2.

</details>

---

### 60. adv-complex-fraction-difference-squares

*Hard · Multiple choice · route: hand-primary · techniques: T13*

For $x \neq -2$ and $x \neq 0$, which expression is equivalent to $\frac{1 - \frac{4}{x^2}}{1 + \frac{2}{x}}$?

- **A.** $\frac{-2}{x}$
- **B.** $\frac{x - 2}{x}$
- **C.** $\frac{x + 2}{x}$
- **D.** $\frac{x - 2}{x^2}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Multiplying the numerator and the denominator of the complex fraction by x^2 yields (x^2 - 4)/(x^2 + 2x). Factoring gives (x - 2)(x + 2)/(x(x + 2)), and dividing out the common factor x + 2, which is nonzero because x ≠ -2, yields (x - 2)/x. Distractors: (-2)/(x) results from cancelling the two 1s and dividing -4/x^2 by 2/x; (x + 2)/(x) keeps the wrong factor of the difference of squares; (x - 2)/(x^2) multiplies only the numerator by x^2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{1-\frac{4}{x^2}}{1+\frac{2}{x}}</code><br><code>y=\frac{x-2}{x}</code>

The second graph lies on top of the first everywhere except the single missing point at x = -2. Testing all four choices (T13) works but takes longer than the hand method; use it to confirm the answer.

</details>

---

### 61. adv-ee3-absolute-value-quotient-b

*Hard · Student-produced response · route: desmos-primary · techniques: T9*

For $x < 2$, the expression $\frac{x^2 - 4}{|x - 2|}$ is equivalent to $ax + b$, where $a$ and $b$ are constants. What is the value of $b$?

**Answer:** -2

<details><summary>Solutions</summary>

**By hand.** Factoring the numerator yields (x - 2)(x + 2). For x < 2, x - 2 is negative, so |x - 2| = -(x - 2). Then (x - 2)(x + 2)/(-(x - 2)) = -(x + 2) = -x - 2, since x - 2 is not 0. So a = -1 and b = -2. Therefore, the value of b is -2. (Treating |x - 2| as x - 2 gives x + 2 and the wrong value 2.)

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=\frac{x^2-4}{\left|x-2\right|}</code><br><code>f(0)</code><br><code>f(1)</code>

Since 0 < 2, f(0) equals a(0) + b = b, and Desmos shows f(0) = -2 (T9). f(1) = -3 confirms a = -1. Enter -2.

</details>

---

### 62. adv-ee3-ball-height-shifted-time-k

*Hard · Student-produced response · route: desmos-primary · techniques: T6*

A model rocket is fired straight up. After $t$ seconds of flight, the rocket is $-5t^2 + 30t + 2$ meters above the ground. If $s$ is defined as $t - 3$, this expression is equivalent to $-5s^2 + k$, where $k$ is a constant. What is the value of $k$?

**Answer:** 47

<details><summary>Solutions</summary>

**By hand.** It's given that s = t - 3, so t = s + 3. Substituting yields -5(s + 3)^2 + 30(s + 3) + 2 = -5(s^2 + 6s + 9) + 30s + 90 + 2 = -5s^2 - 30s - 45 + 30s + 92 = -5s^2 + 47. Therefore, k = 47. Alternate approach: when s = 0, t = 3, and the height is -45 + 90 + 2 = 47, which equals -5(0)^2 + k. (Squaring s + 3 as s^2 + 9 leaves a term of 30s and no single value of k.)

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3,4]</code><br><code>-5x_1^2+30x_1+2\sim-5(x_1-3)^2+k</code>

Here x\_1 stands for t and x\_1 - 3 for s. The tilde regression (T6) returns k = 47 with a perfect fit, which also confirms that no s-term is left over.

</details>

---

### 63. adv-ee3-equal-coefficients-k

*Hard · Student-produced response · route: hand-primary · techniques: —*

The coefficient of $x^3$ in the expansion of $(x^2 + kx + 2)(x^2 - 3x + 5)$ is equal to the coefficient of $x$ in the same expansion, where $k$ is a constant. What is the value of $k$?

**Answer:** 3/4 (≈ 0.75)

<details><summary>Solutions</summary>

**By hand.** Only the products that make an x^3-term or an x-term are needed. The x^3-term comes from x^2 times -3x and kx times x^2, so its coefficient is k - 3. The x-term comes from kx times 5 and 2 times -3x, so its coefficient is 5k - 6. Setting them equal yields k - 3 = 5k - 6, so 3 = 4k and k = 3/4. Therefore, the value of k is 3/4 (or 0.75).

</details>

---

### 64. adv-ee3-exponential-sum-squared

*Hard · Multiple choice · route: either · techniques: T13*

Which expression is equivalent to $\left(2^x + 2^{-x}\right)^2$?

- **A.** $4^x + 4^{-x}$
- **B.** $4^x + 1 + 4^{-x}$
- **C.** $2^{x^2} + 2 + 2^{-x^2}$
- **D.** $4^x + 2 + 4^{-x}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Squaring a sum gives (p + q)^2 = p^2 + 2pq + q^2, not p^2 + q^2. With p = 2^x and q = 2^(-x): p^2 = 2^(2x) = 4^x, q^2 = 2^(-2x) = 4^(-x), and pq = 2^(x - x) = 2^0 = 1. So the square is 4^x + 2(1) + 4^(-x) = 4^x + 2 + 4^(-x). Therefore, the expression is equivalent to 4^x + 2 + 4^(-x). Distractors: 4^x + 4^(-x) squares each term and leaves out the middle term 2pq; 4^x + 1 + 4^(-x) includes pq = 1 but not doubled; 2^(x^2) + 2 + 2^(-x^2) squares the exponents instead of doubling them.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left(2^x+2^{-x}\right)^2</code><br><code>y=4^x+2+4^{-x}</code>

Graph the given expression and then each choice (T13). Only 4^x + 2 + 4^(-x) coincides; its minimum is 4 at x = 0, while 4^x + 4^(-x) has minimum 2 and 4^x + 1 + 4^(-x) has minimum 3.

</details>

---

### 65. adv-ee3-four-factor-x2-coefficient

*Hard · Multiple choice · route: hand-primary · techniques: T6*

When $(x - 1)(x + 2)(x + 3)(x - 4)$ is expanded and written in standard form, what is the coefficient of $x^2$?

- **A.** $-15$
- **B.** $-14$
- **C.** $-13$
- **D.** $-1$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Pairing the factors keeps the work short: (x - 1)(x + 2) = x^2 + x - 2 and (x + 3)(x - 4) = x^2 - x - 12. In the product (x^2 + x - 2)(x^2 - x - 12), an x^2-term comes from three products: x^2 times -12, x times -x, and -2 times x^2. These yield -12x^2, -x^2 and -2x^2, so the coefficient of x^2 is -12 - 1 - 2 = -15. Therefore, the coefficient is -15. Distractors: -14 leaves out the product x times -x; -13 takes x times -x as +x^2; -1 keeps only the product x times -x and leaves out the two products with x^2.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3,4,5]</code><br><code>(x_1-1)(x_1+2)(x_1+3)(x_1-4)\sim ax_1^4+bx_1^3+cx_1^2+dx_1+k</code>

The tilde regression (T6) returns a = 1, b = 0, c = -15, d = -10 and k = 24; read c = -15. Avoid the letter e, which Desmos reads as Euler's number. Pairing the factors by hand is faster.

</details>

---

### 66. adv-ee3-gcf-then-trinomial-a-plus-b

*Hard · Student-produced response · route: hand-primary · techniques: —*

The expression $12x^5y^2 + 18x^4y^3 - 30x^3y^4$ is equivalent to $6x^3y^2(ax + by)(x - y)$, where $a$ and $b$ are constants. What is the value of $a + b$?

**Answer:** 7

<details><summary>Solutions</summary>

**By hand.** The greatest common factor of the three terms is 6x^3y^2: 6 divides 12, 18 and 30, and the smallest powers are x^3 and y^2. Factoring it out yields 6x^3y^2(2x^2 + 3xy - 5y^2). The trinomial must equal (ax + by)(x - y) = ax^2 + (b - a)xy - by^2. Matching coefficients gives a = 2 and b = 5, and b - a = 3 checks the middle term. Indeed, (2x + 5y)(x - y) = 2x^2 - 2xy + 5xy - 5y^2. Therefore, a + b = 7.

</details>

---

### 67. adv-ee3-not-equivalent-difference-squares

*Hard · Multiple choice · route: either · techniques: T13*

Which of the following is NOT equivalent to $9x^2 - 1$?

- **A.** $(3x - 1)^2 + 6x - 2$
- **B.** $(1 - 3x)(-1 - 3x)$
- **C.** $9\left(x - \frac{1}{3}\right)\left(x + \frac{1}{3}\right)$
- **D.** $9\left(x - \frac{1}{9}\right)\left(x + \frac{1}{9}\right)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Check each choice against 9x^2 - 1. (3x - 1)^2 + 6x - 2 = 9x^2 - 6x + 1 + 6x - 2 = 9x^2 - 1. (1 - 3x)(-1 - 3x) = -1 - 3x + 3x + 9x^2 = 9x^2 - 1. 9(x - 1/3)(x + 1/3) = 9(x^2 - 1/9) = 9x^2 - 1. But 9(x - 1/9)(x + 1/9) = 9(x^2 - 1/81) = 9x^2 - 1/9. Therefore, 9(x - 1/9)(x + 1/9) is not equivalent; it factors out 9 and then divides the constant 1 by 9 instead of using the square root of 1/9. Distractors: (3x - 1)^2 + 6x - 2 looks like a perfect square, but the extra terms cancel its middle term; (1 - 3x)(-1 - 3x) reverses and negates the factors, yet it still expands to 9x^2 - 1; 9(x - 1/3)(x + 1/3) is the correct factorization after factoring out 9.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=9x^2-1</code><br><code>y=9\left(x-\frac{1}{9}\right)\left(x+\frac{1}{9}\right)</code>

Graph 9x^2 - 1 and then each choice (T13). Three choices coincide with it. The choice with 1/9 has zeros at ±1/9 instead of ±1/3 and a y-intercept near -0.111 instead of -1, so it is the one that is not equivalent. Zoom in near the origin to see the difference.

</details>

---

### 68. adv-ee3-quartic-over-quadratic-polynomial

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

For $x \neq -3$ and $x \neq 1$, which expression is equivalent to $\frac{x^4 - 10x^2 + 9}{x^2 + 2x - 3}$?

- **A.** $x^2 - 5x - 3$
- **B.** $x^2 - 4x + 3$
- **C.** $x^2 - 2x - 3$
- **D.** $x^2 + 2x - 3$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The numerator is quadratic in x^2: x^4 - 10x^2 + 9 = (x^2 - 1)(x^2 - 9) = (x - 1)(x + 1)(x - 3)(x + 3). The denominator factors as (x + 3)(x - 1). For x ≠ -3 and x ≠ 1, those two factors cancel, leaving (x + 1)(x - 3) = x^2 - 2x - 3. Therefore, the expression is equivalent to x^2 - 2x - 3. Distractors: x^2 - 5x - 3 divides term by term (x^4/x^2, -10x^2/(2x), 9/(-3)), which is not valid for a sum; x^2 - 4x + 3 = (x - 1)(x - 3) cancels x + 1 instead of x - 1, a sign slip; x^2 + 2x - 3 = (x - 1)(x + 3) keeps the denominator's factors, as if the denominator were (x + 1)(x - 3).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^4-10x^2+9}{x^2+2x-3}</code><br><code>y=x^2-2x-3</code>

Graph the given expression and then each choice (T13). Only x^2 - 2x - 3 lies on top of it; the given graph has holes at x = -3 and x = 1, which the stem excludes. Zoom out to compare the whole parabola.

</details>

---

### 69. adv-ee3-substitution-quartic-u

*Hard · Multiple choice · route: hand-primary · techniques: T9*

When $u$ is defined as $x^2 + 1$, the expression $x^4 + 5x^2 + 4$ can be rewritten using only the variable $u$. Which of the following is the result?

- **A.** $u^2 + 3u$
- **B.** $u^2 + 5u - 2$
- **C.** $u^2 + 5u + 4$
- **D.** $u^2 + 7u + 10$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that u = x^2 + 1, so x^2 = u - 1 and x^4 = (u - 1)^2. Substituting yields (u - 1)^2 + 5(u - 1) + 4 = u^2 - 2u + 1 + 5u - 5 + 4 = u^2 + 3u. Alternate approach: x^4 + 5x^2 + 4 = (x^2 + 1)(x^2 + 4) = u(u + 3) = u^2 + 3u. Therefore, the result is u^2 + 3u. Distractors: u^2 + 5u + 4 replaces x^2 with u without accounting for the + 1; u^2 + 7u + 10 substitutes u + 1 for x^2, a sign error; u^2 + 5u - 2 squares u - 1 as u^2 - 1, dropping the middle term.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=x^4+5x^2+4</code><br><code>f(1)</code>

Desmos is a check here, not the main route. When x = 1, u = 2, and f(1) = 10 (T9). At u = 2 the choices give 10, 12, 18 and 28, so only u^2 + 3u matches.

</details>

---

### 70. adv-exponent-difference-squares-a-minus-b

*Hard · Multiple choice · route: hand-primary · techniques: —*

For all $x > 1$, $\frac{x^{a^2}}{x^{b^2}} = x^{32}$, where $a$ and $b$ are constants and $a + b = 4$. What is the value of $a - b$?

- **A.** $4$
- **B.** $8$
- **C.** $28$
- **D.** $32$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Dividing powers with the same base subtracts the exponents, so x^{a^2 - b^2} = x^{32} for all x > 1, and therefore a^2 - b^2 = 32. Factoring the difference of squares yields (a + b)(a - b) = 32. It's given that a + b = 4, so 4(a - b) = 32 and a - b = 8. (Then a = 6 and b = -2, and 36 - 4 = 32 checks.) Distractors: 4 is the value of a + b; 28 subtracts 4 from 32 instead of dividing; 32 is the value of a^2 - b^2, an intermediate result.

</details>

---

### 71. adv-exponent-k

*Hard · Multiple choice · route: hand-primary · techniques: T4, T13*

For all $x > 0$, $\left(x^{3/4}\right)^k \cdot x^{-1/2} = x^{5/2}$, where $k$ is a constant. What is the value of $k$?

- **A.** $\frac{9}{4}$
- **B.** $\frac{8}{3}$
- **C.** $\frac{10}{3}$
- **D.** $4$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Add exponents: 3k/4 - 1/2 = 5/2, so 3k/4 = 3 and k = 4. Distractors: 9/4 adds the exponents 3/4 and k instead of multiplying them, (3/4 + k) - 1/2 = 5/2; 8/3 moves the -1/2 across without changing its sign, 3k/4 = 5/2 - 1/2 = 2; 10/3 ignores the factor x^(-1/2), 3k/4 = 5/2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\left(x^{3/4}\right)^{k}x^{-1/2}</code><br><code>y=x^{5/2}</code>

Add a slider for k; the two curves coincide only at k = 4. Checking each choice this way works but is slower than adding exponents.

</details>

---

### 72. adv-exponential-form-displays-value

*Hard · Multiple choice · route: hand-primary · techniques: T13, T9*

The function $f$ is defined by $f(x) = 3 \cdot 2^x$. Which of the following equivalent forms of $f(x)$ displays the value of $f(2)$ as a constant or coefficient?

- **A.** $f(x) = 3 \cdot 4^{x/2}$
- **B.** $f(x) = 6 \cdot 2^{x - 1}$
- **C.** $f(x) = 12 \cdot 2^{x - 2}$
- **D.** $f(x) = 12 \cdot 4^{x - 2}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** f(2) = 3 · 4 = 12. A form that shows this has exponent 0 at x = 2: 3 · 2^x = 3 · 2^2 · 2^(x-2) = 12 · 2^(x-2). Distractors: 12 · 4^(x-2) has the right coefficient but is not equivalent (it equals 12 at x = 2 but 3/4 at x = 0, not 3); 6 · 2^(x-1) is equivalent but displays f(1) = 6; 3 · 4^(x/2) is equivalent but displays f(0) = 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=3\cdot2^x</code><br><code>f(2)</code><br><code>y=12\cdot2^{x-2}</code><br><code>y=f(x)</code>

f(2) shows 12, so the answer must have 12 out front. Two choices do; graph each over y = f(x) and only 12 · 2^(x-2) lies on top of it. Rewriting with exponent rules by hand is faster than graphing four choices.

</details>

---

### 73. adv-exponential-product-base-half

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

Which expression is equivalent to $2^{2x + 3} \cdot 8^{1 - x}$?

- **A.** $8(\frac{1}{2})^x$
- **B.** $16(\frac{1}{2})^x$
- **C.** $64(\frac{1}{2})^x$
- **D.** $64 \cdot 2^x$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Rewriting 8 as 2^3 yields 8^(1 - x) = 2^(3(1 - x)) = 2^(3 - 3x). Multiplying powers of 2 adds the exponents: 2^(2x + 3) \* 2^(3 - 3x) = 2^(6 - x) = 2^6 \* 2^(-x) = 64(1/2)^x. Therefore, the expression is equivalent to 64(1/2)^x. Distractors: 8((1)/(2))^x drops the factor 8^1 = 8 when splitting 8^(1 - x); 16((1)/(2))^x rewrites 8^(1 - x) as 2^(1 - 3x), applying the 3 only to x; 64·2^x rewrites 8^(1 - x) as 2^(3 - x), applying the 3 only to the 1.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=2^{2x+3}\cdot8^{1-x}</code><br><code>y=64\left(\frac{1}{2}\right)^x</code>

Graph the given expression and each choice (T13). The given graph decreases and crosses the y-axis at 64, which rules out 64 \* 2^x (increasing) and the choices with 8 and 16; only 64(1/2)^x coincides with it.

</details>

---

### 74. adv-exponential-rewrite-base

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

Which expression is equivalent to $\frac{8^x}{2^{x - 3}}$?

- **A.** $4^{x - 3}$
- **B.** $4^{x + 3}$
- **C.** $8 \cdot 4^{x - 3}$
- **D.** $8 \cdot 4^{x}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Write both powers with base 2: 8^x = (2^3)^x = 2^(3x), so the expression is 2^(3x)/2^(x - 3) = 2^(3x - (x - 3)) = 2^(2x + 3). Then 2^(2x + 3) = 2^(2x) · 2^3 = 8 · 4^x. Distractors: 4^(x+3) = 2^(2x+6) halves only the 2x part of the exponent 2x + 3 and doubles the 3; 4^(x-3) = 2^(2x-6) and 8 · 4^(x-3) = 2^(2x-3) come from subtracting 3 instead of adding it when the exponent x - 3 is subtracted.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{8^x}{2^{x-3}}</code><br><code>y=8\cdot4^x</code>

Graph the original and each choice (T13); only y = 8 · 4^x coincides with it. A quick point check helps: at x = 0 the original equals 8, which rules out 4^(x-3) and 4^(x+3) at once.

</details>

---

### 75. adv-factor-theorem-constant

*Hard · Multiple choice · route: either · techniques: T13, T9*

The polynomial $p(x)$ has $x - 3b$ as a factor, where $b$ is a positive constant. Which of the following could define $p(x)$?

- **A.** $x^2 - 3bx - 18b^2$
- **B.** $x^2 + 9b^2$
- **C.** $x^3 + 27b^3$
- **D.** $x^3 - 27b^3$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** By the factor theorem, x - 3b is a factor exactly when p(3b) = 0. Test each: (3b)^3 - 27b^3 = 0, so x^3 - 27b^3 works (it factors as (x - 3b)(x^2 + 3bx + 9b^2)). Distractors: x^3 + 27b^3 gives 54b^3 and has x + 3b as a factor instead (sign error); x^2 - 3bx - 18b^2 = (x - 6b)(x + 3b) gives -18b^2, a factor-pair slip; x^2 + 9b^2 gives 18b^2 and has no real linear factor (treats a sum of squares as a difference of squares).

**Desmos** (not yet verified in Desmos). Type:<br><code>b=1</code><br><code>y=x^2-3bx-18b^2</code><br><code>y=x^2+9b^2</code><br><code>y=x^3+27b^3</code><br><code>y=x^3-27b^3</code>

Pick b = 1 (any positive value works) and graph each choice; the factor x - 3b means a zero at x = 3. Only x^3 - 27b^3 crosses the x-axis at 3. Click the zero to confirm it is exactly 3.

</details>

---

### 76. adv-long-division-missing-term-cubic

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

For $x \neq 3$, which expression is equivalent to $\frac{x^3 - 8x + 5}{x - 3}$?

- **A.** $x - 5 - \frac{10}{x - 3}$
- **B.** $x^2 - 3x + 1 + \frac{2}{x - 3}$
- **C.** $x^2 + 3x + 1 + \frac{5}{x - 3}$
- **D.** $x^2 + 3x + 1 + \frac{8}{x - 3}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The dividend has no x^2 term, so it is written as x^3 + 0x^2 - 8x + 5. Synthetic division by x - 3 uses 3: bring down 1; 1 \* 3 = 3, and 0 + 3 = 3; 3 \* 3 = 9, and -8 + 9 = 1; 1 \* 3 = 3, and 5 + 3 = 8. The quotient is x^2 + 3x + 1 and the remainder is 8, so x^3 - 8x + 5 = (x - 3)(x^2 + 3x + 1) + 8. Therefore, the expression is equivalent to x^2 + 3x + 1 + 8/(x - 3). Distractors: x - 5 - (10)/(x - 3) leaves out the 0 placeholder for the x^2 term; x^2 - 3x + 1 + (2)/(x - 3) runs synthetic division with -3 instead of 3; x^2 + 3x + 1 + (5)/(x - 3) has the right quotient but takes the constant term 5 as the remainder.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^3-8x+5}{x-3}</code><br><code>y=x^2+3x+1+\frac{8}{x-3}</code>

Graph the given expression and each choice (T13). Only x^2 + 3x + 1 + 8/(x - 3) lies on the first graph; the choice with remainder 5 has the right shape but sits visibly off near x = 3.

</details>

---

### 77. adv-long-division-quadratic-divisor

*Hard · Multiple choice · route: desmos-primary · techniques: T6*

The expression $\frac{x^3 + 2x^2 - 5x + 1}{x^2 + 1}$ is equivalent to $x + 2 + \frac{ax + b}{x^2 + 1}$, where $a$ and $b$ are constants. What is the value of $a$?

- **A.** $-6$
- **B.** $-4$
- **C.** $-1$
- **D.** $2$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Multiplying both sides of the identity by x^2 + 1 yields x^3 + 2x^2 - 5x + 1 = (x + 2)(x^2 + 1) + ax + b = x^3 + 2x^2 + x + 2 + ax + b. Matching the x terms yields -5 = 1 + a, so a = -6, and matching the constants yields 1 = 2 + b, so b = -1. Alternate approach: polynomial long division of x^3 + 2x^2 - 5x + 1 by x^2 + 1 gives the quotient x + 2 and the remainder -6x - 1, so a = -6. Distractors: -4 results from adding x instead of subtracting it at the first step of the division; -1 is the value of b, not a; 2 is the constant term of the quotient.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4]</code><br><code>\frac{x_1^3+2x_1^2-5x_1+1}{x_1^2+1}\sim x_1+2+\frac{ax_1+b}{x_1^2+1}</code>

The tilde regression (T6) returns a = -6 and b = -1. Four list values are enough because the identity holds for every x; if the parameters come back as long decimals, re-check the parentheses in the fraction.

</details>

---

### 78. adv-moss-area-exponential-rewrite-a

*Hard · Student-produced response · route: either · techniques: T9*

The area, in square centimeters, covered by a patch of moss $w$ weeks after it is first measured is modeled by the expression $6(4)^{\frac{w + 3}{2}}$. This expression is equivalent to $a(b)^w$, where $a$ and $b$ are positive constants. What is the value of $a$?

**Answer:** 48

<details><summary>Solutions</summary>

**By hand.** Splitting the exponent yields 4^((w + 3)/2) = 4^(3/2) \* 4^(w/2). Since 4^(1/2) = 2, it follows that 4^(3/2) = 2^3 = 8 and 4^(w/2) = (4^(1/2))^w = 2^w. Substituting yields 6 \* 8 \* 2^w = 48(2)^w, so a = 48 and b = 2. Therefore, the value of a is 48. Alternate approach: at w = 0, a(b)^0 = a, so a = 6(4)^(3/2) = 6 \* 8 = 48.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(w)=6(4)^{\frac{w+3}{2}}</code><br><code>f(0)</code><br><code>\frac{f(1)}{f(0)}</code>

Define the model as a function (T9). Because b^0 = 1, a = f(0), and the second line shows 48; enter 48. The third line shows b = 2 as a check.

</details>

---

### 79. adv-negative-exponent-complex-fraction-two-variable

*Hard · Multiple choice · route: hand-primary · techniques: T13*

For $x > 0$, $y > 0$, and $x \neq y$, which expression is equivalent to $\frac{x^{-2} - y^{-2}}{x^{-1} - y^{-1}}$?

- **A.** $x + y$
- **B.** $\frac{x + y}{xy}$
- **C.** $\frac{y - x}{xy}$
- **D.** $\frac{xy}{x + y}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since x^(-2) = (x^(-1))^2, the numerator is a difference of squares in x^(-1) and y^(-1): x^(-2) - y^(-2) = (x^(-1) - y^(-1))(x^(-1) + y^(-1)). Because x is not equal to y, the factor x^(-1) - y^(-1) is not 0 and cancels, leaving x^(-1) + y^(-1) = 1/x + 1/y = (y + x)/(xy). Therefore, the expression is equivalent to (x + y)/(xy). Distractors: x + y treats the negative exponents as positive and simplifies (x^2 - y^2)/(x - y); (y - x)/(xy) divides term by term, x^(-2)/x^(-1) and y^(-2)/y^(-1), giving x^(-1) - y^(-1); (xy)/(x + y) is the reciprocal of the correct result.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{2^{-2}-5^{-2}}{2^{-1}-5^{-1}}</code><br><code>\frac{2+5}{2\cdot5}</code>

Desmos cannot graph a two-variable expression against the choices, so the hand method is faster. As a check (T13), substitute numbers such as x = 2 and y = 5 into the given expression and each choice: the given expression and (x + y)/(xy) both show 0.7, while x + y shows 7, (y - x)/(xy) shows 0.3 and xy/(x + y) shows about 1.43.

</details>

---

### 80. adv-patio-gravel-border-k

*Hard · Student-produced response · route: either · techniques: T6*

A square patio with side length $x$ feet is surrounded by a gravel border that extends $k$ feet beyond each edge of the patio, where $k$ is a positive constant. The area, in square feet, of the gravel border is $20x + 100$. What is the value of $k$?

**Answer:** 5

<details><summary>Solutions</summary>

**By hand.** The border extends k feet on each side, so the outer square has side length x + 2k and area (x + 2k)^2. The area of the border is (x + 2k)^2 - x^2 = 4kx + 4k^2. It's given that this equals 20x + 100 for every x, so 4k = 20 and 4k^2 = 100. Both give k = 5 (k is positive). Common errors: using x + k as the outer side gives 2kx + k^2, so k = 10 from the x-term, which fails the constant term.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3]</code><br><code>(x_1+2k)^2-x_1^2\sim20x_1+100</code>

The tilde regression (T6) returns k = 5. If it reports k = -5 with a poor fit, the start value was off; only k = 5 matches both the 20x and the 100.

</details>

---

### 81. adv-polynomial-product-constant-c

*Hard · Student-produced response · route: desmos-primary · techniques: T6*

For all values of $x$, $(x^2 + kx - 4)(3x - 2) = 3x^3 + 7x^2 + cx + 8$, where $c$ and $k$ are constants. What is the value of $c$?

**Answer:** -18

<details><summary>Solutions</summary>

**By hand.** Expanding the left side yields (x^2 + kx - 4)(3x - 2) = 3x^3 - 2x^2 + 3kx^2 - 2kx - 12x + 8 = 3x^3 + (3k - 2)x^2 + (-2k - 12)x + 8. Matching the x^2 coefficients gives 3k - 2 = 7, so k = 3. Matching the x coefficients gives c = -2k - 12 = -6 - 12 = -18.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4]</code><br><code>(x_1^2+kx_1-4)(3x_1-2)\sim3x_1^3+7x_1^2+cx_1+8</code>

The regression returns k = 3 and c = -18. Two unknowns need at least two x\_1 values; four makes the fit unambiguous.

</details>

---

### 82. adv-quartic-hidden-difference-squares

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

Which expression is equivalent to $x^4 + 2x^2 + 9$?

- **A.** $(x^2 + 1)(x^2 + 9)$
- **B.** $(x^2 - x + 3)(x^2 + x + 3)$
- **C.** $(x^2 - 2x - 3)(x^2 + 2x - 3)$
- **D.** $(x^2 - 2x + 3)(x^2 + 2x + 3)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The expression is not a perfect square, since (x^2 + 3)^2 = x^4 + 6x^2 + 9. Rewriting it as that square minus the difference yields x^4 + 2x^2 + 9 = (x^2 + 3)^2 - 4x^2. This is a difference of squares with A = x^2 + 3 and B = 2x, so it equals (x^2 + 3 - 2x)(x^2 + 3 + 2x) = (x^2 - 2x + 3)(x^2 + 2x + 3). Therefore, the correct choice is (x^2 - 2x + 3)(x^2 + 2x + 3). Distractors: (x^2 + 1)(x^2 + 9) picks factors of 9 without checking the middle term, giving x^4 + 10x^2 + 9; (x^2 - x + 3)(x^2 + x + 3) subtracts x^2 instead of 4x^2, giving x^4 + 5x^2 + 9; (x^2 - 2x - 3)(x^2 + 2x - 3) starts from (x^2 - 3)^2, giving x^4 - 10x^2 + 9.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^4+2x^2+9</code><br><code>y=(x^2-2x+3)(x^2+2x+3)</code>

Graph the given expression and each choice (T13). Only (x^2 - 2x + 3)(x^2 + 2x + 3) lies on top of it; compare the y-intercepts and the minimum height to rule the others out quickly.

</details>

---

### 83. adv-quartic-product-identity-ab

*Hard · Multiple choice · route: either · techniques: T6*

For all values of $x$, $(x^2 + ax + 2)(x^2 + bx + 2) = x^4 - 5x^2 + 4$, where $a$ and $b$ are constants. What is the value of $ab$?

- **A.** $-9$
- **B.** $-7$
- **C.** $-5$
- **D.** $9$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Expanding the left side yields x^4 + (a + b)x^3 + (2 + ab + 2)x^2 + 2(a + b)x + 4. Matching the x^3 coefficient with the right side yields a + b = 0, and matching the x^2 coefficient yields 4 + ab = -5, so ab = -9. As a check, a = 3 and b = -3 satisfy both, and (x^2 + 3x + 2)(x^2 - 3x + 2) = x^4 - 5x^2 + 4. Therefore, the value of ab is -9. Distractors: -7 counts only one of the two 2x^2 products, solving 2 + ab = -5; -5 reads the x^2 coefficient of the right side as ab; 9 solves 4 + ab = -5 with a sign error, as ab = 4 - (-5).

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4,5]</code><br><code>(x_1^2+ax_1+2)(x_1^2+bx_1+2)\sim x_1^4-5x_1^2+4</code>

The tilde regression (T6) returns a = 3 and b = -3 (or the reverse; the product is the same). Multiply the two parameters: ab = -9. If the fit reports a large error, the regression has found a local fit; retype with different list values.

</details>

---

### 84. adv-quartic-quadratic-form-a

*Hard · Student-produced response · route: either · techniques: T6*

The expression $x^4 - 13x^2 + 36$ is equivalent to $(x - a)(x + a)(x - b)(x + b)$, where $a$ and $b$ are constants and $a > b > 0$. What is the value of $a$?

**Answer:** 3

<details><summary>Solutions</summary>

**By hand.** Treat x^2 as a single quantity: x^4 - 13x^2 + 36 = (x^2)^2 - 13(x^2) + 36. Two numbers with product 36 and sum -13 are -9 and -4, so the expression is (x^2 - 9)(x^2 - 4). Each factor is a difference of squares: (x - 3)(x + 3)(x - 2)(x + 2). Since a > b > 0, a = 3 and b = 2. Common errors: reporting 9, the value of a^2, or reporting b = 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4,5]</code><br><code>x_1^4-13x_1^2+36\sim(x_1-a)(x_1+a)(x_1-b)(x_1+b)</code>

The tilde regression (T6) returns values of a and b equal to 3 and 2 up to sign and order. The stem says a > b > 0, so a = 3.

</details>

---

### 85. adv-radical-exponents-two-variable-a-minus-b

*Hard · Student-produced response · route: hand-primary · techniques: T11*

For $x > 0$ and $y > 0$, the expression $\frac{\sqrt[3]{x^2y} \cdot \sqrt{xy^3}}{x^{-\frac{1}{3}}y^{2}}$ is equivalent to $x^a y^b$, where $a$ and $b$ are constants. What is the value of $a - b$?

**Answer:** 5/3 (≈ 1.667)

<details><summary>Solutions</summary>

**By hand.** Rewriting the radicals with rational exponents yields cube root of (x^2 y) = x^(2/3) y^(1/3) and sqrt(x y^3) = x^(1/2) y^(3/2). The exponent of x is 2/3 + 1/2 - (-1/3) = 2/3 + 1/2 + 1/3 = 3/2, and the exponent of y is 1/3 + 3/2 - 2 = -1/6. It follows that a = 3/2 and b = -1/6. Therefore, a - b = 3/2 + 1/6 = 10/6 = 5/3.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{2}{3}+\frac{1}{2}+\frac{1}{3}-\left(\frac{1}{3}+\frac{3}{2}-2\right)</code>

The exponent rules are done by hand; Desmos is slower for the rewriting. Desmos can do the final exponent arithmetic: the line shows 1.66666666667, and the fraction toggle (T11) shows 5/3. Enter 5/3 (or 1.666 or 1.667), not 1.67.

</details>

---

### 86. adv-radical-perfect-square-negative-x

*Hard · Multiple choice · route: hand-primary · techniques: T9, T13*

For $x < -3$, which expression is equivalent to $\sqrt{x^2 + 6x + 9}$?

- **A.** $x + 3$
- **B.** $-x - 3$
- **C.** $x - 3$
- **D.** $-x + 3$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The radicand is a perfect square: x^2 + 6x + 9 = (x + 3)^2. The square root of a square is the absolute value, so sqrt((x + 3)^2) = |x + 3|. For x < -3, x + 3 is negative, so |x + 3| = -(x + 3) = -x - 3. Therefore, the expression is equivalent to -x - 3. Distractors: x + 3 drops the absolute value, giving a negative result for a square root; x - 3 factors the radicand as (x - 3)^2; -x + 3 negates x but not the 3.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=\sqrt{x^2+6x+9}</code><br><code>f(-5)</code>

f(-5) = 2 (T9). Substitute x = -5 into each choice: x + 3 = -2, -x - 3 = 2, x - 3 = -8, -x + 3 = 8, so only -x - 3 matches. Graphing y = f(x) beside each choice (T13) shows the same thing for every x < -3. The structural argument by hand is faster.

</details>

---

### 87. adv-rational-binomial-ratio-difference

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

For $x \neq -1$ and $x \neq 1$, which expression is equivalent to $\frac{x + 1}{x - 1} - \frac{x - 1}{x + 1}$?

- **A.** $\frac{-4x}{x^2 - 1}$
- **B.** $\frac{2x}{x^2 - 1}$
- **C.** $\frac{4x + 2}{x^2 - 1}$
- **D.** $\frac{4x}{x^2 - 1}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The common denominator is (x - 1)(x + 1) = x^2 - 1. The numerator is (x + 1)^2 - (x - 1)^2 = (x^2 + 2x + 1) - (x^2 - 2x + 1) = 4x. Therefore, the expression is equivalent to (4x)/(x^2 - 1). Alternate approach: the numerator is a difference of squares, [(x + 1) - (x - 1)][(x + 1) + (x - 1)] = 2 · 2x = 4x. Distractors: (-4x)/(x^2 - 1) subtracts in the wrong order; (2x)/(x^2 - 1) writes the square of each binomial with x instead of 2x as the middle term; (4x + 2)/(x^2 - 1) distributes the minus sign to the middle term but not to the constant 1.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x+1}{x-1}-\frac{x-1}{x+1}</code><br><code>y=\frac{4x}{x^2-1}</code>

Graph the given expression and each choice (T13). Only y = 4x/(x^2 - 1) lies exactly on top of it; the choice with -4x is its reflection, so check the sign of one branch (at x = 2 the given expression is 3 - 1/3 = 8/3, which is positive).

</details>

---

### 88. adv-rational-exponent-coefficient-quotient

*Hard · Multiple choice · route: hand-primary · techniques: T13*

For $x > 0$, which expression is equivalent to $\frac{(8x^3)^{2/3}}{\sqrt{16x}}$?

- **A.** $\frac{1}{4}x^{3/2}$
- **B.** $\frac{1}{2}x^{3/2}$
- **C.** $x^{3/2}$
- **D.** $x^{5/2}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** In the numerator, (8x^3)^{2/3} = 8^{2/3} · x^{3 · 2/3} = 4x^2, since the cube root of 8 is 2 and 2^2 = 4. In the denominator, sqrt(16x) = sqrt(16) · x^{1/2} = 4x^{1/2}. Dividing yields (4x^2)/(4x^{1/2}) = x^{2 - 1/2} = x^{3/2}. Therefore, the expression is equivalent to x^{3/2}. Distractors: (1)/(4)x^{3/2} forgets the square root of 16 and divides 4 by 16; (1)/(2)x^{3/2} takes half of 16 instead of its square root; x^{5/2} adds the exponents 2 and 1/2 instead of subtracting them.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{(8x^3)^{2/3}}{\sqrt{16x}}</code><br><code>y=x^{3/2}</code>

For x > 0 the two graphs coincide (T13). The choices differ only by a coefficient or an exponent, so the curves sit close together near x = 1; zoom out before deciding. The hand route is faster.

</details>

---

### 89. adv-rational-exponent-simplify

*Hard · Multiple choice · route: hand-primary · techniques: T13*

For $x > 0$, which expression is equivalent to $\frac{x^{3/4} \cdot \sqrt{x}}{\sqrt[4]{x}}$?

- **A.** $x^{1/8}$
- **B.** $x$
- **C.** $x^{3/2}$
- **D.** $x^{5}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Write every factor as a power of x: the square root of x is x^(1/2) and the fourth root of x is x^(1/4). Multiplying powers of the same base adds the exponents and dividing subtracts them, so the exponent is 3/4 + 1/2 - 1/4 = 1. Therefore, the expression equals x^1 = x. Distractors: x^(1/8) multiplies the numerator's exponents (3/4 · 1/2 = 3/8) instead of adding them; x^(3/2) adds the denominator's exponent instead of subtracting it; x^5 divides the exponent 5/4 by 1/4 instead of subtracting.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x^{3/4}\sqrt{x}}{\sqrt[4]{x}}</code><br><code>y=x</code>

Graph the given expression and each choice for x > 0 (T13); only y = x lies on top of it. Adding the exponents by hand takes a few seconds, so Desmos is only a check here.

</details>

---

### 90. adv-rational-product-four-factors

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

For $x > 3$, which expression is equivalent to $\frac{2x^2 + 5x - 3}{x^2 - 9} \cdot \frac{x - 3}{4x^2 - 1}$?

- **A.** $\frac{1}{2x + 1}$
- **B.** $\frac{1}{2x - 1}$
- **C.** $\frac{x - 3}{(x + 3)(2x - 1)}$
- **D.** $\frac{x + 3}{(x - 3)(2x + 1)}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Factor every polynomial: 2x^2 + 5x - 3 = (2x - 1)(x + 3), x^2 - 9 = (x - 3)(x + 3), and 4x^2 - 1 = (2x - 1)(2x + 1). The product is (2x - 1)(x + 3)(x - 3) / ((x - 3)(x + 3)(2x - 1)(2x + 1)). Canceling (2x - 1), (x + 3) and (x - 3) yields 1/(2x + 1). Distractors: (1)/(2x - 1) factors 4x^2 - 1 as (2x - 1)^2; (x - 3)/((x + 3)(2x - 1)) factors 2x^2 + 5x - 3 as (2x + 1)(x - 3); (x + 3)/((x - 3)(2x + 1)) factors x^2 - 9 as (x - 3)^2.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{2x^2+5x-3}{x^2-9}\cdot\frac{x-3}{4x^2-1}</code><br><code>y=\frac{1}{2x+1}</code>

Graph the product and each choice (T13) and compare them for x > 3. Only y = 1/(2x + 1) lies on top of the product there; y = 1/(2x - 1) is close for large x, so zoom in near x = 4 to separate them.

</details>

---

### 91. adv-rational-remainder

*Hard · Student-produced response · route: desmos-primary · techniques: T6*

The expression $\frac{6x^2 + 7x - 13}{2x + 5}$ is equivalent to $3x - 4 + \frac{k}{2x + 5}$, where $k$ is a constant and $x \neq -\frac{5}{2}$. What is the value of $k$?

**Answer:** 7

<details><summary>Solutions</summary>

**By hand.** Multiply through by 2x + 5: 6x^2 + 7x - 13 = (3x - 4)(2x + 5) + k = 6x^2 + 7x - 20 + k. So k = 7. Polynomial long division gives the same remainder.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3]</code><br><code>\frac{6x_1^2+7x_1-13}{2x_1+5}\sim3x_1-4+\frac{k}{2x_1+5}</code>

The regression returns k = 7.

</details>

---

### 92. adv-rational-structure-difference

*Hard · Multiple choice · route: hand-primary · techniques: T13*

For $x \neq \frac{3}{2}$ and $x \neq -4$, which expression is equivalent to $\frac{4x^2 - 12x + 9}{2x - 3} - \frac{x^2 - 16}{x + 4}$?

- **A.** $x - 7$
- **B.** $x + 1$
- **C.** $3x - 7$
- **D.** $3x + 1$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The first numerator is a perfect square, 4x^2 - 12x + 9 = (2x - 3)^2, so the first fraction simplifies to 2x - 3. The second numerator is a difference of squares, x^2 - 16 = (x - 4)(x + 4), so the second fraction simplifies to x - 4. Subtracting yields (2x - 3) - (x - 4) = x + 1. Distractors: x - 7 subtracts x + 4 instead of x - 4 (the wrong factor was cancelled); 3x - 7 adds the two simplified fractions instead of subtracting; 3x + 1 adds them and also keeps x + 4.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{4x^2-12x+9}{2x-3}-\frac{x^2-16}{x+4}</code><br><code>y=x+1</code>

Graph the original and each choice (T13); the original is a line with two holes, and y = x + 1 lies on it. Recognizing the perfect square and the difference of squares by hand is faster.

</details>

---

### 93. adv-rational-subtract-factor-denominator

*Hard · Multiple choice · route: hand-primary · techniques: T13*

The expression $\frac{x}{x - 2} - \frac{4}{x^2 - 2x}$ is defined for $x \neq 0$ and $x \neq 2$. Which expression is equivalent to the given expression?

- **A.** $\frac{x - 4}{x - 2}$
- **B.** $\frac{x - 2}{x}$
- **C.** $\frac{x^2 - 4}{x - 2}$
- **D.** $\frac{x + 2}{x}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Factoring the second denominator yields x^2 - 2x = x(x - 2), so the common denominator is x(x - 2). Rewriting the first fraction yields x/(x - 2) = x^2/(x(x - 2)), and subtracting yields (x^2 - 4)/(x(x - 2)). The numerator is a difference of squares, (x - 2)(x + 2), so for x not equal to 2 the factor x - 2 cancels and the expression equals (x + 2)/x. Distractors: (x - 4)/(x - 2) subtracts the numerators over the first denominator without finding a common denominator; (x - 2)/(x) cancels the wrong factor after writing x^2 - 4 as (x - 2)(x + 2); (x^2 - 4)/(x - 2) drops the factor x from the common denominator.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{x}{x-2}-\frac{4}{x^2-2x}</code><br><code>y=\frac{x+2}{x}</code>

Graph the given expression and each choice (T13); only y = (x + 2)/x lies on the first graph. Desmos draws the simplified choice through x = 2 where the original has a hole, which is fine: the stem excludes x = 2. Factoring by hand is quicker than typing four fractions.

</details>

---

### 94. adv-rationalize-conjugate-a-plus-b

*Hard · Student-produced response · route: hand-primary · techniques: —*

The expression $\frac{\sqrt{5} + 1}{\sqrt{5} - 1}$ is equivalent to $a + b\sqrt{5}$, where $a$ and $b$ are rational numbers. What is the value of $a + b$?

**Answer:** 2

<details><summary>Solutions</summary>

**By hand.** Multiplying the numerator and the denominator by the conjugate sqrt(5) + 1 yields (sqrt(5) + 1)^2 / ((sqrt(5))^2 - 1^2). The denominator is 5 - 1 = 4, and the numerator is 5 + 2 sqrt(5) + 1 = 6 + 2 sqrt(5). It follows that the expression equals (6 + 2 sqrt(5))/4 = 3/2 + (1/2) sqrt(5), so a = 3/2 and b = 1/2. Therefore, a + b = 3/2 + 1/2 = 2. Desmos shows only a decimal value (about 2.618) for the expression, which does not separate a from b, so this item is done by hand.

</details>

---

### 95. adv-remainder-theorem-k

*Hard · Student-produced response · route: either · techniques: T1*

The function $p$ is defined by $p(x) = x^3 + kx^2 - 5x + 6$, where $k$ is a constant. When $p(x)$ is divided by $x + 2$, the remainder is $12$. What is the value of $k$?

**Answer:** 1

<details><summary>Solutions</summary>

**By hand.** By the remainder theorem, the remainder when p(x) is divided by x + 2 is p(-2). Substituting -2 for x yields p(-2) = -8 + 4k + 10 + 6 = 4k + 8. Setting this equal to 12 yields 4k = 4, so k = 1. A sign slip, evaluating p(2) instead of p(-2), gives 8 + 4k - 10 + 6 = 12, so k = 2, which is wrong.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=(-2)^3+x(-2)^2-5(-2)+6</code><br><code>y=12</code>

The first line is p(-2) with the unknown k typed as x. Click the intersection: (1, 12), so k = 1. This is as fast as the hand method once the remainder theorem is known; without it, Desmos cannot do the division directly.

</details>

---

### 96. adv-symmetric-square

*Hard · Student-produced response · route: hand-primary · techniques: T2*

If $x^2 + y^2 = 50$ and $xy = 7$, what is the value of $(x - y)^2$?

**Answer:** 36

<details><summary>Solutions</summary>

**By hand.** (x - y)^2 = x^2 - 2xy + y^2 = 50 - 2(7) = 36. No need to find x and y.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=50</code><br><code>xy=7</code><br><code>(x-y)^2</code>

The curves meet at (7, 1), (1, 7), (-1, -7) and (-7, -1); any pair gives (x - y)^2 = 36. Expanding by hand is much faster.

</details>

---

### 97. adv-three-factor-coefficient-sum

*Hard · Student-produced response · route: either · techniques: T9*

When the product $(x - 2)(x + 3)(2x - 1)$ is expanded, it can be written as $ax^3 + bx^2 + cx + d$ for all $x$, where $a$, $b$, $c$ and $d$ are constants. What is the value of $a + b + c + d$?

**Answer:** -4

<details><summary>Solutions</summary>

**By hand.** Substituting x = 1 into ax^3 + bx^2 + cx + d yields a + b + c + d, so the sum of the coefficients is the value of the product at x = 1: (1 - 2)(1 + 3)(2 - 1) = (-1)(4)(1) = -4. Therefore, a + b + c + d = -4. Alternate approach: (x - 2)(x + 3) = x^2 + x - 6, and (x^2 + x - 6)(2x - 1) = 2x^3 - x^2 + 2x^2 - x - 12x + 6 = 2x^3 + x^2 - 13x + 6, so a + b + c + d = 2 + 1 - 13 + 6 = -4.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=(x-2)(x+3)(2x-1)</code><br><code>f(1)</code>

Define the product as f (T9). Because a(1)^3 + b(1)^2 + c(1) + d = a + b + c + d, the value f(1) = -4 is the answer; enter -4.

</details>

---

### 98. adv-tilde-recentered-b

*Hard · Student-produced response · route: desmos-primary · techniques: T6*

For all values of $x$, $a(x + 2)^2 + b(x + 2) + c = 3x^2 + 5x - 1$, where $a$, $b$, and $c$ are constants. What is the value of $b$?

**Answer:** -7

<details><summary>Solutions</summary>

**By hand.** Expanding the left side yields a(x^2 + 4x + 4) + bx + 2b + c = ax^2 + (4a + b)x + (4a + 2b + c). Matching coefficients with 3x^2 + 5x - 1 gives a = 3 and 4a + b = 5, so 12 + b = 5 and b = -7. Alternate approach: substituting x = -2 makes the left side c, so c = 3(4) - 10 - 1 = 1; then the x-coefficient equation gives b = -7. A common error is matching b directly with 5, ignoring the 4a contributed by the square.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3]</code><br><code>a(x_1+2)^2+b(x_1+2)+c\sim3x_1^2+5x_1-1</code>

The tilde regression (T6) returns a = 3, b = -7 and c = 1. Read b = -7.

</details>

---

### 99. adv-trinomial-factor-positive-ab

*Hard · Student-produced response · route: either · techniques: T6*

The expression $6x^2 + 7x - 20$ is equivalent to $(ax + 5)(bx - 4)$, where $a$ and $b$ are positive constants. What is the value of $a + b$?

**Answer:** 5

<details><summary>Solutions</summary>

**By hand.** Expanding (ax + 5)(bx - 4) yields abx^2 + (5b - 4a)x - 20. Matching coefficients gives ab = 6 and 5b - 4a = 7. With a and b positive, the integer pairs with ab = 6 are (1, 6), (2, 3), (3, 2) and (6, 1); only a = 2, b = 3 gives 5(3) - 4(2) = 7. Check: (2x + 5)(3x - 4) = 6x^2 - 8x + 15x - 20 = 6x^2 + 7x - 20. Therefore, a + b = 5. (Solving ab = 6 and 5b - 4a = 7 exactly also gives a = -15/4, b = -8/5, which the restriction to positive constants excludes.)

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3]</code><br><code>6x_1^2+7x_1-20\sim(ax_1+5)(bx_1-4)</code>

The regression returns a = 2 and b = 3, so a + b = 5. The identity also holds for a = -15/4 and b = -8/5; if the fit lands there, the stem's 'positive constants' rules it out, so factor by hand instead.

</details>

---

### 100. sample-tilde-constants

*Hard · Student-produced response · route: either · techniques: T6*

For all values of $x$, $(2x + c)(x - 3) = 2x^2 + bx - 15$, where $b$ and $c$ are constants. What is the value of $b$?

**Answer:** -1

<details><summary>Solutions</summary>

**By hand.** Match constant terms: -3c = -15, so c = 5. Match x terms: -6 + c = b, so b = -1.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3]</code><br><code>(2x_1+c)(x_1-3)\sim2x_1^2+bx_1-15</code>

Read the fitted parameters: c = 5 and b = -1.

</details>

---
