#!/bin/bash
export LANG="en_US.UTF-8"
export LANGUAGE="en_US:en"

fdisk_mount(){
    mkfs.ext4 $1
    tune2fs -c 0 -i 0 $1
    echo "$1           $2                ext4       defaults              0  2" >>/etc/fstab
    mount -a
}

create_data(){
        data_array=()
        for i in `seq 1 $1`; do
            if [ $i -eq 1 ]; then
                [ -d /data ] || mkdir /data
                data_array[${#data_array[@]}]=/data
            else
                let i=$i-1
                [ -d /data$i ] || mkdir /data$i
                data_array[${#data_array[@]}]=/data$i
            fi
        done
        echo ${data_array[@]}
}

add_disk(){
    root_mount=`df -h  | awk '/\/$/{print $1}'`
    root_mount=${root_mount%%[0-9]}
    disks=`fdisk  -l | grep -E "Disk /dev/[vs]d[a-z]" | awk '{print $2}' | awk -F ':' '{print $1}'|grep -v $root_mount`
    disk_array=($disks)
    length=${#disk_array[@]}
    datas=`create_data $length`
    data_array=($datas)
    echo ${datas[@]}
    #echo $data_mount 
    for ((i=0; i<$length; i++)); do
        df  -h | grep ${disk_array[$i]} >/dev/null 2>&1
        if [ $? -ne 0 ] ; then
            disk_size=`fdisk  -l | grep "Disk ${disk_array[$i]}" | awk '{print $5/(1024*1024*1024)}'`
            if [ "$disk_size" != "" ]; then
                   if [ $disk_size -lt 2000 ]; then
                        fdisk_mount ${disk_array[$i]}  ${data_array[$i]}
                        echo "usege: fdisk_mount ${disk_array[$i]}  ${data_array[$i]}"
                   else
                        echo "磁盘大于2T"
                    fi
            fi
        fi
    done
}


####=====新服务器挂载磁盘====####
add_disk


