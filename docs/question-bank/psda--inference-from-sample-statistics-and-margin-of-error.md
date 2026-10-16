# Inference from sample statistics and margin of error

[← Question bank index](README.md) · Problem-Solving and Data Analysis · 17 questions, easiest first

### 1. psda-infer-library-overdue-estimate

*Easy · Multiple choice · route: hand-primary · techniques: T9*

A library has 3,600 books checked out. In a random sample of 120 of these books, 18 are overdue. Based on the sample, about how many of the 3,600 checked-out books are overdue?

- **A.** $18$
- **B.** $102$
- **C.** $540$
- **D.** $3,060$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that 18 of the 120 sampled books are overdue, so the sample proportion is 18/120 = 0.15. Because the sample is random, the sample proportion estimates the proportion of all 3,600 checked-out books that are overdue: 0.15(3,600) = 540. Therefore, about 540 books are overdue. Distractors: 18 is the number of overdue books in the sample, not scaled to all 3,600 books; 102 is the number of sampled books that are not overdue, 120 - 18; 3,060 is the estimated number of books that are not overdue, 0.85(3,600).

**Desmos** (not yet verified in Desmos). Type:<br><code>3600\cdot\frac{18}{120}</code>

The line shows 540. By hand this is one multiplication, so Desmos is slower; use the line only as a check.

</details>

---

### 2. psda-infer-park-visit-smaller-margin

*Easy · Multiple choice · route: hand-primary · techniques: —*

A team surveyed a random sample of 250 park visitors to estimate the mean time that all visitors spend in the park. The estimate had a margin of error of 9 minutes. Which change to the survey would most likely produce a smaller margin of error?

- **A.** Selecting a random sample of 100 visitors instead of 250 visitors
- **B.** Selecting a random sample of 1,000 visitors instead of 250 visitors
- **C.** Recording each visitor's time to the nearest second instead of the nearest minute
- **D.** Surveying only the visitors who stay in the park longer than 30 minutes

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A larger random sample from the same population generally produces a smaller margin of error, because the sample mean varies less from sample to sample. Increasing the sample from 250 to 1,000 visitors is the change most likely to shrink the margin of error. Distractors: a random sample of 100 visitors is smaller, so its margin of error would likely be larger; recording times to the nearest second changes the precision of each measurement, not the sampling variability that the margin of error describes; surveying only visitors who stay longer than 30 minutes makes the sample unrepresentative of all visitors, which biases the estimate rather than making it more precise.

</details>

---

### 3. psda-infer-plausible-proportion-value

*Easy · Multiple choice · route: hand-primary · techniques: T7, T13*

An estimate of a proportion is $0.62$, with an associated margin of error of $0.04$. Based on this estimate, which value is a plausible value of the proportion being estimated?

- **A.** $0.04$
- **B.** $0.54$
- **C.** $0.64$
- **D.** $0.70$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A margin of error gives an interval of plausible values: the estimate minus the margin to the estimate plus the margin. Here that is 0.62 - 0.04 = 0.58 to 0.62 + 0.04 = 0.66. Of the choices, only 0.64 lies in this interval. Distractors: 0.04 is the margin of error itself, not a value of the proportion; 0.54 subtracts twice the margin of error, 0.62 - 0.08, and lies below the interval; 0.70 adds twice the margin of error, 0.62 + 0.08, and lies above it.

**Desmos** (not yet verified in Desmos). Type:<br><code>L=[0.04,0.54,0.64,0.70]</code><br><code>\left|L-0.62\right|</code>

The second line lists each choice's distance from 0.62: 0.58, 0.08, 0.02, 0.08. Only 0.64 is within 0.04. By hand the interval 0.58 to 0.66 is faster; use the list only as a check.

</details>

---

### 4. psda-fish-mass-sample-mean

*Medium · Multiple choice · route: hand-primary · techniques: —*

Based on a random sample of fish from a lake, researchers estimate that the mean mass of all fish in the lake is between 2.4 kilograms and 3.2 kilograms. This interval is the sample mean plus or minus the margin of error. What is the sample mean, in kilograms?

- **A.** $0.4$
- **B.** $0.8$
- **C.** $2.8$
- **D.** $5.6$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that the interval runs from the sample mean minus the margin of error to the sample mean plus the margin of error, so the sample mean is the midpoint of the interval: (2.4 + 3.2)/2 = 2.8 kilograms. The margin of error is then half the width, (3.2 - 2.4)/2 = 0.4 kilograms. Distractors: 0.4 is the margin of error, not the sample mean; 0.8 is the full width of the interval, 3.2 - 2.4; 5.6 is the sum of the endpoints without dividing by 2.

</details>

---

### 5. psda-infer-apartment-occupants-total

*Medium · Student-produced response · route: either · techniques: T9*

An apartment complex has 3,500 apartments. In a random sample of 120 of the apartments, the mean number of occupants per apartment is 2.4. Using the sample mean, what is the estimated total number of occupants of all the apartments in the complex?

**Answer:** 8400

<details><summary>Solutions</summary>

**By hand.** It's given that the sample is random, so the sample mean of 2.4 occupants per apartment estimates the mean for all 3,500 apartments. The total number of occupants is the mean per apartment times the number of apartments: 2.4(3,500) = 8,400. Therefore, the best estimate is 8,400 occupants. Common slips: 288 multiplies the mean by the sample size, 2.4(120), which estimates the occupants of the sampled apartments only.

**Desmos** (not yet verified in Desmos). Type:<br><code>3500\cdot2.4</code>

The line shows 8400. The work is recognizing that the sample mean estimates the mean for all 3,500 apartments; the 120 is not used in the product.

</details>

---

### 6. psda-infer-bolts-not-defective-total

*Medium · Student-produced response · route: either · techniques: T9*

A factory produced 12,500 bolts in one day. A random sample of 250 of these bolts was inspected, and 6 of the bolts in the sample were defective. Based on the sample, how many of the bolts produced that day are estimated to be not defective?

**Answer:** 12200

<details><summary>Solutions</summary>

**By hand.** It's given that 6 of the 250 sampled bolts were defective, so 250 - 6 = 244 were not, and the sample proportion of bolts that are not defective is 244/250 = 0.976. Because the sample is random, this proportion estimates the proportion for all 12,500 bolts: 0.976(12,500) = 12,200. Alternate approach: the estimated number of defective bolts is (6/250)(12,500) = 300, so 12,500 - 300 = 12,200 are not defective. Entering 300 answers the wrong question.

**Desmos** (not yet verified in Desmos). Type:<br><code>12500\left(1-\frac{6}{250}\right)</code>

The line shows 12200. Enter 12200 (no comma). The step to watch is the complement: the question asks for bolts that are not defective.

</details>

---

### 7. psda-infer-books-read-larger-sample

*Medium · Multiple choice · route: hand-primary · techniques: —*

Two random samples of a county's residents were selected in the same way to estimate the mean number of books read per year. The sample of 400 residents produced a margin of error of 1.8 books. What is the most likely margin of error, in books, for the sample of 1,600 residents?

- **A.** $0.9$
- **B.** $1.8$
- **C.** $3.6$
- **D.** $7.2$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** A larger random sample from the same population generally produces a smaller margin of error, so the margin for the sample of 1,600 residents should be less than 1.8 books. Only 0.9 is less than 1.8. (The margin of error shrinks with the square root of the sample size: 4 times the sample gives about 1/2 the margin, 1.8/2 = 0.9.) Distractors: 1.8 assumes the sample size does not affect the margin of error; 3.6 doubles the margin, as if a larger sample were less precise; 7.2 multiplies the margin by 4, the factor by which the sample grew.

</details>

---

### 8. psda-infer-bus-delay-plausible-mean

*Medium · Multiple choice · route: hand-primary · techniques: —*

A random sample of 150 trips on a bus route had a mean delay of 4.8 minutes, with a margin of error of 0.6 minute. Which statement about the delays of all trips on this route is best supported?

- **A.** The mean delay for all trips on the route is exactly 4.8 minutes.
- **B.** The mean delay for all trips on the route is plausibly 5.3 minutes.
- **C.** The mean delay for all trips on the route is plausibly 6.0 minutes.
- **D.** Every trip on the route has a delay between 4.2 and 5.4 minutes.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The sample mean and margin of error give an interval of plausible values for the mean delay of all trips: 4.8 - 0.6 = 4.2 to 4.8 + 0.6 = 5.4 minutes. Since 5.3 lies in this interval, 5.3 minutes is a plausible value for the mean delay. Distractors: 'exactly 4.8 minutes' treats the sample mean as the population mean and ignores the margin of error; 6.0 minutes adds twice the margin of error, 4.8 + 1.2, and lies outside the interval; 'every trip on the route' applies the interval for the mean to individual trips, whose delays vary more than the mean does.

</details>

---

### 9. psda-infer-two-towns-commute-intervals

*Medium · Multiple choice · route: hand-primary · techniques: —*

Random samples of adults in towns A and B were surveyed. For town A, the mean commute time was 24.5 minutes, with a margin of error of 1.2 minutes. For town B, it was 27.9 minutes, with a margin of error of 1.5 minutes. Which conclusion is best supported?

- **A.** There is convincing evidence that the mean commute time of all adults in town A is greater than that in town B.
- **B.** There is no convincing evidence that the mean commute times of all adults in the two towns differ.
- **C.** There is convincing evidence that every adult in town B has a longer commute than every adult in town A.
- **D.** There is convincing evidence that the mean commute time of all adults in town B is greater than that in town A.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Each sample mean and margin of error gives an interval of plausible values for the town's mean commute time. For town A it is 24.5 - 1.2 = 23.3 to 24.5 + 1.2 = 25.7 minutes; for town B it is 27.9 - 1.5 = 26.4 to 27.9 + 1.5 = 29.4 minutes. Every plausible value for town B is greater than every plausible value for town A (26.4 > 25.7), so there is convincing evidence that the mean for all adults in town B is greater. Distractors: 'town A is greater than that in town B' reverses the comparison; 'no convincing evidence' would follow only if the intervals overlapped, and they do not; 'every adult in town B' applies a conclusion about means to individuals, whose commute times vary far more than the means do.

</details>

---

### 10. psda-margin-of-error-sample-size

*Medium · Multiple choice · route: hand-primary · techniques: —*

Two research teams each selected a random sample of adults from the same region to estimate the mean number of hours of sleep per night for adults in the region. Team 1 sampled 120 adults and reported an estimate of 7.1 hours with a margin of error of 0.5 hours. Team 2 sampled 1,080 adults and reported an estimate of 7.0 hours with a margin of error of 0.17 hours. Which of the following is the best explanation of why Team 2's margin of error is smaller than Team 1's?

- **A.** Team 2's estimate of the mean is smaller than Team 1's.
- **B.** Team 2's sample was larger, so its estimate is less affected by sampling variability.
- **C.** The adults in Team 2's sample had more similar sleep habits than those in Team 1's sample.
- **D.** Team 2's sample was selected more randomly than Team 1's.

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Margin of error shrinks as sample size grows (roughly in proportion to 1 over the square root of the sample size: a sample 9 times as large gives a margin about a third as large, and 0.5/3 ≈ 0.17). Both samples were random from the same population, so the sample size is the only given difference that affects the margin of error. Distractors: the value of the estimate (7.0 vs 7.1) has nothing to do with precision; nothing in the information says Team 2's adults were more alike, and a random sample from the same region should not be; both samples were random, so one is not 'more random' than the other.

</details>

---

### 11. psda-moe-streaming-interpretation

*Medium · Multiple choice · route: hand-primary · techniques: —*

A random sample of 400 households in a city was surveyed. The mean number of streaming subscriptions per household in the sample was 2.6, with an associated margin of error of 0.3. Which of the following is the most appropriate conclusion?

- **A.** The mean number of subscriptions for all households in the city is 2.6.
- **B.** Each household in the sample has between 2.3 and 2.9 subscriptions.
- **C.** The mean number of subscriptions for all households in the country is plausibly between 2.3 and 2.9.
- **D.** The mean number of subscriptions for all households in the city is plausibly between 2.3 and 2.9.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A sample mean with a margin of error gives an interval of plausible values for the population mean: 2.6 - 0.3 = 2.3 to 2.6 + 0.3 = 2.9. The population is the one the sample was drawn from, all households in the city. Distractors: 'is 2.6' treats the sample mean as the exact population mean, ignoring the margin of error; 'each household in the sample' applies the interval to individual households, but a margin of error describes the estimate of a mean, not individual values; 'all households in the country' extends the result beyond the population that was sampled.

</details>

---

### 12. psda-sample-proportion-employees

*Medium · Multiple choice · route: either · techniques: T9*

A company has 1,500 employees. In a random sample of 60 of the employees, 24 said they use the company's fitness room. Based on the sample, what is the best estimate of the number of the company's 1,500 employees who do not use the fitness room?

- **A.** $24$
- **B.** $36$
- **C.** $600$
- **D.** $900$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** In the sample, 24/60 = 2/5 of the employees use the fitness room, so 3/5 do not. The sample proportion estimates the population proportion, so the estimated number who do not use the room is (3/5)(1,500) = 900. Distractors: 600 is the estimated number who do use the room; 36 is the number in the sample who do not use it, not scaled to the company; 24 is the number in the sample who do use it.

**Desmos** (not yet verified in Desmos). Type:<br><code>1500\left(1-\frac{24}{60}\right)</code>

The line shows 900. The proportion in the sample who do not use the room, 36/60, is applied to the whole company.

</details>

---

### 13. psda-infer-dog-park-majority

*Hard · Multiple choice · route: hand-primary · techniques: —*

A town surveyed a random sample of 600 residents about a proposed dog park. Of those surveyed, 53% favored the park, with a margin of error of 4 percentage points. Which conclusion about all residents of the town is best supported?

- **A.** Exactly 53% of all residents favor the park.
- **B.** More than 50% of all residents certainly favor the park.
- **C.** Between 49% and 57% of the 600 residents surveyed favor the park.
- **D.** It is plausible that less than 50% of all residents favor the park.

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The sample percent and margin of error give an interval of plausible values for the percent of all residents who favor the park: 53 - 4 = 49% to 53 + 4 = 57%. This interval includes values less than 50%, such as 49%, so it is plausible that less than half of all residents favor the park. Distractors: 'exactly 53%' treats the sample percent as the population percent and ignores the margin of error; 'more than 50% ... certainly' ignores the part of the interval below 50%; 'between 49% and 57% of the 600 residents surveyed' applies the interval to the sample, whose percent is known exactly (53%), instead of to all residents.

</details>

---

### 14. psda-infer-ev-households-upper-total

*Hard · Student-produced response · route: desmos-primary · techniques: T9*

A city has 84,000 households. In a random sample of 500 of them, 30% own an electric vehicle, with a margin of error of 4 percentage points. Based on the sample, what is the largest plausible value for the number of the city's households that own an electric vehicle?

**Answer:** 28560

<details><summary>Solutions</summary>

**By hand.** It's given that the sample percent is 30% with a margin of error of 4 percentage points, so the plausible values for the percent of all the city's households that own an electric vehicle run from 30% - 4% = 26% to 30% + 4% = 34%. The largest plausible percent is 34%, and 34% of 84,000 is 0.34(84,000) = 28,560. Therefore, the largest plausible number of households is 28,560. Common slips: 25,200 is the point estimate 0.30(84,000); 21,840 is the smallest plausible value 0.26(84,000); 25,204 adds 4 households to the point estimate instead of 4 percentage points to the percent.

**Desmos** (not yet verified in Desmos). Type:<br><code>84000(0.30+0.04)</code>

The line shows 28560. Enter 28560 (no comma). Add the margin of error to the sample percent before multiplying; 84000(0.30) = 25200 is the point estimate, not the largest plausible value.

</details>

---

### 15. psda-infer-garden-households-interval

*Hard · Multiple choice · route: desmos-primary · techniques: T9, T13*

A town has 9,200 households. In a random sample of 400 of them, 35% have a vegetable garden, with a margin of error of 3 percentage points. Based on the sample, which interval contains the plausible values for the number of the town's households that have a vegetable garden?

- **A.** From 2,760 to 3,680
- **B.** From 2,944 to 3,496
- **C.** From 3,217 to 3,223
- **D.** From 5,704 to 6,256

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** It's given that the sample percent is 35% with a margin of error of 3 percentage points, so the plausible percents for all households run from 32% to 38%. Scaling both endpoints to the 9,200 households gives 0.32(9,200) = 2,944 to 0.38(9,200) = 3,496. Distractors: 2,760 to 3,680 applies twice the margin of error, 0.30(9,200) to 0.40(9,200); 3,217 to 3,223 subtracts and adds 3 households to the point estimate 0.35(9,200) = 3,220 instead of 3 percentage points to the percent; 5,704 to 6,256 is the interval for households without a garden, 0.62(9,200) to 0.68(9,200).

**Desmos** (not yet verified in Desmos). Type:<br><code>9200(0.35-0.03)</code><br><code>9200(0.35+0.03)</code>

The lines show 2944 and 3496; match them to the choice that runs from 2,944 to 3,496. Apply the margin to the percent, then scale both endpoints by 9,200.

</details>

---

### 16. psda-infer-greenhouse-sprout-overlap

*Hard · Multiple choice · route: hand-primary · techniques: T7*

In a random sample of seeds planted in greenhouse P, 48% sprouted within a week, with a margin of error of 3 percentage points. In a random sample of seeds planted in greenhouse Q, 41% sprouted within a week, with a margin of error of 5 percentage points. Which conclusion is best supported?

- **A.** There is convincing evidence that a greater percentage of all seeds planted in greenhouse P sprouted within a week.
- **B.** There is convincing evidence that a greater percentage of all seeds planted in greenhouse Q sprouted within a week.
- **C.** There is no convincing evidence that the percentages of all seeds that sprouted within a week differ between the two greenhouses.
- **D.** There is convincing evidence that the percentage for greenhouse P is exactly 7 percentage points greater than that for greenhouse Q.

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Each sample percent and margin of error gives an interval of plausible values. For greenhouse P it is 48 - 3 = 45% to 48 + 3 = 51%; for greenhouse Q it is 41 - 5 = 36% to 41 + 5 = 46%. The intervals overlap from 45% to 46%, so a value such as 45.5% is plausible for both greenhouses, and the data do not show convincingly that the percentages differ. Distractors: 'greater percentage of all seeds planted in greenhouse P' is the trap, since the difference of 7 points exceeds each margin of error separately but the intervals still overlap; 'greater percentage of all seeds planted in greenhouse Q' reverses the sample results; 'exactly 7 percentage points greater' treats the difference of the sample percents as the exact difference for all seeds, ignoring both margins of error.

**Desmos** (not yet verified in Desmos). Type:<br><code>P=48+[-3,3]</code><br><code>Q=41+[-5,5]</code>

P shows [45, 51] and Q shows [36, 46]. The intervals share the values from 45 to 46, so they overlap. Two subtractions by hand are faster; use the lists only as a check.

</details>

---

### 17. psda-infer-orchard-yield-least-total

*Hard · Student-produced response · route: desmos-primary · techniques: T9*

An orchard has 650 apple trees. For a random sample of 40 of the trees, the mean yield is 42 kilograms of fruit per tree, with a margin of error of 3 kilograms. Based on the sample, what is the smallest plausible value for the total yield, in kilograms, of all 650 trees?

**Answer:** 25350

<details><summary>Solutions</summary>

**By hand.** It's given that the sample mean is 42 kilograms per tree with a margin of error of 3 kilograms, so the plausible values for the mean yield of all 650 trees run from 42 - 3 = 39 to 42 + 3 = 45 kilograms per tree. The smallest plausible mean is 39 kilograms per tree, and the total for 650 trees is 650(39) = 25,350 kilograms. Therefore, the smallest plausible total is 25,350 kilograms. Common slips: 27,297 subtracts the 3 kilograms from the total 650(42) = 27,300 instead of from the mean per tree; 1,560 uses the 40 sampled trees, 40(39).

**Desmos** (not yet verified in Desmos). Type:<br><code>650(42-3)</code>

The line shows 25350. Enter 25350 (no comma). Subtract the margin of error from the mean per tree first, then multiply by the 650 trees.

</details>

---
