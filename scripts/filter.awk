BEGIN { FS=OFS="\t" }

NR==1 { print; next }

{
  if ($11 != "" && $19 != "" && $28 != "" && $37 != "") {
    print
  }
}
