from boto import ec2
from fabric.api import *
import xlwt

env.skip_bad_hosts = True
env.shell = "/bin/bash -l -c -o pipefail"

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Servers')
row_index = 1

def get_info():
	global row_index

	version = run('lsb_release -sd')
	kernel = run('uname -r')
	arch = run('uname -m')

	# Update checks pull from byobu updates_available widget
	updates_available = run("/usr/lib/update-notifier/apt-check 2>&1 | awk '-F;' 'END { print $1 }'", warn_only=True)
	if updates_available.return_code != 0:
		updates_available = run("apt-get -s -o Debug::NoLocking=true upgrade | grep -c ^Inst", warn_only=True)

	host = env.instances[env.host]
	sheet.write(row_index, 0, host[0])
	sheet.write(row_index, 1, host[1])
	sheet.write(row_index, 2, env.host)
	sheet.write(row_index, 3, host[2])
	sheet.write(row_index, 4, version)
	sheet.write(row_index, 5, kernel)
	sheet.write(row_index, 6, arch)
	sheet.write(row_index, 7, updates_available)
	row_index += 1

@task(default=True)
def fetch():
	conn = ec2.connect_to_region('us-east-1')
	reservations = conn.get_all_instances()
	instances = {}
	for r in reservations:
		for i in r.instances:
			try:
				if not i.public_dns_name:
					continue
				instances[i.public_dns_name] = (i.id, i.tags['Name'], i.ip_address)
				env.hosts.append(i.public_dns_name)
			except KeyError:
				# Ignore instances without a name
				continue
	env.instances = instances
	sheet.write(0, 0, 'Instance ID')
	sheet.write(0, 1, 'Server Name')
	sheet.write(0, 2, 'IP Address')
	sheet.write(0, 3, 'Public Hostname')
	sheet.write(0, 4, 'OS Version')
	sheet.write(0, 5, 'Kernel Version')
	sheet.write(0, 6, 'Processor Architecture')
	sheet.write(0, 7, 'Pending Available')
	execute(get_info, hosts=instances.keys())
	workbook.save('servers.xls')

