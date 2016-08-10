#ifndef _FRACTFUNC_H_
#define _FRACTFUNC_H_

#include <cassert>

#include "image_public.h"
#include "pointFunc_public.h"
#include "fractWorker_public.h"
#include "vectors.h"
#include "fract_public.h"

/* this contains stuff which is useful for drawing the fractal,
   but can be recalculated at will, so isn't part of the fractal's
   persistent state. We create a new one each time we start drawing. This one
   parcels up the work which is actually performed by the fractThreadFuncs
 */


class fractFunc {
 public:
    fractFunc(d *params,
        int maxiter,
        IFractWorker *fw,
        IImage *_im);
    // ~fractFunc();

    void draw_all();
    void draw(int rsize, int drawsize, float min_progress, float max_progress);    

    friend class STFractWorker;

    // used for calculating (x,y,z,w) pixel coords
    dmat4 rot; // scaled rotation matrix
    dvec4 deltax, deltay; // step from 1 pixel to the next in x,y directions
    dvec4 delta_aa_x, delta_aa_y; // offset between subpixels
    dvec4 topleft; // top left corner of screen
    dvec4 aa_topleft; // topleft - offset to 1st subpixel to draw
    dvec4 eye_point; // where user's eye is (for 3d mode)

 private:
    // MEMBER VARS

    bool ok; // did this instance get constructed ok?
    // (* this should really be done with exns but they are unreliable 
    //  * in the presence of pthreads - grrr *)

    // do every nth pixel twice as deep as the others to
    // see if we need to auto-deepen
    enum { 
        AUTO_DEEPEN_FREQUENCY = 30,
        AUTO_TOLERANCE_FREQUENCY = 30
    };

    // flags for controlling auto-improvement
    enum {
        SHOULD_DEEPEN = 1,
        SHOULD_SHALLOWEN = 2, // yes, I know this isn't a word
        SHOULD_LOOSEN = 4,
        SHOULD_TIGHTEN = 8,
        SHOULD_IMPROVE = (SHOULD_DEEPEN | SHOULD_TIGHTEN),
        SHOULD_RELAX = (SHOULD_SHALLOWEN | SHOULD_LOOSEN)
    };

    // params from ctor    
    // int eaa;
    int maxiter;
    // double period_tolerance;
    int debug_flags;
    render_type_t render_type;

    IImage *im;    
    IFractWorker *worker;
    // for callbacks
    //IFractalSite *site;

    float min_progress;
    float delta_progress;

    void set_progress_range(float min, float max) { 
        min_progress = min;
        delta_progress = max-min;
        assert(delta_progress > 0.0);
    }

    // private drawing methods
    void send_quit();

    // prepare for deepening by clearing 'in'-fated pixels
    void clear_in_fates();

    // clear auto-deepen and last_update
    void reset_counts();
    void reset_progress(float progress);
};

// geometry utilities
dmat4 rotated_matrix(double *params);
dvec4 test_eye_vector(double *params, double dist);

enum {
    DEBUG_QUICK_TRACE = 1,
    DEBUG_DRAWING_STATS = 2,
    DEBUG_TIMING = 4
};

#ifdef __cplusplus
extern "C" {
#endif

extern void calc_4(
    d *params,
    int maxiter,
    pf_obj *pfo, 
    ColorMap *cmap, 
    IImage *im);

#ifdef __cplusplus
}
#endif

#endif /* _FRACTFUNC_H_ */
