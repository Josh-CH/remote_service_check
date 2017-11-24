#!/bin/bash
# Performs very basic service checking. If the exit code of the "service status" command is 0
# and the service is listening on its designated port, then the service returns as running successfully.

# Todo
# 1. Make script compatible with redhat 6 as well (run service not systemctl)

function service_check {
	local service_name="${1}"
	local port="${2}"
	local proto="${3}"
	
	FAIL=0
	/usr/bin/systemctl status "${service_name}"  > /dev/null 2>&1
	if [[ "$?" -ne 0 ]]; then
		FAIL=1
	fi

	if [[ "${proto,,}" == "tcp" ]]; then
		if ! /usr/sbin/ss -tna | grep "LISTEN.*:${port}" > /dev/null 2>&1; then
			FAIL=1
		fi
	elif [[ "${proto,,}" == "udp" ]]; then
		if ! /usr/sbin/ss -una | grep "UNCONN.*:${port}" > /dev/null 2>&1; then
			FAIL=1
		fi
	fi
	
	if [[ "${FAIL}" -eq 0 ]]; then
			exit 0
	else
			exit 1 
	fi
}

if [[ "$#" -eq 0 ]]; then
	echo "Usage: $0 service_name service_port service_protocol"
	exit 1
fi

service_check "$1" "$2" "$3"
