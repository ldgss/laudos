# consulta plan de produccion

# select 
#    n.fch_prd as "Periodo",
#    n.cod_mae as "Producto",
#    ltrim(rtrim(g.den)) as "Den_Producto",
#    c.den as "Clase",
#    u.abr as "U_M",
#    n.can_met as "Plan_Venta",
#    n.can_prd as "Plan_Produccion",
#    round(cast(n.can_prd * f.vol as decimal(28,2)), 2) as "Volumen"
#    from prdnec n
#       inner join genmae g on
#          g.cod_emp = n.cod_emp and
#          g.cod_amb = n.cod_amb and
#          g.tip_mae = n.tip_mae and
#          g.cod_mae = n.cod_mae
#       left outer join genmae p on
#          p.cod_emp = g.cod_emp and
#          p.cod_amb = g.cod_amb and
#          p.tip_mae = g.tip_mae and
#          p.cod_mae = g.cod_sum
#       inner join logvar c on
#          c.cod_aux = g.cod_cls
#       inner join genfac f on
#          f.cod_emp = n.cod_emp and
#          f.cod_amb = n.cod_amb and
#          f.tip_mae = n.tip_mae and
#          f.cod_mae = n.cod_mae
#       inner join logvar u on
#          u.cod_tab = 2 and
#          u.cod_aux = f.uni_med
#       left outer join logvar u2 on
#          u2.cod_tab = 2 and
#          u2.cod_aux = f.uni_aba
#    where n.cod_emp = 1
#       and n.cod_amb = 1
#       and n.cod_met = 'PVHO25'
#    order by 1, 2, 4
# ;