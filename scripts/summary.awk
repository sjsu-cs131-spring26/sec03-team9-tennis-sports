BEGIN { FS=OFS="\t" }

NR==1 { next }

{
  p = $11
  d = $(NF-1)

  count[p]++
  sum[p] += d
}

END {
  print "player\tmatches\tavg_ace_diff"
  for (p in count) {
    printf "%s\t%d\t%.2f\n", p, count[p], sum[p]/count[p]
  }
}
