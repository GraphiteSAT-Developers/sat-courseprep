# Right triangles and trigonometry

[← Question bank index](README.md) · Geometry and Trigonometry · 37 questions, easiest first

### 1. geo-degrees-to-radians-150

*Easy · Multiple choice · route: hand-primary · techniques: T13*

An angle has a measure of 150°. What is the measure of the angle, in radians?

- **A.** $\frac{5\pi}{12}$
- **B.** $\frac{5\pi}{6}$
- **C.** $\frac{6\pi}{5}$
- **D.** $\frac{5\pi}{3}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** To convert degrees to radians, multiply by π/180 radians per degree: 150 · π/180 = 150π/180 = 5π/6. Therefore, the angle measures 5π/6 radians. Distractors: 5π/12 divides 150 by 360 instead of 180, confusing the half turn with the full turn; 6π/5 inverts the ratio (180/150); 5π/3 divides by 90, treating a quarter turn as π.

**Desmos** (not yet verified in Desmos). Type:<br><code>150\cdot\frac{\pi}{180}</code><br><code>\frac{5\pi}{6}</code>

Both lines show 2.618, confirming 5π/6; the other choices give different decimals. Multiplying by π/180 and reducing by hand is faster.

</details>

---

### 2. geo-isosceles-right-leg-9-hypotenuse

*Easy · Multiple choice · route: hand-primary · techniques: —*

In triangle $XYZ$, angles $X$ and $Z$ each measure 45°, and $XY = 9$. What is the length of $XZ$?

- **A.** $9\sqrt{2}$
- **B.** $9\sqrt{3}$
- **C.** $18\sqrt{2}$
- **D.** $81\sqrt{2}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Since angles X and Z measure 45° each, angle Y measures 180° - 45° - 45° = 90°, so XYZ is a 45-45-90 triangle with legs XY and YZ and hypotenuse XZ. In a 45-45-90 triangle the hypotenuse is √2 times a leg, so XZ = 9√2. Therefore, XZ = 9√2. Distractors: 9\sqrt{3} uses the √3 factor of a 30-60-90 triangle; 18\sqrt{2} doubles the leg before multiplying by √2; 81\sqrt{2} squares the leg before multiplying by √2.

</details>

---

### 3. geo-ladder-wall-height-pythagorean

*Easy · Multiple choice · route: hand-primary · techniques: —*

A ladder 6.5 meters long leans against a vertical wall. The base of the ladder sits on level ground 2.5 meters from the wall. How high, in meters, up the wall does the top of the ladder reach?

- **A.** $4$
- **B.** $6$
- **C.** $9$
- **D.** $36$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The wall, the ground, and the ladder form a right triangle in which the ladder is the hypotenuse, 6.5 meters, and the ground distance is a leg, 2.5 meters. By the Pythagorean theorem, h^2 + 2.5^2 = 6.5^2, where h is the height reached. So h^2 = 42.25 - 6.25 = 36 and h = 6. (The sides 2.5, 6, and 6.5 are half of the triple 5, 12, 13.) Therefore, the top of the ladder reaches 6 meters up the wall. Distractors: 4 subtracts the lengths, 6.5 - 2.5, instead of their squares; 9 adds the lengths, 6.5 + 2.5; 36 is h^2, the square of the height, before taking the square root.

</details>

---

### 4. geo-legs-9-40-hypotenuse

*Easy · Multiple choice · route: hand-primary · techniques: —*

A right triangle has legs of lengths 9 and 40. What is the length of the hypotenuse of the triangle?

- **A.** $1,681$
- **B.** $49$
- **C.** $41$
- **D.** $31$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** By the Pythagorean theorem, the square of the hypotenuse c equals the sum of the squares of the legs: c^2 = 9^2 + 40^2 = 81 + 1,600 = 1,681. Since 41^2 = 1,681, c = 41. (9, 40, 41 is a Pythagorean triple.) Therefore, the hypotenuse has length 41. Distractors: 1,681 is c^2, the square of the hypotenuse, reported before taking the square root; 49 adds the legs, 9 + 40, instead of their squares; 31 subtracts the legs, 40 - 9.

</details>

---

### 5. geo-sin-28-cos-x-complement

*Easy · Multiple choice · route: either · techniques: T1, T12*

If $\sin(28^\circ) = \cos(x^\circ)$, where $0 < x < 90$, what is the value of $x$?

- **A.** $28$
- **B.** $62$
- **C.** $118$
- **D.** $152$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The sine of an acute angle equals the cosine of its complement: sin(28°) = cos((90 - 28)°) = cos(62°). Since 0 < x < 90 and cosine takes each value only once on that interval, x = 62. Therefore, x = 62. Distractors: 28 treats sine and cosine as the same function of the same angle; 118 adds 28 to 90 instead of subtracting it from 90; 152 subtracts 28 from 180, using the supplement instead of the complement.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sin(28)</code><br><code>y=\cos(x)</code>

Set the angle mode to Degrees first. Click the intersection with 0 < x < 90: x = 62. The by-hand route (complementary angles) is just as fast.

</details>

---

### 6. geo-tan-e-from-three-sides

*Easy · Multiple choice · route: hand-primary · techniques: —*

In right triangle $DEF$, angle $F$ is the right angle, $DE = 29$, $EF = 20$, and $DF = 21$. What is the value of $\tan E$?

- **A.** $\frac{20}{29}$
- **B.** $\frac{21}{29}$
- **C.** $\frac{20}{21}$
- **D.** $\frac{21}{20}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The tangent of an acute angle in a right triangle is the length of the opposite leg divided by the length of the adjacent leg. For angle E, the opposite leg is DF = 21 and the adjacent leg is EF = 20. Therefore, tan E = 21/20. Distractors: 20/29 is EF/DE, which is cos E; 21/29 is DF/DE, which is sin E; 20/21 is EF/DF, which is tan D, the tangent of the other acute angle.

</details>

---

### 7. geo-30-60-90-longer-leg-hypotenuse

*Medium · Student-produced response · route: hand-primary · techniques: —*

In triangle $RST$, angle $S$ is a right angle, the measure of angle $R$ is 60°, and $ST = 8\sqrt{3}$. What is the length of $RT$?

**Answer:** 16

<details><summary>Solutions</summary>

**By hand.** Since angle S is the right angle, RT is the hypotenuse. Side ST is opposite the 60° angle at R, so it is the longer leg of a 30-60-90 triangle. The longer leg is √3 times the shorter leg, so the shorter leg RS = 8√3/√3 = 8, and the hypotenuse is twice the shorter leg: RT = 2(8) = 16. Therefore, RT = 16. A common mistake is to treat ST as the shorter leg, which gives RT = 16√3.

</details>

---

### 8. geo-cliff-elevation-arccos

*Medium · Multiple choice · route: desmos-primary · techniques: T12*

A surveyor stands on level ground 90 meters from the base of a vertical cliff. A laser measures the straight-line distance from the surveyor to the top of the cliff as 150 meters. To the nearest tenth of a degree, what is the angle of elevation from the surveyor to the top of the cliff?

- **A.** $59.0$
- **B.** $53.1$
- **C.** $36.9$
- **D.** $31.0$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The ground distance (90 meters), the cliff, and the laser line (150 meters) form a right triangle with the laser line as the hypotenuse. The ground distance is adjacent to the angle of elevation θ, so cos θ = 90/150 = 0.6 and θ = arccos(0.6) ≈ 53.13°. Therefore, the angle of elevation is 53.1° to the nearest tenth. Without a calculator: cos 60° = 0.5 and cos 45° ≈ 0.707, and 0.6 lies between them, so θ is between 45° and 60°; 53.1 is the only choice in that range. Distractors: 59.0 is arctan(150/90), dividing the hypotenuse by a leg as if both were legs; 36.9 is arcsin(0.6), pairing the sine with the adjacent side (it is the angle at the top of the cliff); 31.0 is arctan(90/150), treating the 150-meter line as a leg.

**Desmos** (not yet verified in Desmos). Type:<br><code>\arccos\left(\frac{90}{150}\right)</code>

Set the angle mode to Degrees; the line shows 53.130..., so the angle is 53.1°. In Radians the line shows 0.927, the same angle in the wrong unit.

</details>

---

### 9. geo-complementary-radians-k

*Medium · Student-produced response · route: either · techniques: T11, T12*

Angles $A$ and $B$ are complementary, and the measure of angle $A$ is $\frac{3\pi}{10}$ radians. The measure of angle $B$ is $k\pi$ radians, where $k$ is a constant. What is the value of $k$?

**Answer:** 1/5 (≈ 0.2)

<details><summary>Solutions</summary>

**By hand.** Complementary angles add to 90°, which is π/2 radians, since 360° = 2π radians. So the measure of angle B is π/2 - 3π/10 = 5π/10 - 3π/10 = 2π/10 = π/5 radians. Writing π/5 as kπ gives k = 1/5. Therefore, k = 1/5. A common mistake is to subtract from π (the supplement), which gives k = 7/10.

**Desmos** (not yet verified in Desmos). Type:<br><code>B=\frac{\pi}{2}-\frac{3\pi}{10}</code><br><code>\frac{B}{\pi}</code>

The second line shows 0.2; use the fraction toggle to see 1/5. Enter 1/5 or .2. The angle mode setting does not matter here.

</details>

---

### 10. geo-cos-to-tan-nontriple

*Medium · Multiple choice · route: hand-primary · techniques: T12, T13*

In right triangle $PQR$, angle $Q$ is the right angle and $\cos P = \frac{3}{7}$. What is the value of $\tan P$?

- **A.** $\frac{3\sqrt{10}}{20}$
- **B.** $\frac{2\sqrt{10}}{7}$
- **C.** $\frac{7\sqrt{10}}{20}$
- **D.** $\frac{2\sqrt{10}}{3}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Since cos P = 3/7, the leg adjacent to angle P can be taken as 3 and the hypotenuse as 7. By the Pythagorean theorem, the opposite leg is √(7^2 - 3^2) = √40 = 2√10. So tan P = opposite/adjacent = 2√10/3. Therefore, tan P = 2√10/3. Distractors: \frac{3\sqrt{10}}{20} is 3/(2√10), the adjacent leg over the opposite leg (the reciprocal of tan P); \frac{2\sqrt{10}}{7} is opposite/hypotenuse, which is sin P; \frac{7\sqrt{10}}{20} is 7/(2√10), hypotenuse over the opposite leg.

**Desmos** (not yet verified in Desmos). Type:<br><code>\tan\left(\arccos\left(\frac{3}{7}\right)\right)</code><br><code>\frac{2\sqrt{10}}{3}</code>

Desmos is slower than sketching the triangle. As a check, both lines show 2.108... (the angle mode does not matter, since arccos and tan use the same mode).

</details>

---

### 11. geo-escalator-horizontal-30-60-90

*Medium · Multiple choice · route: hand-primary · techniques: T12, T13*

An escalator is 12 meters long from bottom to top and makes a 30° angle with the horizontal floor. What is the horizontal distance, in meters, between the bottom and the top of the escalator?

- **A.** $4\sqrt{3}$
- **B.** $6\sqrt{2}$
- **C.** $6\sqrt{3}$
- **D.** $12\sqrt{3}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The escalator (12 meters) is the hypotenuse of a 30-60-90 triangle, the vertical rise is the leg opposite the 30° angle, and the horizontal distance is the leg opposite the 60° angle. In a 30-60-90 triangle the shorter leg is half the hypotenuse, 6, and the longer leg is √3 times the shorter leg, 6√3. Therefore, the horizontal distance is 6√3 meters. Distractors: 4\sqrt{3} divides the hypotenuse by √3; 6\sqrt{2} uses the √2 ratio of a 45-45-90 triangle; 12\sqrt{3} multiplies the hypotenuse, not the shorter leg, by √3.

**Desmos** (not yet verified in Desmos). Type:<br><code>12\cos(30)</code><br><code>6\sqrt{3}</code>

Desmos is slower than the special right triangle. As a check, in Degrees mode both lines show 10.392..., so the choice 6√3 matches.

</details>

---

### 12. geo-garden-diagonal-path-cosine

*Medium · Multiple choice · route: desmos-primary · techniques: T12*

A rectangular garden is 30 meters long. A straight path runs between two opposite corners of the garden and makes an angle of 28° with the longer side. To the nearest tenth, what is the length, in meters, of the path?

- **A.** $14.1$
- **B.** $26.5$
- **C.** $34.0$
- **D.** $63.9$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The path, the longer side, and a shorter side of the garden form a right triangle in which the path is the hypotenuse and the 30-meter side is adjacent to the 28° angle. So cos 28° = 30/p, where p is the length of the path, and p = 30/cos 28° ≈ 30/0.8829 ≈ 33.98. Therefore, the path is 34.0 meters long to the nearest tenth. Without a calculator: the path is a hypotenuse, so it is longer than 30, and since 28° < 45°, cos 28° > cos 45°, so p < 30√2 ≈ 42.4; 34.0 is the only choice between 30 and 42.4. Distractors: 26.5 is 30 cos 28°, multiplying by the cosine instead of dividing; 14.1 is 30 sin 28°, pairing the sine with the adjacent side; 63.9 is 30/sin 28°, dividing by the sine instead of the cosine.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{30}{\cos(28)}</code>

Open the wrench menu and set the angle mode to Degrees before reading; in Radians the same line gives a wrong value. The line shows 33.977..., so the path is 34.0 meters to the nearest tenth.

</details>

---

### 13. geo-isosceles-right-area

*Medium · Multiple choice · route: hand-primary · techniques: T12*

Triangle $ABC$ has a right angle at $C$, and the measure of angle $A$ is 45°. The length of side $AB$ is 10 units. What is the area of triangle $ABC$, in square units?

- **A.** $12.5$
- **B.** $25$
- **C.** $50$
- **D.** $100$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A right triangle with a 45° angle is an isosceles right triangle, so the legs AC and BC are equal. In a 45-45-90 triangle the hypotenuse is √2 times a leg, so each leg is 10/√2 = 5√2 units. The area is (1/2)(5√2)(5√2) = (1/2)(50) = 25 square units. Therefore, the area is 25. Alternate approach: with hypotenuse c, the legs are c sin 45° and c cos 45°, so the area is (1/2)(c^2)(1/2) = c^2/4 = 100/4 = 25. Distractors: 50 is (1/2)(10)(10), using the hypotenuse as both legs; 100 is 10^2, squaring the hypotenuse with no halving; 12.5 is (1/2)(5)(5), using 5 (half the hypotenuse) as each leg.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{1}{2}\cdot10\sin(45)\cdot10\cos(45)</code>

In Degrees mode the line shows 25. Recognizing the 45-45-90 triangle (legs 5√2) is faster than typing this.

</details>

---

### 14. geo-pole-wire-tangent-height

*Medium · Multiple choice · route: desmos-primary · techniques: T12*

A support wire runs in a straight line from the top of a vertical pole to a point on level ground 15 meters from the base of the pole. The wire makes an angle of 40° with the ground. What is the height, in meters, of the pole, to the nearest tenth?

- **A.** $9.6$
- **B.** $12.6$
- **C.** $17.9$
- **D.** $19.6$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The pole, the ground, and the wire form a right triangle in which the 15-meter ground distance is the leg adjacent to the 40° angle and the pole's height h is the opposite leg. So tan 40° = h/15 and h = 15 tan 40° ≈ 15(0.8391) ≈ 12.59. Therefore, the height is 12.6 meters to the nearest tenth. Distractors: 9.6 is 15 sin 40°, treating the 15 meters as the wire (the hypotenuse); 17.9 is 15/tan 40°, inverting the tangent ratio; 19.6 is 15/cos 40°, the length of the wire rather than the pole.

**Desmos** (not yet verified in Desmos). Type:<br><code>15\tan(40)</code>

Open the settings and switch to Degrees first; in Radians the line gives a wrong value. The line shows 12.586..., so the height is 12.6 meters.

</details>

---

### 15. geo-post-shadow-sun-elevation

*Medium · Student-produced response · route: desmos-primary · techniques: T12*

A vertical post 3.2 meters tall stands on level ground. When the angle of elevation of the sun is 35°, what is the length, in meters, of the shadow of the post, to the nearest tenth?

**Answer:** 23/5 (≈ 4.6)

<details><summary>Solutions</summary>

**By hand.** The post, its shadow, and the sun's ray through the top of the post form a right triangle. The 35° angle is at the tip of the shadow, the post (3.2 meters) is the leg opposite that angle, and the shadow s is the adjacent leg. So tan 35° = 3.2/s, and s = 3.2/tan 35° ≈ 3.2/0.7002 ≈ 4.57. Therefore, the shadow is 4.6 meters long to the nearest tenth. Common mistakes: 3.2 tan 35° ≈ 2.2 inverts the ratio, and 3.2/sin 35° ≈ 5.6 gives the length of the sun's ray from the top of the post to the tip of the shadow.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{3.2}{\tan(35)}</code>

Switch the angle mode to Degrees first; in Radians the line gives a wrong value. The line shows 4.570..., so enter 4.6.

</details>

---

### 16. geo-ramp-angle-arctan

*Medium · Multiple choice · route: desmos-primary · techniques: T12*

A straight ramp rises 7 feet over a horizontal distance of 24 feet. To the nearest degree, what is the measure of the angle that the ramp makes with the horizontal?

- **A.** $16$
- **B.** $17$
- **C.** $73$
- **D.** $74$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The rise of 7 feet is the leg opposite the angle and the horizontal run of 24 feet is the adjacent leg, so tan θ = 7/24 and θ = arctan(7/24) ≈ 16.3°. Therefore, the angle measures 16° to the nearest degree. (The ramp itself is 25 feet long, since 7-24-25 is a Pythagorean triple.) Distractors: 17 is arcsin(7/24) ≈ 17.0°, treating the 24-foot run as the hypotenuse; 73 is arccos(7/24) ≈ 73.0°, treating 7 as the adjacent leg and 24 as the hypotenuse; 74 is 90° - 16°, the other acute angle of the triangle.

**Desmos** (not yet verified in Desmos). Type:<br><code>\arctan\left(\frac{7}{24}\right)</code>

Set the angle mode to Degrees; the line shows 16.26..., so the angle is 16° to the nearest degree. In Radians the line shows 0.284, the same angle in the wrong unit.

</details>

---

### 17. geo-river-width-survey-tangent

*Medium · Multiple choice · route: desmos-primary · techniques: T12*

A surveyor marks point $A$ on a straight riverbank directly across from point $B$ on the other bank. Point $C$ is on the same bank as $A$, 80 meters from $A$, with angle $BAC$ a right angle and angle $ACB$ measuring 58°. To the nearest tenth, what is the length, in meters, of $AB$?

- **A.** $42.4$
- **B.** $50.0$
- **C.** $67.8$
- **D.** $128.0$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Triangle ABC has its right angle at A. For the 58° angle at C, side AB is the opposite leg and side AC = 80 meters is the adjacent leg, so tan 58° = AB/80 and AB = 80 tan 58° ≈ 80(1.6003) ≈ 128.03. Therefore, AB is 128.0 meters to the nearest tenth. Without a calculator: 58° > 45°, so tan 58° > tan 45° = 1 and AB > 80; 128.0 is the only choice greater than 80. Distractors: 42.4 is 80 cos 58°, using the cosine and treating 80 as the hypotenuse; 50.0 is 80/tan 58°, inverting the tangent ratio; 67.8 is 80 sin 58°, using the sine and treating 80 as the hypotenuse.

**Desmos** (not yet verified in Desmos). Type:<br><code>80\tan(58)</code>

Set the angle mode to Degrees first. The line shows 128.026..., so AB is 128.0 meters to the nearest tenth.

</details>

---

### 18. geo-similar-triangle-tan-scaled

*Medium · Student-produced response · route: hand-primary · techniques: —*

Right triangle $ABC$ has its right angle at $C$, with $AC = 15$ and $AB = 17$. Triangle $DEF$ is similar to triangle $ABC$, where $D$, $E$, and $F$ correspond to $A$, $B$, and $C$, respectively, and each side of triangle $DEF$ is 3 times as long as the corresponding side of triangle $ABC$. What is the value of $\tan E$?

**Answer:** 15/8 (≈ 1.875)

<details><summary>Solutions</summary>

**By hand.** By the Pythagorean theorem, BC = √(17^2 - 15^2) = √64 = 8. Corresponding angles of similar triangles are congruent, so angle E is congruent to angle B, and tan E = tan B. In triangle ABC, the leg opposite angle B is AC = 15 and the adjacent leg is BC = 8, so tan B = 15/8. The scale factor of 3 multiplies both legs and does not change the ratio: (45)/(24) = 15/8. Therefore, tan E = 15/8, which can be entered as 15/8 or 1.875. Common mistakes: 8/15 is tan A, and 45/8 multiplies only one side by 3.

</details>

---

### 19. geo-sin-4x-cos-x-complement

*Medium · Student-produced response · route: either · techniques: T1, T12*

If $\sin(4x^\circ) = \cos(x^\circ)$, where $0 < x < 20$, what is the value of $x$?

**Answer:** 18

<details><summary>Solutions</summary>

**By hand.** The sine of an acute angle equals the cosine of its complement: cos(x°) = sin((90 - x)°). So the given equation becomes sin(4x°) = sin((90 - x)°). For 0 < x < 20, both 4x and 90 - x lie between 0 and 90, where the sine function takes each value once, so 4x = 90 - x. Adding x to both sides yields 5x = 90, and x = 18. Therefore, x = 18. Setting 4x = x instead (treating sine and cosine as the same function) gives no solution in the range, and the other solution of the equation, x = 30, is excluded by the restriction.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sin(4x)</code><br><code>y=\cos(x)</code>

Set the angle mode to Degrees first. Click the intersection with 0 < x < 20: (18, 0.951). The next crossing, at x = 30, is outside the given range.

</details>

---

### 20. geo-tan-complement

*Medium · Multiple choice · route: hand-primary · techniques: T12, T11*

In right triangle $ABC$, angle $C$ is the right angle and $\sin A = \frac{5}{13}$. What is the value of $\tan B$?

- **A.** $\frac{5}{13}$
- **B.** $\frac{5}{12}$
- **C.** $\frac{12}{13}$
- **D.** $\frac{12}{5}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** sin A = 5/13 means the side opposite A is 5 and the hypotenuse is 13, so the other leg is 12 (5-12-13). Angle B is opposite the side of length 12, so tan B = 12/5. Distractors: 5/12 is tan A, 12/13 is cos A (= sin B), 5/13 repeats the given.

**Desmos** (not yet verified in Desmos). Type:<br><code>\tan\left(\frac{\pi}{2}-\arcsin\left(\frac{5}{13}\right)\right)</code>

In radian mode this shows 2.4, which the fraction toggle turns into 12/5. The 5-12-13 triangle is faster.

</details>

---

### 21. geo-triangle-angles-sin-cos-equal

*Medium · Multiple choice · route: hand-primary · techniques: —*

In triangle $ABC$, angle $A$ measures $(2x)^\circ$ and angle $B$ measures $(x + 6)^\circ$. If $\sin A = \cos B$, what is the measure, in degrees, of angle $A$?

- **A.** $12$
- **B.** $28$
- **C.** $34$
- **D.** $56$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** If the sine of one angle equals the cosine of another, the angles are complementary or differ by 90°. The second case, 2x = (x + 6) + 90, gives x = 96 and an angle A of 192°, which is impossible in a triangle. So A + B = 90: 2x + (x + 6) = 90, 3x = 84, and x = 28. Then angle A measures 2(28) = 56 degrees (and angle B measures 34°, making angle C a right angle). Therefore, angle A measures 56°. Distractors: 12 sets the two angles equal, 2x = x + 6; 28 is the value of x rather than the measure of angle A; 34 is the measure of angle B.

</details>

---

### 22. geo-truck-ramp-length-sine

*Medium · Multiple choice · route: desmos-primary · techniques: T12*

A straight loading ramp runs from level ground up to the bed of a truck, which is 1.2 meters above the ground. The ramp makes a 14° angle with the ground. What is the length, in meters, of the ramp, to the nearest tenth?

- **A.** $0.3$
- **B.** $1.2$
- **C.** $4.8$
- **D.** $5.0$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The ramp, the ground, and the vertical drop from the truck bed form a right triangle in which the ramp is the hypotenuse and the 1.2-meter height is the leg opposite the 14° angle. So sin 14° = 1.2/L, where L is the ramp length, and L = 1.2/sin 14° ≈ 1.2/0.2419 ≈ 4.96. Therefore, the ramp is 5.0 meters long to the nearest tenth. Distractors: 0.3 is 1.2 tan 14°, multiplying by the tangent instead of dividing by the sine; 1.2 is 1.2/sin 14 evaluated in radian mode; 4.8 is 1.2/tan 14°, the horizontal distance along the ground rather than the ramp.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{1.2}{\sin(14)}</code>

Set the angle mode to Degrees first; in Radians the same line shows 1.211, a wrong value. In Degrees it shows 4.960..., so the ramp is 5.0 meters long.

</details>

---

### 23. geo-30-60-90-area-hypotenuse

*Hard · Multiple choice · route: hand-primary · techniques: —*

Triangle $ABC$ has a right angle at $B$, and the measure of angle $A$ is 30°. The area of triangle $ABC$ is $18\sqrt{3}$ square units. What is the length of side $AC$?

- **A.** $6$
- **B.** $12$
- **C.** $18$
- **D.** $36$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Side AC is opposite the right angle, so it is the hypotenuse. In a 30-60-90 triangle the side opposite the 30° angle, BC, is half the hypotenuse, and the side opposite the 60° angle, AB, is √3 times BC. Let BC = s; then AB = s√3 and the area is (1/2)(s)(s√3) = (s^2√3)/2. Setting this equal to 18√3 and multiplying both sides by 2/√3 yields s^2 = 36, so s = 6 and AC = 2s = 12. Therefore, AC = 12. Distractors: 6 is the shorter leg BC, an intermediate result; 36 is s^2, the square of the shorter leg; 18 takes the coefficient of the given area as a side length.

</details>

---

### 24. geo-altitude-45-30-split-base

*Hard · Multiple choice · route: hand-primary · techniques: —*

In triangle $ABC$, angle $A$ measures 45° and angle $B$ measures 30°. The altitude from vertex $C$ meets side $AB$ at point $D$, and $CD = 6$. What is the length of $AB$?

- **A.** $6\sqrt{3}$
- **B.** $6 + 6\sqrt{3}$
- **C.** $6\sqrt{2} + 6\sqrt{3}$
- **D.** $12 + 6\sqrt{3}$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Segment CD splits triangle ABC into two right triangles with the right angle at D. Triangle ADC has a 45° angle at A, so it is a 45-45-90 triangle and AD = CD = 6. Triangle BDC has a 30° angle at B, so it is a 30-60-90 triangle in which CD = 6 is the shorter leg (opposite the 30° angle) and DB, the longer leg, is 6√3. So AB = AD + DB = 6 + 6√3. Therefore, AB = 6 + 6√3. Distractors: 6\sqrt{3} is DB alone, an intermediate result; 6\sqrt{2} + 6\sqrt{3} adds the hypotenuse AC = 6√2 instead of the leg AD; 12 + 6\sqrt{3} adds the hypotenuse BC = 12 instead of AD.

</details>

---

### 25. geo-altitude-angle-sine

*Hard · Student-produced response · route: hand-primary · techniques: T12, T11*

In triangle $ABC$, angle $C$ is a right angle, $AC = 6$, and $BC = 8$. Point $D$ lies on side $AB$ such that segment $CD$ is perpendicular to $AB$. What is the value of $\sin(\angle ACD)$?

**Answer:** 3/5 (≈ 0.6)

<details><summary>Solutions</summary>

**By hand.** In right triangle ACD, angle D is the right angle, so angle ACD = 90° - angle CAD = 90° - angle A. In right triangle ABC, angle B = 90° - angle A as well, so angle ACD and angle B have the same measure, and sin(∠ACD) = sin B. By the Pythagorean theorem, AB = √(6^2 + 8^2) = 10, and sin B = (leg opposite B)/(hypotenuse) = AC/AB = 6/10 = 3/5. Therefore, sin(∠ACD) = 3/5. Alternate approach: triangles ACD and ABC are similar (both right, sharing angle A), so AD/AC = AC/AB = 3/5. Using 4/5 (which is sin A, or equivalently cos B) is the common slip: that is the sine of angle BCD, not of angle ACD.

**Desmos** (not yet verified in Desmos). Type:<br><code>\cos\left(\arctan\left(\frac{8}{6}\right)\right)</code>

Angle mode does not matter here, because arctan and cos use the same mode. The line shows 0.6; enter 3/5 or .6. The similar-triangle reasoning is faster than building this expression.

</details>

---

### 26. geo-coterminal-radians

*Hard · Multiple choice · route: hand-primary · techniques: T12, T13*

An angle with a measure of $\frac{83\pi}{6}$ radians is coterminal with an angle whose measure is $\theta$ radians, where $0 \leq \theta < 2\pi$. What is the value of $\theta$?

- **A.** $\frac{\pi}{6}$
- **B.** $\frac{5\pi}{6}$
- **C.** $\frac{7\pi}{6}$
- **D.** $\frac{11\pi}{6}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** One full turn is 2π = 12π/6. 83π/6 - 6 · 12π/6 = 83π/6 - 72π/6 = 11π/6, which is in [0, 2π). Distractors: 5π/6 subtracts multiples of π (6π/6) instead of 2π (83 - 78 = 5); π/6 is the reference angle of 11π/6 (or 2π - 11π/6); 7π/6 puts that reference angle in the wrong quadrant.

**Desmos** (not yet verified in Desmos). Type:<br><code>\sin\left(\frac{83\pi}{6}\right)</code><br><code>\cos\left(\frac{83\pi}{6}\right)</code><br><code>\sin\left(\frac{11\pi}{6}\right)</code><br><code>\cos\left(\frac{11\pi}{6}\right)</code>

In radian mode, coterminal angles have the same sine and cosine: the given angle shows sin = -0.5 and cos = 0.866, and only 11π/6 among the choices matches both. Subtracting multiples of 2π by hand is faster.

</details>

---

### 27. geo-isosceles-base-cosine

*Hard · Multiple choice · route: desmos-primary · techniques: T12*

In triangle $JKL$, $JK = JL = 10$ and the measure of angle $K$ is 50°. To the nearest tenth, what is the length of $KL$?

- **A.** $6.4$
- **B.** $7.7$
- **C.** $12.9$
- **D.** $15.3$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Since JK = JL, the altitude from J to side KL bisects KL at a point M, forming right triangle JMK with hypotenuse JK = 10 and a 50° angle at K. Side KM is adjacent to that angle, so KM = 10 cos 50° ≈ 10(0.6428) ≈ 6.428. Then KL = 2(KM) ≈ 12.856. Therefore, KL is 12.9 to the nearest tenth. Without a calculator: angle J = 180° - 50° - 50° = 80° is the largest angle, so KL, opposite it, is longer than 10; and KL = 20 cos 50° < 20 cos 45° = 10√2 ≈ 14.1. Only 12.9 lies between 10 and 14.1. Distractors: 6.4 is KM, half of KL, an intermediate result; 7.7 is 10 sin 50°, the altitude JM; 15.3 is 2(10 sin 50°), using the sine instead of the cosine.

**Desmos** (not yet verified in Desmos). Type:<br><code>2\cdot10\cos(50)</code>

Set the angle mode to Degrees first. The line shows 12.855..., so KL is 12.9 to the nearest tenth.

</details>

---

### 28. geo-legs-differ-by-7-area

*Hard · Student-produced response · route: either · techniques: T1*

The lengths of the two legs of a right triangle differ by 7, and the length of the hypotenuse is 17. What is the area of the triangle?

**Answer:** 60

<details><summary>Solutions</summary>

**By hand.** Let the shorter leg be x; then the longer leg is x + 7. By the Pythagorean theorem, x^2 + (x + 7)^2 = 17^2, which yields 2x^2 + 14x + 49 = 289, then 2x^2 + 14x - 240 = 0 and x^2 + 7x - 120 = 0. Factoring gives (x + 15)(x - 8) = 0, and since a length is positive, x = 8. The legs are 8 and 15 (the 8-15-17 triple), so the area is (1/2)(8)(15) = 60. Therefore, the area is 60. Common mistakes: 120 omits the factor 1/2, and 8 is the shorter leg, an intermediate result.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x^2+(x+7)^2</code><br><code>y=289</code><br><code>\frac{1}{2}\cdot8\cdot15</code>

Here x is the shorter leg. Click the intersection with x > 0: (8, 289), so the legs are 8 and 15. The third line then shows the area, 60. Ignore the intersection at x = -15, which is not a length.

</details>

---

### 29. geo-lighthouse-two-elevations

*Hard · Multiple choice · route: either · techniques: T1, T12*

From point $A$ on level ground, the angle of elevation to the top of a vertical lighthouse is 30°. Point $B$ lies 40 meters closer to the lighthouse, on the line from $A$ to its base, and from $B$ the angle of elevation is 45°. To the nearest tenth, what is the height, in meters, of the lighthouse?

- **A.** $14.6$
- **B.** $40.0$
- **C.** $54.6$
- **D.** $94.6$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Let h be the height and d the distance from B to the base. From B, tan 45° = h/d, so d = h. From A, which is d + 40 meters from the base, tan 30° = h/(d + 40) = 1/√3, so h + 40 = h√3. Then h(√3 - 1) = 40 and h = 40/(√3 - 1) = 20(√3 + 1) ≈ 54.64. Therefore, the lighthouse is 54.6 meters tall to the nearest tenth. Distractors: 14.6 is 40/(√3 + 1), from writing h√3 + h = 40 (adding instead of subtracting); 40.0 uses sin 30° = 1/2 in place of tan 30°, which gives h + 40 = 2h; 94.6 is the horizontal distance from A to the base, h + 40, rather than the height.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x\tan(45)</code><br><code>y=(x+40)\tan(30)</code>

Set the angle mode to Degrees first. Here x is the distance from B to the base and y is the height. Click the intersection: (54.641, 54.641), so the height is 54.6 meters. Zoom out if the intersection is off screen.

</details>

---

### 30. geo-parallel-segment-cos-complement

*Hard · Multiple choice · route: hand-primary · techniques: —*

In triangle $PQR$, angle $R$ is a right angle. Point $S$ lies on side $PR$, and point $T$ lies on side $PQ$ such that segment $ST$ is perpendicular to side $PR$. If $PS = 12$ and $ST = 5$, what is the value of $\cos Q$?

- **A.** $\frac{5}{13}$
- **B.** $\frac{5}{12}$
- **C.** $\frac{12}{13}$
- **D.** $\frac{12}{5}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Triangle PST has a right angle at S, so by the Pythagorean theorem PT = √(12^2 + 5^2) = 13. Triangles PST and PRQ share angle P and both have a right angle (at S and at R), so they are similar, and angle PTS corresponds to angle Q. So cos Q = cos(angle PTS) = TS/PT = 5/13. Equivalently, angles P and Q are complementary, so cos Q = sin P = 5/13. Therefore, cos Q = 5/13. Distractors: 5/12 is ST/PS, which is tan P; 12/13 is PS/PT, which is cos P (equal to sin Q); 12/5 is PS/ST, which is tan Q.

</details>

---

### 31. geo-quadrant-four-cosine

*Hard · Multiple choice · route: hand-primary · techniques: T12, T11*

For an angle with measure $\theta$ radians, where $\frac{3\pi}{2} < \theta < 2\pi$, $\sin\theta = -\frac{5}{13}$. What is the value of $\cos\theta$?

- **A.** $-\frac{12}{13}$
- **B.** $-\frac{5}{13}$
- **C.** $\frac{5}{13}$
- **D.** $\frac{12}{13}$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Because sin^2 θ + cos^2 θ = 1, cos^2 θ = 1 - 25/169 = 144/169, so cos θ = 12/13 or cos θ = -12/13. The condition 3π/2 < θ < 2π places θ in the fourth quadrant, where the x-coordinate of the point on the unit circle is positive, so cos θ is positive. Therefore, cos θ = 12/13. Distractors: -12/13 has the right magnitude but the sign of the second or third quadrant; -5/13 repeats the given sine; 5/13 drops the sign of the sine instead of computing the cosine.

**Desmos** (not yet verified in Desmos). Type:<br><code>\cos\left(\arcsin\left(-\frac{5}{13}\right)\right)</code>

Either angle mode works, since arcsin and cos share it; arcsin returns an angle coterminal with θ. The line shows 0.923 and the fraction toggle gives 12/13. Reasoning with a 5-12-13 triangle and the quadrant sign is faster.

</details>

---

### 32. geo-right-triangle-area-hypotenuse-angle

*Hard · Multiple choice · route: desmos-primary · techniques: T12*

Triangle $ABC$ has a right angle at $C$, hypotenuse $AB = 15$, and an angle of 64° at $A$. To the nearest tenth, what is the area of triangle $ABC$?

- **A.** $44.3$
- **B.** $49.3$
- **C.** $88.7$
- **D.** $101.1$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Side AB is the hypotenuse. The leg opposite angle A is BC = 15 sin 64° ≈ 13.482, and the leg adjacent to angle A is AC = 15 cos 64° ≈ 6.576. The legs are perpendicular, so the area is (1/2)(BC)(AC) ≈ (1/2)(13.482)(6.576) ≈ 44.33. Therefore, the area is 44.3 to the nearest tenth. Without a calculator: for a fixed hypotenuse of 15, the area is largest at 45° and gets smaller as angle A moves away from 45°. At 60° the triangle is a 30-60-90 triangle with legs 7.5 and 7.5√3, so its area is (1/2)(7.5)(7.5√3) ≈ 48.7; at 64° the area is less than 48.7, and 44.3 is the only choice that is. Distractors: 49.3 is (1/2)(15)(15 cos 64°), using the hypotenuse as the base with leg AC as the height; 88.7 is (BC)(AC) without the factor 1/2; 101.1 is (1/2)(15)(15 sin 64°), using the hypotenuse as the base with leg BC as the height.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{1}{2}\cdot15\sin(64)\cdot15\cos(64)</code>

Set the angle mode to Degrees first. The line shows 44.325..., so the area is 44.3 to the nearest tenth.

</details>

---

### 33. geo-shadow-flagpole-hypotenuse

*Hard · Student-produced response · route: hand-primary · techniques: —*

At a certain time, a vertical post 1.5 meters tall casts a shadow 2 meters long on level ground. At the same time, a nearby vertical flagpole casts a shadow 14 meters long. What is the distance, in meters, from the top of the flagpole to the tip of its shadow?

**Answer:** 35/2 (≈ 17.5)

<details><summary>Solutions</summary>

**By hand.** The sun's rays make the same angle with the ground for both objects, so the right triangles formed by each object, its shadow, and the ray through its top are similar. The ratio of height to shadow is 1.5/2 = 0.75, so the flagpole is 0.75(14) = 10.5 meters tall. The requested distance is the hypotenuse of the flagpole's triangle: √(10.5^2 + 14^2) = √(110.25 + 196) = √306.25 = 17.5. (The post's triangle has sides 1.5, 2, and 2.5, a 3-4-5 triangle, and the flagpole's triangle is 7 times as large.) Therefore, the distance is 17.5 meters. Common mistakes: 10.5 is the height of the flagpole, an intermediate result, and 2.5 is the post's hypotenuse.

</details>

---

### 34. geo-sin-cos-degrees

*Hard · Multiple choice · route: either · techniques: T12, T1*

For an angle measure $x$, where $0 < x < 90$, $\sin(x^\circ) = \cos\left((2x + 15)^\circ\right)$. What is the value of $x$?

- **A.** $25$
- **B.** $37.5$
- **C.** $65$
- **D.** $75$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** sin(x°) = cos((90 - x)°), so 2x + 15 = 90 - x, giving 3x = 75 and x = 25. Distractors: 65 is 90 - 25, 37.5 solves 2x + 15 = 90 (drops the x), 75 is 90 - 15.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sin(x)</code><br><code>y=\cos(2x+15)</code>

Switch the calculator to degrees first. Between x = 0 and x = 90 the graphs cross once, at x = 25.

</details>

---

### 35. geo-sin-twice-cos-value

*Hard · Multiple choice · route: hand-primary · techniques: T12, T13*

Angle $C$ of right triangle $ABC$ is a right angle, and $\sin A = 2\cos A$. What is the value of $\cos A$?

- **A.** $\frac{\sqrt{5}}{5}$
- **B.** $\frac{\sqrt{3}}{3}$
- **C.** $\frac{2\sqrt{5}}{5}$
- **D.** $\sqrt{5}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Dividing both sides of sin A = 2 cos A by cos A yields tan A = 2, so the leg opposite angle A can be taken as 2 and the adjacent leg as 1. By the Pythagorean theorem, the hypotenuse is √(2^2 + 1^2) = √5. So cos A = adjacent/hypotenuse = 1/√5 = √5/5. Therefore, cos A = √5/5. Distractors: \frac{\sqrt{3}}{3} uses a hypotenuse of √(2^2 - 1^2) = √3, subtracting the squares instead of adding them; \frac{2\sqrt{5}}{5} is 2/√5, which is sin A; \sqrt{5} is hypotenuse/adjacent, the reciprocal of cos A.

**Desmos** (not yet verified in Desmos). Type:<br><code>\cos(\arctan(2))</code><br><code>\frac{\sqrt{5}}{5}</code>

Desmos is slower than sketching the triangle. As a check, both lines show 0.447... (arctan and cos use the same angle mode, so either mode works).

</details>

---

### 36. geo-sin-x-squared-cos-x

*Hard · Student-produced response · route: either · techniques: T1, T12*

If $\sin\left((x^2)^\circ\right) = \cos(x^\circ)$, where $x > 0$ and $x^2 < 90$, what is the value of $x$?

**Answer:** 9

<details><summary>Solutions</summary>

**By hand.** It's given that x > 0 and x^2 < 90, so both x° and (x^2)° are acute angles. For acute angles, sin(a°) = cos(b°) exactly when a + b = 90. So x^2 + x = 90, which yields x^2 + x - 90 = 0 and (x + 10)(x - 9) = 0. The solution x = -10 is excluded by x > 0, so x = 9. Check: sin(81°) = cos(9°). Therefore, x = 9. Without the restriction x^2 < 90, x = 10 would also satisfy the equation, since sin(100°) = sin(80°) = cos(10°).

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\sin(x^2)</code><br><code>y=\cos(x)</code>

Set the angle mode to Degrees first. Zoom to 0 < x < 10 and click the intersection with x^2 < 90 (x < 9.49): (9, 0.988). The next crossing, at x = 10, has x^2 = 100, which the restriction excludes.

</details>

---

### 37. geo-square-diagonal-2-more

*Hard · Multiple choice · route: hand-primary · techniques: T13*

The length of a diagonal of a square is 2 more than the length of a side of the square. What is the length of a side of the square?

- **A.** $1 + \sqrt{2}$
- **B.** $2 + \sqrt{2}$
- **C.** $2 + 2\sqrt{2}$
- **D.** $4 + 2\sqrt{2}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A diagonal splits the square into two 45-45-90 triangles, so the diagonal is √2 times a side s. It's given that s√2 = s + 2. Subtracting s from both sides yields s(√2 - 1) = 2, so s = 2/(√2 - 1). Multiplying the numerator and denominator by √2 + 1 yields s = 2(√2 + 1)/(2 - 1) = 2 + 2√2. Therefore, the side length is 2 + 2√2. Distractors: 1 + \sqrt{2} computes the denominator (√2 - 1)(√2 + 1) as 2 instead of 1; 2 + \sqrt{2} divides 2 + 2√2 by √2, treating the result as the diagonal; 4 + 2\sqrt{2} is the diagonal, s + 2, rather than the side.

**Desmos** (not yet verified in Desmos). Type:<br><code>s=2+2\sqrt{2}</code><br><code>s\sqrt{2}-s</code>

Desmos is slower than solving by hand. As a check, type a choice as s on the first line: the second line shows 2 exactly when s = 2 + 2√2.

</details>

---
