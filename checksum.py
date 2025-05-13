

def checksum(source_string):
    """Calculate the checksum of the packet."""
    countTo = (len(source_string) // 2) * 2
    count = 0
    sum = 0
    while count < countTo:
        value = source_string[count + 1] * 256 + source_string[count]
        sum += value
        sum &= 0xffffffff  
        count += 2
    if countTo < len(source_string):
        sum += source_string[len(source_string) - 1]
        sum &= 0xffffffff 
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer