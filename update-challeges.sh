#!/bin/sh

sed 's/cluster-[^.]*\.[^.]*\.sandbox[^.]*\.opentlc\.com/{{ cluster_url }}/g' | jq
