BEGIN { FS=OFS="\t" }

NR==1 { next }

{
  bucket = $NF
  count[bucket]++
}

END {
  print "bucket\tcount"
  for (b in count) {
    print b, count[b]
  }
}
