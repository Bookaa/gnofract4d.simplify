
#ifndef PF_H_
#define PF_H_

/* C signature of point-funcs generated by compiler 
   
   This is essentially an opaque object with methods implemented in C. 
   Typical usage:

   //#pixel.re, #pixel.im, #z.re, #z.im 
   double pparams[] = { 1.5, 0.0, 0.0, 0.0};
   double initparams[] = {5.0, 2.0};
   int nItersDone=0;
   int nFate=0;
   double dist=0.0;
   int solid=0;
   pf_obj *pf = pf_new();
   pf->vtbl->init(pf,0.001,initparams,2);
   
   pf->vtbl->calc(
        pf,
        pparams,
        100,
        0,0,0,
        &nItersDone, &nFate, &dist, &solid);
   
   pf->vtbl->kill(pf);
*/

// maximum number of params which can be passed to init
#define PF_MAXPARAMS 200

// number of positional params used
#define N_PARAMS 11

/* the 'fate' of a point. This can be either
   Unknown (255) - not yet calculated
   N - reached an attractor numbered N (up to 30)
   N | FATE_INSIDE - did not escape
   N | FATE_SOLID - color with solid color 
   N | FATE_DIRECT - color with DCA
*/

typedef unsigned char fate_t;

#define FATE_UNKNOWN 255
#define FATE_SOLID 0x80
#define FATE_DIRECT 0x40
#define FATE_INSIDE 0x20

typedef enum
{
    INT = 0,
    FLOAT = 1,
    GRADIENT = 2,
    PARAM_IMAGE = 3
} e_paramtype;

struct s_param
{
    e_paramtype t;
    int intval;
    double doubleval;
    void *gradient;
    void *image;
};

struct s_pf_data;

struct s_pf_vtable {
    /* fill in params with the default values for this formula */
    void (*get_defaults)(
	struct s_pf_data *p,
	double *pos_params,
        struct s_param *params,
	int nparams
	);

    /* fill in fields in pf_data with appropriate stuff */
    void (*init)(
	struct s_pf_data *p,
	double *pos_params,
        struct s_param *params,
	int nparams
	);

    /* calculate one point.
       perform up to nIters iterations,
       return:
       number of iters performed in pnIters
       outcome in pFate: 0 = escaped, 1 = trapped. 
       More fates may be generated in future
       dist : index into color table from 0.0 to 1.0
    */
    void (*calc)(
	struct s_pf_data *p,
        // in params
        const double *params, int nIters, //int warp_param,
	// tolerance params
	// int min_period_iter, double period_tolerance,
	// only used for debugging
	int x, int y, int aa,
        // out params
        int *pnIters, int *pFate, double *pDist, int *pSolid,
	int *pDirectColorFlag, double *pColors
	);
    /* deallocate data in p */
    void (*kill)(
	struct s_pf_data *p
	);
} ;

struct s_pf_data {
    struct s_pf_vtable *vtbl;
    void *arena;
} ;

typedef struct s_pf_vtable pf_vtable;
typedef struct s_pf_data pf_obj;



#ifdef __cplusplus
extern "C" {
#endif

/* create a new pf_obj.*/
extern pf_obj *pf_new(void);

#ifdef __cplusplus
}
#endif

#endif /* PF_H_ */
