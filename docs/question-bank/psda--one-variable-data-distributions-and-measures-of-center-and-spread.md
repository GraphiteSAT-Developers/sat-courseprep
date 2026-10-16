# One-variable data: distributions and measures of center and spread

[← Question bank index](README.md) · Problem-Solving and Data Analysis · 23 questions, easiest first

### 1. psda-homework-minutes-median

*Easy · Multiple choice · route: either · techniques: T7*

The numbers of minutes that 8 students spent on homework last night are 34, 18, 27, 45, 22, 30, 41, and 25. What is the median number of minutes the 8 students spent on homework?

- **A.** $33.5$
- **B.** $30$
- **C.** $28.5$
- **D.** $27$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Ordering the 8 values yields 18, 22, 25, 27, 30, 34, 41, 45. With an even number of values, the median is the mean of the 4th and 5th values: (27 + 30)/2 = 28.5. Therefore, the median is 28.5 minutes. Distractors: 33.5 averages the 4th and 5th values of the unsorted list (45 and 22); 30 is the 5th value alone; 27 is the 4th value alone.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[34,18,27,45,22,30,41,25]</code><br><code>\operatorname{median}(L)</code>

median(L) shows 28.5. Desmos sorts the list for you, which avoids the unsorted-list trap.

</details>

---

### 2. psda-missing-fifth-value-mean

*Easy · Multiple choice · route: either · techniques: T1*

A data set consists of the five values 12, 15, 9, 20, and $x$. The mean of the data set is 15. What is the value of $x$?

- **A.** $14$
- **B.** $15$
- **C.** $19$
- **D.** $75$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A mean of 15 for five values means the values add to 5 · 15 = 75. The four known values add to 12 + 15 + 9 + 20 = 56, so x = 75 − 56 = 19. Distractors: 14 is the mean of the four known values (56/4); 15 is the mean itself; 75 is the sum of all five values.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{12+15+9+20+x}{5}</code><br><code>y=15</code>

Click the intersection of the two lines and read x = 19.

</details>

---

### 3. psda-pets-dot-plot-range

*Easy · Multiple choice · route: hand-primary · techniques: T7*

A dot plot shows the number of pets owned by each of 12 students. The plot has 3 dots at 0, 4 dots at 1, 2 dots at 2, 2 dots at 3, and 1 dot at 6. What is the range of the numbers of pets owned by the 12 students?

- **A.** $6$
- **B.** $5$
- **C.** $4$
- **D.** $3$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The range is the greatest value minus the least value. The values run from 0 pets (3 dots) to 6 pets (1 dot), so the range is 6 − 0 = 6. Distractors: 5 counts the distinct values (0, 1, 2, 3 and 6); 4 is the greatest number of dots at one value; 3 is the range of the dot counts (4 − 1) rather than of the values.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[0,0,0,1,1,1,1,2,2,3,3,6]</code><br><code>\operatorname{max}(L)-\operatorname{min}(L)</code>

The second line shows 6. Typing all 12 values is slower than reading the greatest and least values off the description.

</details>

---

### 4. psda-add-value-mean-median-amounts

*Medium · Multiple choice · route: hand-primary · techniques: T7*

The data set $4, 7, 7, 9, 12, 15$ has six values. A seventh value, 30, is added to the data set. Which of the following correctly describes how the mean and the median change?

- **A.** The mean increases by 3, and the median remains the same.
- **B.** The mean increases by 3, and the median increases by 1.
- **C.** The mean increases by 3, and the median increases by 3.
- **D.** The mean increases by 5, and the median increases by 1.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The six values add to 54, so the mean is 54/6 = 9; the median is the mean of the 3rd and 4th values, (7 + 9)/2 = 8. After 30 is added, the seven values add to 84, so the mean is 84/7 = 12, and the median is the 4th value, 9. Therefore, the mean increases by 3 and the median increases by 1. Distractors: 'the median remains the same' assumes an added outlier never moves the median; 'the median increases by 3' assumes every measure of center shifts by the same amount; 'the mean increases by 5' divides the new total 84 by 6 instead of 7.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[4,7,7,9,12,15]</code><br><code>M=[4,7,7,9,12,15,30]</code><br><code>\operatorname{mean}(M)-\operatorname{mean}(L)</code><br><code>\operatorname{median}(M)-\operatorname{median}(L)</code>

The last two lines show 3 and 1. The sums and middle values are quick by hand, so use Desmos as a check.

</details>

---

### 5. psda-bakery-ovens-combined-mean

*Medium · Student-produced response · route: either · techniques: T9*

A bakery weighed 16 loaves of bread from oven A and 24 loaves from oven B. The loaves from oven A had a mean mass of 480 grams, and the loaves from oven B had a mean mass of 455 grams. What is the mean mass, in grams, of all 40 loaves?

**Answer:** 465

<details><summary>Solutions</summary>

**By hand.** The total mass of the oven A loaves is 16 · 480 = 7,680 grams and of the oven B loaves is 24 · 455 = 10,920 grams. The combined total is 18,600 grams, and dividing by 40 loaves yields 465. Therefore, the mean mass of all 40 loaves is 465 grams. Averaging the two means (467.5) ignores that oven B has more loaves.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{16\cdot480+24\cdot455}{40}</code>

The line shows 465. Enter 465. Weight each mean by its number of loaves; averaging 480 and 455 gives 467.5, which is wrong.

</details>

---

### 6. psda-books-frequency-mean

*Medium · Student-produced response · route: desmos-primary · techniques: T7, T11*

A teacher recorded the number of books each of 15 students read last month. Of the 15 students, 4 read 0 books, 6 read 1 book, 3 read 2 books, and 2 read 4 books. What is the mean number of books read per student?

**Answer:** 4/3 (≈ 1.333)

<details><summary>Solutions</summary>

**By hand.** The mean is the total number of books divided by the number of students. The total is 4 · 0 + 6 · 1 + 3 · 2 + 2 · 4 = 0 + 6 + 6 + 8 = 20 books. Dividing by 15 students yields 20/15 = 4/3. Averaging the four values 0, 1, 2 and 4 (7/4) ignores the frequencies.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[0,0,0,0,1,1,1,1,1,1,2,2,2,4,4]</code><br><code>\operatorname{mean}(L)</code>

Repeat each value as many times as its frequency, then mean(L) shows 1.333. The fraction toggle gives 4/3. Enter 4/3, 1.333 or 1.334; 1.33 is marked wrong.

</details>

---

### 7. psda-fish-length-box-plot-iqr

*Medium · Multiple choice · route: hand-primary · techniques: —*

A box plot summarizes the lengths of 40 fish. The minimum is 18 centimeters, the first quartile is 24 centimeters, the median is 29 centimeters, the third quartile is 33 centimeters, and the maximum is 47 centimeters. What is the interquartile range, in centimeters, of the lengths?

- **A.** $4$
- **B.** $9$
- **C.** $14$
- **D.** $29$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The interquartile range is the third quartile minus the first quartile: 33 − 24 = 9. Therefore, the interquartile range is 9 centimeters. Distractors: 4 is the third quartile minus the median, only the upper half of the box; 14 is the maximum minus the third quartile, the upper whisker; 29 is the range (47 − 18).

</details>

---

### 8. psda-flaws-mean-minus-median

*Medium · Student-produced response · route: desmos-primary · techniques: T7, T11*

During one week, an inspector recorded the number of flaws on each of 20 panels. There were 0 flaws on 6 of the panels, 1 flaw on 9 of the panels, and 3 flaws on 5 of the panels. How much greater is the mean number of flaws per panel than the median number of flaws per panel?

**Answer:** 1/5 (≈ 0.2)

<details><summary>Solutions</summary>

**By hand.** The total number of flaws is 0(6) + 1(9) + 3(5) = 24, so the mean is 24/20 = 1.2 flaws per panel. In the sorted list of 20 values, the 10th and 11th values are both 1 (the first 6 values are 0 and the next 9 are 1), so the median is 1. Therefore, the mean is 1.2 - 1 = 0.2 greater than the median. Using the median of the three listed values (1) and the mean of 0, 1 and 3 (4/3) instead of weighting by the counts gives 1/3, the common slip.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,3,3,3,3,3]</code><br><code>\operatorname{mean}(L)-\operatorname{median}(L)</code>

Repeat each value as many times as its count (6 zeros, 9 ones, 5 threes). The second line shows 0.2; enter 0.2 or 1/5.

</details>

---

### 9. psda-race-time-recording-error

*Medium · Multiple choice · route: either · techniques: T9*

A coach recorded the times of 10 runners in a race, and the mean of the recorded times was 52 seconds. One time was recorded as 61 seconds, but that runner's actual time was 47 seconds. What is the mean, in seconds, of the 10 actual times?

- **A.** $38$
- **B.** $50.6$
- **C.** $52$
- **D.** $53.4$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A mean of 52 seconds for 10 runners means the recorded times add to 520 seconds. Replacing 61 with 47 lowers the total by 14, to 506 seconds. Dividing by 10 yields 50.6. Therefore, the mean of the actual times is 50.6 seconds. Distractors: 38 subtracts the full 14 seconds from the mean instead of from the total; 52 assumes one corrected value does not change the mean; 53.4 adds the 1.4-second change instead of subtracting it.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{10\cdot52-61+47}{10}</code>

The line shows 50.6. Rebuild the total from the mean, swap the wrong time for the right one, then divide by 10.

</details>

---

### 10. psda-trips-frequency-median

*Medium · Multiple choice · route: desmos-primary · techniques: T7*

In a survey, 25 people reported how many trips they took last year. Of the 25 people, 6 took 1 trip, 9 took 2 trips, 5 took 3 trips, 3 took 4 trips, and 2 took 5 trips. What is the median number of trips for the 25 people?

- **A.** $9$
- **B.** $5$
- **C.** $3$
- **D.** $2$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** With 25 values, the median is the 13th value in order. The first 6 values are 1 and the next 9 values (the 7th through the 15th) are 2, so the 13th value is 2. Therefore, the median is 2 trips. Distractors: 9 is the greatest frequency, not a value; 5 is the median of the frequencies 6, 9, 5, 3, 2; 3 is the middle of the five listed values 1 through 5, which ignores the frequencies.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,4,4,4,5,5]</code><br><code>\operatorname{median}(L)</code>

Repeat each value as many times as its frequency (25 entries), then median(L) shows 2.

</details>

---

### 11. psda-weighted-mean-new-members

*Medium · Student-produced response · route: hand-primary · techniques: T9*

A hiking club has 24 members with a mean age of 15.5 years. After 6 new members join, the mean age of the 30 members is 16.1 years. What is the mean age, in years, of the 6 new members?

**Answer:** 37/2 (≈ 18.5)

<details><summary>Solutions</summary>

**By hand.** Work with totals. The 30 members have total age 30 · 16.1 = 483; the original 24 have total 24 · 15.5 = 372. The new members total 483 - 372 = 111, so their mean is 111/6 = 18.5. Averaging 15.5 and 16.1 or subtracting them is wrong because the groups have different sizes.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{30\cdot16.1-24\cdot15.5}{6}</code>

Desmos is only a calculator here; the expression shows 18.5. The setup (totals, not means) is the whole problem.

</details>

---

### 12. psda-combined-shifted-sets-sd

*Hard · Multiple choice · route: hand-primary · techniques: T7*

Data set A consists of 12 values with a mean of 36 and a standard deviation of 5. Data set B is formed by subtracting 8 from each value in data set A. Data set C consists of all 24 values in data sets A and B. Which of the following statements about data set C is true?

- **A.** The mean of data set C is 28, and its standard deviation is less than 5.
- **B.** The mean of data set C is 28, and its standard deviation is greater than 5.
- **C.** The mean of data set C is 32, and its standard deviation is less than 5.
- **D.** The mean of data set C is 32, and its standard deviation is greater than 5.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Subtracting 8 from every value shifts the mean by 8 and leaves the spread unchanged, so data set B has mean 28 and standard deviation 5. Data sets A and B have the same number of values, so the mean of C is the average of 36 and 28, which is 32. The values of C sit in two groups centered 8 apart, at 36 and 28, so they are spread farther from 32 than the values of A are from 36; the standard deviation of C is greater than 5 (its variance is 25 + 16 = 41, so the standard deviation is about 6.4). Distractors: 28 is the mean of data set B alone, not of C; 'less than 5' assumes that combining two data sets averages out their spread, when putting two shifted copies together widens it.

**Desmos** (not yet verified in Desmos). Type:<br><code>A=[31,31,31,31,31,31,41,41,41,41,41,41]</code><br><code>C=[31,31,31,31,31,31,41,41,41,41,41,41,23,23,23,23,23,23,33,33,33,33,33,33]</code><br><code>\operatorname{mean}(C)</code><br><code>\operatorname{stdevp}(C)</code>

Any data set with mean 36 and standard deviation 5 will do as A; this one has six 31s and six 41s. mean(C) shows 32 and stdevp(C) shows about 6.4, greater than 5. The reasoning by hand is faster than building the lists.

</details>

---

### 13. psda-household-cars-added-mean

*Hard · Student-produced response · route: desmos-primary · techniques: T7, T1*

In a survey of 40 households, 5 households had 0 cars, 14 had 1 car, 13 had 2 cars, 6 had 3 cars, and 2 had 4 cars. How many households with 4 cars each must be added to the survey data for the mean number of cars per household to be 2?

**Answer:** 7

<details><summary>Solutions</summary>

**By hand.** The 40 households have 5 · 0 + 14 · 1 + 13 · 2 + 6 · 3 + 2 · 4 = 66 cars. If n households with 4 cars are added, the mean is (66 + 4n)/(40 + n). Setting this equal to 2 yields 66 + 4n = 80 + 2n, so 2n = 14 and n = 7. Therefore, 7 households must be added.

**Desmos** (not yet verified in Desmos). Type:<br><code>V=[0,1,2,3,4]</code><br><code>F=[5,14,13,6,2]</code><br><code>S=\operatorname{total}(V\cdot F)</code><br><code>y=\frac{S+4x}{40+x}</code><br><code>y=2</code>

S shows 66, the total number of cars. Click the intersection of the curve with y = 2 (zoom out; it is at x = 7) and enter 7.

</details>

---

### 14. psda-mean-equals-median

*Hard · Student-produced response · route: either · techniques: T7, T4*

The data set $5, 9, 12, 16, 17, 20, x$ has seven values, where $x > 16$. The mean of the data set is equal to its median. What is the value of $x$?

**Answer:** 33

<details><summary>Solutions</summary>

**By hand.** With x > 16 the sorted list is 5, 9, 12, 16, ..., so the median (4th value) is 16. The mean equals 16 when the sum is 7 · 16 = 112. The six known values sum to 79, so x = 33.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[5,9,12,16,17,20,x]</code><br><code>\operatorname{mean}(L)</code><br><code>\operatorname{median}(L)</code>

Add a slider for x with step 1 and drag until mean(L) equals median(L): both read 16 at x = 33. Or type 7·16 - (5+9+12+16+17+20) directly.

</details>

---

### 15. psda-mode-median-greatest-value

*Hard · Student-produced response · route: hand-primary · techniques: —*

A data set consists of 7 positive integers. The mean of the data set is 10, the median is 12, and the only mode is 14. What is the greatest possible value of the largest integer in the data set?

**Answer:** 24

<details><summary>Solutions</summary>

**By hand.** A mean of 10 for 7 integers means they add to 70. In order, the 4th value is the median, 12. The only mode is 14, so 14 appears at least twice, and it must be the 5th and 6th values (14 cannot be among the first three, which are at most 12). To make the largest value as great as possible, every other value is made as small as possible. Since 14 appears exactly twice and is the only mode, no other value can repeat, so the first three values are at least 1, 2 and 3. Then the largest value is 70 − (1 + 2 + 3 + 12 + 14 + 14) = 24. Therefore, the greatest possible value is 24.

</details>

---

### 16. psda-quiz-scores-correction-shift

*Hard · Multiple choice · route: hand-primary · techniques: —*

The quiz scores of 11 students are all different, and the median score is 74. After a grading error is corrected, the highest score increases by 15 points and the lowest score decreases by 4 points. How do the mean and the median of the 11 scores change?

- **A.** The mean increases by 1, and the median remains 74.
- **B.** The mean increases by 1, and the median increases by 1.
- **C.** The mean increases by 11, and the median remains 74.
- **D.** The mean increases by 11, and the median increases by 11.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The total of the 11 scores changes by 15 − 4 = 11 points, so the mean changes by 11/11 = 1 point; it increases by 1. The highest score only gets higher and the lowest only gets lower, so the order of the scores is unchanged and the 6th score, the median, is still 74. Therefore, the mean increases by 1 and the median remains 74. Distractors: 'the median increases by 1' assumes the median moves with the mean; 'the mean increases by 11' reports the change in the total instead of dividing by 11 scores; the choice with both increasing by 11 makes both mistakes.

</details>

---

### 17. psda-remove-max-mean-median

*Hard · Multiple choice · route: hand-primary · techniques: T7*

The data set $12, 15, 15, 18, 18, 20, 22, 70$ has eight values. If the value 70 is removed from the data set, which of the following correctly describes how the mean and the median of the data set change?

- **A.** The mean decreases, and the median decreases.
- **B.** The mean decreases, and the median remains the same.
- **C.** The mean remains the same, and the median decreases.
- **D.** The mean remains the same, and the median remains the same.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The value 70 is far above every other value, so removing it lowers the total much more than it lowers the count: the mean falls from 190/8 = 23.75 to 120/7, about 17.1, so the mean decreases. The median of the eight values is the average of the 4th and 5th values, (18 + 18)/2 = 18. After 70 is removed, the median of the seven values is the 4th value, 18. Therefore, the median remains the same. Distractors: 'the median decreases' assumes removing a large value must pull every measure down; 'the mean remains the same' confuses the mean with the median; the choice with both remaining the same ignores the effect of an outlier on the mean.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[12,15,15,18,18,20,22,70]</code><br><code>M=[12,15,15,18,18,20,22]</code><br><code>\operatorname{mean}(L)</code><br><code>\operatorname{median}(L)</code><br><code>\operatorname{mean}(M)</code><br><code>\operatorname{median}(M)</code>

mean(L) shows 23.75 and mean(M) shows 17.143, so the mean drops; median(L) and median(M) both show 18. Reasoning about the middle values by hand is faster than typing two lists.

</details>

---

### 18. psda-rice-bags-added-at-mean

*Hard · Multiple choice · route: hand-primary · techniques: —*

The masses of 24 bags of rice filled by a machine have a mean of 500 grams and a standard deviation of 4 grams. Two more bags, each with a mass of 500 grams, are added to the data. How do the mean and the standard deviation of the masses change?

- **A.** The mean increases, and the standard deviation remains the same.
- **B.** The mean increases, and the standard deviation decreases.
- **C.** The mean remains the same, and the standard deviation remains the same.
- **D.** The mean remains the same, and the standard deviation decreases.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Adding values equal to the mean adds 2 · 500 = 1,000 grams to the total and 2 to the count, so the new mean is (24 · 500 + 1,000)/26 = 500; the mean remains the same. The two new values are 0 grams from the mean, so they add nothing to the total squared distance from the mean while increasing the number of values. The typical distance from the mean shrinks, so the standard deviation decreases. Distractors: 'the mean increases' reasons that adding bags adds mass, but the mean is a total per bag; 'the standard deviation remains the same' assumes values at the mean have no effect on spread, but they dilute it.

</details>

---

### 19. psda-scaled-shifted-data-set

*Hard · Multiple choice · route: either · techniques: T7*

The 20 values in data set X have a mean of 14. Data set Y is formed by multiplying each value in data set X by 3 and then subtracting 5. Which statement about data set Y must be true?

- **A.** The mean of data set Y is 37, and the standard deviation of data set Y is equal to the standard deviation of data set X.
- **B.** The mean of data set Y is 42, and the standard deviation of data set Y is equal to the standard deviation of data set X.
- **C.** The mean of data set Y is 37, and the standard deviation of data set Y is 3 times the standard deviation of data set X.
- **D.** The mean of data set Y is 42, and the standard deviation of data set Y is 3 times the standard deviation of data set X.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** If every value is multiplied by 3, the mean is multiplied by 3, and subtracting 5 from every value then lowers the mean by 5. So the mean of data set Y is 3(14) - 5 = 42 - 5 = 37. Multiplying every value by 3 spreads the values out, so the standard deviation is multiplied by 3; subtracting the same number from every value does not change how spread out they are. Therefore, the standard deviation of data set Y is 3 times the standard deviation of data set X. Distractors: 42 is 3 times the mean of X, forgetting the subtraction of 5; the choices saying the standard deviations are equal treat multiplying by 3 like a shift, which changes the center but not the spread.

**Desmos** (not yet verified in Desmos). Type:<br><code>X=[10,12,14,16,18]</code><br><code>Y=3X-5</code><br><code>\operatorname{mean}(X)</code><br><code>\operatorname{mean}(Y)</code><br><code>\operatorname{stdevp}(X)</code><br><code>\operatorname{stdevp}(Y)</code>

Any list with mean 14 works as a test case. mean(X) shows 14 and mean(Y) shows 37; stdevp(Y) shows 3 times stdevp(X) (about 8.49 versus 2.83). The list test confirms the rule; the reasoning is faster once the rule is known.

</details>

---

### 20. psda-sd-frequency-smallest

*Hard · Multiple choice · route: hand-primary · techniques: T7*

Each of four data sets, W, X, Y, and Z, consists of 20 values, each of which is 1, 2, 3, 4, or 5. In data set W, the values 1, 2, 3, 4, and 5 occur 4, 4, 4, 4, and 4 times, respectively. In data set X they occur 10, 0, 0, 0, and 10 times. In data set Y they occur 0, 5, 10, 5, and 0 times. In data set Z they occur 2, 4, 8, 4, and 2 times. Which data set has the smallest standard deviation?

- **A.** Data set W
- **B.** Data set X
- **C.** Data set Y
- **D.** Data set Z

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** All four sets have mean 3, so compare how far the values sit from 3. Y keeps half its values at 3 and the rest only 1 away, with nothing at the extremes, so it is the tightest. Distractors: Z also clusters at 3 but puts 4 values at the extremes, which adds more spread than Y's; W spreads evenly, so a fifth of the data sits 2 away on each side; X is the widest, with every value 2 away from the mean.

**Desmos** (not yet verified in Desmos). Type:<br><code>W=[1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5]</code><br><code>\operatorname{stdev}(W)</code>

Typing all four lists and stdev of each works but takes longer than comparing spreads by eye. If you do, Y shows the smallest value (about 0.73); W is about 1.45, Z about 1.12, X about 2.05.

</details>

---

### 21. psda-shifted-spread-sets-compare

*Hard · Multiple choice · route: hand-primary · techniques: T7*

Data set A consists of 20 values: 2 values of 10, 4 values of 11, 8 values of 12, 4 values of 13, and 2 values of 14. Data set B consists of 20 values: 4 values of 20, 2 values of 21, 8 values of 22, 2 values of 23, and 4 values of 24. Which of the following correctly compares the means and the standard deviations of the two data sets?

- **A.** The means are equal, and the standard deviations are equal.
- **B.** The means are equal, and the standard deviation of data set B is greater.
- **C.** The mean of data set B is greater, and the standard deviations are equal.
- **D.** The mean of data set B is greater, and the standard deviation of data set B is greater.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Each data set is symmetric about its middle value, so the mean of A is 12 and the mean of B is 22; the mean of B is greater. Both sets have 8 values at the center and the same range, but B has 8 values at the extremes (4 at 20, 4 at 24) while A has only 4 there (2 at 10, 2 at 14). B's values are farther from its mean on the whole, so B has the greater standard deviation. Therefore, the mean of data set B is greater and its standard deviation is greater. Distractors: 'the standard deviations are equal' treats B as A shifted up by 10, but the frequencies at the ends differ; 'the means are equal' compares the shapes, which are both centered on the middle value, instead of the values themselves.

**Desmos** (not yet verified in Desmos). Type:<br><code>A=[10,10,11,11,11,11,12,12,12,12,12,12,12,12,13,13,13,13,14,14]</code><br><code>B=[20,20,20,20,21,21,22,22,22,22,22,22,22,22,23,23,24,24,24,24]</code><br><code>\operatorname{stdevp}(A)</code><br><code>\operatorname{stdevp}(B)</code>

stdevp(A) shows about 1.095 and stdevp(B) about 1.342. Typing 40 values is slow; the reasoning about where the values sit is faster.

</details>

---

### 22. psda-temperature-entry-error-effects

*Hard · Multiple choice · route: hand-primary · techniques: T7*

The daily high temperatures, in degrees Fahrenheit, for 10 days were recorded as 82, 85, 86, 87, 88, 88, 90, 91, 93, and 9. The value 9 was an error for 90. When 9 is replaced by 90, how do the median and the standard deviation change?

- **A.** The median increases, and the standard deviation decreases.
- **B.** The median increases, and the standard deviation increases.
- **C.** The median remains the same, and the standard deviation decreases.
- **D.** The median remains the same, and the standard deviation increases.

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** With 10 values, the median is the mean of the 5th and 6th values in order. With the 9 included, the ordered list is 9, 82, 85, 86, 87, 88, 88, 90, 91, 93, so the median is (87 + 88)/2 = 87.5. With 90 instead, the list is 82, 85, 86, 87, 88, 88, 90, 90, 91, 93, so the median is (88 + 88)/2 = 88. The median increases. The value 9 was far from every other value; replacing it with 90 puts all the values close together, so the standard deviation decreases. Distractors: 'the median remains the same' assumes the median ignores an outlier entirely, but the outlier moved the two middle positions; 'the standard deviation increases' reasons that a larger value means more spread, when spread depends on distance from the mean.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[82,85,86,87,88,88,90,91,93,9]</code><br><code>M=[82,85,86,87,88,88,90,91,93,90]</code><br><code>\operatorname{median}(L)</code><br><code>\operatorname{median}(M)</code><br><code>\operatorname{stdev}(L)</code><br><code>\operatorname{stdev}(M)</code>

The medians show 87.5 and 88; the standard deviations drop from about 25.1 to about 3.2. Reasoning about the middle values is faster than typing both lists.

</details>

---

### 23. psda-two-sections-size-from-mean

*Hard · Multiple choice · route: desmos-primary · techniques: T1, T13*

A tutoring program has 30 students in two sections. The mean test score is 70 for section A and 85 for section B, and the mean test score for all 30 students is 76. How many students are in section B?

- **A.** $6$
- **B.** $12$
- **C.** $15$
- **D.** $18$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Let b be the number of students in section B, so 30 − b are in section A. The total of all scores is 30 · 76 = 2,280, so 70(30 − b) + 85b = 2,280. This yields 2,100 + 15b = 2,280, so 15b = 180 and b = 12. Therefore, 12 students are in section B. Distractors: 6 is the difference between the overall mean and section A's mean (76 − 70); 15 assumes equal sections; 18 is the number of students in section A.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{70(30-x)+85x}{30}</code><br><code>y=76</code><br><code>\frac{70\cdot18+85\cdot12}{30}</code>

x is the number of students in section B. Click the intersection of the two lines and read x = 12. The third line checks the choice: 18 students in A and 12 in B give a mean of 76.

</details>

---
