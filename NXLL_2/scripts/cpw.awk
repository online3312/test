#!/usr/bin/awk -f
BEGIN {
	FS=","
	OFS=","
	regex = "^"user"$"
}
$1 ~ regex{
	$2=pass
}
{
print
}

