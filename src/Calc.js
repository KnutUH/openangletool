/** Class for grinding calculations */
class Calc {

    /**
     * Create a calculator.
     */
    constructor() {
        this.solved = false;
    }

    /**
     * Set parameters for the calculations.
     * @param  {Object}  p         The profile data
     * @param  {String}  p.name    The profile's name
     * @param  {number}  p.dw      Diameter of the
     * @param  {numberr} p.lp      Length of the jig from apex to
     * @return {number}  p.beta    The grinding angle at apex
     * @return {number}  p.ds    Diameter of the support
     * @return {number}  p.dj    Diameter of the jig
     * @return {number}  p.o    Horizontal offset of the support
     * @return {number}  p.hc    Heigth of m
     */
    set(p) {
        this.dw = Number.parseFloat(p.dw);
        this.lp = Number.parseFloat(p.lp);
        this.beta = this.rad(Number.parseFloat(p.beta));
        this.ds = Number.parseFloat(p.ds);
        this.dj = Number.parseFloat(p.dj);
        this.o = Number.parseFloat(p.o);
        this.hc = Number.parseFloat(p.hc);

        this.solve();
    }

    rad(d) {
        return d / 180 * Math.PI;
    }

    deg(r) {
        return r * 180 / Math.PI;
    }

    /**
     * For given grinding angle in degrees return the distance from the
     * center of the axel of the grinding wheel to the center of the support.
     *
     * The Law of cosines (https://en.wikipedia.org/wiki/Law_of_cosines) is used.
     * The vertices of triangle considered are,
     *
     *   A: center of axel
     *   B: apex of the blade
     *   C: center of the support
     *
     * To find the length of BC and angle between AB and BC consider the triangle
     * BCD where the vertices are,
     *
     *   B and C as above
     *   D: jig reference point
     *
     * The length of BD is the jig_length minus the radius of the support, the
     * length of CD is the radius of the support plus half the thickness of the
     * jig plus any apex offset. The angle between BC and CD is 90 degrees and
     * the lenght of BC can be found by the Pytagorean theorem. This angle,
     * between BD and BC (correction angle) can be found by the inverse tangence
     * of CD/BD.
     *
     * The grinding angle is the angle between a tangent to the grinding wheel
     * in apex point (B) which is 90 degrees to AB hence the angle between AB and
     * BC is 90 degrees + the grinding angle minus the correction angle
     */
    
    solve() {
        var a = 45./180.*Math.PI;
        var b = Math.PI;
        var xa = this.x(a);
        var xb = this.x(b);
        const eps = 1e-5;

        console.log('solve: a='+a+', b='+b+', xa='+xa+', xb='+xb);

	this.solved = false;
        while ((Math.sign(xa) !== Math.sign(xb)) && (b - a) > eps) {
            var m = 0.5 * (a + b);
            var xm = this.x(m);
            if (Math.sign(xa) === Math.sign(xm)) {
                a = m;
                xa = xm;
            } else {
                b = m;
                xb = xm;
            }
	    this.solved = true;
        }

        if (!this.solved) {
	   return;
	}

        this.alpha = 0.5 * (a + b);

        this.h = 0.5 * (
            this.ds * Math.cos(this.alpha + this.beta)
            - 2 * this.lp * Math.cos(this.alpha + this.beta)
            + this.dw * Math.sin(this.alpha)
            - this.dj * Math.sin(this.alpha + this.beta)
            - this.ds * Math.sin(this.alpha + this.beta)
        );

        this.hr = Math.sqrt(this.o * this.o + this.h * this.h)
            + 0.5 * this.ds
            - 0.5 * this.dw;

        this.hn = this.h
            + 0.5 * this.ds
            - this.hc;
    }

    x(alpha) {
        return -this.o
            + 0.5 * this.dw * Math.cos(alpha)
            - 0.5 * (this.dj + this.ds) * Math.cos(alpha + this.beta)
            + (-0.5 * this.ds + this.lp) * Math.sin(alpha + this.beta);
    }

    get() {
        if (this.solved) {
	   return {
	       alpha: this.deg(this.alpha).toFixed(1).toString(),
	       h: this.h.toFixed(1).toString(),
	       hr: this.hr.toFixed(1).toString(),
	       hn: this.hn.toFixed(1).toString()
	   };
        }
	return {
	    alpha: '-',
	    h: '-',
	    hr: '-',
	    hn: '-'
	};
    }

}

export default Calc;
