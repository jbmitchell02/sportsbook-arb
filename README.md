# Sportsbook Arbitraging
Author: Mitch Mitchell (jbm8efn@virginia.edu)


#### Variables
$v_1, v_2$: Fractional odds of outcome 1 and 2

$b_1, b_2$: Bet size for outcome 1 and 2


#### Profit From Each Outcome
$$p_1=b_1 v_1-b_1-b_2$$

$$p_2=b_2 v_2-b_1-b_2$$


#### Bet Proportions
$$p_1=p_2$$

$$b_1 v_1-b_1-b_2=b_2 v_2-b_1-b_2$$

$$b_1 v_1=b_2 v_2$$

$$b_2=\frac{v_1}{v_2}b_1$$


#### Profit
$$P=p_1=p_2$$

$$=b_1 v_1-b_1-b_2$$

$$=b_1 v_1-b_1-\frac{v_1}{v_2}b_1$$

$$P=b_1(v_1-1-\frac{v_1}{v_2})$$


#### Returns
$$R=\frac{P}{b_1+b_2}$$

$$=\frac{b_1(v_1-1-\frac{v_1}{v_2})}{b_1+\frac{v_1}{v_2}b_1}$$

$$=\frac{b_1(v_1-1-\frac{v_1}{v_2})}{b_1(1+\frac{v_1}{v_2})}$$

$$=\frac{v_1-1-\frac{v_1}{v_2}}{1+\frac{v_1}{v_2}}$$

$$=(\frac{v_1 v_2-v_2-v_1}{v_2})(\frac{v_2+v_1}{v_2})^{-1}$$

$$R=\frac{v_1 v_2-v_1-v_2}{v_1+v_2}=\frac{v_1 v_2}{v_1 + v_2}-1$$
