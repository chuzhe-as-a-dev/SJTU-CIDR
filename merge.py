import ipaddress

ip_ranges = {}  # begin -> end
ip_ranges_reversed = {}  # end -> begin
with open("ips.tsv") as f:
  f.readline()  # skip headers
  for line in f:
    ip_or_ip_range, _ = line.split("\t")
    if "-" in ip_or_ip_range:
      ip_begin, ip_end = ip_or_ip_range.split("-")
      ip_begin, ip_end = ipaddress.ip_address(ip_begin), ipaddress.ip_address(ip_end)
      ip_prev = ip_begin - 1
      if ip_prev in ip_ranges_reversed:
        begin = ip_ranges_reversed[ip_prev]
        ip_ranges[begin] = ip_end
        ip_ranges_reversed.pop(ip_prev)
        ip_ranges_reversed[ip_end] = begin
      else:
        ip_ranges[ip_begin] = ip_end
        ip_ranges_reversed[ip_end] = ip_begin
    else:
      ip = ipaddress.ip_address(ip_or_ip_range)
      ip_prev = ip - 1
      if ip_prev in ip_ranges_reversed:
        begin = ip_ranges_reversed[ip_prev]
        ip_ranges[begin] = ip
        ip_ranges_reversed.pop(ip_prev)
        ip_ranges_reversed[ip] = begin
      else:
        ip_ranges[ip] = ip
        ip_ranges_reversed[ip] = ip

while True:
  ip_ranges_old = ip_ranges
  ip_ranges = {}
  ip_ranges_reversed = {}

  for ip_begin, ip_end in ip_ranges_old.items():
    ip_begin, ip_end = ipaddress.ip_address(ip_begin), ipaddress.ip_address(ip_end)
    ip_prev = ip_begin - 1
    # print("ip_begin:", ip_begin)
    # print("ip_end:", ip_end)
    # print("ip_prev:", ip_prev)
    if ip_prev in ip_ranges_reversed:
      begin = ip_ranges_reversed[ip_prev]
      ip_ranges[begin] = ip_end
      ip_ranges_reversed.pop(ip_prev)
      ip_ranges_reversed[ip_end] = begin
    else:
      ip_ranges[ip_begin] = ip_end
      ip_ranges_reversed[ip_end] = ip_begin
  
  if len(ip_ranges_old) == len(ip_ranges):
    break


for ip_begin, ip_end in ip_ranges.items():
  print(ip_begin, "=>", ip_end)
  for range in ipaddress.summarize_address_range(ip_begin, ip_end):
    print(f"\t{range}")