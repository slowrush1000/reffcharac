1. reff charac. spice template

# {model_name} reff
*
.inc 'inc_file'
.option scale=1u post list
*
{subckt_type}_{model_name} d g s b {model_name} l={length} w={width}
*
v_d d 0 dc 0.0
v_g d 0 dc {vdd}
v_s d 0 dc 0.0
v_b d 0 dc 0.0
*
.dc v_d 0.0 {vdd} 0.01
*
.measure dc start find i(v_d) at=0.0
.measure dc end   find i(v_d) at=0.01
.measure dc reff  param='(end - start)/0.01'
*
.control
run
.endc
*
.end
