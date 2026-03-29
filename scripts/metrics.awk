BEGIN { FS=OFS="\t" }

NR==1 {
  print $0, "ace_diff", "bucket"
  next
}

{
  w = $28 + 0
  l = $37 + 0

  diff = w - l

  bucket = (diff > 5) ? "HIGH" :
           (diff > 0) ? "MID" : "LOW"

  print $0, diff, bucket
}
