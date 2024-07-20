
import glob
import yaml

total_cpu = 0.0
total_ram = 0.0
clusterip_services_list = []
nodeport_services_list = []
other_services_list = []
empty_values_list = []
no_service_list = []
random_service_list = []

def read_resources(file):
    global total_cpu
    global total_ram
    with open(file, 'r') as yfile:
        contents = yaml.safe_load(yfile)
        if contents:
            if 'resources' in contents:
                if 'small' in contents['resources']:
                    if 'cpu' in contents['resources']['small']['requests']:
                        cpu_value = contents['resources']['small']['requests']['cpu']
                        if isinstance(cpu_value, int):
                            total_cpu = total_cpu + float(cpu_value)
                        if isinstance(cpu_value, str):
                            cvalue = float(float(cpu_value[:-1])/1000.0)
                            total_cpu = total_cpu + cvalue
                        if isinstance(cpu_value, float):
                            total_cpu = total_cpu + cpu_value
                    if 'memory' in contents['resources']['small']['requests']:
                        mem_value = contents['resources']['small']['requests']['memory']
                        if 'Mi' in mem_value[-2:]:
                            mvalue = float(float(mem_value[:-2])/1000.0)
                            total_ram = total_ram + mvalue
                        if 'Gi' in mem_value[-2:]:
                            mvalue = float(mem_value[:-2])
                            total_ram = total_ram + mvalue

def read_services(file):
    global clusterip_services_list
    global nodeport_services_list
    global other_services_list
    global empty_values_list
    global no_service_list
    global random_service_list
    with open(file, 'r') as yfile:
        contents = yaml.safe_load(yfile)
        if contents:
            if 'service' in contents:
                if 'type' in contents['service']:
                    if 'ClusterIP' in contents['service']['type']:
                        clusterip_services_list.append(file.split('/')[-2])
                    elif 'NodePort' in contents['service']['type']:
                        nodeport_services_list.append(file.split('/')[-2])
                    else:
                        other_services_list.append(file.split('/')[-2])
                else:
                    random_service_list.append(file.split('/')[-2])
            else:
                no_service_list.append(file.split('/')[-2])
        else:
            empty_values_list.append(file.split('/')[-2])
            return False
        return True

def test_func(file):
    with open(file, 'r') as yfile:
        contents = yaml.safe_load(yfile)
        if contents:
            if 'image' in contents:
                if isinstance(contents['image'], dict):
                    if 'name' in contents['image']:
                        print(file.split('/')[-2]+ ':' + contents['image']['name'])
                    else:
                        print(file.split('/')[-2]+ ':' + contents['image']['repository'])
                else:
                    print(file.split('/')[-2]+ ':' + contents['image'])
            else:
                for key in list(contents.keys()):
                    if key.endswith('Image'):
                        print(file.split('/')[-2]+ ':' + key)




if __name__ == "__main__":
    #for file in glob.glob("./onap_oom/**/values.yaml", recursive=True):
    #    print(file)
    #for file in glob.glob("./oran_oom/**/values.yaml", recursive=True):
    #    print(file)
        #read_resources(file)
    with open("allfiles.txt", 'r') as ffile:
        #filenames = ffile.readlines()
        filenames = ffile.read().splitlines()
        for file in filenames:
            test_func(file)
            #has_values = read_services(file.rstrip())
            #if has_values:
            #    read_resources(file.rstrip())
    print("********************* TOTAL CPU ******************")
    print(total_cpu)
    print("********************* TOTAL RAM ******************")
    print(total_ram)
    print("********************* ClusterIP Service used by: ******************")
    print(clusterip_services_list)
    print("********************* NodePort Service used by: ******************")
    print(nodeport_services_list)
    print("********************* Other Service used by: ******************")
    print(other_services_list)
    print("********************* Empty Values.yaml found in: ******************")
    print(empty_values_list)
    print("********************* No services are defined for these: ******************")
    print(no_service_list)
    print("********************* Service term is abused in these: ******************")
    print(random_service_list)

