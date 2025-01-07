/* Natural Color Blank Start */
var bb_n = {qty} < 12 ? 10.38 : ({qty} < 24 ? 7.99 : ({qty} < 36 ? 6.42 : ({qty} < 72 ? 4.13 : ({qty} < 144 ? 4.01 : ({qty} < 288 ? 3.90 : ({qty} < 576 ? 3.85 : ({qty} < 1008 ? 3.70 : ({qty} < 2016 ? 3.61 : 3.61))))))));
/* Natural Color Blank End */

/* Color Color Blank Start */
var bb_c = {qty} < 12 ? 10.69 : ({qty} < 24 ? 8.22 : ({qty} < 36 ? 6.56 : ({qty} < 72 ? 4.26 : ({qty} < 144 ? 4.14 : ({qty} < 288 ? 4.03 : ({qty} < 576 ? 3.97 : ({qty} < 1008 ? 3.82 : ({qty} < 2016 ? 3.72 : 3.72))))))));
/* Color Color Blank End */

/* Color Screen Printing Start */
var pwl_c = {qty} < 12 ? 11.26 : ({qty} < 24 ? 8.65 : ({qty} < 36 ? 6.91 : ({qty} < 72 ? 4.49 : ({qty} < 144 ? 4.36 : ({qty} < 288 ? 4.24 : ({qty} < 576 ? 4.19 : ({qty} < 1008 ? 4.03 : ({qty} < 2016 ? 3.93 : 3.93))))))));
/* Color Screen Printing End */

/* Natural color Screen Printing Start */
var pwl_n = {qty} < 12 ? 10.93 : ({qty} < 24 ? 8.42 : ({qty} < 36 ? 6.76 : ({qty} < 72 ? 4.36 : ({qty} < 144 ? 4.24 : ({qty} < 288 ? 4.12 : ({qty} < 576 ? 4.07 : ({qty} < 1008 ? 3.91 : ({qty} < 2016 ? 3.81 : 3.81))))))));
/* Natural color Screen Printing End */


/* For Developer Point dont edit this */

var rush = {rush1} ? 100 : 0;


var custom_color_Front = 0 + ({cc1} ? 1 : 0);
var custom_color_Front_fee = {pwl} ? ({custom_color_Front} * 30) : 0;

var color_front = 0 + ({f6} ? 6 : 0) + ({f5} ? 5 : 0) + ({f4} ? 4 : 0) + ({fs3} ? 3 : 0) + ({f2} ? 2 : 0) + ({f1} ? 1 : 0);

var color_setup = {pwl} ? 60 * {color_front} : 0;

var base = {bb} ? ({n} ? {bb_n} : {bb_c}) : ({pwl} ? ({n} ? {pwl_n} : {pwl_c}) : 0);
var rush_fee = {rush};

var color_front_fee = {f2} ? (0.5 * ({color_front} - 1)) : 0;

var totalfee = (({base} + {color_front_fee}) * {qty});

var total = {totalfee} + {color_setup} + {rush_fee} + {custom_color_Front_fee};
