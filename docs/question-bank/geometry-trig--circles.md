# Circles

[← Question bank index](README.md) · Geometry and Trigonometry · 33 questions, easiest first

### 1. geo-arc-length-100-degrees

*Easy · Multiple choice · route: hand-primary · techniques: T9*

A circle has a radius of 9 units. What is the length, in units, of an arc of the circle that is intercepted by a central angle measuring 100°?

- **A.** $\frac{45\pi}{2}$
- **B.** $18\pi$
- **C.** $5\pi$
- **D.** $\frac{5\pi}{2}$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The arc is 100/360 = 5/18 of the full circle. The circumference is 2π(9) = 18π units, so the arc length is (5/18)(18π) = 5π units. Therefore, the arc length is 5π. Distractors: 5π/2 uses πr instead of 2πr for the circumference; 18π is the whole circumference, with the fraction never applied; 45π/2 is the area of the sector, (5/18)(81π), rather than the arc length.

**Desmos** (not yet verified in Desmos). Type:<br><code>2\pi\cdot9\cdot\frac{100}{360}</code>

Shows 15.708, which is 5π; Desmos will not display the π form, so compare the choices as decimals (5π ≈ 15.71). Taking 100/360 of 18π by hand is quicker.

</details>

---

### 2. geo-circ-equation-from-center-radius

*Easy · Multiple choice · route: hand-primary · techniques: —*

A circle in the $xy$-plane has center $(-3, 5)$ and radius 6. Which equation represents the circle?

- **A.** $(x - 3)^2 + (y + 5)^2 = 6$
- **B.** $(x - 3)^2 + (y + 5)^2 = 36$
- **C.** $(x + 3)^2 + (y - 5)^2 = 6$
- **D.** $(x + 3)^2 + (y - 5)^2 = 36$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A circle in the xy-plane with center (h, k) and radius r has equation (x - h)^2 + (y - k)^2 = r^2. It's given that the center is (-3, 5) and the radius is 6. Substituting -3 for h, 5 for k and 6 for r yields (x - (-3))^2 + (y - 5)^2 = 6^2, or (x + 3)^2 + (y - 5)^2 = 36. Therefore, the equation is (x + 3)^2 + (y - 5)^2 = 36. Distractors: (x + 3)^2 + (y - 5)^2 = 6 uses the radius r instead of r^2 on the right side; (x - 3)^2 + (y + 5)^2 = 36 copies the signs of the center's coordinates into the parentheses, which puts the center at (3, -5); (x - 3)^2 + (y + 5)^2 = 6 makes both mistakes.

</details>

---

### 3. geo-circ-point-on-standard-form

*Easy · Multiple choice · route: hand-primary · techniques: T13*

The equation $(x + 4)^2 + (y - 3)^2 = 100$ represents a circle in the $xy$-plane. Which of the following points is on the circle?

- **A.** $(-4, 3)$
- **B.** $(-4, 103)$
- **C.** $(2, 11)$
- **D.** $(6, 13)$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A point is on the circle exactly when its coordinates satisfy the given equation. Substituting x = 2 and y = 11 yields (2 + 4)^2 + (11 - 3)^2 = 36 + 64 = 100, which is true. Therefore, (2, 11) is on the circle. Distractors: (-4, 3) is the center of the circle, which is inside the circle rather than on it, since (-4 + 4)^2 + (3 - 3)^2 = 0; (-4, 103) moves 100 units up from the center, using r^2 = 100 as the radius instead of r = 10, and gives 0 + 10,000 = 10,000; (6, 13) adds the radius 10 to both coordinates of the center, and gives 100 + 100 = 200, so it lies outside the circle.

**Desmos** (not yet verified in Desmos). Type:<br><code>(x+4)^2+(y-3)^2=100</code><br><code>(-4,3)</code><br><code>(-4,103)</code><br><code>(2,11)</code><br><code>(6,13)</code>

Only the point (2, 11) sits on the circle; (-4, 3) is the center, and (-4, 103) and (6, 13) lie outside it (zoom out to see (-4, 103)). Substituting each point by hand takes a few seconds, so Desmos is only a check.

</details>

---

### 4. geo-circ-sector-radians-area-easy

*Easy · Multiple choice · route: either · techniques: T9*

A sector of a circle has a radius of 10 and a central angle of 1.5 radians. The area of a sector is $\frac{1}{2}r^2\theta$, where $r$ is the radius and $\theta$ is the central angle in radians. What is the area of this sector?

- **A.** $7.5$
- **B.** $15$
- **C.** $75$
- **D.** $150$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** It's given that the area of a sector is (1/2)r^2θ. Substituting 10 for r and 1.5 for θ yields (1/2)(10^2)(1.5) = (1/2)(100)(1.5) = 75. Therefore, the area of the sector is 75. Distractors: 7.5 is (1/2)(10)(1.5), using r instead of r^2; 15 is (10)(1.5) = rθ, the arc length of the sector rather than its area; 150 is (10^2)(1.5), with the factor 1/2 dropped.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{1}{2}\cdot10^2\cdot1.5</code>

The line shows 75. Substituting by hand, (1/2)(100)(1.5), is just as quick.

</details>

---

### 5. geo-circ-skating-rink-arc

*Easy · Student-produced response · route: hand-primary · techniques: —*

A circular skating rink has a radius of 30 meters. A skater glides along the edge of the rink through a central angle of 1.2 radians. The length of an arc of a circle is the product of the radius and the central angle of the arc in radians. How far, in meters, does the skater glide?

**Answer:** 36

<details><summary>Solutions</summary>

**By hand.** It's given that the length of an arc is the product of the radius and the central angle in radians. The skater's path is an arc of the rink's edge with a radius of 30 meters and a central angle of 1.2 radians, so its length is (30)(1.2) = 36 meters. Therefore, the skater glides 36 meters. Multiplying 1.2 by 2π(30) instead, as if 1.2 were a fraction of the full circumference, gives 72π ≈ 226.19, which is longer than the whole edge of the rink.

</details>

---

### 6. geo-radians-7pi-12-to-degrees

*Easy · Multiple choice · route: either · techniques: T12*

What is the degree measure of an angle whose measure is $\frac{7\pi}{12}$ radians?

- **A.** $52.5$
- **B.** $105$
- **C.** $210$
- **D.** $1,260$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since 360° = 2π radians, π radians = 180°, so multiplying a radian measure by 180/π converts it to degrees: (7π/12)(180/π) = 7(180)/12 = 7(15) = 105. Therefore, the angle measures 105°. Distractors: 52.5 uses π radians = 90°; 210 uses π radians = 360°; 1,260 multiplies 7 by 180 and forgets to divide by 12.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{7\pi}{12}\cdot\frac{180}{\pi}</code>

The line shows 105, the measure in degrees; the angle mode setting does not matter for this conversion. By hand it is equally quick.

</details>

---

### 7. geo-tangent-point-distance-center

*Easy · Multiple choice · route: hand-primary · techniques: —*

A circle has center $O$ and a radius of 8. Line $\ell$ is tangent to the circle at point $T$, and point $P$ lies on line $\ell$ such that $PT = 15$. What is the length of segment $OP$?

- **A.** $289$
- **B.** $23$
- **C.** $17$
- **D.** $7$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** A radius drawn to the point of tangency is perpendicular to the tangent line, so angle OTP is a right angle and triangle OTP is a right triangle with legs OT = 8 and PT = 15 and hypotenuse OP. By the Pythagorean theorem, OP^2 = 8^2 + 15^2 = 64 + 225 = 289, so OP = 17. Therefore, OP = 17. Distractors: 289 is OP^2, the value before taking the square root; 23 is 8 + 15, adding the legs instead of their squares; 7 is 15 - 8, the difference of the legs.

</details>

---

### 8. geo-circ-chord-distance-radius

*Medium · Student-produced response · route: hand-primary · techniques: —*

In a circle with center $O$, chord $AB$ has a length of 30. The distance from $O$ to chord $AB$ is 8. What is the radius of the circle?

**Answer:** 17

<details><summary>Solutions</summary>

**By hand.** The distance from O to chord AB is measured along the segment from O perpendicular to AB, and a segment from the center perpendicular to a chord bisects the chord. So that segment meets AB at its midpoint M, with AM = 30/2 = 15 and OM = 8. Triangle OMA has a right angle at M, and OA is a radius. By the Pythagorean theorem, OA^2 = 15^2 + 8^2 = 225 + 64 = 289, so OA = 17. Therefore, the radius is 17. Using the whole chord, 30^2 + 8^2 = 964, misses the bisection step and gives a radius of about 31.05.

</details>

---

### 9. geo-circ-clock-minute-hand-arc

*Medium · Multiple choice · route: hand-primary · techniques: —*

The minute hand of a wall clock is 9 centimeters long. An arc with a central angle of $\theta^\circ$ has a length equal to $\frac{\theta}{360}$ of the circumference of its circle. How far, in centimeters, does the tip of the hand travel from 3:00 to 3:40?

- **A.** $54\pi$
- **B.** $18\pi$
- **C.** $12\pi$
- **D.** $6\pi$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The minute hand makes one full turn, 360°, in 60 minutes, so it turns 360/60 = 6° each minute. From 3:00 to 3:40 is 40 minutes, so the central angle is 40(6) = 240°. It's given that the arc length is θ/360 of the circumference, and the circumference of a circle with radius r is 2πr. Substituting 240 for θ and 9 for r yields (240/360)(2π)(9) = (2/3)(18π) = 12π. Therefore, the tip travels 12π centimeters. Distractors: 6π uses the 120° the hand still has to turn to reach 4:00, not the 240° it turned; 18π is the full circumference, with the fraction 2/3 never applied; 54π is the sector area (2/3)(81π), using r^2 in place of 2r.

</details>

---

### 10. geo-circ-diameter-endpoints-equation

*Medium · Multiple choice · route: desmos-primary · techniques: T10, T13*

In the $xy$-plane, the endpoints of a diameter of a circle are $(-3, 4)$ and $(5, -2)$. Which equation represents the circle?

- **A.** $(x + 1)^2 + (y + 1)^2 = 25$
- **B.** $(x - 4)^2 + (y + 3)^2 = 25$
- **C.** $(x - 1)^2 + (y - 1)^2 = 100$
- **D.** $(x - 1)^2 + (y - 1)^2 = 25$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The center of a circle is the midpoint of any diameter: ((-3 + 5)/2, (4 + (-2))/2) = (1, 1). The radius is half the length of the diameter. By the distance formula, the diameter has length √((5 - (-3))^2 + (-2 - 4)^2) = √(64 + 36) = √100 = 10, so the radius is 5 and r^2 = 25. Therefore, the circle is (x - 1)^2 + (y - 1)^2 = 25. Distractors: (x - 1)^2 + (y - 1)^2 = 100 uses the diameter 10 as the radius; (x + 1)^2 + (y + 1)^2 = 25 copies the signs of the center (1, 1) into the parentheses, which puts the center at (-1, -1); (x - 4)^2 + (y + 3)^2 = 25 takes half the differences of the endpoints' coordinates, (8/2, -6/2) = (4, -3), instead of half their sums.

**Desmos** (not yet verified in Desmos). Type:<br><code>A=(-3,4)</code><br><code>B=(5,-2)</code><br><code>\operatorname{midpoint}(A,B)</code><br><code>\operatorname{distance}(A,B)/2</code>

The midpoint line shows (1, 1), the center, and the last line shows 5, the radius, so r^2 = 25. As a check, type (x-1)^2+(y-1)^2=25 and confirm the circle passes through both points A and B.

</details>

---

### 11. geo-circ-line-through-center-greatest-y

*Medium · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the line with equation $y = x + 1$ intersects the circle with equation $(x - 3)^2 + (y - 4)^2 = 8$ at two points. What is the greater of the $y$-coordinates of these two points?

- **A.** $2$
- **B.** $4$
- **C.** $5$
- **D.** $6$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Substituting x + 1 for y in the circle's equation yields (x - 3)^2 + (x + 1 - 4)^2 = 8, or (x - 3)^2 + (x - 3)^2 = 8. So 2(x - 3)^2 = 8, (x - 3)^2 = 4, and x - 3 = 2 or x - 3 = -2, which gives x = 5 or x = 1. Substituting into y = x + 1 yields the points (5, 6) and (1, 2). Therefore, the greater y-coordinate is 6. Alternate approach: the center (3, 4) lies on the line, so the two points are the ends of a diameter along the line. Distractors: 2 is the y-coordinate of the other intersection point; 4 is the y-coordinate of the center, where the line passes through the circle's interior; 5 is the x-coordinate of the point (5, 6), the wrong coordinate.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=x+1</code><br><code>(x-3)^2+(y-4)^2=8</code>

Click the two gray intersection points: (1, 2) and (5, 6). The greater y-coordinate is 6; take the y-value, not the x-value 5.

</details>

---

### 12. geo-circ-point-inside-expanded

*Medium · Multiple choice · route: desmos-primary · techniques: T10, T13*

In the $xy$-plane, a circle has equation $x^2 + y^2 + 6x - 8y = 0$. Which of the following points lies in the interior of the circle?

- **A.** $(-7, 2)$
- **B.** $(0, 0)$
- **C.** $(3, -4)$
- **D.** $(5, -2)$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Completing the square in x and in y: x^2 + 6x + 9 + y^2 - 8y + 16 = 9 + 16, so (x + 3)^2 + (y - 4)^2 = 25. The circle has center (-3, 4) and radius 5, and a point is inside it exactly when (x + 3)^2 + (y - 4)^2 < 25. For (-7, 2): (-4)^2 + (-2)^2 = 16 + 4 = 20, which is less than 25. Therefore, (-7, 2) lies inside the circle. Distractors: (0, 0) gives 9 + 16 = 25, so it is on the circle, not inside; the missing constant term in the given equation is the clue. (3, -4) is the center with both signs reversed, read straight from +6x and -8y; it gives 36 + 64 = 100. (5, -2) lies inside the circle with that reversed center (3, -4), but for the actual circle it gives 64 + 36 = 100, so it is outside.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2+6x-8y=0</code><br><code>(-7,2)</code><br><code>(0,0)</code><br><code>(3,-4)</code><br><code>(5,-2)</code>

Desmos graphs the expanded form directly. Only (-7, 2) falls inside the circle. (0, 0) sits exactly on the circle (zoom in to see it on the curve, not inside), and (3, -4) and (5, -2) are far outside.

</details>

---

### 13. geo-circ-sprinkler-sector-radius

*Medium · Student-produced response · route: either · techniques: T2*

A lawn sprinkler turns through $80^\circ$, watering a sector-shaped region with an area of $32\pi$ square feet. A sector with central angle $\theta^\circ$ has $\frac{\theta}{360}$ of the area of the full circle. What is the radius, in feet, of the region?

**Answer:** 12

<details><summary>Solutions</summary>

**By hand.** It's given that a sector with central angle θ° has θ/360 of the area of the full circle, and a circle with radius r has area πr^2. Substituting 80 for θ and 32π for the area yields (80/360)πr^2 = 32π. Dividing both sides by π yields (2/9)r^2 = 32, and multiplying both sides by 9/2 yields r^2 = 144. Since r is positive, r = 12. Therefore, the radius of the region is 12 feet. Reporting r^2 = 144 instead of r is the common slip; using the arc-length relationship (80/360)(2πr) = 32π gives r = 72, which treats the area as a length.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\frac{80}{360}\pi x^2</code><br><code>y=32\pi</code>

Click the intersection with positive x: (12, 100.531), so the radius is 12. Ignore the intersection at x = -12, since a radius is positive. Solving the one-variable equation by hand is about as fast.

</details>

---

### 14. geo-circ-translate-left-up

*Medium · Multiple choice · route: either · techniques: T13*

In the $xy$-plane, circle $A$ has equation $(x - 1)^2 + (y + 6)^2 = 20$. Circle $B$ is the image of circle $A$ after a translation 4 units to the left and 3 units up. Which equation represents circle $B$?

- **A.** $(x + 3)^2 + (y + 3)^2 = 20$
- **B.** $(x + 3)^2 + (y + 9)^2 = 20$
- **C.** $(x - 5)^2 + (y + 3)^2 = 20$
- **D.** $(x - 5)^2 + (y + 9)^2 = 20$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Circle A has center (1, -6) and radius √20. A translation moves the center and keeps the radius. Moving 4 units to the left subtracts 4 from the x-coordinate, and moving 3 units up adds 3 to the y-coordinate, so the center of circle B is (1 - 4, -6 + 3) = (-3, -3). Therefore, circle B has equation (x + 3)^2 + (y + 3)^2 = 20. Distractors: (x + 3)^2 + (y + 9)^2 = 20 moves the center 3 units down instead of up, to (-3, -9); (x - 5)^2 + (y + 3)^2 = 20 moves the center 4 units right instead of left, to (5, -3); (x - 5)^2 + (y + 9)^2 = 20 reverses both directions, which happens when 4 is added to x and 3 is subtracted from y inside the parentheses.

**Desmos** (not yet verified in Desmos). Type:<br><code>(x-1)^2+(y+6)^2=20</code><br><code>(x+3)^2+(y+3)^2=20</code><br><code>(x+3)^2+(y+9)^2=20</code><br><code>(x-5)^2+(y+3)^2=20</code><br><code>(x-5)^2+(y+9)^2=20</code>

Compare each choice with the original circle (center (1, -6)). Only the circle from (x + 3)^2 + (y + 3)^2 = 20 sits 4 units left of and 3 units above the original. Moving the center by hand, (1 - 4, -6 + 3) = (-3, -3), is just as fast.

</details>

---

### 15. geo-circ-unit-circle-point-coordinates

*Medium · Multiple choice · route: hand-primary · techniques: —*

In the $xy$-plane, point $P$ lies on the circle with radius 1 and center at the origin $O$. The angle from the positive $x$-axis to segment $OP$, measured counterclockwise, is $\frac{4\pi}{3}$ radians. Which of the following are the coordinates of point $P$?

- **A.** $\left(-\frac{\sqrt{3}}{2}, -\frac{1}{2}\right)$
- **B.** $\left(-\frac{1}{2}, -\frac{\sqrt{3}}{2}\right)$
- **C.** $\left(-\frac{1}{2}, \frac{\sqrt{3}}{2}\right)$
- **D.** $\left(\frac{1}{2}, \frac{\sqrt{3}}{2}\right)$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** A point on the unit circle at an angle of θ radians, measured counterclockwise from the positive x-axis, has coordinates (cos θ, sin θ). The angle 4π/3 radians is 240°, which is 60° past the negative x-axis, so P is in the third quadrant, where both coordinates are negative. Its reference angle is π/3 radians (60°), with cos(π/3) = 1/2 and sin(π/3) = √3/2, so P = (cos(4π/3), sin(4π/3)) = (-1/2, -√3/2). Therefore, the coordinates of P are (-1/2, -√3/2). Distractors: (-√3/2, -1/2) swaps cosine and sine, which is the point at 7π/6 radians; (-1/2, √3/2) is the point at 2π/3 radians, in the second quadrant, from measuring 4π/3 as π/3 short of π instead of π/3 past it; (1/2, √3/2) is the reference-angle point at π/3, with both third-quadrant signs dropped.

</details>

---

### 16. geo-circle-point-k

*Medium · Multiple choice · route: desmos-primary · techniques: T10*

In the $xy$-plane, the circle with equation $x^2 + y^2 - 10x + 6y + 18 = 0$ passes through the point $(5, k)$, where $k > 0$. What is the value of $k$?

- **A.** $1$
- **B.** $4$
- **C.** $5$
- **D.** $7$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Complete the square: (x - 5)^2 + (y + 3)^2 = 16, center (5, -3), radius 4. With x = 5, (y + 3)^2 = 16 so y = 1 or y = -7; k = 1. Distractors: 4 is the radius, 5 is the center's x-coordinate, 7 adds the radius to 3 instead of to -3.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2-10x+6y+18=0</code><br><code>x=5</code>

Desmos graphs the expanded form directly. Click the upper intersection with x = 5: (5, 1).

</details>

---

### 17. geo-sector-angle-garden

*Medium · Student-produced response · route: either · techniques: T1*

A circular garden has a radius of 12 feet. A flower bed in the shape of a sector of the garden has a central angle of $\theta^\circ$ and an area of $30\pi$ square feet. What is the value of $\theta$?

**Answer:** 75

<details><summary>Solutions</summary>

**By hand.** A sector with central angle θ° is θ/360 of the circle. The area of the whole garden is π(12)^2 = 144π square feet, so (θ/360)(144π) = 30π. Dividing both sides by π and multiplying both sides by 360 yields 144θ = 10,800, so θ = 75. Therefore, θ = 75. Using the circumference 24π in place of the area 144π, which gives θ = 450, is the common slip.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=\pi\cdot12^2\cdot\frac{x}{360}</code><br><code>y=30\pi</code>

The intersection is (75, 94.25), so θ = 75. By hand, 30/144 of 360 is the same one-step proportion.

</details>

---

### 18. geo-sector-area-radians-diameter

*Medium · Multiple choice · route: either · techniques: T9*

A circle has a diameter of 16 units. A sector of the circle has a central angle that measures $\frac{3\pi}{4}$ radians. What is the area, in square units, of the sector?

- **A.** $24\pi$
- **B.** $48\pi$
- **C.** $64\pi$
- **D.** $96\pi$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** It's given that the diameter is 16, so the radius is 8 and the area of the whole circle is π(8^2) = 64π. A central angle of 3π/4 radians is (3π/4)/(2π) = 3/8 of a full turn, so the sector's area is (3/8)(64π) = 24π. Therefore, the area of the sector is 24π square units. Alternate approach: the sector area formula (1/2)r^2θ gives (1/2)(64)(3π/4) = 24π. Distractors: 48π omits the 1/2 in (1/2)r^2θ; 64π is the area of the whole circle; 96π uses the diameter 16 as the radius.

**Desmos** (not yet verified in Desmos). Type:<br><code>\frac{1}{2}\cdot8^2\cdot\frac{3\pi}{4}</code>

The line shows 75.398..., which is 24π (24π ≈ 75.40); Desmos will not display the π form, so compare the choices as decimals. Taking 3/8 of 64π by hand is about as quick.

</details>

---

### 19. geo-tan-2pi-3-unit-circle

*Medium · Multiple choice · route: either · techniques: T12, T13*

What is the value of $\tan\left(\frac{2\pi}{3}\right)$?

- **A.** $-\sqrt{3}$
- **B.** $-\frac{\sqrt{3}}{3}$
- **C.** $\frac{\sqrt{3}}{3}$
- **D.** $\sqrt{3}$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** The angle 2π/3 radians (120°) lies in quadrant II with reference angle π/3. On the unit circle its point is (-1/2, √3/2), so tan(2π/3) = sin/cos = (√3/2)/(-1/2) = -√3. Therefore, tan(2π/3) = -√3. Distractors: -√3/3 divides cosine by sine (the cotangent); √3/3 is the cotangent with the quadrant II sign lost; √3 is tan(π/3), the reference-angle value with the sign lost.

**Desmos** (not yet verified in Desmos). Type:<br><code>\tan\left(\frac{2\pi}{3}\right)</code><br><code>-\sqrt{3}</code>

Set the angle mode to Radians first. The first line shows -1.732..., which matches the second line, the choice -√3. In Degrees mode the first line shows 0.0366, a wrong value.

</details>

---

### 20. geo-circ-center-h-through-point

*Hard · Multiple choice · route: desmos-primary · techniques: T13*

In the $xy$-plane, a circle with radius 5 has center $(h, 3)$ and passes through the point $(1, 7)$, where $h$ is a positive constant. What is the value of $h$?

- **A.** $-2$
- **B.** $4$
- **C.** $6$
- **D.** $9$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** The distance from the center (h, 3) to the point (1, 7) equals the radius 5. By the distance formula, (1 - h)^2 + (7 - 3)^2 = 5^2, so (1 - h)^2 + 16 = 25 and (1 - h)^2 = 9. Then 1 - h = 3 or 1 - h = -3, which gives h = -2 or h = 4. Since h is positive, h = 4. Therefore, h = 4. Distractors: -2 is the other solution, discarded because h is positive; 6 is 1 + 5, treating the radius as the horizontal distance from (1, 7) to the center and ignoring the vertical distance 4; 9 is the value of (1 - h)^2, an intermediate result.

**Desmos** (not yet verified in Desmos). Type:<br><code>(1,7)</code><br><code>(x+2)^2+(y-3)^2=25</code><br><code>(x-4)^2+(y-3)^2=25</code><br><code>(x-6)^2+(y-3)^2=25</code><br><code>(x-9)^2+(y-3)^2=25</code>

Two circles pass through (1, 7): the ones with h = -2 and h = 4. The stem says h is positive, so h = 4. The circles with h = 6 and h = 9 miss the point.

</details>

---

### 21. geo-circ-fountain-tangent-path

*Hard · Multiple choice · route: hand-primary · techniques: —*

A circular fountain has a radius of 6 meters. A straight path is tangent to the edge of the fountain at point $T$, and a lamppost on the path is 8 meters from $T$. What is the shortest distance, in meters, from the lamppost to the edge of the fountain?

- **A.** $4$
- **B.** $8$
- **C.** $10$
- **D.** $14$

**Answer:** A

<details><summary>Solutions</summary>

**By hand.** Let O be the center of the fountain and L the lamppost. A radius drawn to the point of tangency is perpendicular to the tangent line, so triangle OTL has a right angle at T, with OT = 6 and TL = 8. By the Pythagorean theorem, OL = √(6^2 + 8^2) = √100 = 10 meters. The closest point of the edge to L lies on segment OL, one radius from O, so the shortest distance is 10 - 6 = 4 meters. Therefore, the shortest distance is 4 meters. Distractors: 8 is the distance along the path from the lamppost to T, a point on the edge but not the closest one; 10 is the distance from the lamppost to the center, an intermediate result; 14 is 8 + 6, adding the two given lengths.

</details>

---

### 22. geo-circ-leading-coefficient-radius

*Hard · Multiple choice · route: either · techniques: T10*

In the $xy$-plane, the graph of $2x^2 + 2y^2 - 12x + 20y + 18 = 0$ is a circle. What is the radius of the circle?

- **A.** $4$
- **B.** $5$
- **C.** $10$
- **D.** $25$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Dividing every term of the given equation by 2 yields x^2 + y^2 - 6x + 10y + 9 = 0. Completing the square in x and in y: x^2 - 6x + 9 + y^2 + 10y + 25 = -9 + 9 + 25, so (x - 3)^2 + (y + 5)^2 = 25. The radius is √25 = 5. Therefore, the radius of the circle is 5. Distractors: 4 divides the x- and y-terms by 2 but not the constant, so the right side becomes -18 + 9 + 25 = 16 and the radius 4; 10 is the diameter; 25 is r^2, reported without taking the square root.

**Desmos** (not yet verified in Desmos). Type:<br><code>2x^2+2y^2-12x+20y+18=0</code><br><code>A=(3,0)</code><br><code>B=(3,-10)</code><br><code>\operatorname{distance}(A,B)/2</code>

Desmos graphs the equation without dividing by 2. Click the circle to show its top and bottom points, (3, 0) and (3, -10); type them as A and B, and the last line shows the radius, 5. By hand, divide by 2 first and complete the square.

</details>

---

### 23. geo-circ-radian-central-inscribed

*Hard · Multiple choice · route: hand-primary · techniques: —*

Points $A$, $B$, and $C$ lie on a circle with center $O$. Central angle $AOB$ measures $\frac{5\pi}{9}$ radians, and point $C$ lies on the major arc $AB$. What is the measure, in degrees, of angle $ACB$?

- **A.** $25$
- **B.** $50$
- **C.** $100$
- **D.** $130$

**Answer:** B

<details><summary>Solutions</summary>

**By hand.** Since π radians = 180°, the central angle measures (5π/9)(180/π) = 100°, so minor arc AB measures 100°. Because C lies on the major arc, inscribed angle ACB intercepts minor arc AB, and an inscribed angle measures half its intercepted arc. So angle ACB measures 100/2 = 50°. Therefore, angle ACB measures 50°. Distractors: 25 converts with π radians = 90°, giving 50° for the central angle and then halving it; 100 is the central angle in degrees, never halved; 130 is 180 - 50, the inscribed angle for a point on the minor arc, which intercepts the 260° major arc instead.

</details>

---

### 24. geo-circ-sector-arc-area-radius

*Hard · Student-produced response · route: hand-primary · techniques: —*

A sector of a circle has an arc length of $6\pi$ and an area of $27\pi$. For a sector with a central angle of $\theta$ radians, the arc length is $\theta$ times the radius, and the area is $\frac{1}{2}\theta$ times the square of the radius. What is the radius of the sector?

**Answer:** 9

<details><summary>Solutions</summary>

**By hand.** Let r be the radius. It's given that the arc length is rθ and the area is (1/2)r^2θ. The area can be written as (1/2)r(rθ), so the area equals (1/2)r times the arc length. Substituting the given values yields 27π = (1/2)r(6π) = 3πr, so r = 9. Therefore, the radius of the sector is 9. Check: θ = 6π/9 = 2π/3 radians, and (1/2)(81)(2π/3) = 27π. Common slip: dividing the area by the arc length, 27π/(6π) = 4.5, forgets the factor 1/2.

</details>

---

### 25. geo-circ-tangent-x-axis-constant

*Hard · Student-produced response · route: hand-primary · techniques: T10*

In the $xy$-plane, the graph of $x^2 + y^2 + 10x - 6y + k = 0$ is a circle that is tangent to the $x$-axis, where $k$ is a constant. What is the value of $k$?

**Answer:** 25

<details><summary>Solutions</summary>

**By hand.** Completing the square in x and in y: x^2 + 10x + 25 + y^2 - 6y + 9 = -k + 25 + 9, so (x + 5)^2 + (y - 3)^2 = 34 - k. The circle has center (-5, 3) and r^2 = 34 - k. A circle is tangent to the x-axis when its radius equals the distance from its center to the x-axis, which is the absolute value of the center's y-coordinate, 3. So r = 3, r^2 = 9, and 34 - k = 9, which gives k = 25. Therefore, k = 25. Common slips: using the distance to the y-axis, 5, as the radius gives 34 - k = 25 and k = 9; setting 34 - k equal to r = 3 instead of r^2 = 9 gives k = 31.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2+10x-6y+k=0</code><br><code>y=0</code>

Add a slider for k and drag it until the circle just touches the x-axis at one point, (-5, 0); that happens at k = 25. Completing the square by hand is faster and exact, so use Desmos only as a check.

</details>

---

### 26. geo-circ-two-circles-common-chord

*Hard · Multiple choice · route: desmos-primary · techniques: T2*

In the $xy$-plane, the circles with equations $x^2 + y^2 = 25$ and $(x - 9)^2 + y^2 = 52$ intersect at two points. What is the distance between these two points?

- **A.** $4$
- **B.** $5$
- **C.** $8$
- **D.** $9$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Expanding the second equation yields x^2 - 18x + 81 + y^2 = 52. Subtracting the first equation, x^2 + y^2 = 25, from it yields -18x + 81 = 27, so x = 3. Substituting 3 for x in x^2 + y^2 = 25 yields y^2 = 16, so y = 4 or y = -4, and the points are (3, 4) and (3, -4). The distance between them is 4 - (-4) = 8. Therefore, the distance is 8. Distractors: 4 is the y-coordinate of one point, half of the common chord; 5 is the radius of the first circle; 9 is the distance between the centers (0, 0) and (9, 0), not between the intersection points.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2=25</code><br><code>(x-9)^2+y^2=52</code>

Click the two gray intersection points: (3, 4) and (3, -4). They lie on the same vertical line, so the distance between them is 4 - (-4) = 8.

</details>

---

### 27. geo-circ-wiper-blade-region

*Hard · Multiple choice · route: either · techniques: T9*

A wiper arm turns $\frac{2\pi}{3}$ radians about its pivot, and its blade spans from 10 to 28 inches from the pivot. A sector with central angle $\theta$ radians has area $\frac{1}{2}\theta$ times the square of its radius. What is the area, in square inches, of the region the blade wipes?

- **A.** $456\pi$
- **B.** $\frac{784\pi}{3}$
- **C.** $228\pi$
- **D.** $108\pi$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** The wiped region is the sector of radius 28 inches with the sector of radius 10 inches removed, both with central angle 2π/3. It's given that a sector with radius r and central angle θ radians has area (1/2)r^2θ. The outer sector has area (1/2)(28^2)(2π/3) = 784π/3 and the inner sector has area (1/2)(10^2)(2π/3) = 100π/3, so the wiped region has area 784π/3 - 100π/3 = 684π/3 = 228π square inches. Therefore, the area is 228π. Distractors: 108π subtracts the radii before squaring, (1/2)(28 - 10)^2(2π/3) = (1/2)(324)(2π/3); 784π/3 is the outer sector alone, ignoring the part of the arm the blade does not cover; 456π drops the factor 1/2, giving (2π/3)(684).

**Desmos** (not yet verified in Desmos). Type:<br><code>A(r)=\frac{1}{2}r^2\cdot\frac{2\pi}{3}</code><br><code>A(28)-A(10)</code><br><code>228\pi</code>

The second line shows 716.283, and typing 228π on the third line shows the same value. Desmos does not give the answer in terms of π, so compare decimals. By hand, (π/3)(784 - 100) is quick too.

</details>

---

### 28. geo-circle-chord-on-line

*Hard · Multiple choice · route: desmos-primary · techniques: T10, T2*

In the $xy$-plane, the circle with equation $x^2 + y^2 - 2x + 4y - 20 = 0$ intersects the line $y = 2$ at points $A$ and $B$. What is the length of segment $AB$?

- **A.** $3$
- **B.** $5$
- **C.** $6$
- **D.** $10$

**Answer:** C

<details><summary>Solutions</summary>

**By hand.** Substituting 2 for y in the circle's equation yields x^2 + 4 - 2x + 8 - 20 = 0, or x^2 - 2x - 8 = 0, which factors as (x - 4)(x + 2) = 0. So the intersection points are (4, 2) and (-2, 2), and AB = 4 - (-2) = 6. Therefore, AB = 6. Alternate approach: completing the square gives (x - 1)^2 + (y + 2)^2 = 25, a circle with center (1, -2) and radius 5; the line y = 2 is 4 units from the center, so half the chord is √(25 - 16) = 3 and the chord is 6. Distractors: 3 is half the chord; 5 is the radius; 10 is the diameter.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2-2x+4y-20=0</code><br><code>y=2</code>

Desmos graphs the expanded form directly. Click the two intersection points, (-2, 2) and (4, 2); they share a y-coordinate, so AB = 4 - (-2) = 6.

</details>

---

### 29. geo-circle-general-form-top-point

*Hard · Multiple choice · route: desmos-primary · techniques: T10, T2, T13*

The equation $x^2 + y^2 + 8x - 4y - 5 = 0$ represents a circle in the $xy$-plane. Which of the following is the point on the circle with the greatest $y$-coordinate?

- **A.** $(-4, -3)$
- **B.** $(-4, 2)$
- **C.** $(4, 3)$
- **D.** $(-4, 7)$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** Completing the square in x and in y: (x^2 + 8x + 16) + (y^2 - 4y + 4) = 5 + 16 + 4, so (x + 4)^2 + (y - 2)^2 = 25. The circle has center (-4, 2) and radius 5. The point with the greatest y-coordinate is directly above the center, 5 units up: (-4, 2 + 5) = (-4, 7). Therefore, the point is (-4, 7). Distractors: (-4, 2) is the center; (-4, -3) is the lowest point on the circle, 5 units below the center; (4, 3) comes from reading the center as (4, -2), a sign error in (x + 4)^2 and (y - 2)^2, and then adding the radius.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2+8x-4y-5=0</code><br><code>x=-4</code>

Desmos graphs the expanded form directly. Click the circle and the gray dot at its top, or click the upper intersection with the vertical line x = -4: (-4, 7). Plotting each choice as a point also shows which one sits on the circle at the top.

</details>

---

### 30. geo-circle-radius-constant-c

*Hard · Student-produced response · route: hand-primary · techniques: T10*

In the $xy$-plane, the graph of the equation $x^2 + y^2 - 6x + 10y + c = 0$ is a circle with a radius of 7, where $c$ is a constant. What is the value of $c$?

**Answer:** -15

<details><summary>Solutions</summary>

**By hand.** Completing the square in x and in y: x^2 - 6x + 9 + y^2 + 10y + 25 = -c + 9 + 25, so (x - 3)^2 + (y + 5)^2 = 34 - c. For a circle with radius 7, the right side must equal 7^2 = 49, so 34 - c = 49 and c = -15. Therefore, c = -15. Common slips: 34 - 7 = 27 uses the radius in place of r^2, and c = 15 drops the sign.

**Desmos** (not yet verified in Desmos). Type:<br><code>x^2+y^2-6x+10y+c=0</code><br><code>(x-3)^2+(y+5)^2=49</code>

Add a slider for c and drag it until the first circle lies exactly on the second (center (3, -5), radius 7); it lands at c = -15. Completing the square by hand gets there in two lines, so Desmos is only a check.

</details>

---

### 31. geo-circle-tangent-vertical-line

*Hard · Multiple choice · route: either · techniques: T13, T10*

In the $xy$-plane, a circle has its center at $(2, -3)$ and is tangent to the line $x = 7$. Which of the following is an equation of the circle?

- **A.** $(x - 2)^2 + (y + 3)^2 = 5$
- **B.** $(x + 2)^2 + (y - 3)^2 = 25$
- **C.** $(x - 2)^2 + (y + 3)^2 = 49$
- **D.** $(x - 2)^2 + (y + 3)^2 = 25$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** A tangent line is perpendicular to the radius at the point of tangency, so the radius equals the distance from the center to the line. The line x = 7 is vertical, and the horizontal distance from (2, -3) to it is 7 - 2 = 5, so r = 5 and r^2 = 25. A circle with center (h, k) and radius r has equation (x - h)^2 + (y - k)^2 = r^2, so the circle is (x - 2)^2 + (y + 3)^2 = 25. Distractors: (x - 2)^2 + (y + 3)^2 = 5 uses r instead of r^2; (x - 2)^2 + (y + 3)^2 = 49 squares the 7 from the line's equation, as if the center were at the origin; (x + 2)^2 + (y - 3)^2 = 25 has the signs of the center reversed.

**Desmos** (not yet verified in Desmos). Type:<br><code>x=7</code><br><code>(x-2)^2+(y+3)^2=25</code><br><code>(x-2)^2+(y+3)^2=49</code><br><code>(x-2)^2+(y+3)^2=5</code><br><code>(x+2)^2+(y-3)^2=25</code>

Only the circle with right side 25 touches the line x = 7 at a single point, (7, -3); the one with 49 crosses it, the one with 5 misses it, and the one centered at (-2, 3) is on the wrong side. By hand, the radius is the distance from the center to the tangent line.

</details>

---

### 32. geo-inscribed-angle-arc-x

*Hard · Student-produced response · route: hand-primary · techniques: T1*

Points $A$, $B$, and $C$ lie on a circle. Angle $ABC$ is inscribed in the circle and intercepts arc $AC$, which does not contain point $B$. The measure of arc $AC$ is $(6x - 10)^\circ$ and the measure of angle $ABC$ is $(2x + 7)^\circ$. What is the value of $x$?

**Answer:** 12

<details><summary>Solutions</summary>

**By hand.** An inscribed angle measures half its intercepted arc, so 2x + 7 = (6x - 10)/2. Doubling: 4x + 14 = 6x - 10, so 2x = 24 and x = 12. Setting the angle equal to the arc (2x + 7 = 6x - 10) gives x = 17/4, the central-angle mistake.

**Desmos** (not yet verified in Desmos). Type:<br><code>y=6x-10</code><br><code>y=2(2x+7)</code>

After writing the inscribed-angle relation by hand, the intersection (12, 62) confirms x = 12 (arc 62°, angle 31°). Solving the one-step linear equation by hand is faster.

</details>

---

### 33. geo-sum-angles-sine-negative-root3

*Hard · Multiple choice · route: hand-primary · techniques: —*

What is the sum of all values of $\theta$, where $0 \leq \theta < 2\pi$, for which $\sin\theta = -\frac{\sqrt{3}}{2}$?

- **A.** $\pi$
- **B.** $\frac{5\pi}{3}$
- **C.** $2\pi$
- **D.** $3\pi$

**Answer:** D

<details><summary>Solutions</summary>

**By hand.** The sine is √3/2 in absolute value when the reference angle is π/3. The sine is negative in quadrants III and IV, so the values of θ in [0, 2π) are π + π/3 = 4π/3 and 2π - π/3 = 5π/3. Their sum is 4π/3 + 5π/3 = 9π/3 = 3π. Therefore, the sum is 3π. Distractors: π is π/3 + 2π/3, the solutions of sin θ = +√3/2, with the sign ignored; 5π/3 reports only one of the two solutions; 2π is 5π/6 + 7π/6, the solutions of cos θ = -√3/2, confusing sine with cosine.

</details>

---
