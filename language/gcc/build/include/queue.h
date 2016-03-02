#ifndef _SRC_QUEUE_H_
#define _SRC_QUEUE_H_
#include "common.h"

int iinit_queue(bo_value_t *bo, bo_in_queue_t *input);
int iallocate_queue(bo_value_t *bo, bo_in_queue_t *input);
void idisp_queue(bo_in_queue_t *input);
inline int iis_full(bo_in_queue_t *input);
inline int iis_empty(bo_in_queue_t *input);
inline int iqueue_size(bo_in_queue_t *input);
int ienqueue(bo_in_queue_t *input, bo_in_msg_t *val);
int idequeue(bo_in_queue_t *input, bo_in_msg_t *val);
bool idelete_redunary_queue(bo_value_t *bo, bo_in_queue_t *input);
void idisp_check(bo_in_queue_t *input);

bool oinit_queue(bo_value_t *bo, bo_out_queue_t *output);
bool oallocate_queue(bo_value_t *bo, bo_out_queue_t *output);
void odisp_queue(bo_out_queue_t *output);
inline int ois_full(bo_out_queue_t *output);
inline int ois_empty(bo_out_queue_t *output);
inline int oqueue_size(bo_out_queue_t *output);
int oenqueue(bo_out_queue_t *output, bo_out_msg_t *val);
int odequeue(bo_out_queue_t *output, bo_out_msg_t *val);
bool odelete_redunary_queue(bo_value_t *bo, bo_out_queue_t *output);

bool rinit_queue(bo_value_t *bo, bo_rmdl_queue_t *remodel);
bool rallocate_queue(bo_value_t *bo, bo_rmdl_queue_t *remodel);
void rdisp_queue(bo_rmdl_queue_t *remodel);
inline int ris_full(bo_rmdl_queue_t *remodel);
inline int ris_empty(bo_rmdl_queue_t *remodel);
inline int rqueue_size(bo_rmdl_queue_t *remodel);
int renqueue(bo_rmdl_queue_t *remodel, bo_rmdl_msg_t *val);
int rdequeue(bo_rmdl_queue_t *remodel, bo_rmdl_msg_t *val);
bool rdelete_redunary_queue(bo_value_t *bo, bo_rmdl_queue_t *remodel);
inline void remodel_init_msg(bo_rmdl_msg_t *rNode);
inline void remodel_copy_value(bo_rmdl_msg_t *new, bo_rmdl_msg_t *old);
bo_rmdl_msg_t* remodel_create_node(bo_value_t *bo, time_t time, 
                                double value, uint16_t key);


#endif
