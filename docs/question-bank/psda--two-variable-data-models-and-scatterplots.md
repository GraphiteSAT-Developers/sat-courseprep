# Two-variable data: models and scatterplots

[← Question bank index](README.md) · Problem-Solving and Data Analysis · 23 questions, easiest first

### 1. psda-apartment-rent-association

*Easy · Multiple choice · route: hand-primary · techniques: —*

A scatterplot shows the distance $x$, in kilometers, from the city center and the monthly rent $y$, in dollars, for 40 apartments. The points lie close to a straight line, and $y$ tends to decrease as $x$ increases. Which of the following best describes the association between $x$ and $y$?

- **A.** A strong negative linear association
- **B.** A strong positive linear association
- **C.** A weak negative linear association
- **D.** A strong negative nonlinear association

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that y tends to decrease as x increases, so the association is negative. It's also given that the points lie close to a straight line, so the association is linear and strong. Therefore, the association is a strong negative linear association. Distractors: "strong positive" reverses the direction; "weak negative" ignores that the points lie close to the line; "negative nonlinear" ignores that the pattern is a straight line.

</details>

---

### 2. psda-bamboo-shoot-prediction

*Easy · Multiple choice · route: either · techniques: T9*

For a certain type of bamboo, the equation $y = 4.5x + 12$ models the height $y$, in centimeters, of a shoot $x$ days after the shoot is first measured. What height, in centimeters, does the model predict for a shoot 10 days after it is first measured?

- **A.** $16.5$
- **B.** $45$
- **C.** $57$
- **D.** $165$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that y = 4.5x + 12. Substituting 10 for x yields y = 4.5(10) + 12 = 45 + 12 = 57. Therefore, the model predicts a height of 57 centimeters. Distractors: 45 is 4.5(10) without the 12; 16.5 is 4.5 + 12, the prediction for 1 day; 165 is (4.5 + 12)(10), a grouping slip.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=4.5x+12</code><br><code>f(10)</code>

The second line shows 57, the predicted height in centimeters. Substituting by hand is just as fast.

</details>

---

### 3. psda-model-predict-customers

*Easy · Multiple choice · route: either · techniques: T9*

For each of 20 days, a store owner recorded the number of hours $x$ the store was open and the number of customers $y$. The equation $y = 3.5x + 12$ models the relationship. What is the predicted number of customers on a day the store is open for 8 hours?

- **A.** $20$
- **B.** $28$
- **C.** $40$
- **D.** $44$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Substituting 8 for x in y = 3.5x + 12 yields y = 3.5(8) + 12 = 28 + 12 = 40. Therefore, the model predicts 40 customers. Distractors: 28 is 3.5 · 8 without the 12; 20 adds 8 and 12 instead of multiplying 8 by 3.5; 44 rounds 3.5 up to 4 before multiplying.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=3.5x+12</code><br><code>f(8)</code>

f(8) shows 40.

</details>

---

### 4. psda-shipping-weight-rate-interpretation

*Easy · Multiple choice · route: hand-primary · techniques: —*

For 30 packages, a scatterplot shows the weight $x$, in kilograms, and the shipping cost $y$, in dollars, of each package. A line of best fit for the data is $y = 2.4x + 15$. Which statement is the best interpretation of 2.4 in this context?

- **A.** For each additional kilogram of weight, the estimated shipping cost increases by 2.40 dollars.
- **B.** For each additional kilogram of weight, the estimated shipping cost increases by 15.00 dollars.
- **C.** For each additional dollar of shipping cost, the estimated weight increases by 2.4 kilograms.
- **D.** The estimated shipping cost of a package that weighs 0 kilograms is 2.40 dollars.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that the line of best fit is y = 2.4x + 15, where x is the weight in kilograms and y is the shipping cost in dollars. The coefficient of x is the rate of change of the line: each time x increases by 1, the predicted y increases by 2.4. Therefore, for each additional kilogram of weight, the estimated shipping cost increases by 2.40 dollars. Distractors: "increases by 15.00 dollars" interprets the wrong number, since 15 is the constant term; "each additional dollar" of cost reverses the roles of the two variables; a package that "weighs 0 kilograms" describes the y-intercept, whose value is 15, not 2.4.

</details>

---

### 5. psda-bicycle-resale-intercept

*Medium · Multiple choice · route: hand-primary · techniques: —*

For a sample of used bicycles, the equation $y = -35x + 420$ models the resale price $y$, in dollars, of a bicycle that is $x$ years old. Which statement is the best interpretation of 420 in this context?

- **A.** The estimated resale price decreases by 420 dollars for each additional year of age.
- **B.** The highest resale price of any bicycle in the sample is 420 dollars.
- **C.** The estimated age of a bicycle with a resale price of 0 dollars is 420 years.
- **D.** The estimated resale price of a bicycle of age 0 years is 420 dollars.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that y = -35x + 420. Substituting 0 for x yields y = 420, so 420 is the value the model gives for a bicycle that is 0 years old. Therefore, the estimated resale price of a bicycle of age 0 years is 420 dollars. Distractors: "decreases by 420 dollars" each year confuses the constant term with the rate, which is 35 dollars per year; "the highest resale price" treats a model value as an actual data value, but the model describes estimates, not any one bicycle in the sample; a resale price of 0 dollars at "420 years" confuses the y-intercept with the x-intercept, which is 420/35 = 12 years.

</details>

---

### 6. psda-iced-drinks-residual

*Medium · Student-produced response · route: either · techniques: T9*

For 12 days, a café recorded the high temperature $x$, in degrees Fahrenheit, and the number of iced drinks sold, $y$. The data are modeled by $y = 3x - 95$. One day had a high of 80 degrees Fahrenheit and 138 iced drinks sold. What is the residual (actual minus predicted) for that day?

**Answer:** -7

<details><summary>Solutions</summary>

**By hand.** It's given that the line of best fit is y = 3x - 95. Substituting 80 for x yields a predicted value of 3(80) - 95 = 240 - 95 = 145 drinks. A residual is the actual value minus the predicted value, so the residual is 138 - 145 = -7. Therefore, the residual for that day is -7. Reporting 7 subtracts in the wrong order (predicted minus actual), and reporting 145 gives the prediction instead of the residual.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=3x-95</code><br><code>138-f(80)</code>

The second line shows -7. Enter -7: the actual value is below the prediction, so the residual is negative.

</details>

---

### 7. psda-points-above-model-line

*Medium · Multiple choice · route: desmos-primary · techniques: T7*

A scatterplot shows the data points $(1, 2)$, $(2, 3)$, $(3, 7)$, $(4, 11)$, $(5, 14)$, and $(6, 15)$. The equation $y = 3x - 2$ models the data. How many of the data points lie above the line that represents the model?

- **A.** $2$
- **B.** $3$
- **C.** $4$
- **D.** $5$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A point lies above the line when its actual y-value exceeds the predicted value 3x - 2, that is, when its residual is positive. The predicted values at x = 1 through 6 are 1, 4, 7, 10, 13 and 16, so the residuals are 1, -1, 0, 1, 1 and -1. Three residuals are positive. Therefore, 3 of the points lie above the line. Distractors: 2 counts the points below the line (negative residuals), as if residuals were predicted minus actual; 4 also counts (3, 7), which lies on the line; 5 counts every point that is not on the line.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4,5,6]</code><br><code>y_1=[2,3,7,11,14,15]</code><br><code>y_1-(3x_1-2)</code>

The last line shows the residual list [1, -1, 0, 1, 1, -1]. Count the positive entries: 3. The 0 is a point on the line, not above it.

</details>

---

### 8. psda-points-constant-ratio-relationship

*Medium · Multiple choice · route: either · techniques: T5*

A data set consists of the points $(0, 400)$, $(1, 300)$, $(2, 225)$, and $(3, 168.75)$. Which statement best describes the relationship between $x$ and $y$ for these points?

- **A.** Linear: $y$ decreases by 100 for each increase of 1 in $x$.
- **B.** Linear: $y$ decreases by 25% for each increase of 1 in $x$.
- **C.** Exponential: $y$ decreases by 75% for each increase of 1 in $x$.
- **D.** Exponential: $y$ decreases by 25% for each increase of 1 in $x$.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The first differences are 300 - 400 = -100, 225 - 300 = -75 and 168.75 - 225 = -56.25, which are not equal, so the relationship is not linear. The ratios are 300/400 = 0.75, 225/300 = 0.75 and 168.75/225 = 0.75, which are equal, so the relationship is exponential: each increase of 1 in x multiplies y by 0.75, a decrease of 25%. Therefore, the relationship is exponential and y decreases by 25% for each increase of 1 in x. Distractors: "Linear" with "decreases by 100" uses only the first difference; "Linear" with 25% finds the right percent but calls a constant-percent change linear; "decreases by 75%" mistakes the factor 0.75 that is kept for the percent that is lost.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3]</code><br><code>y_1=[400,300,225,168.75]</code><br><code>y_1\sim ab^{x_1}</code>

The exponential fit is exact: a = 400 and b = 0.75, so each step keeps 75% of y, a 25% decrease. Checking the ratios by hand is about as fast.

</details>

---

### 9. psda-points-leveling-association

*Medium · Multiple choice · route: hand-primary · techniques: —*

A data set consists of the points $(1, 20)$, $(2, 31)$, $(3, 37)$, $(4, 40)$, $(5, 41)$, and $(6, 41.5)$. Which of the following best describes the association between $x$ and $y$ shown by a scatterplot of these points?

- **A.** A negative nonlinear association
- **B.** A positive linear association
- **C.** A positive nonlinear association
- **D.** No association

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** As x increases, every y-value is larger than the one before, so the association is positive. The increases are 11, 6, 3, 1 and 0.5, which shrink instead of staying constant, so the points bend and level off rather than following a line. Therefore, the association is a positive nonlinear association. Distractors: "positive linear" notices the direction but not the shrinking increases; "negative nonlinear" mistakes the shrinking increases for decreasing values of y; "no association" looks only at the last few points, where y barely changes.

</details>

---

### 10. psda-printer-value-decay-interpretation

*Medium · Multiple choice · route: hand-primary · techniques: —*

The value $y$, in dollars, of a certain office printer $x$ years after it is purchased is modeled by $y = 640(0.85)^x$. Which statement is the best interpretation of 0.85 in this context?

- **A.** The estimated value decreases by 0.85 dollars each year.
- **B.** The estimated value decreases by 15 dollars each year.
- **C.** The estimated value decreases by 85% each year.
- **D.** The estimated value decreases by 15% each year.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** It's given that y = 640(0.85)^x. Each time x increases by 1, the value is multiplied by 0.85, so each year the printer keeps 85% of its value and loses 1 - 0.85 = 0.15, or 15%. Therefore, the estimated value decreases by 15% each year. Distractors: "0.85 dollars each year" reads the factor as a constant amount, as if the model were linear; "15 dollars each year" turns the 15% into a fixed amount; "85% each year" mistakes the share kept for the share lost.

</details>

---

### 11. psda-residual-from-model

*Medium · Multiple choice · route: desmos-primary · techniques: T9*

A scatterplot shows the relationship between two variables, $x$ and $y$. The equation $y = 4.5x + 2$ models the relationship. One of the data points in the scatterplot is $(6, 31)$. By how much does the actual value of $y$ for this data point exceed the value of $y$ predicted by the model?

- **A.** $2$
- **B.** $4$
- **C.** $27$
- **D.** $29$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The model's predicted value at x = 6 is 4.5(6) + 2 = 27 + 2 = 29. The actual value is 31, so the actual value exceeds the predicted value by 31 - 29 = 2. Distractors: 29 is the predicted value itself; 27 is 4.5 · 6 without the 2; 4 is 31 - 27, subtracting the predicted value computed without the 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=4.5x+2</code><br><code>31-f(6)</code>

The second line shows 2: the actual value minus the predicted value.

</details>

---

### 12. psda-tidal-pool-quadratic-fit

*Medium · Multiple choice · route: desmos-primary · techniques: T5, T13*

The depth $y$, in centimeters, of water in a tidal pool was measured $x$ hours after noon. The data are $(0, 5)$, $(1, 8)$, $(2, 9)$, $(3, 8)$, and $(4, 5)$. Which equation represents $y$ in terms of $x$ for all five data points?

- **A.** $y = 4x + 5$
- **B.** $y = -x^2 + 5$
- **C.** $y = x^2 - 4x + 5$
- **D.** $y = -x^2 + 4x + 5$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The y-values rise from 5 to 9 and then fall back to 5, so the relationship is not linear and the model opens downward. Substituting x = 0 into y = -x^2 + 4x + 5 yields y = 5, substituting x = 1 yields -1 + 4 + 5 = 8, substituting x = 2 yields -4 + 8 + 5 = 9, and the symmetry about x = 2 gives 8 at x = 3 and 5 at x = 4, matching every data point. Distractors: y = 4x + 5 is the line through the first two points only and gives 13 at x = 2; y = -x^2 + 5 keeps the y-value at x = 0 but drops the linear term and gives 4 at x = 1; y = x^2 - 4x + 5 has the sign of the squared term reversed and gives 1, not 9, at x = 2.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3,4]</code><br><code>y_1=[5,8,9,8,5]</code><br><code>y_1\sim ax_1^2+bx_1+c</code>

The quadratic regression gives a = -1, b = 4 and c = 5 with every residual 0, so y = -x^2 + 4x + 5 fits exactly. The table points rise and then fall, so a linear regression would not fit.

</details>

---

### 13. psda-tree-species-equal-height

*Medium · Multiple choice · route: desmos-primary · techniques: T9, T13*

For two species of tree, lines of best fit model the height $y$, in meters, of a tree that is $x$ years old. Species A: $y = 0.5x + 2.4$. Species B: $y = 0.35x + 4.2$. According to the models, at what age, in years, do trees of the two species have the same predicted height?

- **A.** $3.6$
- **B.** $8.4$
- **C.** $12$
- **D.** $44$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The predicted heights are equal when 0.5x + 2.4 = 0.35x + 4.2. Subtracting 0.35x and 2.4 from both sides yields 0.15x = 1.8, so x = 1.8/0.15 = 12. Therefore, the trees have the same predicted height at 12 years. Distractors: 8.4 is the common predicted height, 0.5(12) + 2.4, not the age; 3.6 is 1.8/0.5, dividing by species A's rate alone; 44 is (2.4 + 4.2)/0.15, adding the intercepts instead of subtracting them.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=0.5x+2.4</code><br><code>g(x)=0.35x+4.2</code><br><code>f(12)-g(12)</code>

The two lines cross at (12, 8.4) when graphed; the third line shows 0, confirming the age 12. Read the x-coordinate, not the height 8.4.

</details>

---

### 14. psda-best-fit-predict-eight

*Hard · Student-produced response · route: desmos-primary · techniques: T5, T9, T11*

A scatterplot shows the five data points $(1, 3.2)$, $(2, 5.1)$, $(3, 6.6)$, $(4, 8.9)$, and $(5, 10.7)$. Graphed in the $xy$-plane, the line of best fit found by least-squares regression has slope 1.88. What is the $y$-value predicted by the line of best fit when $x = 8$?

**Answer:** 163/10 (≈ 16.3)

<details><summary>Solutions</summary>

**By hand.** The least-squares line passes through the point of means, (3, 6.9), and its slope is the sum of (x - 3)(y - 6.9) divided by the sum of (x - 3)^2. The x-deviations are -2, -1, 0, 1, 2, so the numerator is -2(3.2) - 1(5.1) + 0 + 1(8.9) + 2(10.7) = 18.8 and the denominator is 10, giving slope 1.88. Then the intercept is 6.9 - 1.88(3) = 1.26, and at x = 8 the prediction is 1.88(8) + 1.26 = 16.3. On the test this is a regression problem, not a hand computation; the line through the first and last points (slope 1.875) gives a slightly different prediction and is not the least-squares line.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4,5]</code><br><code>y_1=[3.2,5.1,6.6,8.9,10.7]</code><br><code>y_1\sim mx_1+b</code><br><code>8m+b</code>

The regression gives m = 1.88 and b = 1.26, and 8m + b shows 16.3. Use the stored m and b, not retyped decimals. Enter 16.3.

</details>

---

### 15. psda-candle-height-regression

*Hard · Multiple choice · route: desmos-primary · techniques: T5*

The height $y$, in centimeters, of a burning candle was measured $x$ hours after it was lit. The data are $(1, 18.6)$, $(2, 16.9)$, $(3, 15.5)$, $(4, 13.4)$, and $(5, 12.1)$. Which equation represents the least-squares regression line for these measurements?

- **A.** $y = -1.65x + 20.25$
- **B.** $y = -1.65x + 18.6$
- **C.** $y = -1.65x + 15.3$
- **D.** $y = 1.65x + 10.35$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The least-squares line always passes through the point of means. Here x̄ = 15/5 = 3 and ȳ = 76.5/5 = 15.3. The heights decrease as time increases, so the slope is negative. The slope is Σ(x - x̄)(y - ȳ) / Σ(x - x̄)^2 = -16.5/10 = -1.65, and the intercept is 15.3 - (-1.65)(3) = 15.3 + 4.95 = 20.25. Therefore, the line is y = -1.65x + 20.25. Alternate approach: of the choices, only -1.65x + 20.25 and 1.65x + 10.35 pass through (3, 15.3), and only the first has the negative slope the data show. Distractors: -1.65x + 18.6 uses the first height as the intercept; -1.65x + 15.3 uses ȳ as the intercept, forgetting to adjust for x̄ = 3; 1.65x + 10.35 passes through the means but has the sign of the slope reversed.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4,5]</code><br><code>y_1=[18.6,16.9,15.5,13.4,12.1]</code><br><code>y_1\sim mx_1+b</code>

The regression gives m = -1.65 and b = 20.25, so the line is y = -1.65x + 20.25.

</details>

---

### 16. psda-cells-exponential-model

*Hard · Multiple choice · route: desmos-primary · techniques: T5, T13*

A biologist records the number of cells $y$ in a culture $x$ hours after an experiment begins. The data are $(0, 64)$, $(1, 80)$, $(2, 100)$, and $(3, 125)$. Which of the following equations best models the relationship between $x$ and $y$?

- **A.** $y = 16x + 64$
- **B.** $y = 20.3x + 61.8$
- **C.** $y = 64(1.25)^x$
- **D.** $y = 80(1.25)^x$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Check how y changes for each increase of 1 in x. The differences are 16, 20 and 25, which are not constant, so a linear model does not fit. The ratios are 80/64 = 1.25, 100/80 = 1.25 and 125/100 = 1.25, which are constant, so the relationship is exponential with growth factor 1.25 and initial value y = 64 at x = 0. Therefore, y = 64(1.25)^x. Distractors: y = 16x + 64 is the line through the first two points only; y = 20.3x + 61.8 is the linear line of best fit, which a linear regression produces but which does not pass through any of the points; y = 80(1.25)^x uses the value at x = 1 as the initial value.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3]</code><br><code>y_1=[64,80,100,125]</code><br><code>y_1\sim ab^{x_1}</code><br><code>y_1\sim mx_1+c</code>

The exponential regression gives a = 64 and b = 1.25 with every residual 0, so it fits the data exactly. The linear regression gives m ≈ 20.3 and c ≈ 61.8 but leaves residuals, so the exponential model is the better one.

</details>

---

### 17. psda-exhibit-visitors-models-compare

*Hard · Student-produced response · route: desmos-primary · techniques: T9*

Two models estimate the number of visitors $y$ to a museum exhibit during week $x$ after it opens. Model A is $y = 1200 + 150x$ and model B is $y = 1200(1.1)^x$. What is the least whole number of weeks $x$ for which model B predicts more visitors than model A?

**Answer:** 6

<details><summary>Solutions</summary>

**By hand.** Model A adds 150 visitors each week; model B multiplies by 1.1 each week. By repeated multiplication, (1.1)^2 = 1.21, (1.1)^3 = 1.331, (1.1)^4 = 1.4641, (1.1)^5 = 1.61051 and (1.1)^6 = 1.771561. Comparing the models week by week: at x = 5, model A gives 1200 + 750 = 1950 and model B gives 1200(1.1)^5 ≈ 1932.6, so model A is still higher. At x = 6, model A gives 1200 + 900 = 2100 and model B gives 1200(1.1)^6 ≈ 2125.9, so model B is higher. Therefore, the least whole number of weeks is 6. Answering 1 assumes the 10% growth (120 visitors) beats 150 from the start; answering 5 stops at the last week model A is still ahead.

**Desmos** (not yet verified in Desmos). Type:<br><code>f(x)=1200+150x</code><br><code>g(x)=1200(1.1)^x</code><br><code>g(5)-f(5)</code><br><code>g(6)-f(6)</code>

g(5) - f(5) is about -17.4 (model A still higher) and g(6) - f(6) is about 25.9 (model B higher), so enter 6. Graphing y = f(x) and y = g(x) shows the curves cross near x = 5.8.

</details>

---

### 18. psda-forum-members-exponential-fit

*Hard · Multiple choice · route: desmos-primary · techniques: T5, T13*

The number of members $y$ of an online forum was recorded $x$ months after the forum launched. The data are $(0, 118)$, $(1, 152)$, $(2, 186)$, $(3, 236)$, and $(4, 291)$. Which equation is the best model for these data?

- **A.** $y = 43x + 110.6$
- **B.** $y = 119.4(1.025)^x$
- **C.** $y = 152(1.25)^x$
- **D.** $y = 119.4(1.25)^x$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The ratios of consecutive values are 152/118 ≈ 1.29, 186/152 ≈ 1.22, 236/186 ≈ 1.27 and 291/236 ≈ 1.23, all close to 1.25, while the differences 34, 34, 50 and 55 grow. So the data grow by about 25% each month, an exponential pattern with a starting value near 118 at x = 0. Therefore, the best model is y = 119.4(1.25)^x. Distractors: 43x + 110.6 is the least-squares linear fit, which misses the growing differences; 119.4(1.025)^x writes 25% growth as a factor of 1.025; 152(1.25)^x uses the value at x = 1 as the starting value, so it overestimates every point.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,1,2,3,4]</code><br><code>y_1=[118,152,186,236,291]</code><br><code>y_1\sim ab^{x_1}</code><br><code>y=43x+110.6</code>

The exponential regression gives a ≈ 119.4 and b ≈ 1.25. Graphing the linear choice next to the table shows it runs above the middle points and below the ends, while the exponential curve follows them.

</details>

---

### 19. psda-newsletter-linear-vs-exponential

*Hard · Student-produced response · route: desmos-primary · techniques: T5, T9, T11*

A newsletter had 250 subscribers when a campaign began and 360 subscribers 2 months later. Model L assumes the same increase each month; model E assumes the same percent increase each month. How much greater is model E's prediction than model L's for 4 months after the campaign began?

**Answer:** 242/5 (≈ 48.4)

<details><summary>Solutions</summary>

**By hand.** Model L increases by the same amount each month: (360 - 250)/2 = 55 subscribers per month, so after 4 months it predicts 250 + 55(4) = 470. Model E multiplies by the same factor b each month, so 250b^2 = 360, b^2 = 1.44, and b = 1.2 (a 20% increase per month). After 4 months it predicts 250(1.2)^4 = 518.4. The difference is 518.4 - 470 = 48.4. Using 1.44 as the monthly factor, or comparing at 2 months (where both models give 360, a difference of 0), are the common slips.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[0,2]</code><br><code>y_1=[250,360]</code><br><code>y_1\sim mx_1+k</code><br><code>y_1\sim ab^{x_1}</code><br><code>ab^4-(4m+k)</code>

The linear regression gives m = 55 and k = 250; the exponential regression gives a = 250 and b = 1.2. The last line shows 48.4. Use the parameter names, not retyped decimals, so the result is exact.

</details>

---

### 20. psda-regression-line

*Hard · Multiple choice · route: desmos-primary · techniques: T5*

A seedling's height $y$, in centimeters, was recorded $x$ weeks after planting: $(1, 4.0)$, $(2, 6.5)$, $(3, 7.0)$, $(4, 9.5)$, $(5, 11.0)$. Which equation gives the least-squares line of best fit for these data?

- **A.** $y = 1.7x + 2.5$
- **B.** $y = 1.7x + 4$
- **C.** $y = 1.75x + 2.25$
- **D.** $y = 2.5x + 1.7$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Means: x̄ = 3, ȳ = 7.6. Slope = Σ(x - x̄)(y - ȳ) / Σ(x - x̄)^2 = 17/10 = 1.7; intercept = 7.6 - 1.7(3) = 2.5. Nobody computes this by hand on the test; the fast elimination is that the best-fit line must pass through (x̄, ȳ) = (3, 7.6), which only y = 1.7x + 2.5 does. Distractors: 1.75x + 2.25 is the line through the first and last points, 1.7x + 4 uses the first y-value as the intercept, 2.5x + 1.7 swaps slope and intercept.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,3,4,5]</code><br><code>y_1=[4,6.5,7,9.5,11]</code><br><code>y_1\sim mx_1+b</code>

The regression gives m = 1.7 and b = 2.5.

</details>

---

### 21. psda-spring-length-regression-prediction

*Hard · Student-produced response · route: desmos-primary · techniques: T5, T9*

The length $y$, in millimeters, of a spring was measured with a mass of $x$ grams hanging from it. The data are $(10, 52)$, $(20, 57)$, $(30, 61)$, $(40, 66)$, and $(50, 69)$. Graphed in the $xy$-plane, the least-squares regression line for these data has slope 0.43. Based on the least-squares regression line, what is the predicted length, in millimeters, for a mass of 60 grams?

**Answer:** 739/10 (≈ 73.9)

<details><summary>Solutions</summary>

**By hand.** The least-squares line passes through the means x̄ = 30 and ȳ = 305/5 = 61. Its slope is Σ(x - x̄)(y - ȳ) / Σ(x - x̄)^2 = 430/1000 = 0.43, so the intercept is 61 - 0.43(30) = 61 - 12.9 = 48.1. Substituting 60 for x yields 0.43(60) + 48.1 = 25.8 + 48.1 = 73.9. Therefore, the predicted length is 73.9 millimeters. Extending the last two points instead (69 + 3 = 72) or the first and last points (69 + 4.25 = 73.25) ignores the middle data and gives a different line.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[10,20,30,40,50]</code><br><code>y_1=[52,57,61,66,69]</code><br><code>y_1\sim mx_1+b</code><br><code>m(60)+b</code>

The regression gives m = 0.43 and b = 48.1; the last line shows 73.9. Enter 73.9.

</details>

---

### 22. psda-study-hours-intercept-from-means

*Hard · Multiple choice · route: desmos-primary · techniques: T5, T7*

For 5 students, the hours $x$ spent studying and the quiz scores $y$ were $(1, 58)$, $(2, 66)$, $(4, 75)$, $(5, 81)$, and $(8, 90)$. The least-squares regression line for these data is $y = 4.5x + b$, where $b$ is a constant. What is the value of $b$?

- **A.** $53.5$
- **B.** $56$
- **C.** $69.5$
- **D.** $74$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The least-squares regression line always passes through the point of means (x̄, ȳ). Here x̄ = (1 + 2 + 4 + 5 + 8)/5 = 4 and ȳ = (58 + 66 + 75 + 81 + 90)/5 = 370/5 = 74. Substituting (4, 74) into y = 4.5x + b yields 74 = 18 + b, so b = 56. Therefore, the value of b is 56. Distractors: 53.5 substitutes the first data point, 58 - 4.5, but the regression line need not pass through any data point; 69.5 is 74 - 4.5, forgetting to multiply the slope by x̄ = 4; 74 is ȳ itself.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[1,2,4,5,8]</code><br><code>y_1=[58,66,75,81,90]</code><br><code>y_1\sim mx_1+b</code>

The regression gives m = 4.5 and b = 56. As a check, mean(x\_1) = 4 and mean(y\_1) = 74, and 74 - 4.5(4) = 56.

</details>

---

### 23. psda-ticket-price-revenue-quadratic

*Hard · Student-produced response · route: desmos-primary · techniques: T5, T9*

A theater recorded the revenue $y$, in dollars, from one show at each ticket price of $x$ dollars: $(10, 1500)$, $(15, 1875)$, $(20, 2000)$, $(25, 1875)$, and $(30, 1500)$. A quadratic model fits these data exactly. What revenue, in dollars, does the model predict for a ticket price of 35 dollars?

**Answer:** 875

<details><summary>Solutions</summary>

**By hand.** The revenues rise to 2000 at x = 20 and fall symmetrically, so the vertex of the quadratic is (20, 2000) and the model is y = a(x - 20)^2 + 2000. Substituting (10, 1500) yields 1500 = 100a + 2000, so a = -5. Substituting 35 for x yields y = -5(15)^2 + 2000 = -1125 + 2000 = 875. Therefore, the model predicts a revenue of 875 dollars. Alternate approach: by symmetry about x = 20, the prediction at 35 equals the prediction at 5, and the first differences 375, 125, -125, -375 fall by 250 each step, so the next difference is -625 and 1500 - 625 = 875. Continuing the last linear step (1500 - 375 = 1125) misses that the drop grows each step.

**Desmos** (not yet verified in Desmos). Type:<br><code>x_1=[10,15,20,25,30]</code><br><code>y_1=[1500,1875,2000,1875,1500]</code><br><code>y_1\sim ax_1^2+bx_1+c</code><br><code>a(35)^2+b(35)+c</code>

The quadratic fit is exact (a = -5, b = 200, c = 0) and the last line shows 875.

</details>

---
