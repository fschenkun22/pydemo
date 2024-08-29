import time
import paho.mqtt.client as mqtt
import json
import threading

def send_mqtt():
    def on_publish(client, userdata, mid, reason_code=None, properties=None):
        print(f"Message with mid {mid} published.")

    mqttc = mqtt.Client()
    mqttc.on_publish = on_publish
    mqttc.username_pw_set("homeassistant", "OoQu6pheeyaifohZieK2nat0maigei3ziraco9na2Eeghoolia3geec3Tohvot5a")
    try:
        mqttc.connect("fd1c:33c1:ced0:7eb7:fb99:93df:a5c4:c5a1", 1883, 60)
    except Exception as e:
        print("MQTT连接失败")
        print(e)
        return
    mqttc.loop_start()

    # 定义个json对象
    json_obj = {
        "name":"Mqtt test temperature",
        "unique_id":"my_diy_temperature",
        "state_topic":"homeassistant/sensor/my_diy_temperature/state",
        "unit_of_measurement":"°C",
        "device_class":"temperature",
        "availability_topic":"homeassistant/sensor/my_diy_temperature/availability",
        "payload_available":"online",
        "payload_not_available":"offline",
    }
    json_str = json.dumps(json_obj)

    # # 发布100度
    msg_info = mqttc.publish("homeassistant/sensor/my_diy_temperature/state", time.time() , qos=0)

    # 设备下线
    # msg_info = mqttc.publish("homeassistant/sensor/my_diy_temperature/availability", "online", qos=0)

    # # 发布配置信息
    # msg_info = mqttc.publish("homeassistant/sensor/my_diy_temperature/config",json_str, qos=0)

    # Due to race-condition described above, the following way to wait for all publish is safer
    msg_info.wait_for_publish()
    mqttc.disconnect()
    mqttc.loop_stop()

if __name__ == '__main__':
    def run():
        send_mqtt()
        threading.Timer(1, run).start()
    run()
    print("start")
