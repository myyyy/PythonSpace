1. 引入mosquitto仓库并更新
$sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa

$sudo apt-get update


2. 执行以下命令安装mosquitto包

$sudo apt-get install mosquitto


3. 安装mosquitto开发包

$sudo apt-get install libmosquitto-dev


4. 安装mosquitto客户端

$sudo apt-get install mosquitto-clients


5. 查询mosquitto是否正确运行

$sudo service mosquitto status 

以下输出表示安装成功

```

● mosquitto.service - LSB: mosquitto MQTT v3.1 message broker
   Loaded: loaded (/etc/init.d/mosquitto; generated; vendor preset: enabled)
   Active: active (running) since Sat 2018-03-10 14:16:08 UTC; 16min ago
     Docs: man:systemd-sysv-generator(8)
   CGroup: /system.slice/mosquitto.service
           └─24098 /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf

Mar 10 14:16:08 raspberrypi systemd[1]: Starting LSB: mosquitto MQTT v3.1 message broker...
Mar 10 14:16:08 raspberrypi mosquitto[24092]: Starting network daemon:: mosquitto.
Mar 10 14:16:08 raspberrypi systemd[1]: Started LSB: mosquitto MQTT v3.1 message broker.

```
