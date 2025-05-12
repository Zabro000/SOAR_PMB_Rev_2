[Transient Analysis]
{
   Npanes: 2
   {
      traces: 4 {524290,0,"V(reset_clk)"} {524291,0,"V(output_rail)"} {524292,0,"V(deny_signal)"} {524293,0,"V(reset_gate)"}
      X: (' ',1,0,0.1,1)
      Y[0]: (' ',0,-5,5,50)
      Y[1]: ('m',1,1e+308,0.0001,-1e+308)
      Volts: (' ',0,0,1,-5,5,50)
      Log: 0 0 0
   },
   {
      traces: 3 {524294,0,"V(batt_1_comparator)"} {524295,0,"V(logic_power)"} {524296,0,"V(batt_1)"}
      X: (' ',1,0,0.1,1)
      Y[0]: (' ',0,-2,2,18)
      Y[1]: ('m',1,1e+308,0.0001,-1e+308)
      Volts: (' ',0,0,1,-2,2,18)
      Log: 0 0 0
   }
}
