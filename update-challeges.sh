#!/bin/sh

#sed 's/cluster-[^.]*\.[^.]*\.sandbox[^.]*\.opentlc\.com/{{ cluster_url }}/g' | jq
sed 's/cluster-[^.]*\.dynamic\.redhatworkshops\.io/{{ cluster_url }}/g' | jq
