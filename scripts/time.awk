BEGIN { FS=OFS="\t" }

NR==1 { next }

{
  date = $6
  ym = substr(date,1,4) "-" substr(date,5,2)

  d = $(NF-1)

  count[ym]++
  sum[ym] += d
}

END {
  print "month\tmatches\tavg_ace_diff"
  for (m in count) {
    printf "%s\t%d\t%.2f\n", m, count[m], sum[m]/count[m]
  }
}
