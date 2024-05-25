
*.include "common.inc"
.inc '45nm_LP.pm'
*.option scale=1u
v_g_nmos g_nmos 0 dc 1.1
v_s_nmos s_nmos 0 dc 0.0
v_b_nmos b_nmos 0 dc 0.0
v_g_pmos g_pmos 0 dc 0.0
v_s_pmos s_pmos 0 dc 1.1
v_b_pmos b_pmos 0 dc 1.1
v_d d 0 dc 0.0
m_nmos d g_nmos s_nmos b_nmos nmos L=1.0u W=10.0u
m_pmos d g_pmos s_pmos b_pmos pmos L=1.0u W=20.0u
.dc v_d 0.0 1.1 0.01
.measure dc pmos_start find i(v_d) at = 1.1
.measure dc pmos_end   find i(v_d) at = 1.09
.measure dc pmos_reff  param='(pmos_end - pmos_start)/(0.01)'
.measure dc nmos_start find i(v_d) at = 0.0
.measure dc nmos_end   find i(v_d) at = 0.01
.measure dc nmos_reff  param='(nmos_end - nmos_start)/(0.01)'
.control
run
.endc
.end
